from ursina import *
import cv2
from hand_detection import HandDetector
from game_controls import move_entity_with_hand, apply_gesture_action

# Setup aplikasi
app = Ursina()
detector = HandDetector()
cap = cv2.VideoCapture(0)

# Asset jalan 3D
roads = [
    Entity(model='source/g.glb', scale=(1, 1, 1), position=(0, -2, 10), rotation=(0, 180, 0), color=color.white),
    Entity(model='source/g.glb', scale=(1, 1, 1), position=(0, -2, 20), rotation=(0, 180, 0), color=color.white)
]

# Player
player = Entity(
    model='cube',
    scale=1,
    position=(0, -1.5, 10),
    color=color.azure
)

# Emoji player (akan diganti berdasarkan target gesture)
emoji_display = Entity(
    parent=player,
    model='quad',
    texture='thumb.png',
    scale=(0.5, 0.5),
    position=(0, 1, 0)
)

# Daftar urutan gesture
gesture_sequence = ["peace", "thumbs_up", "stop", "fist", "one_finger_up"]
gesture_textures = {
    "peace": 'two.png',
    "thumbs_up": 'thumb.png',
    "stop": 'stop.png',
    "fist": 'fist.png',
    "one_finger_up": 'one.png'
}
gesture_index = 0
road_speed = 0.3

def update():
    global gesture_index
    ret, frame = cap.read()
    if not ret:
        return

    gesture, hand_pos = detector.get_hand_data(frame)

    if gesture:
        apply_gesture_action(player, gesture)
        if gesture == gesture_sequence[gesture_index]:
            gesture_index += 1
            if gesture_index >= len(gesture_sequence):
                gesture_index = 0  # Game selesai / restart
            else:
                emoji_display.texture = gesture_textures[gesture_sequence[gesture_index]]
        else:
            gesture_index = 0
            emoji_display.texture = gesture_textures[gesture_sequence[0]]

    # Gerakkan jalan
    for road in roads:
        road.z -= road_speed
        if road.z < -10:
            road.z = 20
    
    player.z = roads[0].z
    player.x = 0
    player.y = -1.5


    # Tampilkan frame webcam
    cv2.imshow("Webcam Feed", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        application.quit()

def input(key):
    if key == 'escape':
        cap.release()
        cv2.destroyAllWindows()
        application.quit()

app.run()
