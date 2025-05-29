from ursina import *

def move_entity_with_hand(entity, hand_position, screen_size):
    """
    Gerakkan entitas berdasarkan posisi tangan.
    """
    if hand_position:
        x_ratio = hand_position[0] / screen_size[0]
        y_ratio = hand_position[1] / screen_size[1]
        entity.x = (x_ratio - 0.5) * 8
        entity.y = (0.5 - y_ratio) * 6

def apply_gesture_action(entity, gesture):
    """
    Tindakan game berdasarkan gesture.
    """
    if gesture == "thumbs_up":
        entity.y += 0.1  # Lompat
    elif gesture == "peace":
        entity.color = color.green  # Perbaikan di sini (tanpa tanda kurung)
    elif gesture == "fist":
        entity.color = color.pink  # Perbaikan di sini
    elif gesture == "open_palm":
        entity.scale = (1, 1, 1)  # Reset skala
    elif gesture == "one_finger_up":
        entity.rotation_y += 5
    elif gesture == "point":
        entity.scale_x = 1.5