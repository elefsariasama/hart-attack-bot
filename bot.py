import cv2
import numpy as np
import pyautogui
import mss
import time

# Load template
tent_template = cv2.imread("assets/tent.png", 0)

# Settings
THRESHOLD = 0.75

def find_tent(frame_gray):
    result = cv2.matchTemplate(frame_gray, tent_template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >= THRESHOLD)
    if loc[0].size > 0:
        y, x = loc[0][0], loc[1][0]
        return (x, y)
    return None

def move_towards(x, y, screen_center):
    dx = x - screen_center[0]
    dy = y - screen_center[1]

    if dx < -20: pyautogui.press('a')
    elif dx > 20: pyautogui.press('d')

    if dy < -20: pyautogui.press('w')
    elif dy > 20: pyautogui.press('s')

def shoot():
    pyautogui.press('space')

with mss.mss() as sct:
    monitor = sct.monitors[1]
    center = (monitor['width']//2, monitor['height']//2)

    while True:
        img = np.array(sct.grab(monitor))
        frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        tent = find_tent(frame)
        if tent:
            move_towards(tent[0], tent[1], center)

        shoot()
        time.sleep(0.1)
