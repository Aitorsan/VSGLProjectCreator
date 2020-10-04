import sys
from itertools import islice
from subprocess import Popen, PIPE
from PIL import Image, ImageTk
from textwrap import dedent
from threading import Thread
import datetime
from queue import Queue, Empty
import logging
import signal
import time
import threading
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk, VERTICAL, HORIZONTAL, N, S, E, W
import argparse
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DisplaySubprocessOutputDemo:

    def __init__(self, build_type, build_tool, launch_dir):
        script_dir = os.path.join(launch_dir, 'depsManager.py')
        self.process = Popen(['python3',script_dir,'--build_type',build_type,'--build_tool',build_tool,'-d',launch_dir],\
            stdout=PIPE,stderr=PIPE)
    
        # launch thread to read the subprocess output
        # log the subprocess output into the logger in a background thread
        t = Thread(target=self.reader_thread)
        t.daemon = True # close pipe if GUI process exits
        t.start()

    def reader_thread(self):
        try:
            with self.process.stdout as pipe:
                for line in iter(pipe.readline, b''):
                    logger.info( line.decode())
        finally:
            logger.info('--- DEPENDENCY PROCESS END --- ')
            time.sleep(2)
            os._exit(1)
            
    def quit(self):
        self.process.kill() # exit subprocess if GUI is closed (zombie!)

class QueueHandler(logging.Handler):

    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        self.log_queue.put(record)

class ConsoleUi:
    # Poll messages from a logging queue and display them in a scrolled text widget
    def __init__(self, frame):
        self.frame = frame
        # Create a ScrolledText wdiget
        self.text_options = {"state": "disabled",
                             "bg": "black",
                             "fg": "#08c614",
                             "insertbackground": "#08c614",
                             "selectbackground": "#f01c1c",
                             "heigh":"30"}

        self.scrolled_text = ScrolledText(self.frame, **self.text_options)
        self.scrolled_text.pack(fill=tk.BOTH,expand =True)
        self.scrolled_text.configure(font='TkFixedFont')
        self.scrolled_text.tag_config('INFO', foreground='green')
        self.scrolled_text.tag_config('DEBUG', foreground='gray')
        self.scrolled_text.tag_config('WARNING', foreground='orange')
        self.scrolled_text.tag_config('ERROR', foreground='red')
        self.scrolled_text.tag_config('CRITICAL', foreground='red', underline=1)
        # Create a logging handler using a queue
        self.log_queue = Queue()
        self.queue_handler = QueueHandler(self.log_queue)
        formatter = logging.Formatter('%(message)s')
        self.queue_handler.setFormatter(formatter)
        logger.addHandler(self.queue_handler)
        # Start polling messages from the queue
        self.frame.after(70, self.poll_log_queue)

    def display(self, record):
        msg = self.queue_handler.format(record)
        self.scrolled_text.configure(state='normal')
        self.scrolled_text.insert(tk.END, msg + '\n', record.levelname)
        self.scrolled_text.configure(state='disabled')
        # Autoscroll to the bottom
        self.scrolled_text.yview(tk.END)

    def poll_log_queue(self):
        # Check every 100ms if there is a new message in the queue to display
        while True:
            try:
                record = self.log_queue.get(block=False)
            except Empty:
                break
            else:
                self.display(record)
        self.frame.after(100, self.poll_log_queue)

class App:

    def __init__(self, build_type, build_tool, launch_dir, icons_dir):
        self.root = tk.Tk()
        self.root.title('Building dependencies')
        self.root.iconbitmap(icons_dir)
        self.console_frame = ttk.Labelframe(self.root, text="Console")
        self.console_frame.pack(fill=tk.BOTH,expand =True)
        self.console = ConsoleUi(self.console_frame)
        self.subproc_out = DisplaySubprocessOutputDemo(build_type, build_tool, launch_dir)
        self.root.protocol('WM_DELETE_WINDOW', self.quit)
        self.root.bind('<Control-q>', self.quit)
        signal.signal(signal.SIGINT, self.quit)

    def quit(self, *args):
        self.root.destroy()

def parse_args():
    parser = argparse.ArgumentParser(description="depency build parameters")
    parser.add_argument('-b','--build_type',type=str ,metavar='',help='build type Debug or Release')
    parser.add_argument('-t','--build_tool', type=str,metavar='',help='NMake, make, VS')
    parser.add_argument('-d','--launch_dir', type=str,metavar='',help='script launch directory')
    return parser.parse_args()

def main():
    args = parse_args()
    build_type='Debug'
    build_tool = 'NMake Makefiles'
    launch_dir = args.launch_dir
    if args.build_type:
        build_type = args.build_type
    if args.build_tool :
        build_tool = args.build_tool
    logging.basicConfig(level=logging.INFO)
    icons_dir =  r'{}'.format(os.path.join(launch_dir,'icons','opengl.ico'))
    app = App(build_type,build_tool,launch_dir,icons_dir)
    app.root.mainloop()

if __name__ == '__main__':
    main()