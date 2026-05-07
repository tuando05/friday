import pyttsx3
import threading
import queue


class Speaker:
    def __init__(self, config):
        self._config = config
        self._enabled = config.TTS_ENABLED
        self._rate = config.TTS_RATE
        self._volume = config.TTS_VOLUME
        self._voice_id = config.TTS_VOICE_ID
        
        self._queue = queue.Queue()
        self._stop_event = threading.Event()
        self._thread = None
        
        if self._enabled:
            self._thread = threading.Thread(target=self._worker, daemon=True)
            self._thread.start()

    def say(self, text):
        if not self._enabled or not text:
            return
        # Clean text (remove markdown or special symbols if necessary)
        cleaned_text = text.strip()
        if cleaned_text:
            self._queue.put(cleaned_text)

    def stop(self):
        self._stop_event.set()
        self._queue.put(None)  # Signal to stop worker
        if self._thread:
            self._thread.join(timeout=1.0)

    def _worker(self):
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', self._rate)
            engine.setProperty('volume', self._volume)
            
            if self._voice_id:
                engine.setProperty('voice', self._voice_id)
            
            while not self._stop_event.is_set():
                try:
                    text = self._queue.get(timeout=0.1)
                    if text is None:
                        break
                    
                    engine.say(text)
                    engine.runAndWait()
                except queue.Empty:
                    continue
                except Exception as e:
                    print(f"[SPEAKER] Error: {e}")
        except Exception as e:
            print(f"[SPEAKER] Init Error: {e}")
            self._enabled = False
