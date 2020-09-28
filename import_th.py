import threading
import subprocess
import tkinter as tk
from queue import Queue


class MyClass(threading.Thread):
    def __init__(self,root):
        self.stdout = None
        self.stderr = None
        self.q = Queue(maxsize = 1024)
         # show subprocess' stdout in GUI
        self.label = tk.Label(root, text="  ", font=(None, 200))
        self.label.pack(ipadx=4, padx=4, ipady=4, pady=4, fill='both')
        threading.Thread.__init__(self)

    def run(self):
        p = subprocess.Popen('python3 download.py'.split(),
                             shell=False,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)

        self.stdout, self.stderr = p.communicate()
        reader_thread(self.q)

    
    def reader_thread(self, q):
        """Read subprocess output and put it into the queue."""
        try:
            with self.process.stdout as pipe:
                for line in iter(pipe.readline, b''):
                    q.put(line)
        finally:
            q.put(None)

root = tk.Tk()
root.title("Console")
myclass = MyClass(root)
myclass.daemon =True
myclass.start()
root.mainloop()
