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
        
        self.setWindowTitle("My App")
        
        layout1 = QVBoxLayout()

        veloinp = QInputDialog()
        velolabel = veloinp.setLabelText("Enter your velocity:")
        angleinp = QInputDialog()
        anglelabel = angleinp.setLabelText("Enter your angle:")
        elevinp = QInputDialog()
        elevlabel = elevinp.setLabelText("Enter your elevation:")
        confbutt = QPushButton("Confirm")

        layout1.addWidget(veloinp)
        layout1.addWidget(angleinp)
        layout1.addWidget(elevinp)
        layout1.addWidget(confbutt)
        
        veloinp.textValueSelected.connect(self.input_velocity)
        angleinp.textValueSelected.connect(self.input_angle)
        elevinp.textValueSelected.connect(self.input_elevation)
        confbutt.pressed.connect(self.calculate_range)

        widget = QWidget()
        widget.setLayout(layout1)
        self.setCentralWidget(widget)

    
    def input_velocity(self, v):
        calclist[0] = int(v)

    def input_angle(self, a):
        calclist[1] = int(a)

    def input_elevation(self, e):
        calclist[2] = int(e)
    
    def calculate_range(self):
        CalcRange(calclist[0], calclist[1], calclist[2])

    
app = QApplication(sys.argv)

window = MainWindow()
window.show() # IMPORTANT!!!!! Windows are hidden by default.

# Start the event loop.
app.exec_()