import json
import queue
import threading
import time


class VoiceError(Exception):
    pass


class VoiceManager:
    def __init__(self, config):
        self._config = config
        self._engine = None
        self._active = False
        self._stop_event = threading.Event()
        self._thread = None
        self._transcript_queue = queue.Queue()

    def set_transcript_queue(self, transcript_queue):
        self._transcript_queue = transcript_queue

    def is_active(self):
        return self._active

    def start(self):
        if self._active:
            return True, "Voice da dang chay."
        try:
            self._engine = AudioEngine(self._config)
            self._stop_event.clear()
            self._thread = threading.Thread(target=self._run, daemon=True)
            self._thread.start()
            self._active = True
            return True, "Da bat voice listener."
        except VoiceError as exc:
            return False, str(exc)

    def stop(self):
        if not self._active:
            return True, "Voice dang tat."
        self._stop_event.set()
        if self._engine:
            self._engine.stop()
        self._active = False
        return True, "Da tat voice listener."

    def _run(self):
        self._log("listening...")
        try:
            self._engine.start()
            for transcript in self._engine.run(self._stop_event):
                if transcript:
                    self._log(f"text: {transcript}")
                    self._transcript_queue.put(transcript)
        except Exception as exc:
            self._log(f"error: {exc}")
        finally:
            if self._engine:
                self._engine.stop()
            self._active = False
            self._log("stopped")

    def _log(self, message):
        print(f"[VOICE] {message}")


class AudioEngine:
    def __init__(self, config):
        self._config = config
        self._frame_ms = int(getattr(config, "VOICE_FRAME_MS", 20))
        self._sample_rate = int(getattr(config, "VOICE_SAMPLE_RATE", 16000))
        self._wake_threshold = float(getattr(config, "VOICE_WAKE_THRESHOLD", 0.7))
        self._silence_ms = int(getattr(config, "VOICE_SILENCE_MS", 800))
        self._max_record_ms = int(getattr(config, "VOICE_MAX_RECORD_MS", 8000))
        self._device = getattr(config, "VOICE_DEVICE", None)
        self._wake_word = getattr(config, "VOICE_WAKE_WORD", "")
        self._asr_model_path = getattr(config, "VOICE_ASR_MODEL", None)
        self._audio_queue = queue.Queue()
        self._mic_stream = None
        self._wake_detector = WakeWordDetector(self._wake_word, self._wake_threshold)
        self._asr = AsrEngine(self._asr_model_path, self._sample_rate)
        self._vad = VoskVoiceActivityDetector(
            self._asr.model,
            self._sample_rate,
            self._frame_ms,
        )

    def start(self):
        self._mic_stream = MicrophoneStream(
            self._audio_queue,
            sample_rate=self._sample_rate,
            frame_ms=self._frame_ms,
            device=self._device,
        )
        self._mic_stream.start()

    def stop(self):
        if self._mic_stream:
            self._mic_stream.stop()
            self._mic_stream = None

    def run(self, stop_event):
        buffer_frames = []
        recording = False
        speech_seen = False
        last_voice_time = None
        record_start = None
        frame_count = 0

        while not stop_event.is_set():
            try:
                frame = self._audio_queue.get(timeout=0.1)
                frame_count += 1
            except queue.Empty:
                continue

            # Log audio level every 50 frames (~1 second)
            if frame_count % 50 == 0:
                import numpy as np
                audio_data = np.frombuffer(frame, dtype=np.int16)
                amplitude = np.abs(audio_data).mean()
                score = self._wake_detector.detect(frame)
                print(f"[VOICE] Heartbeat: level={amplitude:.1f}, score={score:.2f}")

            if not recording:
                score = self._wake_detector.detect(frame)
                if score >= self._wake_threshold:
                    recording = True
                    speech_seen = False
                    buffer_frames = []
                    record_start = time.time()
                    last_voice_time = time.time()
                    print(f"[VOICE] 🟢 Đã nghe Wake Word ({self._wake_word}). Đang lắng nghe lệnh...")
                continue

            buffer_frames.append(frame)
            if self._vad.is_speech(frame):
                speech_seen = True
                last_voice_time = time.time()

            if record_start and (time.time() - record_start) * 1000 >= self._max_record_ms:
                print("[VOICE] max record timeout")
                transcript = self._asr.transcribe(b"".join(buffer_frames))
                if transcript:
                    yield transcript
                recording = False
                continue

            if speech_seen and last_voice_time:
                silence_elapsed = (time.time() - last_voice_time) * 1000
                if silence_elapsed >= self._silence_ms:
                    print("[VOICE] silence detected")
                    transcript = self._asr.transcribe(b"".join(buffer_frames))
                    if transcript:
                        yield transcript
                    recording = False


