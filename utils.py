import os
import cv2
import time
import numpy as np
from config import HIGHSCORE_FILE, CAMERA_INDEX

import mediapipe as mp
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

def calibrate_distance():
    cap = cv2.VideoCapture(CAMERA_INDEX)
    distances = []

    print("Calibration started: Show palm to camera for 10 seconds...")

    start = time.time()
    while time.time() - start < 10:
        ret, frame = cap.read()
        if not ret:
            continue
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                h, w, c = frame.shape
                wrist = hand_landmarks.landmark[0]
                middle_tip = hand_landmarks.landmark[12]
                x1, y1 = int(wrist.x * w), int(wrist.y * h)
                x2, y2 = int(middle_tip.x * w), int(middle_tip.y * h)
                pixel_distance = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
                distances.append(pixel_distance)

                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                cv2.circle(frame, (x2, y2), 10, (255, 0, 0), cv2.FILLED)
                cv2.putText(frame, f"Calibrating: {int(pixel_distance)} px", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0),2)

        cv2.imshow("Calibration", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    return np.mean(distances) if distances else 150

def load_highscore():
    if os.path.exists(HIGHSCORE_FILE):
        with open(HIGHSCORE_FILE, 'r') as f:
            return int(f.read())
    return 0

def save_highscore(score):
    with open(HIGHSCORE_FILE, 'w') as f:
        f.write(str(score))
