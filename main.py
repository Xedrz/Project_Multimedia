from ursina import *
import cv2
import threading
from hand_detection import HandDetector
from game_controls import apply_gesture_effect
import numpy as np
from PIL import Image
import time
import random

app = Ursina()

# Setup window game
window.title = 'Gesture Game'
window.borderless = False
window.fullscreen = False
window.exit_button.visible = False
window.fps_counter.enabled = True

# Setup posisi dan sudut kamera 3D
camera.rotation_x = 5
camera.rotation_y = -20
camera.position = (4, 3, -12)

# Inisialisasi webcam dan hand detector
detector = HandDetector()
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Tidak dapat membuka webcam")
    application.quit()

# Set resolusi webcam kecil agar lebih cepat prosesnya
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

gesture_result = None
gesture_frame = None

# Panel untuk menampilkan webcam di UI game
empty_frame = np.zeros((240, 320, 3), dtype=np.uint8)
empty_img = Image.fromarray(empty_frame)
webcam_texture = Texture(empty_img)

webcam_panel = Entity(
    parent=camera.ui,
    model='quad',
    texture=webcam_texture,
    scale=(0.4, 0.3),
    position=(-0.7, -0.4)
)

def webcam_loop():
    """
    Thread yang terus-menerus mengambil frame dari webcam,
    mendeteksi gesture, dan memperbarui texture untuk UI game.
    """
    global gesture_result, gesture_frame, webcam_texture, webcam_panel
    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        gesture, _, annotated = detector.get_hand_data(frame)
        gesture_result = gesture
        gesture_frame = annotated

        # Konversi ke RGB dan flip horizontal agar mirip cermin
        rgb_frame = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
        rgb_frame = cv2.flip(rgb_frame, 1)

        # Update texture pada panel UI
        img = Image.fromarray(rgb_frame)
        webcam_panel.texture = Texture(img)

        time.sleep(1/20)  # Batasi frame rate ~20 fps

# Jalankan thread webcam di background
threading.Thread(target=webcam_loop, daemon=True).start()

# Setup data gesture dan musuh
gesture_textures = {
    "peace": 'assets/two.png',
    "stop": 'assets/stop.png',
    "one_finger_up": 'assets/one.png',
    "fist": 'assets/fist.png',
    "thumbs_up": 'assets/thumb.png'
}

gesture_sequence = ["peace", "stop", "one_finger_up", "fist", "thumbs_up"]
colors = [color.green, color.blue, color.yellow, color.orange, color.pink]
musuh_posisi = [(0, 0, 100), (0, 0, 200), (0, 0, 300), (0, 0, 400), (0, 0, 500)]

# Buat jalan/jalanan sebagai background
roads = [
    Entity(model='source/g.glb', scale=(5, 0.1, 50), position=(0, -2, 10), color=color.gray),
    Entity(model='source/g.glb', scale=(5, 0.1, 50), position=(0, -2, 60), color=color.gray)
]

# Buat objek pemain
player = Entity(
    model='sphere',
    scale=2,
    position=(0, 0, 0),
    collider='box',
    color=color.white
)

# Buat musuh berupa objek dengan gambar gesture masing-masing
enemies = []
for i, gesture in enumerate(gesture_sequence):
    enemy = Entity(
        model='quad',
        texture=gesture_textures[gesture],
        scale=4,
        position=musuh_posisi[i],
        collider='box',
        name=gesture
    )
    enemies.append(enemy)

# UI teks instruksi dan informasi
instruction_text = Text(
    text="Tiru gesture musuh!",
    parent=camera.ui,
    position=(0, 0.4),
    origin=(0, 0),
    scale=1.5,
    color=color.white
)

info_text = Text(
    text="Tekan Q untuk Quit | R untuk Replay",
    parent=camera.ui,
    position=(0, 0.33),  
    origin=(0, 0),
    scale=1,
    color=color.light_gray
)

win_text = Text(
    text="",
    parent=camera.ui,
    position=(0, 0),
    scale=3,
    color=color.green,
    enabled=False
)

# Variabel kontrol game
current_enemy_index = 0
player_speed = 0.01
world_speed = 0.2
win = False
check_gesture = False
gesture_cooldown = 0

wrong_gesture = False
wrong_gesture_timer = 0

gesture_detection_timer = 0
gesture_detection_limit = 30  # batas waktu (frame) deteksi gesture

def reset_game():
    """
    Mengatur ulang posisi pemain, musuh, dan variabel game untuk memulai ulang permainan.
    """
    global current_enemy_index, win, check_gesture, gesture_cooldown
    global wrong_gesture, wrong_gesture_timer, gesture_detection_timer

    player.position = (0, 0, 0)
    player.color = color.white
    player.scale = (2, 2, 2)
    player.rotation_y = 0

    for i, enemy in enumerate(enemies):
        enemy.enabled = True
        enemy.position = musuh_posisi[i]

    current_enemy_index = 0
    win = False
    check_gesture = False
    gesture_cooldown = 0
    wrong_gesture = False
    wrong_gesture_timer = 0
    gesture_detection_timer = 0
    instruction_text.text = "Tiru gesture untuk melewati tantangan!"
    win_text.enabled = False

def update():
    """
    Fungsi update dipanggil setiap frame oleh Ursina.
    Mengatur pergerakan pemain, musuh, cek gesture, dan logika kemenangan/kesalahan.
    """
    global current_enemy_index, win, check_gesture, gesture_cooldown
    global wrong_gesture, wrong_gesture_timer, gesture_detection_timer

    # Pergerakan jalan agar terlihat berjalan
    for road in roads:
        road.z -= world_speed
        if road.z < -30:
            road.z += 100

    # Pergerakan musuh ke arah pemain
    for enemy in enemies:
        enemy.z -= world_speed

    # Jika game sudah selesai atau terjadi gesture salah, jalankan timer untuk reset
    if win or wrong_gesture:
        if wrong_gesture:
            wrong_gesture_timer -= 1
            if wrong_gesture_timer <= 0:
                reset_game()
        return

    # Logika deteksi gesture jika masih ada musuh yang harus ditiru
    if current_enemy_index < len(enemies):
        current_enemy = enemies[current_enemy_index]
        distance = current_enemy.z - player.z

        if 0 < distance < 10:
            # Saat musuh mendekat, mulai cek gesture pemain
            check_gesture = True
            instruction_text.text = f"Tiru: {current_enemy.name}!"
            gesture_detection_timer += 1

            if gesture_result == current_enemy.name:
                # Gesture cocok dengan musuh
                print("Final detected gesture:", gesture_result)
                apply_gesture_effect(player, gesture_result)
                current_enemy.enabled = False
                current_enemy_index += 1
                gesture_cooldown = 30
                check_gesture = False
                gesture_detection_timer = 0

            elif gesture_detection_timer >= gesture_detection_limit:
                # Gesture tidak sesuai/deteksi timeout -> reset game
                instruction_text.text = "Gesture salah / tidak terdeteksi! Reset..."
                wrong_gesture = True
                wrong_gesture_timer = 30
                return
        else:
            # Jika belum dekat musuh, lanjutkan berjalan maju
            instruction_text.text = "Tiru Gerakan!"
            player.z += player_speed
    else:
        # Semua musuh sudah ditiru dengan benar, player menang
        win = True
        win_text.text = "You win!"
        win_text.enabled = True

def input(key):
    """
    Fungsi untuk menangani input keyboard.

    Parameter:
    key (str): Tombol keyboard yang ditekan.
    """
    global win
    if key == 'q':
        application.quit()
    if key == 'r':
        reset_game()

# Mulai game
reset_game()
app.run()
cap.release()
detector.release()
