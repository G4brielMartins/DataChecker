from PySide6.QtWidgets import QVBoxLayout, QStackedLayout, QWidget, QMainWindow, QHBoxLayout, QApplication
from PySide6.QtGui import QAction, QActionGroup
from PySide6.QtCore import Qt
from .BarraLateral import BarraLateral
from .MenuSuperior import MenuSuperior
from .Mensagem import Mensagem
from .FileManager import FileManager
from .GraphManager import GraphManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Data Checker")
        self.resize(1200, 800)
        self.setMinimumSize(1000, 700)
        self.center_window()

        # Instâncias dos gerenciadores de arquivos, gráficos e mensagem
        self.file_manager = FileManager(self)
        self.graph_manager = GraphManager(self)
        self.message = Mensagem(self)

        # Layout principal
        main_layout = QHBoxLayout()

        # Adiciona o conteúdo central e a barra lateral
        content_layout = QVBoxLayout()
        content_layout.addWidget(self.message.label)
        content_layout.addLayout(self.graph_manager.graphs_layout)
        content_widget = QWidget()
        content_widget.setLayout(content_layout)
        main_layout.addWidget(content_widget)

        # Barra lateral e menu superior
        self.sidebar = BarraLateral(self)
        self.addToolBar(Qt.RightToolBarArea, self.sidebar)

        self.menu_superior = MenuSuperior(self)
        self.setMenuBar(self.menu_superior)

        # Configura o layout principal
        container_widget = QWidget()
        container_widget.setLayout(main_layout)
        self.setCentralWidget(container_widget)

    def center_window(self):
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())
        self.move(window_geometry.topLeft())
