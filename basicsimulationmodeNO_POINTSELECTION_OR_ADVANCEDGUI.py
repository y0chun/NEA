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

        main_layout = QVBoxLayout()
        slider_layout = QHBoxLayout()
        graph_layout = QVBoxLayout()
        input_layout = QVBoxLayout()

        self.veloinp = QLineEdit(self)
        self.velolabel = QLabel("Enter your velocity:")
        self.angleinp = QLineEdit(self)
        self.anglelabel = QLabel("Enter your angle:")
        self.elevinp = QLineEdit(self)
        self.elevlabel = QLabel("Enter your elevation:")
 
        self.figure = Figure(figsize=(5,10),dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.animbutton = QPushButton('Animate')
        self.animbutton.pressed.connect(self.animate)

        graph_layout.addWidget(self.canvas)
        graph_layout.addWidget(self.animbutton)

        input_layout.addWidget(self.velolabel)
        input_layout.addWidget(self.veloinp)
        input_layout.addWidget(self.anglelabel)
        input_layout.addWidget(self.angleinp)
        input_layout.addWidget(self.elevlabel)
        input_layout.addWidget(self.elevinp)


        main_layout.addLayout(graph_layout)
        main_layout.addLayout(input_layout)
        
        widget = QWidget()
        widget.setLayout(main_layout)
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
        self.circle.center=(float(self.veloinp.text()) * np.cos((np.pi/180)*float(self.angleinp.text())) * t, float(self.veloinp.text()) * np.sin((np.pi/180)*float(self.angleinp.text())) * t - (0.5) * g * (t)**2 + float(self.elevinp.text()))
        return self.circle, 

def main():
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()