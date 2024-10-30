from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStackedLayout, QTabWidget, QMenuBar, QLabel
from PySide6.QtGui import QAction
from ActVibModules.ActVibSystem import ActVibData
from .MenuBar import MenuBar
from ...core.Utils import get_ir, get_fr_from_ir
from .GraphWidget import GraphWidget
from ..dialogs.FileDialog import ImportFileDialog
from PySide6.QtCore import Qt

from PySide6.QtWidgets import QLabel, QVBoxLayout, QStackedLayout, QWidget, QMainWindow, QMenuBar, QApplication
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.data = None  # Inicializa sem dados carregados

        # Aumentando o tamanho da janela e centralizando no ecrã
        self.setWindowTitle("Data Checker")
        self.resize(1200, 800)  # Aumentando o tamanho inicial da janela para 1200x800
        self.setMinimumSize(1000, 700)  # Define o tamanho mínimo da janela

        # Centralizar a janela na tela
        self.center_window()

        # Layout principal
        main_layout = QVBoxLayout()

        # Mensagem inicial (centralizada e com estilo)
        self.message_label = QLabel("Carregue um arquivo para iniciar")
        self.message_label.setAlignment(Qt.AlignCenter)  # Centraliza a mensagem
        self.message_label.setStyleSheet("font-size: 20px; color: blue;")  # Aumenta o tamanho da fonte
        main_layout.addWidget(self.message_label)

        # Layout para os gráficos (inicialmente vazio)
        self.graphs_layout = QStackedLayout()
        main_layout.addLayout(self.graphs_layout)
        
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Criação de uma barra de menu com a opção "Menu"
        menu_bar = QMenuBar(self)
        
        # Opção "Menu" com subopções
        main_menu = menu_bar.addMenu('Menu')
        
        # Subopção "Selecionar Arquivo"
        select_action = QAction('Selecionar Arquivo', self)
        select_action.triggered.connect(self.open_file_dialog)
        main_menu.addAction(select_action)

        # Subopção "Retornar" para resetar a interface
        reset_action = QAction('Retornar', self)
        reset_action.triggered.connect(self.reset_interface)
        main_menu.addAction(reset_action)
        
        # Opção "Gráficos", inicialmente habilitado, mas sem submenus
        self.graph_menu = menu_bar.addMenu('Gráficos')
        self.graph_menu.setEnabled(False)  # Desabilitar até que o arquivo seja carregado
        self.graph_menu.aboutToShow.connect(self.show_graph_options)  # Carrega as opções ao clicar

        self.setMenuBar(menu_bar)

    def center_window(self):
        # Centralizar a janela na tela usando a geometria da tela disponível
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())
        self.move(window_geometry.topLeft())

    def open_file_dialog(self):
        dialog = ImportFileDialog(self)
        if dialog.exec():
            file_paths = dialog.selectedFiles()
            if file_paths:
                # Carrega o arquivo selecionado
                self.data = ActVibData(file_paths[0])
                self.show_success_message()  # Exibe a mensagem de sucesso
                # Habilitar o menu de gráficos após o arquivo ser carregado
                self.graph_menu.setEnabled(True)
                # Mostra a mensagem de pendência para o usuário
                self.message_label.setText("Arquivo carregado com sucesso! Entre no menu Gráficos para selecionar o tipo.")
                self.message_label.setStyleSheet("font-size: 18px; color: green;")  # Estilo de sucesso

    def show_graph_options(self):
        # Limpar o menu "Gráficos" e adicionar as opções RI e RF ao clicar
        self.graph_menu.clear()  # Garante que as opções não sejam duplicadas
        self.graph_ri_action = QAction('Gráfico RI', self)
        self.graph_ri_action.triggered.connect(self.set_ri)  # Conectando corretamente o método
        self.graph_menu.addAction(self.graph_ri_action)

        self.graph_rf_action = QAction('Gráfico RF', self)
        self.graph_rf_action.triggered.connect(self.set_rf)  # Conectando corretamente o método
        self.graph_menu.addAction(self.graph_rf_action)

    def show_success_message(self):
        # Centraliza a mensagem e limpa os gráficos se existirem
        self.message_label.setText("Sua implementação de dados se deu com sucesso.")
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setStyleSheet("font-size: 20px; color: green;")  # Mensagem de sucesso
        while self.graphs_layout.count():
            widget = self.graphs_layout.widget(0)
            self.graphs_layout.removeWidget(widget)
            widget.deleteLater()

    def reset_interface(self):
        # Reseta a interface ao estado inicial e mostra uma mensagem personalizada
        self.message_label.setText("Você voltou ao menu principal. Carregue um novo arquivo para continuar.")
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setStyleSheet("font-size: 20px; color: red;")  # Mensagem de retorno ao menu principal
        self.graph_menu.setEnabled(False)
        self.graph_menu.clear()  # Limpa as opções de gráficos ao resetar a interface
        while self.graphs_layout.count():
            widget = self.graphs_layout.widget(0)
            self.graphs_layout.removeWidget(widget)
            widget.deleteLater()

    def set_ri(self):
        # Verificar se os dados foram carregados e mostrar o gráfico RI
        if self.data is not None:
            y, x = get_ir(self.data["imu1accz"], self.data["dac1"], 416)
            ri_graph = GraphWidget(x, y, x_label="Tempo (s)", y_label="Amplitude (V)")
            self.graphs_layout.addWidget(ri_graph)
            self.graphs_layout.setCurrentIndex(self.graphs_layout.count() - 1)
            self.message_label.hide()  # Remove a mensagem de sucesso ao escolher o gráfico

    def set_rf(self):
        # Verificar se os dados foram carregados e mostrar o gráfico RF
        if self.data is not None:
            y, x = get_ir(self.data["imu1accz"], self.data["dac1"], 416)
            y, x = get_fr_from_ir([y, x])
            rf_graph = GraphWidget(x, y, x_label="Frequência (Hz)", y_label="Magnitude (dB)")
            self.graphs_layout.addWidget(rf_graph)
            self.graphs_layout.setCurrentIndex(self.graphs_layout.count() - 1)
            self.message_label.hide()  # Remove a mensagem de sucesso ao escolher o gráfico
