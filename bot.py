import cv2
import numpy as np
import pyautogui
import mss
import time
import os

# Load templates
ASSET_PATH = 'assets'
tent_template = cv2.imread(os.path.join(ASSET_PATH, 'tent.png'), 0)
threshold = 0.7

def find_object(template, gray_frame, threshold=0.7):
    result = cv2.matchTemplate(gray_frame, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >= threshold)
    if loc[0].size > 0:
        y, x = loc[0][0], loc[1][0]
        return (x, y)
    return None

def move_towards(x, y, screen_center):
    dx = x - screen_center[0]
    dy = y - screen_center[1]

    if dx < -20:
        pyautogui.press('a')
    elif dx > 20:
        pyautogui.press('d')

    if dy < -20:
        pyautogui.press('w')
    elif dy > 20:
        pyautogui.press('s')

def shoot():
    pyautogui.press('space')

def main_loop():
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # Layar utama
        center = (monitor['width'] // 2, monitor['height'] // 2)

        print("Bot aktif. Tekan Ctrl+C untuk berhenti.")
        time.sleep(2)

        while True:
            screenshot = np.array(sct.grab(monitor))
            frame_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

            tent_pos = find_object(tent_template, frame_gray, threshold)
            if tent_pos:
                move_towards(*tent_pos, screen_center=center)

            shoot()
            time.sleep(0.08)

if __name__ == "__main__":
    main_loop()
