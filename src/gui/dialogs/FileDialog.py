import os

from PySide6.QtWidgets import QFileDialog
from PySide6.QtWidgets import QApplication, QMainWindow

class FileDialog(QFileDialog):
    def __init__(self, parent: QMainWindow):
        super().__init__(
            parent,
            "Importar Arquivos",
            os.path.expanduser('~user'),
            "Feathers (*.feather)"
        )
        
        self.setFileMode(QFileDialog.ExistingFiles)
        self.file

app = QApplication([])
w = QMainWindow()
d = FileDialog(w)
w.show()
d.show()
app.exec()