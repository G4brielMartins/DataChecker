from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMainWindow

from ..dialogs.FileDialog import ImportFileDialog
from ...core.FileManager import FileManager

class ActImportFile(QAction):
    def __init__(self, parent):
        super().__init__("Importar...", parent)
        import_file_dialog = ImportFileDialog(parent)
        self.triggered.connect(import_file_dialog.show)