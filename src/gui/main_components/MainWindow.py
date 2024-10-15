from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStackedLayout, QPushButton
from ActVibModules.ActVibSystem import ActVibData

from ...core import Utils as dt
from .GraphWidget import GraphWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Data Checker")