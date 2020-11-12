from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation
 
v = 10
ap = 40
e = 0
g = 9.8                                                                                                             
theta = (np.pi/180)*ap     
x_data = []
y_data = []
 
class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
 
        title = "Embed"
        top = 400
        left = 400
        width = 900
        height = 500
 
        self.setWindowTitle(title)
        self.setGeometry(top, left, width, height)
 
        self.MyUI()
 
 
    def MyUI(self):
 
        canvas = Canvas(self, width=8, height=4)
        canvas.move(0,0)
 
        button = QPushButton("Click Me", self)
        button.move(100, 450)
 
 
class Canvas(FigureCanvas):
    def __init__(self, parent = None, width = 5, height = 5, dpi = 100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
 
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
 
        self.animate(self)
 
 
    def animate(self):                                                          

        self.ax = self.fig.add.subplot(111)

        ax.set_xlim(0,25)
        ax.set_ylim(0,25)


        animation = FuncAnimation(fig, func = animation_frame, frames = np.arange(0, 10, 0.01), interval = 10)
        self.canvas.draw()

    def animation_frame(self, t):
        x_data.append(v * np.cos(theta) * t)
        y_data.append(v * np.sin(theta) * t - (0.5) * g * (t)**2 + e)

        line.set_xdata(x_data)
        line.set_ydata(y_data)
        return line,




 
 
 
 
app = QApplication(sys.argv)
window = Window()
window.show()
app.exec()