from tkinter import *
from datetime import date,datetime
from parse import *
import time
import threading
import re

# file reader
FILE_PATH = r'C:\Users\Kiki\Documents\Entropia Universe\chat.log'

def follow(file,callback):
    file.seek(0, 2)
    while True:
        line = file.readline()
        if not line:
            time.sleep(0.1)
            continue
        callback(line)


class LogApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Entropia Universe Tracker")

        # fonts
        titles_font = ("Aria Bold", 24)

        # date session start label
        current_datetime = date.today()
        start_date_label = Label(self.root,text="session start date : " + current_datetime.strftime("%d-%m-%Y"), font =titles_font)
        start_date_label.grid(column=0,row=0)

        self.log_thread = None

        #  label
        self.clock_label = Label(self.root,text="waiting for session start",font=titles_font)
        self.clock_label.grid(column=0,row=1)

        self.ressource_count = 0 
        self.ressource_label = Label(self.root,text=self.ressource_count,font=titles_font)
        self.ressource_label.grid(column=0,row=2)
        
        self.log_text = Text(self.root, wrap='word', state='normal', font=('Helvetica', 12))
        self.log_text.grid(column=0,row=3)

        self.sweat_session_start_btn = Button(self.root,text="Let's sweat !",command=self.sweat_start)
        self.sweat_session_start_btn.grid(column=0,row=4)

        

        self.elapsed_seconds = 0
        self.running = False
        self.timer_thread = None

    def sweat_start(self):
        self.start_log_following()
        self.start_timer()

    def start_log_following(self):
        if self.log_thread is None:
            file_path = FILE_PATH
            self.log_thread = threading.Thread(target=self.follow_log_file, args=(file_path,))
            self.log_thread.daemon = True
            self.log_thread.start()

    def follow_log_file(self, file_path):
        with open(file_path, 'r',encoding="utf-8") as file:
            follow(file, self.process_log_line)

    def process_log_line(self, line):
        if 'You received Vibrant Sweat x' in line:
            self.log_text.insert('end', line)    
            self.log_text.see('end')
            match = re.search(r'\((\d+)\)', line)
            if match:
                self.ressource_count = self.ressource_count + int(match.group(1))
                self.ressource_label.config(text=self.ressource_count)

                
    
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
    root = Tk()
    app = LogApp(root)
    root.mainloop()