from tkinter import Tk

from database.db_api import Database
from widgets.main_window import MainWindow


# persist the defined database schema and open up the connection
db = Database()

# main Tk window
mw = MainWindow(Tk(), db)

# start the main loop
mw.mainloop()