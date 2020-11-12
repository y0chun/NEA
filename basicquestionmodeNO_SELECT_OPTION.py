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
g = 9.81
dt = 0.01

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

def CalcMaxHeight(velo,anglep,elev):
    anginr = (np.pi/180)*anglep
    uy = velo*np.sin(anginr)
    e = elev
    hmax = ((uy**2/(2*g))) + e
    roundedhmax = round(hmax, 2)
    return roundedhmax

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

        self.setWindowTitle("Question Mode")

        range_layout = QVBoxLayout()
        height_layout = QVBoxLayout()
        time_layout = QVBoxLayout()

        ans_layout = QHBoxLayout()
        inputANDans_layout = QVBoxLayout()

        self.veloinp = QLineEdit(self)
        self.velolabel = QLabel("Enter your velocity:")
        self.angleinp = QLineEdit(self)
        self.anglelabel = QLabel("Enter your angle:")
        self.elevinp = QLineEdit(self)
        self.elevlabel = QLabel("Enter your elevation:")
        self.ansinp = QLineEdit(self)
        self.anslabel = QLabel("Enter your answer for the range:")

        self.correctans = QLabel("Correct")
        self.falseans = QLabel("False")
        self.stackedwidget = QStackedWidget()

        self.checkbutt1 = QPushButton("Check Range Answer")
        self.confbutt2 = QPushButton("Confirm Max Height")
        self.confbutt3 = QPushButton("Confirm Time Taken")

        range_layout.addWidget(self.velolabel)
        range_layout.addWidget(self.veloinp)
        range_layout.addWidget(self.anglelabel)
        range_layout.addWidget(self.angleinp)
        range_layout.addWidget(self.elevlabel)
        range_layout.addWidget(self.elevinp)

        height_layout.addWidget(self.velolabel)
        height_layout.addWidget(self.veloinp)
        height_layout.addWidget(self.anglelabel)
        height_layout.addWidget(self.angleinp)
        height_layout.addWidget(self.elevlabel)
        height_layout.addWidget(self.elevinp)

        time_layout.addWidget(self.velolabel)
        time_layout.addWidget(self.veloinp)
        time_layout.addWidget(self.anglelabel)
        time_layout.addWidget(self.angleinp)
        time_layout.addWidget(self.elevlabel)
        time_layout.addWidget(self.elevinp)

        ans_layout.addWidget(self.anslabel)
        ans_layout.addWidget(self.ansinp)
        
        self.stackedwidget.addWidget(self.correctans)
        self.stackedwidget.addWidget(self.falseans)
        ans_layout.addWidget(self.stackedwidget)
        self.stackedwidget.hide()

        ans_layout.addLayout(inputANDans_layout)
        range_layout.addLayout(ans_layout)
        height_layout.addLayout(ans_layout)
        time_layout.addLayout(ans_layout)

        range_layout.addWidget(self.checkbutt1)
        height_layout.addWidget(self.confbutt2)
        time_layout.addWidget(self.confbutt3)
        
        self.veloinp.editingFinished.connect(self.input_velocity)
        self.angleinp.editingFinished.connect(self.input_angle)
        self.elevinp.editingFinished.connect(self.input_elevation)
        self.checkbutt1.pressed.connect(self.check_rangeans)
        self.confbutt2.pressed.connect(self.calculate_maxheight)
        self.confbutt3.pressed.connect(self.calculate_time)

        widget = QWidget()
        widget.setLayout(range_layout)
        self.setCentralWidget(widget)

    def input_velocity(self):
        calclist[0] = float(self.veloinp.text())

    def input_angle(self):
        calclist[1] = float(self.angleinp.text())

    def input_elevation(self):
        calclist[2] = float(self.elevinp.text())
    
    def calculate_range(self):
        CalcRange(calclist[0], calclist[1], calclist[2])
    
    def check_rangeans(self):
        if float(self.ansinp.text()) == CalcRange(calclist[0], calclist[1], calclist[2]):
            self.stackedwidget.setCurrentWidget(self.correctans)
            self.stackedwidget.show()
        else:
            self.stackedwidget.setCurrentWidget(self.falseans)
            self.stackedwidget.show()

    
    def calculate_maxheight(self):
        CalcMaxHeight(calclist[0], calclist[1], calclist[2])

    def check_maxheightans(self):
        if float(self.ansinp.text()) == CalcMaxHeight(calclist[0], calclist[1], calclist[2]):
            self.stackedwidget.setCurrentWidget(self.correctans)
            self.stackedwidget.show()
        else:
            self.stackedwidget.setCurrentWidget(self.falseans)
            self.stackedwidget.show()

    def calculate_time(self):
        CalcTimeTaken(calclist[0], calclist[1], calclist[2])

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