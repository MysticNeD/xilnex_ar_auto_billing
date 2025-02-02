"""
Author: Bryan

Read below for disclamer

"""


import pyautogui as pa
import time
import keyboard
import os
import sys
import cv2
import numpy as np
from mss import mss
import logging
import pyperclip
from datetime import datetime
from threading import Thread
import ctypes

# create autolog everytimme in Downloads\Xilnex_Auto_AR_Billing
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_file_path = os.path.join(os.path.expanduser("~"), "Downloads", "Xilnex_Auto_AR_Billing", f"automation_{timestamp}.log")

logging.basicConfig(filename=log_file_path, filemode='w', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

running = False
max_attempts = 10 # can reduce attempts to increase efficiency

# if need to change from coordinates to picture locate, add image start from here and copy the format
image_path = "Xilnex_Auto_AR_Billing\\Confirmation_2_Enter.png"
image2_path = 'Xilnex_Auto_AR_Billing\\billed_success.png'
image3_path = 'Xilnex_Auto_AR_Billing\\billed_fail.png'
image4_path = 'Xilnex_Auto_AR_Billing\\menu.png'
image5_path = 'Xilnex_Auto_AR_Billing\\final run.png'

template1 = cv2.imread(image_path, cv2.IMREAD_COLOR)
template2 = cv2.imread(image2_path, cv2.IMREAD_COLOR)
template3 = cv2.imread(image3_path, cv2.IMREAD_COLOR)
template4 = cv2.imread(image4_path, cv2.IMREAD_COLOR)
template5 = cv2.imread(image5_path, cv2. IMREAD_COLOR)

def capture_screen():
    try:
        with mss() as sct:
            screenshot = sct.grab(sct.monitors[1])
            img = np.array(screenshot)
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            logging.info("Captured screen for template matching.")
        return img
    except Exception as e:
        logging.error(f"Error capturing screen: {e}")
        return None

def match_template_on_screen(template, threshold=0.5):    # dont change threshold if not necessary
    try:
        screen = capture_screen()
        if screen is None:
            logging.warning("Screen capture failed. Template matching skipped.")
            return None if not return_confidence else (None,0.0)
        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        logging.info(f"Template matching max value: {max_val}")
        if max_val >= threshold:
            logging.info(f"Template found with value: {max_val} at location: {max_loc}")
            return (max_loc, max_val) if return_confidence else max_loc
        else:
            logging.info("Template not found.")
        return None if not return_confidence else (None,0.0)
    except Exception as e:
        logging.error(f"Error in template matching: {e}")
        return None if not return_confidence else (None,0.0)

# checkpoint.
def check_clickboard_change(original_content, new_content):
    if new_content != original_content:
        logging.info("Clipboard updated")
        print("Clipboard updated")
        return True
    else:
        logging.error("Cliboard did not updated. Error happens. Stopping program")
        print("Clipboard updated failed")
        sys.exit()
    


def locate_and_click_image():
    attempt = 0
    found = False
    while attempt < max_attempts:
        location = match_template_on_screen(template1, threshold=0.3) # do not change threshold
        if location:
            logging.info(f"Confirmation template found. Pressing Enter. Attempt {attempt + 1}")
            pa.press('enter')
            print("confirmation done")
            time.sleep(5) # do not change
            pa.click(x=850, y=680, duration=0.3)
            time.sleep(0.5) # can reduce
            pa.hotkey('ctrl', 'w')
            logging.info("ctrl+w hotkey done")
            print("ctrl+w hotkey done")
            found = True
            break
        else:
            attempt += 1
            logging.warning(f"Confirmation template not found. Retrying... ({attempt}/{max_attempts})")
            time.sleep(2) # can reduce
    if not found:
        logging.error("Confirmation template not found after maximum attempts. Clicking fallback position.")
        pa.click(x=850, y=680, duration=1)
        time.sleep(5) # do not change
        pa.hotkey('ctrl', 'w')

"""
explanation of (locate_and_click_image):
When you click confirm invoice, it shows up with confirmation
mostly have 2's, but in minor cases there are only one confirmation
and it is easy to freeze (crashed) if the pc pressed enter again
time.sleep(5) is calculated to minimize the risk of crashed after pressed enter and not "sales confirmed"

"""
def caps_lock_status() -> bool:
    VK_CAPITAL = 0x14
    return bool(ctypes.windll.user32.GetKeyState(VK_CAPITAL) & 1)

def start_automation():
    global running
    if not caps_lock_status():
        if not running:
            running = True
            logging.info("Automation started from GUI")
            Thread(target=perform_action, daemon=True).start()
    else:
        print("Cannot start automation because Caps Lock is ON")
    
def stop_automation():
    global running
    if running: 
        running = False
        logging.info("Automation stopped from GUI")

def toggle_running():
    global running
    if caps_lock_status():
        print("Cannot toggle automation because caps lock is ON")
        return
    running = not running
    if running:
        logging.info("Automation started.")
    else:
        logging.info("Automation paused.")

keyboard.add_hotkey("F8", toggle_running)  # can change "F8" to any other hotkey

def stop_program():
    global running
    running = False
    logging.info("Stopping the program and exiting.")
    os._exit(0)

keyboard.add_hotkey("F9", stop_program)

"""
final_action bug: sometimes the error shows “clickboard update failed" because it was copied ealier, currently no solution
for every time.sleep() except row 166 can be reduced if necessary
(FYI: you dont need to reduce time.sleep() because final_action() will only start when it is on last scroll, it did not increase the efficiency very well)
"""
def final_action():
    if running:
        logging.info("Final run started.")
        pa.press('space')
        time.sleep(4)
        pa.hotkey('ctrl','w')
        logging.info('4th bill')
        time.sleep(3)
        pa.click(x=124, y=477, duration = 1)
        time.sleep(0.3)
        pa.click(button= 'right')
        if not running: return

        original_content = pyperclip.paste()

        pa.click(x=208, y=490, duration=0.2)
        if not running: return

        time.sleep(0.5)
        new_content = pyperclip.paste()
            
        check_clickboard_change(original_content, new_content)

        time.sleep(0.5)    
        pa.click(x=125, y=477, button='right', duration=0.3)
        if not running: return
        time.sleep(0.5)
        pa.click(x=205, y=760, duration=0.5)
        if not running: return
        time.sleep(0.5)
        pa.press('enter')
        time.sleep(3)

        perform_repetitive_action()

        logging.info('5th bill')
        time.sleep(3)
        pa.click(x=135, y=527, duration=0.5)
        time.sleep(0.2)
        pa.click(button='right')
        if not running: return

        original_content = pyperclip.paste()

        pa.click(x=205, y=545, duration=0.2)
        if not running: return
            
        time.sleep(0.5)
        new_content = pyperclip.paste()

        check_clickboard_change(original_content, new_content)

        pa.click(x=135, y=527, button='right', duration=0.3)
        time.sleep(0.5)
        pa.click(x=209, y=808, duration=0.5)
        if not running: return
        time.sleep(0.5)
        pa.press('enter')
        time.sleep(3)

        perform_repetitive_action()
        logging.info("6th bill.")
        time.sleep(3)
        pa.click(x=130, y=572, duration=0.5)
        time.sleep(0.2)
        pa.click(button='right')
        if not running: return

        original_content = pyperclip.paste()

        pa.click(x=206, y=592, duration=0.2)
        if not running: return
            
        time.sleep(0.5)
        new_content = pyperclip.paste()

        check_clickboard_change(original_content, new_content)

        pa.click(x=130, y=572, button='right', duration=0.3)
        time.sleep(0.5)
        pa.click(x=190, y=848, duration=0.5)
        if not running: return
        time.sleep(0.5)
        pa.press('enter')
        time.sleep(3)

        perform_repetitive_action()

        logging.info("7th bill.")
        time.sleep(2)
        pa.click(x=138, y=614, duration=0.5)
        time.sleep(0.2)
        pa.click(button='right')
        if not running: return

        original_content = pyperclip.paste()

        pa.click(x=221, y=632, duration=0.2)
        if not running: return
            
        time.sleep(0.5)
        new_content = pyperclip.paste()

        check_clickboard_change(original_content, new_content)

        pa.click(x=138, y=614, button='right', duration=0.3)
        time.sleep(0.5)
        pa.click(x=218, y=893, duration=0.5)
        if not running: return
        time.sleep(0.5)
        pa.press('enter')
        time.sleep(3)

        perform_repetitive_action()

        logging.info("8th bill.")
        time.sleep(2)
        pa.click(x=118, y=658, duration=0.5)
        time.sleep(0.2)
        pa.click(button='right')
        if not running: return

        original_content = pyperclip.paste()

        pa.click(x=207, y=687, duration=0.2)
        if not running: return
            
        time.sleep(0.5)
        new_content = pyperclip.paste()

        check_clickboard_change(original_content, new_content)

        pa.click(x=118, y=658, button='right', duration=0.3)
        time.sleep(0.5)
        pa.click(x=195, y=947, duration=0.5)
        if not running: return
        time.sleep(0.5)
        pa.press('enter')
        time.sleep(3)

        perform_repetitive_action()

        logging.info("9th bill.")
        time.sleep(2)
        pa.click(x=132, y=709, duration=0.5)
        time.sleep(0.2)
        pa.click(button='right')
        if not running: return

        original_content = pyperclip.paste()

        pa.click(x=204, y=729, duration=0.2)
        if not running: return
            
        time.sleep(0.5)
        new_content = pyperclip.paste()

        check_clickboard_change(original_content, new_content)

        pa.click(x=132, y=709, button='right', duration=0.3)
        time.sleep(0.5)
        pa.click(x=204, y=987, duration=0.5)
        if not running: return
        time.sleep(0.5)
        pa.press('enter')
        time.sleep(3)

        perform_repetitive_action()

        logging.info("10th bill.")
        time.sleep(2)
        pa.click(x=132, y=751, duration=0.5)
        time.sleep(0.2)
        pa.click(button='right')
        if not running: return

        original_content = pyperclip.paste()

        pa.click(x=211, y=424, duration=0.2)
        if not running: return
            
        time.sleep(0.5)
        new_content = pyperclip.paste()

        check_clickboard_change(original_content, new_content)

        pa.click(x=132, y=751, button='right', duration=0.3)
        time.sleep(0.5)
        pa.click(x=212, y=686, duration=0.5)
        if not running: return
        time.sleep(0.5)
        pa.press('enter')
        time.sleep(3)

        perform_repetitive_action()

        logging.info("11th bill.")
        time.sleep(2)
        pa.click(x=119, y=797, duration=0.5)
        time.sleep(0.2)
        pa.click(button='right')
        if not running: return

        original_content = pyperclip.paste()

        pa.click(x=192, y=472, duration=0.2)
        if not running: return
            
        time.sleep(0.5)
        new_content = pyperclip.paste()

        check_clickboard_change(original_content, new_content)

        pa.click(x=119, y=797, button='right', duration=0.3)
        time.sleep(0.5)
        pa.click(x=199, y=734, duration=0.5)
        if not running: return
        time.sleep(0.5)
        pa.press('enter')
        time.sleep(3)

        perform_repetitive_action()

        logging.info("12th bill.")
        time.sleep(2)
        pa.click(x=133, y=842, duration=0.5)
        time.sleep(0.2)
        pa.click(button='right')
        if not running: return

        original_content = pyperclip.paste()

        pa.click(x=210, y=515, duration=0.2)
        if not running: return
            
        time.sleep(0.5)
        new_content = pyperclip.paste()

        check_clickboard_change(original_content, new_content)

        pa.click(x=133, y=842, button='right', duration=0.3)
        time.sleep(0.5)
        pa.click(x=209, y=779, duration=0.5)
        if not running: return
        time.sleep(0.5)
        pa.press('enter')
        time.sleep(3)

        perform_repetitive_action()

        logging.info("13th bill, final bill.")
        time.sleep(2)
        pa.click(x=117, y=888, duration=0.5)
        time.sleep(0.2)
        pa.click(button='right')
        if not running: return

        original_content = pyperclip.paste()

        pa.click(x=198, y=565, duration=0.2)
        if not running: return
            
        time.sleep(0.5)
        new_content = pyperclip.paste()

        check_clickboard_change(original_content, new_content)

        pa.click(x=117, y=888, button='right', duration=0.3)
        time.sleep(0.5)
        pa.click(x=187, y=830, duration=0.5)
        if not running: return
        time.sleep(0.5)
        pa.press('enter')
        time.sleep(3)

        perform_repetitive_action()

# every time.sleep() in perform_repetitive_action is tested until maximum affordable time, not recommended to reduce
def perform_repetitive_action():
    try:
        logging.info("Performing billing action.")
        pa.click(x=1201, y=188, duration=0.5)
        if not running: return
        time.sleep(0.5)
        pa.click(x=748, y=220, duration=0.5)
        if not running: return
        time.sleep(0.5)
        pa.write('ko', interval= 0.2)
        if not running: return
        time.sleep(0.5)
        pa.press('enter')
        if not running: return
        time.sleep(0.5)
        pa.click(x=302, y=495, duration=0.7)
        if not running: return
        time.sleep(0.5)
        pa.write('S.T ', interval=0.2)
        if not running: return
        time.sleep(0.5)
        pa.hotkey('ctrl', 'v')
        if not running: return
        time.sleep(0.5)
        pa.click(x=949, y=990, duration=1)
        if not running: return
        time.sleep(0.5)
        pa.click(x=156, y=940, duration=0.6)
        if not running: return
        time.sleep(0.5)
        pa.press('enter')
        time.sleep(1)
        locate_and_click_image()
        time.sleep(0.2)
        """
        (have bug)
        found_image2 = False
        for attempt in range(3):
            found_image2, confidence2 = match_template_on_screen(template2, threshold=0.72, return_confidence=True)
            logging.info(f"Attempt {attempt+1}: billed_success match confidence: {confidence2}")
            print(f"Attempt {attempt+1}: billed_success match confidence: {confidence2}")

            if found_image2:
                logging.info(f"Found billed_success image: {image2_path}. Continuing process.")
                print(f"Found billed_success image: {image2_path}. Continuing process.")
                break  # 成功匹配到 billed_success，跳出循环

            time.sleep(0.2)  # 避免检测速度过快

        found_image3 = match_template_on_screen(template3, threshold=0.5)

        if found_image2:
            pass  # 已找到 billed_success，继续后续流程
        elif found_image3 or not found_image2:
            found_image4 = match_template_on_screen(template4, threshold=0.8)
            if found_image4:
                logging.info("Menu detected. Terminating process.")
                print("Menu detected. Terminating process.")
                sys.exit()
            else:
                logging.info("Found billed_fail or no images found. Performing ctrl+w.")
                print("Found fail or no image")
                time.sleep(5)
                pa.click(x=850, y=680, duration=1)
                pa.hotkey('ctrl', 'w')
        """
    except Exception as e:
        logging.error(f"Error during repetitive action: {e}")

def perform_action():
    while True:
        if running:
            logging.info("Main automation action started.")
            pa.click(x=156, y=346, duration=1)
            time.sleep(0.3)
            pa.click(button='right')
            if not running: return
            
            original_content = pyperclip.paste()

            pa.click(x=239, y=370, duration=0.2)
            if not running: return

            time.sleep(0.5)
            new_content = pyperclip.paste()
            
            check_clickboard_change(original_content, new_content)

            time.sleep(0.5)    
            pa.click(x=156, y=346, button='right', duration=0.3)
            if not running: return
            time.sleep(0.5)
            pa.click(x=290, y=628, duration=0.5)
            if not running: return
            time.sleep(0.5)
            pa.press('enter')
            time.sleep(3)

            detected = match_template_on_screen(template5, threshold=0.8)
            if detected:
                print("Detected Final Loop.")
                final_action()
                logging.info('All Billed. Stop Program')
                stop_program()

            perform_repetitive_action()

            logging.info("Resetting to second position.")
            time.sleep(2)
            pa.click(x=138, y=396, duration=0.5)
            time.sleep(0.2)
            pa.click(button='right')
            if not running: return

            original_content = pyperclip.paste()

            pa.click(x=207, y=414, duration=0.2)
            if not running: return
            
            time.sleep(0.5)
            new_content = pyperclip.paste()

            check_clickboard_change(original_content, new_content)

            pa.click(x=138, y=396, button='right', duration=0.3)
            time.sleep(0.5)
            pa.click(x=280, y=675, duration=0.5)
            if not running: return
            time.sleep(0.5)
            pa.press('enter')
            time.sleep(3)

            perform_repetitive_action()

            logging.info("Resetting to third position.")
            time.sleep(5) # can reduce
            pa.click(x=139, y=436, duration=0.5)
            time.sleep(0.2)
            pa.click(button='right')
            if not running: return

            original_content = pyperclip.paste()

            pa.click(x=221, y=454, duration=0.2)
            if not running: return
            
            time.sleep(0.5)
            new_content = pyperclip.paste()

            check_clickboard_change(original_content, new_content)

            time.sleep(0.5)
            pa.click(x=139, y=436, button='right', duration=0.3)
            time.sleep(0.5)
            pa.click(x=348, y=729, duration=0.5)
            if not running: return
            time.sleep(0.5)
            pa.press('enter')
            time.sleep(3)

            perform_repetitive_action()

            logging.info("Loop done. Preparing to scroll for new loop.")
            time.sleep(5) # can reduce
            pa.moveTo(x=156, y=346, duration=0.2)
            time.sleep(0.5)
            pa.scroll(-200)
            time.sleep(0.5)
        time.sleep(0.1)

perform_action()

# Created and modified by Bryan @ 13/11/2024
# This is not the final version of the code. Any changes (after the date) of code
    # unilateral (this side) does not done and not intention by me.
# For more information please reach out to me. 

#------------------------------------------------------------------------------------------#

# This code has been tested from 18/11/24 to 19/11/24, in result with 1700+ test and 0 error
# It is to confirm that the code has been perfectly runs in the version of Xilnex before 20/11/24
# Any update version that is not informed to me or modified by me that caused any error should not in my behalf
