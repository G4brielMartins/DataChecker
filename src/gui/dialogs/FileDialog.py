import os

from PySide6.QtWidgets import QFileDialog
from PySide6.QtWidgets import QApplication, QMainWindow

from ..main_components.Actions import ActImportFile

class FileDialog(QFileDialog):
    def __init__(self, parent: QMainWindow):
        super().__init__(parent, "Importar Arquivos")
        self.setDirectory(os.path.expanduser('~'))
        self.setFileMode(QFileDialog.ExistingFiles)
        self.setNameFilter("Feathers (*.feather);; Todos (*)")
        
        import_files_act = ActImportFile(self)
        self.filesSelected.connect(import_files_act)

app = QApplication([])
w = QMainWindow()
d = FileDialog(w)
w.show()
d.exec()
app.exec()