import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets, QtGui
import sys

class GraphWidget(pg.PlotWidget):
    def __init__(self, x, y, x_label="", y_label=""):
        super().__init__()

        # Configurar fundo branco
        self.setBackground('white')

        # Ajustar as margens da área de plotagem
        self.setContentsMargins(50, 50, 50, 50)  # Margens: esquerda, cima, direita, baixo

        # Plotar os dados
        self.plot(x, y, pen=pg.mkPen('blue'))

        # Adicionar rótulos estilizados aos eixos (mais bonitinhos)
        label_style = {'font-size': '17pt', 'font-family': 'Arial', 'font-weight': 'bold'}

        # Ajustar o offset dos rótulos dos eixos
        self.setLabel('left', y_label, color='black', **label_style, offset=30)
        self.setLabel('bottom', x_label, color='black', **label_style, offset=30)

        # Estilizar os números dos eixos
        tick_font = QtGui.QFont('Arial', 10)
        self.getAxis('left').setTickFont(tick_font)
        self.getAxis('bottom').setTickFont(tick_font)

        # Adicionar grades claras
        self.showGrid(x=True, y=True, alpha=0.2)

        # Aumentar a área de plotagem
        self.setMinimumSize(800, 600)
