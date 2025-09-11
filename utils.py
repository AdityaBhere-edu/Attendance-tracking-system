import cv2
import mediapipe as mp
from datetime import datetime
import pandas as pd

class LivenessDetector:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)

    def detect_blink(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.mp_face_mesh.process(rgb_frame)
        if not result.multi_face_landmarks:
            return False

        for face_landmarks in result.multi_face_landmarks:
            LEFT_EYE = [33, 160, 158, 133, 153, 144]
            RIGHT_EYE = [362, 385, 387, 263, 373, 380]

            def eye_aspect_ratio(eye_points):
                vertical_1 = abs(eye_points[1].y - eye_points[5].y)
                vertical_2 = abs(eye_points[2].y - eye_points[4].y)
                horizontal = abs(eye_points[0].x - eye_points[3].x)
                return (vertical_1 + vertical_2) / (2.0 * horizontal)

            def extract_points(indices):
                return [face_landmarks.landmark[i] for i in indices]

            left_ratio = eye_aspect_ratio(extract_points(LEFT_EYE))
            right_ratio = eye_aspect_ratio(extract_points(RIGHT_EYE))
            avg_ratio = (left_ratio + right_ratio) / 2.0

            return avg_ratio < 0.21  # Blink threshold

def mark_attendance(name, filename='attendance.csv'):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    df = pd.read_csv(filename)
    df.loc[len(df)] = [name, now]
    df.to_csv(filename, index=False)
    print(f"[INFO] Attendance marked for {name} at {now}")
