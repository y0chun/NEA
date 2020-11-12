import sys
import time

import numpy as np

from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
if is_pyqt5():
    from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
else:
    from matplotlib.backends.backend_qt4agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure

import random

v = 10
ap = 40
e = 0
g = 9.8                                                                                                             
theta = (np.pi/180)*ap     

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        self.canvas = FigureCanvas(Figure(figsize=(10, 5)))

        layout = QtWidgets.QVBoxLayout(self._main)
        layout.addWidget(self.canvas)
        self._update_canvas()

    def _update_canvas(self):
        data = [random.random() for i in range(10)]
        ax = self.canvas.add_subplot(111)
        ax.hold(False)
        ax.plot(data, linestyle='dashed')
        self.canvas.draw()

#v * np.sin(theta) * (t + time.time()) - (0.5) * g * ((t + time.time()))**2 + e

if __name__ == "__main__":
    qapp = QtWidgets.QApplication(sys.argv)
    app = ApplicationWindow()
    app.show()
    qapp.exec_()