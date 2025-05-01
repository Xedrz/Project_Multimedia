"""
Program utama untuk menjalankan game gesture tangan.
"""

import cv2
import time
import numpy as np
from gesture_detector import GestureDetector
from challenge_manager import ChallengeManager

def draw_text(frame, text, position, color=(255, 255, 255), size=1.2, thickness=2):
    """
    Menampilkan teks pada frame.
    Args:
        frame (np.array): Frame dari webcam.
        text (str): Teks yang akan ditampilkan.
        position (tuple): Posisi (x, y) teks.
        color (tuple): Warna teks.
        size (float): Ukuran font.
        thickness (int): Ketebalan font.
    """
    cv2.putText(frame, text, position, cv2.FONT_HERSHEY_SIMPLEX, size, color, thickness)

def main():
    """
    Fungsi utama untuk menjalankan filter game gesture tangan.
    """
    cap = cv2.VideoCapture(0)
    gesture = GestureDetector()
    challenge = ChallengeManager()

    last_pass = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        landmarks = gesture.detect(rgb)

        current_challenge = challenge.get_current_challenge()
        matched = gesture.match_gesture(landmarks, current_challenge)

        draw_text(frame, f"Rintangan: {current_challenge}", (50, 50), (0, 255, 255), 1.5)

        if matched:
            draw_text(frame, "✅ Lolos!", (50, 100), (0, 255, 0), 1.2)
            if time.time() - last_pass > 2:
                challenge.new_challenge()
                last_pass = time.time()
        else:
            draw_text(frame, "❌ Coba lagi", (50, 100), (0, 0, 255), 1.2)

        cv2.imshow("Gesture Challenge Game", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
