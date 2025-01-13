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
import bill

# create autolog everytimme in Downloads\Xilnex_Auto_AR_Billing
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_file_path = os.path.join(os.path.expanduser("~"), "Downloads", "Xilnex_Auto_AR_Billing", f"automation_{timestamp}.log")

logging.basicConfig(filename=log_file_path, filemode='w', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

running = False
max_attempts = 10 # can reduce attempts to increase efficiency

# if need to change from coordinates to picture locate, add image start from here and copy the format
image_path = "C:\\Users\\yourusername\\Downloads\\Xilnex_Auto_AR_Billing\\Pictures\\Confirmation_2_Enter.png"
image2_path = 'C:\\Users\\yourusername\\Downloads\\Xilnex_Auto_AR_Billing\\Pictures\\billed_success.png'
image3_path = 'C:\\Users\\yourusername\\Downloads\\Xilnex_Auto_AR_Billing\\Pictures\\billed_fail.png'
image4_path = 'C:\\Users\\yourusername\\Downloads\\Xilnex_Auto_AR_Billing\\Pictures\\menu.png'
image5_path = 'C:\\Users\\yourusername\\Downloads\\Xilnex_Auto_AR_Billing\\Pictures\\final run.png'
image6_path = 'C:\\Users\\yourusername\\Downloads\\Xilnex_Auto_AR_Billing\\Pictures\\sales_invoice_tab.png'
image7_path = 'C:\\Users\\yourusername\\Downloads\\Xilnex_Auto_AR_Billing\\Pictures\\sales_confirmed.png'
bill_image = 'C:\\Users\\yourusername\\Downloads\\Xilnex_Auto_AR_Billing\\Pictures\\bill_text.png'


template1 = cv2.imread(image_path, cv2.IMREAD_COLOR)
template2 = cv2.imread(image2_path, cv2.IMREAD_COLOR)
template3 = cv2.imread(image3_path, cv2.IMREAD_COLOR)
template4 = cv2.imread(image4_path, cv2.IMREAD_COLOR)
template5 = cv2.imread(image5_path, cv2. IMREAD_COLOR)
template6 = cv2.imread(image6_path, cv2.IMREAD_COLOR)
template7 = cv2.imread(image7_path, cv2.IMREAD_COLOR)

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
    
def sit_detect(template6, threshold = 0.5, timeout = 15, return_confidence=False):
    start_time = time.time()
    with mss() as sct:
        while time.time() - start_time < timeout:
            logging.info("Start to detect Sales Invoice Tab")
            screenshot = np.array(sct.grab(sct.monitors[0]))
            screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)
            template6 = cv2.imread(image6_path, cv2.IMREAD_COLOR)
            result = cv2.matchTemplate(screenshot, template6, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, _ = cv2.minMaxLoc(result)
            if max_val >= threshold:
                logging.info(f"Sales Invoice Tab Detected with confidence {return_confidence}. Perform Action")
                return True if return_confidence else max_val
            time.sleep(0.5)
    logging.warning("Tab not detected during timeout period")
    return False

def sc_detect(template7, threshold = 0.6, timeout = 20, return_confidence=False):
    start_time2 = time.time()
    with mss() as sct:
        while time.time() - start_time2 < timeout:
            logging.info("Waiting for Sales Confirmed")
            screenshot2 = np.array(sct.grab(sct.monitors[0]))
            screenshot2 = cv2.cvtColor(screenshot2, cv2.COLOR_BGRA2BGR)
            template7 = cv2.imread(image7_path, cv2.IMREAD_COLOR)
            result = cv2.matchTemplate(screenshot2, template7, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, _ = cv2.minMaxLoc(result)
            if max_val >= threshold:
                logging.info(f"Sales Confirmed. Perform Action")
                return True if return_confidence else max_val
            time.sleep(0.5)
    logging.warning("Tab not detected during timeout period")
    return False

def match_template_on_screen(template, threshold=0.5, return_confidence=False):    # dont change threshold if not necessary
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

def sc_check():
    found_image7 = sit_detect(image7_path, threshold = 0.6, return_confidence=True)
    if found_image7:
        logging.info(f"Sales Confirmed detected with confidence.")
        time.sleep(1)
        pa.click(x=850, y=680, duration=0.3)
        time.sleep(0.5) # can reduce
        pa.hotkey('ctrl', 'w')
        logging.info("ctrl+w hotkey done")
        print("ctrl+w hotkey done")

    else:
        logging.warning("Cannot find Sales Confirmed.")
        time.sleep(5)
        pa.click(x=850, y=680, duration=1)
        time.sleep(5) # do not change
        pa.hotkey('ctrl', 'w')   

def locate_and_click_image():
    attempt = 0
    found = False
    while attempt < max_attempts:
        location = match_template_on_screen(template1, threshold=0.5) # do not change threshold
        if location:
            logging.info(f"Confirmation template found. Pressing Enter. Attempt {attempt + 1}")
            pa.press('enter')
            print("confirmation done")
            time.sleep(1) # do not change
            sc_check()
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
        found = True

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
        print("Cannot start automation because CAPS LOCK is ON")

def stop_automation():
    global running
    if running: 
        running = False
        logging.info("Automation stopped from GUI")

def toggle_running():
    global running
    if caps_lock_status():
        print("Cannot perform automation because CAPS LOCK is ON")
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
        pass
        """
        found_image2 = False
        for attempt in range(3):
            found_image2, confidence2 = match_template_on_screen(template2, threshold=0.8, return_confidence=True)
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

def check_sit():
    found_image6= sit_detect(image6_path, threshold = 0.8, return_confidence=True)
    if found_image6:
        logging.info(f"Sales Invoice Tab detected.")
        time.sleep(2)
        perform_repetitive_action()
    else:
        logging.warning("Waiting for 5 seoonds before starting the action")
        time.sleep(5)
        perform_repetitive_action()

def perform_action():
    while True:
        if running:
            logging.info("Main automation action started.")
            pa.click(x=156, y=346, duration=1)
            time.sleep(0.3)
            if not running: return
            original_content = pyperclip.paste()
            pa.hotkey('ctrl','c')
            if not running: return
            time.sleep(0.5)
            new_content = pyperclip.paste()
            check_clickboard_change(original_content, new_content)  
            pa.click(x=156, y=346, button='right', duration=0.3)
            if not running: return
            time.sleep(0.5)
            bill.click_bill(bill_image) #pa.click(x=290, y=628, duration=0.5)
            if not running: return
            time.sleep(0.5)
            pa.press('enter')
            time.sleep(5)

            detected = match_template_on_screen(template5, threshold=0.8)
            if detected:
                print("Detected Final Loop.")
                final_action()
                logging.info('All Billed. Stop Program')
                stop_program()

            check_sit()

            logging.info("Resetting to second position.")
            time.sleep(2)
            pa.click(x=138, y=396, duration=0.5)
            time.sleep(0.2)
            if not running: return
            original_content = pyperclip.paste()
            pa.hotkey('ctrl','c')
            if not running: return
            time.sleep(0.5)
            new_content = pyperclip.paste()

            check_clickboard_change(original_content, new_content)

            pa.click(x=138, y=396, button='right', duration=0.3)
            time.sleep(0.5)
            bill.click_bill(bill_image) #pa.click(x=280, y=675, duration=0.5)
            if not running: return
            time.sleep(0.5)
            pa.press('enter')
            time.sleep(0.5)

            check_sit()

            logging.info("Resetting to third position.")
            time.sleep(5) # can reduce
            pa.click(x=139, y=436, duration=0.5)
            time.sleep(0.2)
            if not running: return
            original_content = pyperclip.paste()
            pa.hotkey('ctrl','c')
            if not running: return
            
            time.sleep(0.5)
            new_content = pyperclip.paste()

            check_clickboard_change(original_content, new_content)

            time.sleep(0.5)
            pa.click(x=139, y=436, button='right', duration=0.3)
            time.sleep(0.5)
            bill.click_bill(bill_image) #pa.click(x=348, y=729, duration=0.5)
            if not running: return
            time.sleep(0.5)
            pa.press('enter')
            time.sleep(0.5)

            check_sit()

            logging.info("Loop done. Preparing to scroll for new loop.")
            time.sleep(5) # can reduce
            pa.moveTo(x=156, y=346, duration=0.2)
            time.sleep(0.5)
            pa.scroll(-200)
            time.sleep(0.5)
        time.sleep(0.1)

perform_action()
