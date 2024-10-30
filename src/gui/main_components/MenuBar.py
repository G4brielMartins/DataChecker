from PySide6.QtWidgets import QMenuBar, QMainWindow

from .Actions import ActImportFile

class MenuBar(QMenuBar):
    def __init__(self, parent: QMainWindow):
        super().__init__(parent)
        
        file_menu = self.addMenu("Arquivo")
        
        import_file = ActImportFile(parent)
        file_menu.addAction(import_file)
        
        self.addMenu("Grafico")
        
        self.addMenu("Sensores")