from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStackedLayout, QPushButton
from ActVibModules.ActVibSystem import ActVibData

from ...core import DataChecker as dt
from .GraphWidget import GraphWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.data = ActVibData("data/R1_A12_0.75.feather")
        
        self.setWindowTitle("Data Checker")
        main_layout = QVBoxLayout()

        # Botões
        buttons_layout = QHBoxLayout()
        
        self.b_ri = QPushButton("Gráfico RI")
        self.b_ri.setCheckable(True)
        self.b_ri.clicked.connect(self.set_ri)
        buttons_layout.addWidget(self.b_ri)
        
        self.b_rf = QPushButton("Gráfico RF")
        self.b_rf.setCheckable(True)
        self.b_rf.clicked.connect(self.set_rf)
        buttons_layout.addWidget(self.b_rf)
        
        main_layout.addLayout(buttons_layout)
        
        # Gráficos
        self.graphs_layout = QStackedLayout()
        
        y, x = dt.get_ir(self.data["imu1accz"], self.data["dac1"], 416)
        ri_graph = GraphWidget(x, y)
        self.graphs_layout.addWidget(ri_graph)
        
        y, x = dt.get_fr_from_ir([y, x])
        rf_graph = GraphWidget(x, y)
        self.graphs_layout.addWidget(rf_graph)
        
        main_layout.addLayout(self.graphs_layout)
        
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        
    def set_ri(self):
        self.b_rf.setEnabled(True)
        self.b_ri.setEnabled(False)
        self.graphs_layout.setCurrentIndex(0)
    
    def set_rf(self):
        self.b_rf.setEnabled(False)
        self.b_ri.setEnabled(True)
        self.graphs_layout.setCurrentIndex(1)