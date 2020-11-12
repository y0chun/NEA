import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sys

calclist = []

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

        widget1 = QInputDialog()
        label1 = widget1.setLabelText("Enter your velocity:")
        widget2 = QInputDialog()
        label2 = widget2.setLabelText("Enter your angle:")
        widget3 = QInputDialog()
        label3 = widget3.setLabelText("Enter your elevation:")

        layout1.addWidget(label1)
        layout1.addWidget(widget1)
        layout1.addWidget(label2)
        layout1.addWidget(widget2)
        layout1.addWidget(label3)
        layout1.addWidget(widget3)
        
        widget1.textValueSelected.connect(self.textvalue_selected1)
        widget2.textValueSelected.connect(self.textvalue_selected2)
        widget3.textValueSelected.connect(self.textvalue_selected3)

        widget = QWidget()
        widget.setLayout(layout1)
        self.setCentralWidget(widget)

    
    def textvalue_selected1(self, v):
        calclist.append(int(v))

    def textvalue_selected2(self, a):
        calclist.append(int(a))

    def textvalue_selected3(self, e):
        calclist.append(int(e))
        CalcRange(calclist[1], calclist[2], calclist[3])

app = QApplication(sys.argv)

window = MainWindow()
window.show() # IMPORTANT!!!!! Windows are hidden by default.

# Start the event loop.
app.exec_()

