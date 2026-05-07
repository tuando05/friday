import queue
import threading

from core import commands, services


def format_assistant_message(name, content):
    if content is None:
        return f"{name}:"
    cleaned = content.strip()
    if not cleaned:
        return f"{name}:"
    return f"{name}:\n{cleaned}"


def input_worker(input_queue, stop_event, prompt_text):
    while not stop_event.is_set():
        try:
            text = input(prompt_text())
        except (EOFError, KeyboardInterrupt):
            input_queue.put(None)
            return
        input_queue.put(text)

def main():
    svc = services.build_services()
    print(f"--- {svc.config.AI_NAME} Mark 1 Modular Online ---")
    
    # Khởi tạo trí nhớ
    chat_history = svc.memory.load_memory()
    
    input_queue = queue.Queue()
    transcript_queue = queue.Queue()
    stop_event = threading.Event()

    svc.voice.set_transcript_queue(transcript_queue)

    input_thread = threading.Thread(
        target=input_worker,
        args=(input_queue, stop_event, lambda: f"\n{svc.config.BOSS_NAME}: "),
        daemon=True,
    )
    input_thread.start()

    def handle_text(text, source):
        nonlocal chat_history

        if source == "voice":
            print(f"[VOICE] nhan dien: {text}")

        result = commands.handle_command(text, chat_history, svc)
        if result.handled:
            if result.message:
                print(format_assistant_message(svc.config.AI_NAME, result.message))
            chat_history = result.chat_history
            return result.should_exit

        reply = svc.brain.generate_response(text, chat_history)
        chat_history.append({'role': 'user', 'content': text})
        chat_history.append({'role': 'assistant', 'content': reply})
        svc.memory.save_memory(chat_history)
        print(format_assistant_message(svc.config.AI_NAME, reply))
        svc.speaker.say(reply)
        return False

    try:
        while True:
            try:
                user_input = input_queue.get(timeout=0.1)
                if user_input is None:
                    break
                if handle_text(user_input, "text"):
                    break
            except queue.Empty:
                pass

            while True:
                try:
                    transcript = transcript_queue.get_nowait()
                except queue.Empty:
                    break
                if handle_text(transcript, "voice"):
                    stop_event.set()
                    svc.voice.stop()
                    return
    except KeyboardInterrupt:
        pass
    finally:
        stop_event.set()
        svc.voice.stop()
        svc.speaker.stop()

if __name__ == "__main__":
    main()