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

calclist = [0,0,0]
g = 9.8        

def CalcRange(velo,anglep,elev):
    anginr = (np.pi/180)*anglep
    a = -g/2
    b = velo*np.sin(anginr)
    c = elev
    ux = velo*np.cos(anginr)
    t = (-b-math.sqrt(b**2-4*a*c)) / (2 * a)
    sx= ux*t
    roundedsx = round(sx, 2)
    return roundedsx

def CalcTimeTaken(velo,anglep,elev):
    anginr = (np.pi/180)*anglep
    a = -g/2
    b = velo*np.sin(anginr)
    c = elev
    time = (-b-math.sqrt(b**2-4*a*c)) / (2 * a)
    roundedtime = round(time, 2)
    return roundedtime

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__( *args, **kwargs)

        self.setWindowTitle("Simulation Mode")

        main_layout = QVBoxLayout()
        header_layout = QHBoxLayout()
        simdisplay_layout = QVBoxLayout()
        slider_layout = QHBoxLayout()
        graph_layout = QVBoxLayout()
        input_layout = QVBoxLayout()

        self.windowbutton = QPushButton("Switch to Question Mode")
        #self.windowbutton.pressed.connect()

        self.rangedisplay = QLabel("Final Range: ")
        self.timedisplay = QLabel("Final Time Taken: ")

        self.veloinp = QLineEdit(self)
        self.velolabel = QLabel("Enter your velocity:")
        self.anglespin = QDoubleSpinBox(cleanText = None, decimals = 2, maximum = 90, minimum = 0, prefix = None, singleStep = 1, stepType = None, suffix = None, value = 0)
        self.anglelabel = QLabel("Enter your angle:")
        self.elevinp = QLineEdit(self)
        self.elevlabel = QLabel("Enter your elevation:")

        self.elevslider = QSlider(Qt.Vertical)
        self.elevslider.setMinimum(0)
        self.elevslider.setMaximum(100)
        self.elevslider.setSingleStep(1)
        self.elevslider.sliderReleased.connect(self.get_elevation)
        
        self.sliderlabel = QGraphicsScene(self)
        self.sliderlabel.addText("Adjust elevation") 
        self.view = QGraphicsView(self.sliderlabel)
        self.view.rotate(270)
        self.view.show()

        self.figure = Figure(figsize=(5,10),dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.animbutton = QPushButton("Start")
        self.animbutton.pressed.connect(self.animate)
        self.animbutton.pressed.connect(self.display_range_time)

        simdisplay_layout.addWidget(self.rangedisplay)
        simdisplay_layout.addWidget(self.timedisplay)
        simdisplay_layout.setAlignment(Qt.AlignRight)

        header_layout.addWidget(self.windowbutton)
        header_layout.addLayout(simdisplay_layout)

        slider_layout.addWidget(self.view)
        slider_layout.addWidget(self.elevslider)
        slider_layout.addWidget(self.canvas)

        graph_layout.addLayout(slider_layout)
        graph_layout.addWidget(self.animbutton)

        input_layout.addWidget(self.velolabel)
        input_layout.addWidget(self.veloinp)
        input_layout.addWidget(self.anglelabel)
        input_layout.addWidget(self.anglespin)
        input_layout.addWidget(self.elevlabel)
        input_layout.addWidget(self.elevinp)

        main_layout.addLayout(header_layout)
        main_layout.addLayout(graph_layout)
        main_layout.addLayout(input_layout)

        self.veloinp.editingFinished.connect(self.input_velocity)
        self.anglespin.editingFinished.connect(self.input_angle)
        self.elevinp.editingFinished.connect(self.input_elevation)
        
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

    def animate(self):
        try:
            self.cl = self.figure.clf()
            self.ax = self.figure.add_subplot()
            self.circle = Circle((0,0), 0.3) 
            self.ax.add_artist(self.circle) 
            self.ax.set_xlim([0,30]) 
            self.ax.set_ylim([0,30])
            self.animation = animation.FuncAnimation(self.figure,self.animate_loop,frames=np.arange(0, CalcTimeTaken(float(self.veloinp.text()), float(self.anglespin.text()), float(self.elevinp.text())), 0.01),interval=10,repeat=False) 
            self.canvas.draw()
        except:
            print("Error")
    
    def animate_loop(self,t):
        self.circle.center=(float(self.veloinp.text()) * np.cos((np.pi/180)*float(self.anglespin.text())) * t, float(self.veloinp.text()) * np.sin((np.pi/180)*float(self.anglespin.text())) * t - (0.5) * g * (t)**2 + float(self.elevinp.text()))
        return self.circle

    def input_velocity(self):
        calclist[0] = float(self.veloinp.text())

    def input_angle(self):
        calclist[1] = float(self.anglespin.text())

    def input_elevation(self):
        calclist[2] = float(self.elevinp.text())
    
    def get_elevation(self):
        elevation = str(self.elevslider.value())
        self.elevinp.setText(elevation)
    
    def display_range_time(self):
        self.rangedisplay.setText(f'Final Range: {str(CalcRange(calclist[0], calclist[1], calclist[2]))}')
        self.timedisplay.setText(f'Final Time Taken: {str(CalcTimeTaken(calclist[0], calclist[1], calclist[2]))}')

def main():
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()