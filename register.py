import cv2
import os

def register_face(name, save_dir='registered_faces'):
    os.makedirs(save_dir, exist_ok=True)
    cam = cv2.VideoCapture(0)
    count = 0
    print("[INFO] Capturing images. Press 'q' to stop.")
    while True:
        ret, frame = cam.read()
        if not ret:
            break
        cv2.imshow("Register Face", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if count % 10 == 0:
            filepath = os.path.join(save_dir, f"{name}_{count}.jpg")
            cv2.imwrite(filepath, frame)
            print(f"[INFO] Saved {filepath}")
        count += 1
    cam.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    user_name = input("Enter name to register: ")
    register_face(user_name)



