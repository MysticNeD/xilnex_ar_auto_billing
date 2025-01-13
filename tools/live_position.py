import pyautogui as pa
import keyboard
import time

x, y = pa.position()
running = False

def run_live():
    global running, x, y
    running = not running
    if running:
        print("Started")
        while running:
            x1, y1 = pa.position()
            if x1 != x or y1 != y:
                x, y = x1, y1
                print(x, y)
            time.sleep(0.1)  # prevent crash
    else:
        print("Stopped")

keyboard.add_hotkey("F8", run_live)

# kill terminal to stop
