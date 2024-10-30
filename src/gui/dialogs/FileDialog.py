import os
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFileDialog, QDialog, QTableWidget, QTableWidgetItem
from ...core.FileManager import FileManager

class ImportFileDialog(QFileDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Importar Arquivos")
        self.setDirectory(os.path.expanduser('~'))
        self.setFileMode(QFileDialog.ExistingFiles)
        self.setNameFilter("Feathers (*.feather);; Todos (*)")
        self.setMaximumHeight(800)
        
        self.filesSelected.connect(self.import_file)
        
    def import_file(self, file_paths):
        file_mngr = FileManager()
        file_mngr.add_files(file_paths)
        
        print(file_mngr[0].name, file_mngr[1].name)

class ManageFileDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Gerenciar Arquivos")
        
        table_header = ["Nome", "IMUs", "DACs", "Caminho"]
        files_table = QTableWidget(file_mngr.count_files(), len(table_header))
