import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import cv2
from PIL import Image, ImageTk
import os
import sys
import pandas as pd
from datetime import datetime
from utils import LivenessDetector, mark_attendance

CAM_INDEX = 0
REGISTER_DIR = 'registered_faces'
ATTENDANCE_FILE = 'attendance.csv'


def clear_attendance_log(filename=ATTENDANCE_FILE):
    with open(filename, 'w') as f:
        f.write("Name,Time\n")
    print("Attendance log cleared.")


class FaceAttendanceApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Face Attendance System with Blink Liveness")
        self.geometry("1100x700")

        self.detector = LivenessDetector()

        # Registration variables
        self.reg_cam = None
        self.reg_video_running = False
        self.current_reg_frame = None
        self.captured_image = None
        self.photo_panel = None

        # Attendance variables
        self.cam = None
        self.video_running = False
        self.blink_count = 0
        self.attendance_marked = False

        self.known_user = "User"  # Placeholder, replace with real user recognition

        # UI Setup
        self.tabControl = ttk.Notebook(self)
        self.register_tab = ttk.Frame(self.tabControl)
        self.attendance_tab = ttk.Frame(self.tabControl)
        self.log_tab = ttk.Frame(self.tabControl)

        self.tabControl.add(self.register_tab, text='Register User')
        self.tabControl.add(self.attendance_tab, text='Attendance')
        self.tabControl.add(self.log_tab, text='View Logs')
        self.tabControl.pack(expand=1, fill="both")

        self.setup_register_tab()
        self.setup_attendance_tab()
        self.setup_log_tab()

    # -------- Registration Tab --------
    def setup_register_tab(self):
        for w in self.register_tab.winfo_children():
            w.destroy()

        ttk.Label(self.register_tab, text="Do you want to register a new user?").pack(anchor='center', pady=20)

        start_btn = ttk.Button(self.register_tab, text="Start Registration", command=self.show_registration_ui)
        start_btn.pack(anchor='center')

    def show_registration_ui(self):
        for w in self.register_tab.winfo_children():
            w.destroy()

        ttk.Label(self.register_tab, text="Enter Name to Register:").pack(anchor='w', padx=10, pady=5)
        self.name_var = tk.StringVar()
        ttk.Entry(self.register_tab, textvariable=self.name_var, width=40).pack(anchor='w', padx=10, pady=5)

        self.reg_video_label = ttk.Label(self.register_tab)
        self.reg_video_label.pack(anchor='w', padx=10, pady=10)

        self.capture_btn = ttk.Button(self.register_tab, text="Capture Photo", command=self.capture_photo)
        self.capture_btn.pack(anchor='w', padx=10, pady=10)

        self.confirm_btn = ttk.Button(self.register_tab, text="Confirm & Save", command=self.save_photo)
        self.confirm_btn.pack(anchor='w', padx=10, pady=5)
        self.confirm_btn.config(state='disabled')

        self.retake_btn = ttk.Button(self.register_tab, text="Retake Photo", command=self.retake_photo)
        self.retake_btn.pack(anchor='w', padx=10, pady=5)
        self.retake_btn.config(state='disabled')

        self.reg_status = ttk.Label(self.register_tab, text="", foreground="green")
        self.reg_status.pack(anchor='w', padx=10, pady=5)

        self.start_reg_video()

    def start_reg_video(self):
        if self.reg_video_running:
            return
        self.reg_cam = cv2.VideoCapture(CAM_INDEX)
        self.reg_video_running = True
        self.update_reg_video()

    def update_reg_video(self):
        if not self.reg_video_running:
            return
        ret, frame = self.reg_cam.read()
        if not ret:
            self.reg_video_running = False
            self.reg_cam.release()
            return

        self.current_reg_frame = frame
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)
        self.reg_video_label.imgtk = imgtk
        self.reg_video_label.configure(image=imgtk)
        self.after(30, self.update_reg_video)

    def capture_photo(self):
        name = self.name_var.get().strip()
        if not name:
            messagebox.showwarning("Input Error", "Please enter a name to register.")
            return

        if self.current_reg_frame is None:
            messagebox.showerror("Camera Error", "No live preview available. Try again.")
            return

        self.reg_video_running = False

        self.captured_image = self.current_reg_frame.copy()
        frame_rgb = cv2.cvtColor(self.captured_image, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)
        self.reg_video_label.configure(image=imgtk)
        self.reg_video_label.image = imgtk

        self.confirm_btn.config(state='normal')
        self.retake_btn.config(state='normal')
        self.capture_btn.config(state='disabled')
        self.reg_status.config(text="Preview your photo. Confirm to save or retake.")

    def save_photo(self):
        name = self.name_var.get().strip()
        if self.captured_image is None:
            messagebox.showwarning("No Image", "No photo captured to save.")
            return

        os.makedirs(REGISTER_DIR, exist_ok=True)
        filename = f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        filepath = os.path.join(REGISTER_DIR, filename)
        cv2.imwrite(filepath, self.captured_image)

        self.reg_status.config(text=f"Saved photo as {filename}. Capture another if needed.")

        self.confirm_btn.config(state='disabled')
        self.retake_btn.config(state='disabled')
        self.capture_btn.config(state='normal')
        self.captured_image = None
        self.reg_video_running = True
        self.update_reg_video()

    def retake_photo(self):
        self.reg_status.config(text="Retake photo. Click 'Capture Photo' when ready.")
        self.confirm_btn.config(state='disabled')
        self.retake_btn.config(state='disabled')
        self.capture_btn.config(state='normal')
        self.captured_image = None
        self.reg_video_running = True
        self.update_reg_video()

    # -------- Attendance Tab --------
    def setup_attendance_tab(self):
        for w in self.attendance_tab.winfo_children():
            w.destroy()

        self.video_label = ttk.Label(self.attendance_tab)
        self.video_label.pack(padx=10, pady=10)

        self.blink_status = ttk.Label(self.attendance_tab,
                                      text="Click 'Start Attendance' and blink twice to mark attendance.",
                                      font=("Arial", 14))
        self.blink_status.pack(pady=5)

        controls_frame = ttk.Frame(self.attendance_tab)
        controls_frame.pack(pady=10)

        self.btn_start_cam = ttk.Button(controls_frame, text="Start Attendance", command=self.start_attendance)
        self.btn_start_cam.grid(row=0, column=0, padx=5)

        self.btn_stop_cam = ttk.Button(controls_frame, text="Stop Attendance", command=self.stop_attendance,
                                       state='disabled')
        self.btn_stop_cam.grid(row=0, column=1, padx=5)

    def start_attendance(self):
        if self.video_running:
            return
        self.cam = cv2.VideoCapture(CAM_INDEX)
        self.video_running = True
        self.btn_start_cam.config(state='disabled')
        self.btn_stop_cam.config(state='normal')
        self.blink_count = 0
        self.attendance_marked = False
        self.update_video()

    def update_video(self):
        if not self.video_running:
            return

        ret, frame = self.cam.read()
        if not ret:
            self.stop_attendance()
            return

        blink_detected = self.detector.detect_blink(frame) if not self.attendance_marked else False

        if not self.attendance_marked:
            if blink_detected:
                self.blink_count += 1
                self.blink_status.config(text=f"Status: Blink detected ({self.blink_count}/2)")
                if self.blink_count >= 2:
                    mark_attendance(self.known_user, ATTENDANCE_FILE)
                    self.attendance_marked = True
                    self.blink_status.config(text="Attendance marked successfully! You can stop or try again.")

                    messagebox.showinfo("Attendance", "Attendance marked successfully!")
            else:
                self.blink_status.config(text="Status: Please blink twice to confirm liveness")
        else:
            self.blink_status.config(text="Attendance done. You may stop or blink again to add more.")

        if not self.attendance_marked:
            if blink_detected:
                display_text = "LIVE PERSON ✅"
                color = (0, 255, 0)
            else:
                display_text = "Please blink to confirm liveness"
                color = (255, 255, 0)
        else:
            display_text = "Attendance Marked ✔"
            color = (0, 255, 0)

        cv2.putText(frame, display_text, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)

        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)
        self.after(30, self.update_video)

    def stop_attendance(self):
        if not self.video_running:
            return
        self.video_running = False
        self.cam.release()
        self.video_label.config(image="")
        self.btn_start_cam.config(state='normal')
        self.btn_stop_cam.config(state='disabled')
        self.blink_status.config(text="Attendance stopped. Click 'Start Attendance' to begin again.")
        self.blink_count = 0
        self.attendance_marked = False

    # -------- Log Tab --------
    def setup_log_tab(self):
        for w in self.log_tab.winfo_children():
            w.destroy()

        ttk.Label(self.log_tab, text="Attendance Log").pack(pady=10)

        # Treeview setup for sortable, scrollable table
        columns = ('Name', 'Time')
        self.tree = ttk.Treeview(self.log_tab, columns=columns, show='headings')
        self.tree.heading('Name', text='Name', command=lambda: self.treeview_sort_column('Name', False))
        self.tree.heading('Time', text='Time', command=lambda: self.treeview_sort_column('Time', False))
        self.tree.column('Name', width=200)
        self.tree.column('Time', width=300)
        self.tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.log_tab, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Buttons for refresh, clear, export, filter
        btn_frame = ttk.Frame(self.log_tab)
        btn_frame.pack(pady=5)

        self.btn_refresh_log = ttk.Button(btn_frame, text="Refresh Log", command=self.load_log)
        self.btn_refresh_log.grid(row=0, column=0, padx=5)

        self.btn_clear_log = ttk.Button(btn_frame, text="Clear Log", command=self.clear_log)
        self.btn_clear_log.grid(row=0, column=1, padx=5)

        self.btn_export_log = ttk.Button(btn_frame, text="Export Log", command=self.export_log)
        self.btn_export_log.grid(row=0, column=2, padx=5)

        ttk.Label(btn_frame, text="Filter by Name:").grid(row=1, column=0, padx=5, pady=5)
        self.filter_var = tk.StringVar()
        self.entry_filter = ttk.Entry(btn_frame, textvariable=self.filter_var)
        self.entry_filter.grid(row=1, column=1, padx=5, pady=5)

        self.btn_filter_log = ttk.Button(btn_frame, text="Apply Filter", command=self.load_log)
        self.btn_filter_log.grid(row=1, column=2, padx=5, pady=5)

        self.load_log()

    def load_log(self):
        self.tree.delete(*self.tree.get_children())

        if not os.path.exists(ATTENDANCE_FILE):
            return

        df = pd.read_csv(ATTENDANCE_FILE)
        filter_text = self.filter_var.get().strip().lower()
        if filter_text:
            df = df[df['Name'].str.lower().str.contains(filter_text)]

        for _, row in df.iterrows():
            self.tree.insert('', 'end', values=(row['Name'], row['Time']))

    def clear_log(self):
        if messagebox.askyesno("Confirm Clear", "Are you sure you want to clear all attendance records?"):
            with open(ATTENDANCE_FILE, 'w') as f:
                f.write("Name,Time\n")
            self.load_log()
            messagebox.showinfo("Cleared", "Attendance log has been cleared.")

    def export_log(self):
        if not os.path.exists(ATTENDANCE_FILE):
            messagebox.showwarning("Export Error", "No log file to export.")
            return

        export_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All Files", "*.*")],
            title="Save Attendance Log As"
        )
        if export_path:
            try:
                df = pd.read_csv(ATTENDANCE_FILE)
                df.to_csv(export_path, index=False)
                messagebox.showinfo("Exported", f"Log exported successfully to:\n{export_path}")
            except Exception as e:
                messagebox.showerror("Export Failed", f"An error occurred:\n{e}")

    def treeview_sort_column(self, col, reverse):
        l = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
        try:
            l.sort(key=lambda t: datetime.strptime(t[0], '%Y-%m-%d %H:%M:%S'), reverse=reverse)
        except ValueError:
            l.sort(reverse=reverse)
        for index, (val, k) in enumerate(l):
            self.tree.move(k, '', index)
        self.tree.heading(col, command=lambda: self.treeview_sort_column(col, not reverse))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--clear-log':
        clear_attendance_log()
        sys.exit(0)

    app = FaceAttendanceApp()
    app.mainloop()
