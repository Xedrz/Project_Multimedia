from ursina import *
import random

def apply_gesture_action(entity, gesture):
    """
    Tindakan game berdasarkan gesture.
    """
    colors = [color.green, color.blue, color.yellow, color.orange, color.pink]
    
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