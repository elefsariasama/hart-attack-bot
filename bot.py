import cv2
import numpy as np
import pyautogui
import time
import os

# ======== Konfigurasi ========
TENT_THRESHOLD = 0.65
ASTEROID_THRESHOLD = 0.65
PLAYER_THRESHOLD = 0.7
MOVE_DELAY = 0.05

# Lokasi assets
ASSETS_DIR = os.path.join(os.path.dirname(__file__), 'assets')
tent_template = cv2.imread(os.path.join(ASSETS_DIR, 'tent_v2.png'), 0)
player_template = cv2.imread(os.path.join(ASSETS_DIR, 'player_rocket.png'), 0)
asteroid_templates = [
    cv2.imread(os.path.join(ASSETS_DIR, 'asteroid_blue_v2.png'), 0),
    cv2.imread(os.path.join(ASSETS_DIR, 'asteroid_green_v2.png'), 0),
    cv2.imread(os.path.join(ASSETS_DIR, 'asteroid_purple_v2.png'), 0),
]

# Validasi gambar
if tent_template is None or player_template is None or any(t is None for t in asteroid_templates):
    raise Exception("Satu atau lebih template gambar gagal dimuat.")

# ======== Fungsi Deteksi ========
def match(template, frame, threshold):
    result = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    if max_val >= threshold:
        return max_loc
    return None

def detect_player(frame):
    return match(player_template, frame, PLAYER_THRESHOLD)

def detect_tent(frame):
    return match(tent_template, frame, TENT_THRESHOLD)

def detect_asteroids(frame):
    asteroid_positions = []
    for template in asteroid_templates:
        pos = match(template, frame, ASTEROID_THRESHOLD)
        if pos:
            asteroid_positions.append(pos)
    return asteroid_positions

# ======== Fungsi Kontrol ========
def move_towards(target, current):
    tx, ty = target
    cx, cy = current

    if cx < tx - 10:
        pyautogui.keyDown('d')
        time.sleep(MOVE_DELAY)
        pyautogui.keyUp('d')
    elif cx > tx + 10:
        pyautogui.keyDown('a')
        time.sleep(MOVE_DELAY)
        pyautogui.keyUp('a')

    if cy < ty - 10:
        pyautogui.keyDown('s')
        time.sleep(MOVE_DELAY)
        pyautogui.keyUp('s')
    elif cy > ty + 10:
        pyautogui.keyDown('w')
        time.sleep(MOVE_DELAY)
        pyautogui.keyUp('w')

def shoot():
    pyautogui.press('space')

def is_danger_close(player_pos, asteroid_pos, radius=80):
    px, py = player_pos
    for ax, ay in asteroid_pos:
        if abs(px - ax) < radius and abs(py - ay) < radius:
            return True
    return False

# ======== Main Loop ========
def main_loop():
    print("Bot aktif! Fokus: kejar tenda, hindari asteroid.")
    time.sleep(2)

    while True:
        screenshot = pyautogui.screenshot()
        frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

        player = detect_player(frame)
        tent = detect_tent(frame)
        asteroids = detect_asteroids(frame)

        if player and tent:
            if is_danger_close(player, asteroids):
                # Hindar dulu sebelum ke tenda
                print("⚠️ Asteroid dekat! Hindar...")
                if player[0] < 960:
                    pyautogui.keyDown('a')
                    time.sleep(0.1)
                    pyautogui.keyUp('a')
                else:
                    pyautogui.keyDown('d')
                    time.sleep(0.1)
                    pyautogui.keyUp('d')
            else:
                move_towards(tent, player)

        if player:
            # Jika asteroid sangat dekat, tembak
            for a in asteroids:
                if is_danger_close(player, [a], radius=60):
                    shoot()
                    break

        time.sleep(0.03)

if __name__ == "__main__":
    main_loop()
