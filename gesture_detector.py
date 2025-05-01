"""
Modul untuk mendeteksi gesture tangan menggunakan MediaPipe.
"""

import mediapipe as mp

class GestureDetector:
    """
    Kelas untuk mendeteksi gesture tangan dan mencocokkannya dengan emoji rintangan.
    """

    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=False, max_num_hands=1)
        self.landmarks = []

    def detect(self, frame):
        """
        Mendeteksi tangan dari frame webcam.
        Args:
            frame (np.array): Gambar frame dari webcam.
        Returns:
            list: Landmark tangan jika terdeteksi, kosong jika tidak.
        """
        results = self.hands.process(frame)
        if results.multi_hand_landmarks:
            return results.multi_hand_landmarks[0].landmark
        return []

    def match_gesture(self, landmarks, emoji):
        """
        Mencocokkan gesture dengan emoji rintangan.
        Args:
            landmarks (list): Landmark dari tangan pengguna.
            emoji (str): Emoji rintangan.
        Returns:
            bool: True jika cocok, False jika tidak.
        """
        if not landmarks:
            return False

        if emoji == "✋":  # Semua jari terbuka
            return all(landmarks[i].y < landmarks[i - 2].y for i in [8, 12, 16, 20])
        elif emoji == "☝️":  # Hanya telunjuk
            return (landmarks[8].y < landmarks[6].y and
                    all(landmarks[i].y > landmarks[i - 2].y for i in [12, 16, 20]))
        elif emoji == "✌️":  # Dua jari (peace)
            return (landmarks[8].y < landmarks[6].y and
                    landmarks[12].y < landmarks[10].y and
                    all(landmarks[i].y > landmarks[i - 2].y for i in [16, 20]))
        return False
