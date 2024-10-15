from PySide6.QtWidgets import QMainWindow

from .MenuBar import MenuBar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Data Checker")
        self.setMinimumWidth(600)
        self.setMinimumHeight(400)
        
        menu_bar = MenuBar(self)
        self.setMenuBar(menu_bar)