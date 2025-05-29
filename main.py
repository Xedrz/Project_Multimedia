from ursina import *
import cv2
import time
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

# Timer cube yang mendekati layar
timer_cube = Entity(
    model='cube',
    scale=0.5,
    position=(0, 0, 20),
    color=color.red
)

# Emoji target display
target_display = Entity(
    parent=camera.ui,
    model='quad',
    texture='thumb.png',
    scale=(0.15, 0.15),
    position=(0, 0.4, 0)
)

# Text display
instruction_text = Text(
    text="Follow the gesture!",
    parent=camera.ui,
    position=(0, 0.3, 0),
    scale=1.5,
    color=color.white
)

win_text = Text(
    text="",
    parent=camera.ui,
    position=(0, 0, 0),
    scale=3,
    color=color.green,
    enabled=False
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

# Game variables
gesture_index = 0
road_speed = 0.3
game_completed = False
win_animation_time = 0
last_gesture_time = 0
timer_speed = 0.1
timer_active = True
timer_reset_z = 20
timer_warning_z = 5

def reset_timer():
    global timer_speed, timer_active
    timer_cube.z = timer_reset_z
    timer_speed = 0.1 + (gesture_index * 0.05)  # Makin sulit makin cepat
    timer_active = True

def update():
    global gesture_index, game_completed, win_animation_time, last_gesture_time, timer_speed, timer_active
    
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame from camera")
        return

    try:
        # Tracking tangan
        gesture, hand_pos = detector.get_hand_data(frame)
        
        # Gambar landmark tangan di frame
        if hand_pos:
            cv2.circle(frame, hand_pos, 10, (0, 255, 0), -1)
            move_entity_with_hand(player, hand_pos, (frame.shape[1], frame.shape[0]))

        if not game_completed:
            # Update timer cube
            if timer_active:
                timer_cube.z -= timer_speed * time.dt * 60
                
                # Cek jika timer cube sudah mencapai layar (z <= 0)
                if timer_cube.z <= 0:
                    # Reset ke step 1 jika gagal
                    gesture_index = 0
                    target_display.texture = gesture_textures[gesture_sequence[0]]
                    instruction_text.text = f"Too slow! Back to Gesture 1/{len(gesture_sequence)}"
                    reset_timer()
                
                # Ubah warna jadi kuning saat mendekati deadline
                if timer_cube.z < timer_warning_z:
                    timer_cube.color = color.yellow
                else:
                    timer_cube.color = color.red

            if gesture:
                current_time = time.time()
                
                # Cooldown untuk menghindari deteksi berulang terlalu cepat
                if current_time - last_gesture_time > 0.5:
                    if gesture == gesture_sequence[gesture_index]:
                        # Berhasil melakukan gesture yang benar
                        gesture_index += 1
                        last_gesture_time = current_time
                        
                        if gesture_index >= len(gesture_sequence):
                            # Game selesai
                            game_completed = True
                            win_text.text = "WIN!!!"
                            win_text.enabled = True
                            target_display.enabled = False
                            instruction_text.enabled = False
                            timer_cube.enabled = False
                        else:
                            # Lanjut ke gesture berikutnya
                            target_display.texture = gesture_textures[gesture_sequence[gesture_index]]
                            instruction_text.text = f"Gesture {gesture_index+1}/{len(gesture_sequence)}"
                            reset_timer()
                    else:
                        # Gesture salah
                        instruction_text.text = f"Wrong gesture! Try again: {gesture_sequence[gesture_index]}"
        else:
            # Animasi WIN berputar
            win_animation_time += time.dt
            win_text.rotation_z = sin(win_animation_time * 2) * 10
            win_text.scale = 3 + sin(win_animation_time * 3) * 0.5

        # Gerakkan jalan
        for road in roads:
            road.z -= road_speed
            if road.z < -10:
                road.z = 20
        
        player.z = roads[0].z
        player.y = -1.5

        # Tampilkan frame webcam dengan tracking
        cv2.imshow("Hand Tracking", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            application.quit()

    except Exception as e:
        print(f"Error in update loop: {e}")

def input(key):
    if key == 'escape' or key == 'q':
        cap.release()
        cv2.destroyAllWindows()
        application.quit()

# Inisialisasi game
reset_timer()
target_display.texture = gesture_textures[gesture_sequence[0]]
instruction_text.text = f"Gesture 1/{len(gesture_sequence)}"

app.run()