# main.py
from ursina import *
import cv2
import random
import threading
from hand_detection import HandDetector

app = Ursina()

# Kamera sedikit miring dan di kanan jalan
camera.rotation_x = 5
camera.rotation_y = -20
camera.position = (4, 3, -12)

# Hand detector dan webcam
detector = HandDetector()
cap = cv2.VideoCapture(0)

# Set resolusi lebih rendah untuk mengurangi lag
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

gesture_result = None
gesture_frame = None

# Thread loop untuk webcam
def webcam_loop():
    global gesture_result, gesture_frame
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        gesture, _, annotated = detector.get_hand_data(frame)
        gesture_result = gesture
        gesture_frame = annotated

# Mulai thread webcam
threading.Thread(target=webcam_loop, daemon=True).start()

# Gesture dan tekstur emoji
gesture_textures = {
    "peace": 'assets/two.png',
    "thumbs_up": 'assets/thumb.png',
    "stop": 'assets/stop.png',
    "fist": 'assets/fist.png',
    "one_finger_up": 'assets/one.png'
}

gesture_sequence = list(gesture_textures.keys())
colors = [color.green, color.blue, color.yellow, color.orange, color.pink]

# Jalan
roads = [
    Entity(model='source/g.glb', scale=(1,0.1,50), position=(0,-2,10), color=color.gray),
    Entity(model='source/g.glb', scale=(1,0.1,50), position=(0,-2,60), color=color.gray)
]

# Player
player = Entity(
    model='sphere',
    scale=2,
    position=(0,0,0),
    collider='box'
)

# Musuh
enemies = []
musuh_posisi = [
    (0, 0, 100),
    (0, 0, 200),
    (0, 0, 300),
    (0, 0, 400),
    (0, 0, 500)
]
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

# UI
instruction_text = Text(
    text="Tiru gesture musuh!",
    parent=camera.ui,
    position=(0,0.45),
    origin=(0,0),
    scale=1.5,
    color=color.white
)

win_text = Text(
    text="",
    parent=camera.ui,
    position=(0,0),
    scale=3,
    color=color.green,
    enabled=False
)

current_enemy_index = 0
player_speed = 0.01
world_speed = 0.2
win = False

def apply_gesture_effect(entity, gesture):
    if gesture == "thumbs_up":
        entity.y += 0.2
        entity.color = color.green
    elif gesture == "peace":
        entity.color = random.choice(colors)
        entity.rotation_y += 15
    elif gesture == "fist":
        entity.scale = (1.2, 1.2, 1.2)
        entity.color = color.red
    elif gesture == "one_finger_up":
        entity.rotation_x += 15
        entity.color = color.blue
    elif gesture == "stop":
        entity.scale = (0.8, 0.8, 0.8)
        entity.color = color.yellow

def update():
    global current_enemy_index, win

    # Jalan bergerak
    for road in roads:
        road.z -= world_speed
        if road.z < -30:
            road.z += 100

    # Musuh bergerak
    for enemy in enemies:
        enemy.z -= world_speed

    # Player tetap bergerak sedikit
    player.z += player_speed

    # Deteksi gesture saat mendekati musuh
    if current_enemy_index < len(enemies):
        current_enemy = enemies[current_enemy_index]
        if abs(player.z - current_enemy.z) < 1:
            if gesture_result == current_enemy.name:
                apply_gesture_effect(player, gesture_result)
                current_enemy.enabled = False
                current_enemy_index += 1
            else:
                instruction_text.text = f"Tunjukkan: {current_enemy.name}"

            # Tampilkan frame gesture (opsional)
            if gesture_frame is not None:
                cv2.imshow("Hand", gesture_frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    cap.release()
                    cv2.destroyAllWindows()
                    application.quit()
    else:
        if not win:
            win = True
            win_text.text = "BERHASIL!"
            win_text.enabled = True

def input(key):
    if key == 'escape':
        cap.release()
        cv2.destroyAllWindows()
        application.quit()

app.run()
