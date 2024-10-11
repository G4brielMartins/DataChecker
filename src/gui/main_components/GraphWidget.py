from typing import Sequence

import pyqtgraph as pg

class GraphWidget(pg.PlotWidget):
    def __init__(self, x: Sequence[float], y: Sequence[float]):
        super().__init__()
        
        self.plot(x=x, y=y)