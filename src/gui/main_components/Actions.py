from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMainWindow

class ActImportFile(QAction):
    def __init__(self, parent: QMainWindow):
        super().__init__("Importar", parent)
        
        self.triggered.connect(self.import_file)
    
    def import_file(self):
        feather_paths = 