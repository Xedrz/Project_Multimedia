import cv2
import mediapipe as mp
import numpy as np
from collections import Counter

class HandDetector:
    def __init__(self, max_hands=1, detection_confidence=0.8, tracking_confidence=0.8):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=max_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.gesture_buffer = []
        self.buffer_size = 5

    def get_hand_data(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)
        
        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]
            h, w, _ = frame.shape
            landmarks = hand.landmark
            
            # Gambar landmark untuk visualisasi
            annotated_image = frame.copy()
            self.mp_drawing.draw_landmarks(
                annotated_image, hand, self.mp_hands.HAND_CONNECTIONS)
            
            # Fungsi untuk mengecek apakah jari terentang
            def is_finger_extended(tip, pip, dip=None, mcp=None):
                if dip is None:  # Untuk ibu jari
                    return tip.x < pip.x if tip.x < mcp.x else tip.x > pip.x
                else:
                    return tip.y < pip.y and pip.y < dip.y

            # Ambil landmark penting
            thumb_tip = landmarks[4]
            thumb_pip = landmarks[3]
            thumb_mcp = landmarks[2]
            
            index_tip = landmarks[8]
            index_pip = landmarks[6]
            index_dip = landmarks[5]
            
            middle_tip = landmarks[12]
            middle_pip = landmarks[10]
            middle_dip = landmarks[9]
            
            ring_tip = landmarks[16]
            ring_pip = landmarks[14]
            ring_dip = landmarks[13]
            
            pinky_tip = landmarks[20]
            pinky_pip = landmarks[18]
            pinky_dip = landmarks[17]
            
            # Cek jari yang terentang
            thumb_ext = is_finger_extended(thumb_tip, thumb_pip, mcp=thumb_mcp)
            index_ext = is_finger_extended(index_tip, index_pip, index_dip)
            middle_ext = is_finger_extended(middle_tip, middle_pip, middle_dip)
            ring_ext = is_finger_extended(ring_tip, ring_pip, ring_dip)
            pinky_ext = is_finger_extended(pinky_tip, pinky_pip, pinky_dip)
            
            gesture = None
            
            # Fist (semua jari menekuk)
            if not any([thumb_ext, index_ext, middle_ext, ring_ext, pinky_ext]):
                gesture = "fist"
                
            # Peace (telunjuk dan tengah terentang)
            elif index_ext and middle_ext and not any([thumb_ext, ring_ext, pinky_ext]):
                gesture = "peace"
                
            # Thumbs up (hanya ibu jari terentang)
            elif thumb_ext and not any([index_ext, middle_ext, ring_ext, pinky_ext]):
                gesture = "thumbs_up"
                
            # Stop (semua jari terentang)
            elif all([thumb_ext, index_ext, middle_ext, ring_ext, pinky_ext]):
                gesture = "stop"
                
            # One finger (hanya telunjuk terentang)
            elif index_ext and not any([thumb_ext, middle_ext, ring_ext, pinky_ext]):
                gesture = "one_finger_up"
            
            # Gunakan buffer untuk menghindari deteksi palsu
            if gesture is not None:
                self.gesture_buffer.append(gesture)
                if len(self.gesture_buffer) > self.buffer_size:
                    self.gesture_buffer.pop(0)
                
                # Ambil gesture yang paling konsisten
                if len(self.gesture_buffer) >= self.buffer_size//2:
                    gesture_counts = Counter(self.gesture_buffer)
                    most_common = gesture_counts.most_common(1)[0]
                    gesture = most_common[0]
            
            center = (int(landmarks[9].x * w), int(landmarks[9].y * h))
            return gesture, center, annotated_image

        return None, None, frame

    def release(self):
        self.hands.close()