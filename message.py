import time
import sys

def display_analyzing_message(stop_event):
    """
    Display a lively and friendly animated analyzing message while processing the query.
    """
    message = "Shino is thinking about your question 💭"
    animation_chars = ["-", "\\", "|", "/"]
    animation_index = 0
    while not stop_event.is_set():
        sys.stdout.write(f"\r{message} {animation_chars[animation_index]}")
        sys.stdout.flush()
        time.sleep(0.2)
        animation_index = (animation_index + 1) % len(animation_chars)

        # Add extra flair with a caring message
        if animation_index == 0:
            sys.stdout.write("\r" + " " * (len(message) + 4) + "\r")
            sys.stdout.write(f"\r{message}")
            sys.stdout.flush()
    sys.stdout.write("\n")
    sys.stdout.flush()
