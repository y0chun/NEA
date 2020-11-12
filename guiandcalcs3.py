import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sys

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
    print(f"The range is: {roundedsx}m")

def CalcMaxHeight(velo,anglep,elev):
    anginr = (np.pi/180)*anglep
    uy = velo*np.sin(anginr)
    e = elev
    hmax = ((uy**2/(2*g))) + e
    roundedhmax = round(hmax, 2)
    print(f"The maximum height is: {roundedhmax}m")

def CalcTimeTaken(velo,anglep,elev):
    anginr = (np.pi/180)*anglep
    a = -g/2
    b = velo*np.sin(anginr)
    c = elev
    time = (-b-math.sqrt(b**2-4*a*c)) / (2 * a)
    roundedtime = round(time, 2)
    print(f"The time taken is: {roundedtime}m")

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        self.setWindowTitle("Question Mode")
        
        
        layout1 = QVBoxLayout()
        layout2 = QHBoxLayout()

        self.veloinp = QLineEdit(self)
        self.velolabel = QLabel("Enter your velocity:")
        self.angleinp = QLineEdit(self)
        self.anglelabel = QLabel("Enter your angle:")
        self.elevinp = QLineEdit(self)
        self.elevlabel = QLabel("Enter your elevation:")
        self.confbutt1 = QPushButton("Confirm Range")
        self.confbutt2 = QPushButton("Confirm Max Height")
        self.confbutt3 = QPushButton("Confirm Time Taken")

        layout1.addWidget(self.velolabel)
        layout1.addWidget(self.veloinp)
        layout1.addWidget(self.anglelabel)
        layout1.addWidget(self.angleinp)
        layout1.addWidget(self.elevlabel)
        layout1.addWidget(self.elevinp)
        layout2.addWidget(self.confbutt1)
        layout2.addWidget(self.confbutt2)
        layout2.addWidget(self.confbutt3)
        layout1.addLayout(layout2)
        
        self.veloinp.editingFinished.connect(self.input_velocity)
        self.angleinp.editingFinished.connect(self.input_angle)
        self.elevinp.editingFinished.connect(self.input_elevation)
        self.confbutt1.pressed.connect(self.calculate_range)
        self.confbutt2.pressed.connect(self.calculate_maxheight)
        self.confbutt3.pressed.connect(self.calculate_time)

        widget = QWidget()
        widget.setLayout(layout1)
        self.setCentralWidget(widget)

    
    def input_velocity(self):
        calclist[0] = int(self.veloinp.text())

    def input_angle(self):
        calclist[1] = int(self.angleinp.text())

    def input_elevation(self):
        calclist[2] = int(self.elevinp.text())
    
    def calculate_range(self):
        CalcRange(calclist[0], calclist[1], calclist[2])
    
    def calculate_maxheight(self):
        CalcMaxHeight(calclist[0], calclist[1], calclist[2])

    def calculate_time(self):
        CalcTimeTaken(calclist[0], calclist[1], calclist[2])

    
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()