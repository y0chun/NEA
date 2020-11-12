import sys
import numpy as np
import math

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import matplotlib.animation as animation
from matplotlib.figure import Figure

g = 9.8                                                                                                              

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__( *args, **kwargs)

        self.setWindowTitle("Simulation Mode")

        layout1 = QVBoxLayout()
        layout2 = QVBoxLayout()

        self.veloinp = QLineEdit(self)
        self.velolabel = QLabel("Enter your velocity:")
        self.angleinp = QLineEdit(self)
        self.anglelabel = QLabel("Enter your angle:")
        self.elevinp = QLineEdit(self)
        self.elevlabel = QLabel("Enter your elevation:")

        self.figure = Figure(figsize=(5,10),dpi=100)
        self.canvas = FigureCanvas(self.figure)
        animbutton = QPushButton('Animate')
        animbutton.pressed.connect(self.animate)

        layout1.addWidget(self.canvas)
        layout1.addWidget(animbutton)
        layout2.addWidget(self.velolabel)
        layout2.addWidget(self.veloinp)
        layout2.addWidget(self.anglelabel)
        layout2.addWidget(self.angleinp)
        layout2.addWidget(self.elevlabel)
        layout2.addWidget(self.elevinp)

        layout1.addLayout(layout2)
        
        widget = QWidget()
        widget.setLayout(layout1)
        self.setCentralWidget(widget)


    def animate(self):
        self.ax = self.figure.add_subplot()
        self.ax.cla() 
        self.circle = Circle((0,0), 0.3) 
        self.ax.add_artist(self.circle) 
        self.ax.set_xlim([0,30]) 
        self.ax.set_ylim([0,30])

        self.animation = animation.FuncAnimation(self.figure,self.animate_loop,frames=np.arange(0, 10, 0.01),interval=10) 
        self.canvas.draw()
    
    def animate_loop(self,t):
        self.circle.center=(int(self.veloinp.text()) * np.cos((np.pi/180)*int(self.angleinp.text())) * t, int(self.veloinp.text()) * np.sin((np.pi/180)*int(self.angleinp.text())) * t - (0.5) * g * (t)**2 + int(self.elevinp.text()))
        return self.circle, 

def main():
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()