***

# Smart Attendance Backup

A desktop facial-recognition attendance system built with DeepFace, OpenCV, Tkinter, and MediaPipe. Supports anti-spoofing via blink detection, GUI admin features, and local student registration. Designed for Windows laptops/desktops.

***

## Features

- **Face Recognition Attendance:** Uses a webcam to recognize registered faces and logs attendance with date and time.
- **Blink Anti-Spoofing:** Prevents photo/video attacks with live blink detection using MediaPipe.
- **Easy Registration:** Add new students by capturing their photo through the app.
- **Admin Dashboard:** Secure login, recent activity, and attendance logs.
- **User-Friendly GUI:** All interactions via a modern, desktop app interface.

***

## Requirements

- Windows 10/11 laptop or desktop
- Python 3.10
- Webcam (built-in or external)

***

## Dependencies

Before running, open Command Prompt and install the required packages:

```
pip install opencv-python mediapipe deepface pillow numpy pandas
```

**Note:**
- On first install, DeepFace or dlib may prompt for CMake and Microsoft Visual Studio Build Tools. Install if prompted.
- You may need administrative rights for some packages.
- These instructions tested as of September 2025.

***

## Installation Steps

1. Download or clone the project files to your PC.
2. Extract everything to a folder (recommended: `face_attendance_backup`).
3. Open Command Prompt, navigate to your project folder.

***

## How to Run

```
python app.py
```

- The main window will appear.
- As a student:  
  - Use "Register New Face" after entering the Student section to register.
- As admin:  
  - Click "Admin" and log in (default password: `admin123` – you can change this in `app.py`).
  - View logs, registered students, and recent activity.
- Attendance records (`attendance.csv`) and photos (in `registered_faces/`) are saved in your working folder.

***

## Folder Structure

```
face_attendance_backup/
│   app.py
│   attendance.csv         # attendance records (created by app)
│
├── registered_faces/      # student face images (auto-created)
│   └── {name}.jpg
└── app.log                # error/debug log file
```

***

## Troubleshooting

- If webcam access fails, close other apps using the camera and retry.
- If a dependency will not install, ensure your Python and pip are up-to-date.
- If face recognition or blink detection is inconsistent, adjust webcam position/lighting.
- See [DeepFace GitHub](https://github.com/serengil/deepface) if you have DeepFace or dlib issues.

***

## Credits
Uses DeepFace, OpenCV, Tkinter, and MediaPipe.


[1](https://github.com/othneildrew/Best-README-Template)
[2](https://github.com/python-project-templates)
[3](https://github.com/catiaspsilva/README-template)
[4](https://realpython.com/readme-python-project/)
[5](https://dev.to/sumonta056/github-readme-template-for-personal-projects-3lka)
[6](https://github.com/alan-turing-institute/python-project-template)
[7](https://github.com/topics/readme-template)
[8](https://www.makeareadme.com)
[9](https://github.com/rochacbruno/python-project-template)
