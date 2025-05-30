import cv2
import mediapipe as mp
import numpy as np
from collections import Counter

class HandDetector:
    """
    Kelas untuk mendeteksi gesture tangan menggunakan MediaPipe Hands.

    Parameter:
    max_hands (int): Maksimum jumlah tangan yang dideteksi.
    detection_confidence (float): Ambang kepercayaan untuk deteksi tangan.
    tracking_confidence (float): Ambang kepercayaan untuk pelacakan tangan.

    Atribut:
    gesture_buffer (list): Buffer untuk menyimpan gesture terakhir guna stabilisasi.
    buffer_size (int): Ukuran buffer gesture.
    prev_gesture (str): Gesture yang terakhir stabil terdeteksi.
    """

    def __init__(self, max_hands=1, detection_confidence=0.7, tracking_confidence=0.7):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=max_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.gesture_buffer = []
        self.buffer_size = 5
        self.prev_gesture = None

        # Variabel untuk stabilisasi gesture (harus stabil beberapa frame berturut-turut)
        self.last_valid_gesture = None
        self.stable_counter = 0
        self.required_stability = 2

    def get_finger_state(self, landmarks, finger_tips, finger_pips, finger_dips=None, finger_mcps=None):
        """
        Menentukan apakah jari-jari tangan dalam keadaan terentang atau tidak.

        Parameter:
        landmarks (list): Daftar landmark tangan dari MediaPipe.
        finger_tips (list): Landmark ujung jari.
        finger_pips (list): Landmark sendi tengah jari.
        finger_dips (list): Landmark sendi paling dekat ujung jari (opsional, kecuali untuk ibu jari).
        finger_mcps (list): Landmark sendi pangkal jari (opsional, untuk ibu jari).

        Return:
        list: Daftar boolean, True jika jari terentang, False jika tidak.
        """
        extended = []
        for i, (tip, pip) in enumerate(zip(finger_tips, finger_pips)):
            if finger_dips is None:  # Deteksi ibu jari
                mcp = finger_mcps[i]
                # Logika sederhana cek ibu jari terentang (posisi x landmark)
                if tip.x < pip.x < mcp.x or tip.x > pip.x > mcp.x:
                    extended.append(True)
                else:
                    extended.append(False)
            else:
                dip = finger_dips[i]
                # Deteksi jari lain: apakah ujung jari lebih tinggi (y lebih kecil) dari sendi pip dan dip
                if tip.y < pip.y < dip.y:
                    extended.append(True)
                else:
                    extended.append(False)
        return extended

    def get_hand_data(self, frame):
        """
        Mengambil data tangan dan mendeteksi gesture dari frame video.

        Parameter:
        frame (numpy.ndarray): Frame video BGR dari webcam.

        Return:
        tuple: (gesture (str atau None), posisi pusat tangan (tuple) atau None, frame dengan anotasi (numpy.ndarray))
        """
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)

        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]
            h, w, _ = frame.shape

            # Salin frame untuk anotasi
            annotated_image = frame.copy()
            self.mp_drawing.draw_landmarks(
                annotated_image, hand, self.mp_hands.HAND_CONNECTIONS)

            landmarks = hand.landmark

            # Landmark penting tiap jari
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

            # Cek status jari (terentang atau tidak)
            thumb_ext = self.get_finger_state(
                landmarks, [thumb_tip], [thumb_pip], finger_mcps=[thumb_mcp])[0]
            index_ext = self.get_finger_state(
                landmarks, [index_tip], [index_pip], finger_dips=[index_dip])[0]
            middle_ext = self.get_finger_state(
                landmarks, [middle_tip], [middle_pip], finger_dips=[middle_dip])[0]
            ring_ext = self.get_finger_state(
                landmarks, [ring_tip], [ring_pip], finger_dips=[ring_dip])[0]
            pinky_ext = self.get_finger_state(
                landmarks, [pinky_tip], [pinky_pip], finger_dips=[pinky_dip])[0]

            # Tentukan gesture berdasarkan status jari
            gesture = None
            if index_ext and middle_ext and not ring_ext and not pinky_ext:
                gesture = "peace"
            elif all([thumb_ext, index_ext, middle_ext, ring_ext, pinky_ext]):
                gesture = "stop"
            elif index_ext and not any([thumb_ext, middle_ext, ring_ext, pinky_ext]):
                gesture = "one_finger_up"
            elif not any([thumb_ext, index_ext, middle_ext, ring_ext, pinky_ext]):
                gesture = "fist"
            elif thumb_ext and not any([index_ext, middle_ext, ring_ext, pinky_ext]):
                gesture = "thumbs_up"

            # Stabilkan gesture supaya tidak berubah-ubah terlalu cepat
            if gesture is not None:
                print("Detected gesture (raw):", gesture)
                if gesture == self.last_valid_gesture:
                    self.stable_counter += 1
                else:
                    self.last_valid_gesture = gesture
                    self.stable_counter = 1

                if self.stable_counter >= self.required_stability:
                    self.gesture_buffer.append(gesture)
                    if len(self.gesture_buffer) > self.buffer_size:
                        self.gesture_buffer.pop(0)

                    # Ambil gesture yang paling sering muncul dalam buffer sebagai gesture akhir
                    if len(self.gesture_buffer) == self.buffer_size:
                        gesture_counts = Counter(self.gesture_buffer)
                        gesture = gesture_counts.most_common(1)[0][0]
                        self.prev_gesture = gesture

            # Posisi pusat tangan untuk referensi UI/game
            center = (int(landmarks[9].x * w), int(landmarks[9].y * h))
            return self.prev_gesture, center, annotated_image

        # Jika tidak ada tangan terdeteksi
        self.prev_gesture = None
        return None, None, frame

    def release(self):
        """Menutup instance MediaPipe Hands untuk membebaskan resource."""
        self.hands.close()
