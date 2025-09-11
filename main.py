import cv2
from utils import LivenessDetector, mark_attendance

KNOWN_USER = "User"  # Replace with actual face recognition logic later

def run_attendance_system():
    cam = cv2.VideoCapture(0)
    detector = LivenessDetector()

    print("[INFO] Starting attendance system. Press 'q' to quit.")

    while True:
        ret, frame = cam.read()
        if not ret:
            break

        blink_detected = detector.detect_blink(frame)

        if blink_detected:
            cv2.putText(frame, "LIVE PERSON ✅", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
            mark_attendance(KNOWN_USER)
        else:
            cv2.putText(frame, "POSSIBLE SPOOF ⚠", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

        cv2.imshow("Face Attendance with Liveness", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    run_attendance_system()