class MicrophoneStream:
    def __init__(self, audio_queue, sample_rate=16000, frame_ms=20, device=None):
        self._queue = audio_queue
        self._sample_rate = sample_rate
        self._frame_ms = frame_ms
        self._device = device
        self._stream = None
        self._frame_samples = int(sample_rate * frame_ms / 1000)

    def start(self):
        try:
            import sounddevice as sd
        except Exception as exc:
            raise VoiceError("Can cai sounddevice de dung voice.") from exc

        def callback(indata, frames, time_info, status):
            if status:
                return
            self._queue.put(bytes(indata))

        self._stream = sd.RawInputStream(
            samplerate=self._sample_rate,
            blocksize=self._frame_samples,
            channels=1,
            dtype="int16",
            callback=callback,
            device=self._device,
        )
        self._stream.start()

    def stop(self):
        if self._stream:
            self._stream.stop()
            self._stream.close()
            self._stream = None


class WakeWordDetector:
    def __init__(self, wake_word, threshold):
        self._wake_word = wake_word
        self._threshold = threshold
        self._model = None
        self._available = False

        try:
            from openwakeword.model import Model
            # Explicitly use ONNX since tflite-runtime is not available
            self._model = Model(
                wakeword_models=[wake_word] if wake_word else None,
                inference_framework="onnx"
            )
            self._available = True
        except Exception as e:
            print(f"[VOICE] Error loading wakeword model '{wake_word}': {e}")
            self._available = False

    def detect(self, frame):
        if not self._available:
            return 0.0
        try:
            import numpy as np
        except Exception:
            return 0.0

        audio = np.frombuffer(frame, dtype=np.int16)
        scores = self._model.predict(audio)
        
        score = 0.0
        if isinstance(scores, dict):
            # Tim key chua wake_word (vi du: 'hey_jarvis_v0.1')
            for key, val in scores.items():
                if self._wake_word and self._wake_word in key:
                    score = val
                    break
            else:
                score = max(scores.values()) if scores else 0.0
        else:
            score = float(scores)
        return score

class VoskVoiceActivityDetector:
    def __init__(self, model, sample_rate, frame_ms):
        self._sample_rate = sample_rate
        self._frame_ms = frame_ms
        self._recognizer = None
        self._available = False

        try:
            from vosk import KaldiRecognizer
            self._recognizer = KaldiRecognizer(model, sample_rate)
            self._recognizer.SetWords(False)
            self._available = True
        except Exception:
            self._recognizer = None
            self._available = False

    def is_speech(self, frame):
        if not self._available:
            return True
        if self._frame_ms not in (10, 20, 30):
            return True
        try:
            self._recognizer.AcceptWaveform(frame)
            partial = json.loads(self._recognizer.PartialResult())
            text = partial.get("partial", "").strip()
            return bool(text)
        except Exception:
            return True


class AsrEngine:
    def __init__(self, model_path, sample_rate):
        self._model_path = model_path
        self._sample_rate = sample_rate
        self._model = None
        if not model_path:
            raise VoiceError("Can cai dat VOICE_ASR_MODEL de dung ASR offline.")
        try:
            from vosk import Model
            self._model = Model(model_path)
        except Exception as exc:
            raise VoiceError("Khong the tai model Vosk.") from exc

    def transcribe(self, audio_bytes):
        if not audio_bytes:
            return ""
        try:
            from vosk import KaldiRecognizer
        except Exception:
            return ""

        recognizer = KaldiRecognizer(self._model, self._sample_rate)
        recognizer.AcceptWaveform(audio_bytes)
        result = json.loads(recognizer.Result())
        text = result.get("text", "").strip()
        return text

    @property
    def model(self):
        return self._model
