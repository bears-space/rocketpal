#!/usr/bin/env python3

import logging

from tkinter import Tk
from tkinter.ttk import Frame, Label


if __name__ == "__main__":
    # Set default logging level
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)

    # Prepare main window
    root = Tk()
    root.title("FSG - Flight Simulation GUI")
    root.geometry("1280x720")
    frame = Frame(root, padding=10)
    frame.grid()

    # Hello world test
    a = Label(frame, text="Hello world!").grid(column=0, row=0)

    # Enter GUI main loop
    root.mainloop()
