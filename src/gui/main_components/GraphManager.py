import numpy as np  
from PySide6.QtWidgets import QStackedLayout
from PySide6.QtGui import QAction
from .GraphWidget import GraphWidget
from ActVibModules.DSPFuncs import easyFourier 

class GraphManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self.graphs_layout = QStackedLayout()
        self.current_data = None

    def set_data(self, data):
        self.current_data = data

    def show_graph_options(self):
        self.main_window.graph_menu.clear()
        self.graph_ri_action = QAction('Gráfico RI', self.main_window)
        self.graph_ri_action.triggered.connect(self.set_ri)
        self.main_window.graph_menu.addAction(self.graph_ri_action)

        self.graph_rf_action = QAction('Gráfico RF', self.main_window)
        self.graph_rf_action.triggered.connect(self.set_rf)
        self.main_window.graph_menu.addAction(self.graph_rf_action)

    def get_ir(self, signal, dac):
        # Retorna os dados diretamente no domínio do tempo para o gráfico RI
        x = np.linspace(0, len(signal) / 416, len(signal))  # Tempo assumindo fs = 416 Hz
        y = signal
        return y, x

    def get_fr_from_ir(self, signal, fs=416):
        # Aplica a FFT usando easyFourier para obter o gráfico RF (domínio da frequência)
        mag, freq = easyFourier(signal, fs=fs)
        return mag, freq

    def set_ri(self):
        if self.current_data is not None:
            y, x = self.get_ir(self.current_data["imu1accz"], self.current_data["dac1"])
            ri_graph = GraphWidget(x, y, x_label="Tempo (s)", y_label="Amplitude (V)")
            self.graphs_layout.addWidget(ri_graph)
            self.graphs_layout.setCurrentIndex(self.graphs_layout.count() - 1)
            self.main_window.message.label.hide()  # Corrigido para ocultar o label de mensagem

    def set_rf(self):
        if self.current_data is not None:
            y, x = self.get_fr_from_ir(self.current_data["imu1accz"], fs=416)
            rf_graph = GraphWidget(x, y, x_label="Frequência (Hz)", y_label="Magnitude (dB)")
            self.graphs_layout.addWidget(rf_graph)
            self.graphs_layout.setCurrentIndex(self.graphs_layout.count() - 1)
            self.main_window.message.label.hide()  # Corrigido para ocultar o label de mensagem

    def clear_graphs(self):
        while self.graphs_layout.count():
            widget = self.graphs_layout.widget(0)
            self.graphs_layout.removeWidget(widget)
            widget.deleteLater()


