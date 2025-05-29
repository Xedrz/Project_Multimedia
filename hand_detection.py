import cv2
import mediapipe as mp

class HandDetector:
    def __init__(self, max_hands=1, detection_confidence=0.7, tracking_confidence=0.6):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=max_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )

    def get_hand_data(self, frame):
        """
        Mengembalikan gesture tangan (str) dan posisi tangan (tuple x,y).
        """
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)

        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]
            h, w, _ = frame.shape
            landmarks = hand.landmark

            def finger_open(tip_id, pip_id):
                return landmarks[tip_id].y < landmarks[pip_id].y

            fingers = {
                'thumb': landmarks[4].x > landmarks[3].x,
                'index': finger_open(8, 6),
                'middle': finger_open(12, 10),
                'ring': finger_open(16, 14),
                'pinky': finger_open(20, 18),
            }

            gesture = None
            if all(fingers.values()):
                gesture = "stop"
            elif fingers['thumb'] and not any(fingers[f] for f in ['index', 'middle', 'ring', 'pinky']):
                gesture = "thumbs_up"
            elif fingers['index'] and fingers['middle'] and not any(fingers[f] for f in ['ring', 'pinky', 'thumb']):
                gesture = "peace"
            elif not any(fingers.values()):
                gesture = "fist"
            elif fingers['index'] and not any(fingers[f] for f in ['middle', 'ring', 'pinky', 'thumb']):
                gesture = "one_finger_up"

            center = (int(landmarks[9].x * w), int(landmarks[9].y * h))
            return gesture, center

        return None, None

    def release(self):
        self.hands.close()
