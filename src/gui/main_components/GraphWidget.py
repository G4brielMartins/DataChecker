import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets, QtGui

class GraphWidget(pg.PlotWidget):
    def __init__(self, x, y, x_label="", y_label=""):
        super().__init__()

        # Configurar fundo branco
        self.setBackground('white')

        # Ajustar as margens da área de plotagem
        self.setContentsMargins(50, 50, 50, 50)

        # Plotar os dados com uma linha mais delicada (espessura reduzida para 1)
        self.plot(x, y, pen=pg.mkPen('blue', width=1))

        # Adicionar rótulos estilizados aos eixos
        label_style = {'font-size': '17pt', 'font-family': 'Arial', 'font-weight': 'bold'}
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
