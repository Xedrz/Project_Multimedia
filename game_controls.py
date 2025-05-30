# game_controls.py
from ursina import color
import random

colors = [color.green, color.blue, color.yellow, color.orange, color.pink]
"""
Modul ini menangani efek atau aksi yang terjadi ketika gesture tertentu terdeteksi.
"""

def apply_gesture_effect(entity, gesture):
    """
    Menerapkan efek gesture ke entitas (misalnya player) berdasarkan jenis gesture.

    Args:
        entity (Entity): Objek dalam game (biasanya player).
        gesture (str): Nama gesture yang terdeteksi, seperti 'peace', 'stop', dll.
    """
    if gesture == "one_finger_up":
        entity.y += 0.2
        entity.color = color.green
    elif gesture == "peace":
        entity.color = random.choice(colors)
        entity.rotation_y += 15
    elif gesture == "stop":
        entity.scale = (1.2, 1.2, 1.2)
        entity.color = color.red
    elif gesture == "fist":
        entity.scale = (2.5, 2.5, 2.5)
        entity.color = color.azure
    elif gesture == "thumbs_up":
        entity.rotation_x += 25
        entity.color = color.lime
