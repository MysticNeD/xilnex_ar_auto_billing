import cv2
import numpy as np
import pyautogui as pa
import time

bill_image = 'C:\\Users\\yourusername\\Downloads\\Xilnex_Auto_AR_Billing\\bill_text.png'

def click_bill(template, threshold = 0.8):
    template = cv2.imread(template, 0)
    w, h = template.shape[::-1]

    screenshot = pa.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

    res = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)

    for pt in zip(*loc[::-1]):
        pa.moveTo(x=pt[0] + w // 2, y=pt[1] + h // 2, duration=0.5)
        time.sleep(0.1)
        pa.click()
        break

if __name__ == "__main__":
    click_bill(bill_image)

