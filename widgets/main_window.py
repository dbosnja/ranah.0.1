class MainWindow:
    def __init__(self, root, db):
        self.root = root
        self.db = db
    
    def mainloop(self):
        self.root.mainloop()