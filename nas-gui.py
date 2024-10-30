import os
import time
import shutil
import random
from tkinter import *
from tkinter.font import Font
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from threading import Thread

# Constants
WATCH_PATH = r"C:\Users\sidha\OneDrive\Desktop\shared"

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, display_message_func):
        super().__init__()
        self.display_message_func = display_message_func

    def on_modified(self, event):
        self.display_message_func(f"File modified: {os.path.basename(event.src_path)} (Type: {self.get_file_type(event.src_path)})")

    def on_created(self, event):
        self.display_message_func(f"File added: {os.path.basename(event.src_path)} (Type: {self.get_file_type(event.src_path)})")

    def on_deleted(self, event):
        self.display_message_func(f"File removed: {os.path.basename(event.src_path)} (Type: {self.get_file_type(event.src_path)})")

    @staticmethod
    def get_file_type(file_path):
        _, extension = os.path.splitext(file_path)
        return extension if extension else "Unknown"

class CyberRobotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sidhaant's Home NAS (Network Attached Storage)")
        self.root.geometry("1000x600")
        self.root.configure(bg='black')

        # Title
        cyber_font = Font(family="Impact", size=32, weight="bold")
        title = Label(root, text="Sidhaant's Home NAS (Network Attached Storage)", font=cyber_font, fg="cyan", bg="black")
        title.pack(pady=20)

        # Alerts Frame
        self.alerts_frame = Frame(root, bg="black")
        self.alerts_frame.pack(pady=10)

        # File Count
        self.file_count_label = Label(self.alerts_frame, text=f"Number of files: {self.get_file_count()}", fg="yellow", bg="black", font=("Helvetica", 20))
        self.file_count_label.pack()

        # Storage Info
        self.storage_label = Label(self.alerts_frame, text=self.get_storage_info(), fg="yellow", bg="black", font=("Helvetica", 20))
        self.storage_label.pack()

        # Message Bubble (Alerts)
        self.message_label = Label(self.alerts_frame, text="", fg="yellow", bg="black", font=("Helvetica", 16, "bold"))
        self.message_label.pack()

        # Binary Matrix Animation Frames (closer to the robot)
        self.matrix_left = Text(root, width=6, height=20, bg="black", fg="green", font=("Courier", 14), borderwidth=0)
        self.matrix_right = Text(root, width=6, height=20, bg="black", fg="green", font=("Courier", 14), borderwidth=0)
        self.matrix_left.place(relx=0.32, rely=0.4, anchor="e")
        self.matrix_right.place(relx=0.68, rely=0.4, anchor="w")

        # ASCII Art Robot
        self.robot_label = Label(root, text=self.robot_art(), fg="white", bg="black", font=("Courier", 16), justify="left")
        self.robot_label.pack(pady=(10, 0))

        # Start Matrix Animation Threads
        Thread(target=self.matrix_fall, args=(self.matrix_left,), daemon=True).start()
        Thread(target=self.matrix_fall, args=(self.matrix_right,), daemon=True).start()

    def robot_art(self):
        return (
            "                  ,--.    ,--.\n"
            "                 ((O ))--((O ))\n"
            "               ,'_`--'____`--'_`.\n"
            "              _:  ____________  :_\n"
            "             | | ||::::::::::|| | |\n"
            "             | | ||::::::::::|| | |\n"
            "             | | ||::::::::::|| | |\n"
            "             |_| |/__________\\| |_| \n"
            "               |________________|\n"
            "            __..-'            `-..__\n"
            "         .-| : .----------------. : |-.\n"
            "       ,\\ || | |\\______________/| | || /.\n"
            "      /`\\. :| | ||  __  __  __  || | |; /\\\n"
            "     :`-._\\;.| || '--''--''--' || |,:/_.-':\n"
            "     |    :  | || .----------. || |  :    |\n"
            "     |    |  | || '----Sid---' || |  |    |\n"
            "     |    |  | ||   _   _   _  || |  |    |\n"
            "     :,--.;  | ||  (_) (_) (_) || |  :,--.;\n"
            "     (`-'|)  | ||______________|| |  (|`-')\n"
            "      `--'   | |/______________\\| |   `--'\n"
            "             |____________________|\n"
            "              `.________________,'\n"
            "               (_______)(_______)\n"
            "               (_______)(_______)\n"
            "               (_______)(_______)\n"
            "               (_______)(_______)\n"
            "              |        ||        |\n"
            "              '--------''--------' \n"
        )

    def get_file_count(self):
        return len(os.listdir(WATCH_PATH))

    def get_storage_info(self):
        total, used, _ = shutil.disk_usage(WATCH_PATH)
        total_gb = total // (2**30)
        used_gb = used // (2**30)
        return f"Storage: {used_gb}GB used of {total_gb}GB"

    def display_message(self, message):
        self.message_label.config(text=message)
        self.file_count_label.config(text=f"Number of files: {self.get_file_count()}")
        self.storage_label.config(text=self.get_storage_info())
        self.animate_mouth()

    def animate_mouth(self):
        # Basic mouth animation placeholder (toggle visibility)
        def toggle():
            current_text = self.robot_label.cget("text")
            if current_text.count("-") > 0:
                self.robot_label.config(text=self.robot_art().replace("-", "o"))  # Mouth open
            else:
                self.robot_label.config(text=self.robot_art())  # Mouth closed
            self.root.after(300, toggle)
        toggle()

    def matrix_fall(self, text_widget):
        while True:
            text_widget.delete("1.0", END)
            for _ in range(20):
                line = "".join(random.choice("01") for _ in range(6))
                text_widget.insert(END, line + "\n")
            time.sleep(0.1)

def start_watcher(gui):
    event_handler = FileChangeHandler(gui.display_message)
    observer = Observer()
    observer.schedule(event_handler, WATCH_PATH, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# Main execution
if __name__ == "__main__":
    root = Tk()
    gui = CyberRobotGUI(root)
    Thread(target=start_watcher, args=(gui,), daemon=True).start()
    root.mainloop()
