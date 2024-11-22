from PySide6.QtWidgets import QFileDialog, QMainWindow, QVBoxLayout, QHBoxLayout, QMenuBar, QLabel, QWidget
from PySide6.QtGui import QAction
from PySide6.QtGui import QActionGroup
from ActVibModules.ActVibSystem import ActVibData
import re


class FileManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self.data_files = []  # Lista para armazenar os arquivos carregados
        self.current_data = None  # Dados do arquivo selecionado

    def open_file_dialog(self):
        dialog = QFileDialog(self.main_window)
        dialog.setFileMode(QFileDialog.ExistingFiles)  # Permitir seleção de múltiplos arquivos
        if dialog.exec():
            file_paths = dialog.selectedFiles()
            for path in file_paths:
                file_name = path.split("/")[-1]  # Obtém o nome do arquivo
                self.data_files.append({"name": file_name, "data": ActVibData(path)})  # Armazena nome e dados
            self.sort_files()  # Ordena os arquivos carregados
            self.update_file_count_message()

            # Habilitar o menu de escolha de arquivos e os botões da barra lateral
            self.main_window.file_menu.setEnabled(True)
            self.main_window.graph_menu.setEnabled(True)
            self.main_window.sidebar.enable_graph_buttons()

    def sort_files(self):
        # Função personalizada para ordenar arquivos
        def custom_sort_key(file_entry):
            name = file_entry["name"]
            # Extrai partes principais do nome do arquivo
            match = re.match(r"([A-Z]+)(\d+)([a-z0-9]*)", name, re.IGNORECASE)
            if match:
                letter, number, suffix = match.groups()
                # Converte o número para inteiro para ordenação numérica
                number = int(number)
                # Ordem: Letra principal (R/A) em ordem alfabética, número crescente, e depois o sufixo
                return (letter, number, suffix)
            return name  # Caso não corresponda ao padrão, retorna o nome original para ordenar por string

        # Ordena a lista de arquivos usando a chave personalizada
        self.data_files.sort(key=custom_sort_key)

    def update_file_count_message(self):
        count = len(self.data_files)
        self.main_window.message.label.setText(f"{count} arquivo(s) carregado(s) com sucesso. Escolha um para visualizar.")
        self.main_window.message.label.setStyleSheet("font-size: 18px; color: green;")

    def populate_file_menu(self):
        self.main_window.file_menu.clear()
        action_group = QActionGroup(self.main_window)
        for i, file_entry in enumerate(self.data_files):
            file_name = file_entry["name"]  # Usa o nome armazenado
            file_action = QAction(file_name, self.main_window)
            file_action.setCheckable(True)
            file_action.triggered.connect(lambda _, idx=i: self.select_file(idx))
            action_group.addAction(file_action)
            self.main_window.file_menu.addAction(file_action)

    def select_file(self, index):
        self.current_data = self.data_files[index]["data"]
        file_name = self.data_files[index]["name"]
        self.main_window.message.label.setText(f"Arquivo ativo: {file_name}")
        self.main_window.message.label.setStyleSheet("font-size: 18px; color: blue;")
        self.main_window.graph_manager.set_data(self.current_data)

    def reset_interface(self):
        self.main_window.message.label.setText("Você voltou ao menu principal. Carregue novos arquivos para continuar.")
        self.main_window.message.label.setStyleSheet("font-size: 18px; color: red;")
        self.main_window.graph_menu.setEnabled(False)
        self.main_window.file_menu.setEnabled(False)
        self.main_window.sidebar.disable_graph_buttons()
        self.data_files.clear()
        self.current_data = None
        self.main_window.file_menu.clear()
        self.main_window.graph_manager.clear_graphs()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data Checker")

        # Configurações principais
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Menu Bar
        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar)

        self.file_menu = self.menu_bar.addMenu("Arquivos")
        self.graph_menu = self.menu_bar.addMenu("Gráficos")
        self.graph_menu.setEnabled(False)

        # Mensagem de feedback
        self.message = QLabel("Carregue arquivos para começar.")
        self.message.setStyleSheet("font-size: 18px; color: black;")
        self.layout.addWidget(self.message)

        # Gerenciador de arquivos
        self.file_manager = FileManager(self)

        # Ação para abrir arquivos
        open_action = QAction("Abrir Arquivo(s)", self)
        open_action.triggered.connect(self.file_manager.open_file_dialog)
        self.file_menu.addAction(open_action)

        # Resetar a interface
        reset_action = QAction("Resetar Interface", self)
        reset_action.triggered.connect(self.file_manager.reset_interface)
        self.file_menu.addAction(reset_action)


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
