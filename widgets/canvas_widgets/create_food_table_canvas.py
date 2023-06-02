from tkinter import Canvas, PhotoImage

from .frame_widgets import CreateFoodLabelFrame


class CreateFoodTableCanvas:
    """description"""

    def __init__(self, parent, db):
        self.parent = parent
        self.db = db

        self._initialize_canvas()

    def _initialize_canvas(self):
        self.canvas = Canvas(self.parent, width=700, height=700)
        self.canvas.grid(row=0, column=0, sticky='news')
        self.canvas.rowconfigure(0, weight=1)
        self.canvas.columnconfigure(0, weight=1)
        
        frame = CreateFoodLabelFrame(self.canvas, self.db)
        self.frame_id = self.canvas.create_window(0, 0, window=frame.frame, anchor='nw')

        self.canvas.bind('<Configure>', lambda _: self._configure_frame_surface())
    
    def _configure_frame_surface(self):
        self.canvas.itemconfigure(self.frame_id, width=self.canvas.winfo_width())
        self.canvas.itemconfigure(self.frame_id, height=self.canvas.winfo_height())
