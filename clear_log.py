# clear_log.py
import os

ATTENDANCE_FILE = 'attendance.csv'

def clear_log():
    if os.path.exists(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, 'w') as f:
            f.write("Name,Time\n")
        print("attendance.csv has been cleared.")
    else:
        print(f"{ATTENDANCE_FILE} does not exist.")

if __name__ == "__main__":
    clear_log()
