import tkinter as tk
from tkinter import Frame,Label,Button
from parse import *
import time
import threading
import re
from playsound3 import playsound

# file reader
FILE_PATH = r'C:\Users\Kiki\Documents\Entropia Universe\chat.log' 

class LogApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Entropia Universe Tracker")
        self.root.minsize(200, 100)

        self.frame = Frame(self.root)
        self.frame.pack()
        # fonts
        titles_font = ("Aria Bold", 24)

        self.log_thread = None

        #  label
        self.clock_label = Label(self.frame,text="waiting for session start",font=titles_font)
        self.clock_label.grid(column=0,row=0)

        self.ressource_count = 0 
        self.ressource_label = Label(self.frame,text=self.ressource_count,font=titles_font)
        self.ressource_label.grid(column=0,row=1)

        self.sweat_session_start_btn = Button(self.frame,text="Let's sweat !",command=self.toogle_sweat)
        self.sweat_session_start_btn.grid(column=0,row=2)
        
        self.elapsed_seconds = 0
        self.running = False
        self.timer_thread = None

        self.following = False

        self.last_read_time = time.time()

        self.no_new_lines_interval = 120

    def toogle_sweat(self):
        if not self.following:
            self.start_following()
            self.start_timer()
            self.sweat_session_start_btn.config(text="Pause")
        else:
            self.stop_following()
            self.stop_timer()
            self.sweat_session_start_btn.config(text="Let's sweat !")

    def follow(self):
        self.last_read_time = time.time()
        with open(FILE_PATH, "r") as f:
            f.seek(0, 2)
            while self.following:
                line = f.readline()
                if line:
                    if 'You received Vibrant Sweat x' in line:
                        self.last_read_time = time.time()
                        match = re.search(r'\((\d+)\)', line)
                        if match:
                            self.ressource_count = self.ressource_count + int(match.group(1))
                            self.ressource_label.config(text=self.ressource_count)
                    elif 'You were killed' in line:
                        self.last_read_time = time.time()
                        playsound("./file.wav")
                else:
                    time.sleep(0.1)
                    if time.time() - self.last_read_time > self.no_new_lines_interval:
                        playsound("./file.wav")  
                        self.last_read_time = time.time()

    def start_following(self):
        self.following = True
        self.follow_thread = threading.Thread(target=self.follow)
        self.follow_thread.start()

    def stop_following(self):
        self.following = False
        self.follow_thread.join()  # Attendre la fin du thread

    
    def start_timer(self):
        if not self.running:
            self.running = True
            self.timer_thread = threading.Thread(target=self.update_timer)
            self.timer_thread.start()

    def update_timer(self):
        while self.running:
            mins, secs = divmod(self.elapsed_seconds, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            self.clock_label.config(text=timer)
            time.sleep(1)
            self.elapsed_seconds += 1

    def stop_timer(self):
        self.running = False
        if self.timer_thread:
            self.timer_thread.join()

    def reset_timer(self):
        self.elapsed_seconds = 0
        self.clock_label.config(text="00:00")
        self.running = False

if __name__ == '__main__':
    root = tk.Tk()
    app = LogApp(root)
    root.wm_attributes("-topmost", True)
    root.mainloop()