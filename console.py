import sys
from itertools import islice
from subprocess import Popen, PIPE
from textwrap import dedent
from threading import Thread
import datetime
from queue import Queue, Empty # Python 3
import logging
import signal
import time
import threading
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk, VERTICAL, HORIZONTAL, N, S, E, W


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def iter_except(function, exception):
    """Works like builtin 2-argument `iter()`, but stops on `exception`."""
    try:
        while True:
            yield function()
    except exception:
        return

class DisplaySubprocessOutputDemo:
    def __init__(self):
        self.process = Popen('python3 download.py'.split(),stdout=PIPE,stderr=PIPE)
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
       
    def quit(self):
        self.process.kill() # exit subprocess if GUI is closed (zombie!)

class QueueHandler(logging.Handler):

    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        self.log_queue.put(record)


class ConsoleUi:
    """Poll messages from a logging queue and display them in a scrolled text widget"""

    def __init__(self, frame):
        self.frame = frame
        # Create a ScrolledText wdiget
        self.scrolled_text = ScrolledText(frame, state='disabled', height=12)
        self.scrolled_text.grid(row=0, column=0, sticky=(N, S, W, E))
        self.scrolled_text.configure(font='TkFixedFont')
        self.scrolled_text.tag_config('INFO', foreground='black')
        self.scrolled_text.tag_config('DEBUG', foreground='gray')
        self.scrolled_text.tag_config('WARNING', foreground='orange')
        self.scrolled_text.tag_config('ERROR', foreground='red')
        self.scrolled_text.tag_config('CRITICAL', foreground='red', underline=1)
        # Create a logging handler using a queue
        self.log_queue = Queue()
        self.queue_handler = QueueHandler(self.log_queue)
        formatter = logging.Formatter('%(asctime)s: %(message)s')
        self.queue_handler.setFormatter(formatter)
        logger.addHandler(self.queue_handler)
        # Start polling messages from the queue
        self.frame.after(100, self.poll_log_queue)

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

    def __init__(self, root):
        self.root = root
        root.title('Logging Handler')
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        # Create the panes and frames
        vertical_pane = ttk.PanedWindow(self.root, orient=VERTICAL)
        vertical_pane.grid(row=0, column=0, sticky="nsew")
        horizontal_pane = ttk.PanedWindow(vertical_pane, orient=HORIZONTAL)
        vertical_pane.add(horizontal_pane)
        form_frame = ttk.Labelframe(horizontal_pane, text="MyForm")
        #form_frame.columnconfigure(1, weight=1)
        horizontal_pane.add(form_frame, weight=1)
        # create list box with a new style to avoid icon overlaping
        self.s = ttk.Style()
        self.s.configure('treeStyle.Treeview', rowheight=40)
        self.project_list_box = ttk.Treeview(form_frame, height=4, style='treeStyle.Treeview')
        #change select mode to not allow multiple selection of items
        self.project_list_box.config(selectmode='browse')
         # configure the heigh of the tree
        self.project_list_box.config(height=10)
        self.project_list_box.pack(fill=tk.BOTH,expand=True,padx = 4,pady=4)

        console_frame = ttk.Labelframe(horizontal_pane, text="Console")
        console_frame.columnconfigure(0, weight=1)
        console_frame.rowconfigure(0, weight=1)
        horizontal_pane.add(console_frame, weight=1)
        third_frame = ttk.Labelframe(vertical_pane, text="Third Frame")
        vertical_pane.add(third_frame, weight=1)
        # Initialize all frames
        self.console = ConsoleUi(console_frame)
        self.subproc_out = DisplaySubprocessOutputDemo()
        self.root.protocol('WM_DELETE_WINDOW', self.quit)
        self.root.bind('<Control-q>', self.quit)
        signal.signal(signal.SIGINT, self.quit)

    def quit(self, *args):
        self.root.destroy()


def main():
    logging.basicConfig(level=logging.DEBUG)
    root = tk.Tk()
    app = App(root)
    app.root.mainloop()


if __name__ == '__main__':
    main()