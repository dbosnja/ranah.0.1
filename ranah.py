from tkinter import Tk

from database.db_api import Database
from widgets.main_window import MainWindow


# initialize ranah database
db = Database()

# main ranah window
mw = MainWindow(Tk(), db)

# start the main loop
mw.mainloop()

