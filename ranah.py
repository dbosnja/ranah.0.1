#! /home/dom_ak45/.local/share/virtualenvs/ranah.0.1-U4ckHnxd/bin/python
import os

from tkinter import Tk

from database.db_api import Database
from widgets.main_window import MainWindow


# TODO: update this somehow to be cross-platform
os.chdir("/home/dom_ak45/projects/ranah/ranah.0.1/")


# initialize ranah database
db = Database()


# main ranah window
mw = MainWindow(Tk(), db)


# start the main loop
mw.mainloop()

