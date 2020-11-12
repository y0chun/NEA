import sys
import numpy as np

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import matplotlib.animation as animation
from matplotlib.figure import Figure

v = 10
ap = 40
e = 0
g = 9.8                                                                                                             
theta = (np.pi/180)*ap     

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__( *args, **kwargs)

        self.setWindowTitle("Simulation Mode")

        self.fig = Figure(figsize=(8,8),dpi=100)
        self.canvas = FigureCanvas(self.fig)
        #self.toolbar = NavigationToolbar(self.canvas, self)

        button = QPushButton('Animate')
        button.pressed.connect(self.animate)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)


    def animate(self):
        self.ax = self.fig.add_subplot(111)  # create an axis
        self.ax.cla()  # discards the old graph
        self.circle = Circle((0,0), 0.3) # circle radius 0.3 set at point 0,0
        self.ax.add_artist(self.circle) # adds the circle to the axis
        self.ax.set_xlim([0,30]) # x and y limits set
        self.ax.set_ylim([0,30])

        self.animation = animation.FuncAnimation(self.fig,self.animate_loop,frames=np.arange(0, 10, 0.01),interval=10) # 
        self.canvas.draw()
    
    def animate_loop(self,t):
        self.circle.center=(v * np.cos(theta) * t, v * np.sin(theta) * t - (0.5) * g * (t)**2 + e) #sets circle centre with the given x and y positions (in this case the projectile equations for x and y position)
        return self.circle, 

def main():
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()