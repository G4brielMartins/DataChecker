from PySide6.QtGui import QAction

from ...core.FileManager import FileManager

class ActImportFile(QAction):
    def __init__(self, parent):
        super().__init__("Importar", parent)
        
        self.triggered.connect(self.import_files)
    
    def import_files(self, file_paths):
        file_mng = FileManager()
        file_mng.add_files(file_paths)
        
        print(file_mng[:])