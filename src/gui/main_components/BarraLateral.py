from PySide6.QtWidgets import QToolBar, QPushButton
from PySide6.QtCore import Qt

class BarraLateral(QToolBar):
    def __init__(self, main_window):
        super().__init__("Sidebar", main_window)

        self.setOrientation(Qt.Vertical)
        self.setFixedWidth(300)
        self.setMovable(False)

        # Botão para Carregar Arquivos
        load_button = QPushButton("Carregar Arquivos")
        load_button.clicked.connect(main_window.file_manager.open_file_dialog)
        self.addWidget(load_button)

        # Botão para Retornar ao Menu Principal
        return_button = QPushButton("Retornar ao Menu")
        return_button.clicked.connect(main_window.file_manager.reset_interface)
        self.addWidget(return_button)

        # Botão para exibir o Gráfico RI (inicialmente desabilitado)
        self.ri_button = QPushButton("Gráfico RI")
        self.ri_button.setEnabled(False)
        self.ri_button.clicked.connect(main_window.graph_manager.set_ri)
        self.addWidget(self.ri_button)

        # Botão para exibir o Gráfico RF (inicialmente desabilitado)
        self.rf_button = QPushButton("Gráfico RF")
        self.rf_button.setEnabled(False)
        self.rf_button.clicked.connect(main_window.graph_manager.set_rf)
        self.addWidget(self.rf_button)

    def enable_graph_buttons(self):
        """Habilita os botões de gráficos após o carregamento do arquivo"""
        self.ri_button.setEnabled(True)
        self.rf_button.setEnabled(True)

    def disable_graph_buttons(self):
        """Desabilita os botões de gráficos ao resetar a interface"""
        self.ri_button.setEnabled(False)
        self.rf_button.setEnabled(False)
        

