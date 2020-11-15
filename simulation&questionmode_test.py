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

def CalcXYPosition(velo,anglep,elev,time):
    anginr = (np.pi/180)*anglep
    e = elev
    t = time
    ux = velo*np.cos(anginr)
    sx = ux*t
    uy = velo*np.sin(anginr)
    sy = (uy * t) + (0.5 * -g * t**2) + e
    roundedsx = round(sx, 2)
    roundedsy = round(sy, 2)
    return roundedsx, roundedsy

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
        self.windowbutton.pressed.connect(self.switch_mode)

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

        self.sim_widget = QWidget()
        self.sim_widget.setLayout(main_layout)

        select_layout = QHBoxLayout()
        input_layout = QVBoxLayout()
        ans_layout = QHBoxLayout()
        interface_layout = QVBoxLayout()
        whole_layout = QHBoxLayout()

        graph_layout = QVBoxLayout()

        self.selectgvalue = QPushButton("Select G Value")

        self.selectlabel = QLabel("Select A Target Value")
        self.selectlabel.setAlignment(Qt.AlignCenter)
        self.selectrange = QPushButton("Range")
        self.selectmaxheight = QPushButton("Max Height")
        self.selecttimetaken = QPushButton("Time Taken")
        self.selectinitvelo = QPushButton("Initial Velocity")
        self.selectang = QPushButton("Angle of Projection")
        self.selectgivenvelocity = QPushButton("Velocity at given time")
        self.selectxypos = QPushButton("X & Y Position")
        self.selectdirec = QPushButton("Angle of flight")

        self.veloinp = QLineEdit(self)
        self.velolabel = QLabel("Enter your velocity:")
        self.angleinp = QLineEdit(self)
        self.anglelabel = QLabel("Enter your angle:")
        self.elevinp = QLineEdit(self)
        self.elevlabel = QLabel("Enter your elevation:")
        self.timeinp = QLineEdit(self)
        self.timelabel = QLabel("Enter your time:")
        self.ansinp = QLineEdit(self)
        self.anslabel = QLabel("Enter your answer:")

        self.correctans = QLabel("Correct")
        self.falseans = QLabel("False")
        self.ansdisplay_widget = QStackedWidget()

        self.checkbuttR = QPushButton("Check Range")
        self.checkbuttH = QPushButton("Check Max Height")
        self.checkbuttT = QPushButton("Check Time Taken")
        self.checkbuttXY = QPushButton("Check XY Position")
        self.multicheck_widget = QStackedWidget()

        self.figure = Figure(figsize=(5,5),dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.animbutton = QPushButton("Start")
        self.animbutton.pressed.connect(self.animate)

        select_layout.addWidget(self.selectrange)
        select_layout.addWidget(self.selectmaxheight)
        select_layout.addWidget(self.selecttimetaken)
        select_layout.addWidget(self.selectxypos)

        input_layout.addWidget(self.velolabel)
        input_layout.addWidget(self.veloinp)
        input_layout.addWidget(self.anglelabel)
        input_layout.addWidget(self.angleinp)
        input_layout.addWidget(self.elevlabel)
        input_layout.addWidget(self.elevinp)
        input_layout.addWidget(self.timelabel)
        input_layout.addWidget(self.timeinp)

        ans_layout.addWidget(self.anslabel)
        ans_layout.addWidget(self.ansinp)
        
        self.selectgvalue.pressed.connect(self.showgvalue)

        self.ansdisplay_widget.addWidget(self.correctans)
        self.ansdisplay_widget.addWidget(self.falseans)
        ans_layout.addWidget(self.ansdisplay_widget)
        self.ansdisplay_widget.hide()

        self.multicheck_widget.addWidget(self.checkbuttR)
        self.multicheck_widget.addWidget(self.checkbuttH)
        self.multicheck_widget.addWidget(self.checkbuttT)
        self.multicheck_widget.addWidget(self.checkbuttXY)
        self.multicheck_widget.show()

        self.selectrange.pressed.connect(self.choose_range)
        self.selectmaxheight.pressed.connect(self.choose_maxheight)
        self.selecttimetaken.pressed.connect(self.choose_timetaken)
        self.selectxypos.pressed.connect(self.choose_xypos)

        self.veloinp.editingFinished.connect(self.input_velocity)
        self.angleinp.editingFinished.connect(self.input_angle)
        self.elevinp.editingFinished.connect(self.input_elevation)
        self.timeinp.editingFinished.connect(self.input_time)

        self.checkbuttR.pressed.connect(self.check_rangeans)
        self.checkbuttH.pressed.connect(self.check_maxheightans)
        self.checkbuttT.pressed.connect(self.check_timetakenans)
        self.checkbuttXY.pressed.connect(self.check_xypos)

        interface_layout.addWidget(self.selectgvalue)
        interface_layout.addWidget(self.selectlabel)
        interface_layout.addLayout(select_layout)
        interface_layout.addLayout(input_layout)
        interface_layout.addLayout(ans_layout)
        interface_layout.addWidget(self.multicheck_widget)

        whole_layout.addLayout(interface_layout)
        whole_layout.addWidget(self.canvas)

        self.que_widget = QWidget()
        self.que_widget.setLayout(whole_layout)

        self.main_widget = QStackedWidget()
        self.main_widget.addWidget(self.sim_widget)
        self.main_widget.addWidget(self.que_widget)

        self.setCentralWidget(self.main_widget)

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
    
    def switch_mode(self):
        self.main_widget.setCurrentWidget(self.que_widget)
        self.setWindowTitle("Question Mode")

    def input_velocity(self):
        calclist[0] = float(self.veloinp.text())

    def input_angle(self):
        calclist[1] = float(self.anglespin.text())

    def input_elevation(self):
        calclist[2] = float(self.elevinp.text())
        rounded_elev = round(float(self.elevinp.text()), 0)
        self.elevslider.setValue(int(rounded_elev))

    def input_time(self):
        calclist[3] = float(self.timeinp.text())
    
    def get_elevation(self):
        elevation = str(self.elevslider.value())
        self.elevinp.setText(elevation)
    
    def display_range_time(self):
        self.rangedisplay.setText(f'Final Range: {str(CalcRange(calclist[0], calclist[1], calclist[2]))}')
        self.timedisplay.setText(f'Final Time Taken: {str(CalcTimeTaken(calclist[0], calclist[1], calclist[2]))}')
    
    def showgvalue(self):
        gdialog = QDialog()
        g_layout = QHBoxLayout()
        self.nineeightcheck = QCheckBox()
        self.nineeightlabel = QLabel("9.8")
        self.nineeightonecheck = QCheckBox()
        self.nineeightonelabel = QLabel("9.81")
        self.customginput = QLineEdit(self)
        self.customglabel = QLabel("Enter a g value:")

        g_layout.addWidget(self.nineeightlabel)
        g_layout.addWidget(self.nineeightcheck)
        g_layout.addWidget(self.nineeightonelabel)
        g_layout.addWidget(self.nineeightonecheck)
        g_layout.addWidget(self.customglabel)
        g_layout.addWidget(self.customginput)

        gdialog.setWindowTitle("Change g value")
        gdialog.setLayout(g_layout)
        gdialog.exec_()
    
    def setgvalue(self):
        if self.nineeightcheck.isChecked == True:
            g = 9.8
        if self.nineeightcheck.isChecked == True:
            g = 9.81
        if self.nineeightcheck.isChecked == True:
            g = self.customginput.text()
    
    def calculate_range(self):
        CalcRange(calclist[0], calclist[1], calclist[2])
    
    def check_rangeans(self):
        if float(self.ansinp.text()) == CalcRange(calclist[0], calclist[1], calclist[2]):
            self.ansdisplay_widget.setCurrentWidget(self.correctans)
            self.ansdisplay_widget.show()
            self.animate()
        else:
            self.ansdisplay_widget.setCurrentWidget(self.falseans)
            self.ansdisplay_widget.show()
    
    def calculate_maxheight(self):
        CalcMaxHeight(calclist[0], calclist[1], calclist[2])

    def check_maxheightans(self):
        if float(self.ansinp.text()) == CalcMaxHeight(calclist[0], calclist[1], calclist[2]):
            self.ansdisplay_widget.setCurrentWidget(self.correctans)
            self.ansdisplay_widget.show()
            self.animate()
        else:
            self.ansdisplay_widget.setCurrentWidget(self.falseans)
            self.ansdisplay_widget.show()

    def calculate_timetaken(self):
        CalcTimeTaken(calclist[0], calclist[1], calclist[2])

    def check_timetakenans(self):
        if float(self.ansinp.text()) == CalcTimeTaken(calclist[0], calclist[1], calclist[2]):
            self.ansdisplay_widget.setCurrentWidget(self.correctans)
            self.ansdisplay_widget.show()
            self.animate()
        else:
            self.ansdisplay_widget.setCurrentWidget(self.falseans)
            self.ansdisplay_widget.show()

    def calculate_xypos(self):
        CalcXYPosition(calclist[0], calclist[1], calclist[2], calclist[3])

    def check_xypos(self):
        if float(self.ansinp.text()) == CalcXYPosition(calclist[0], calclist[1], calclist[2], calclist[3]):
            self.ansdisplay_widget.setCurrentWidget(self.correctans)
            self.ansdisplay_widget.show()
            self.animate()
        else:
            self.ansdisplay_widget.setCurrentWidget(self.falseans)
            self.ansdisplay_widget.show()
    
    def choose_range(self):
        self.multicheck_widget.setCurrentWidget(self.checkbuttR)
        self.multicheck_widget.show()

    def choose_maxheight(self):
        self.multicheck_widget.setCurrentWidget(self.checkbuttH)
        self.multicheck_widget.show()

    def choose_timetaken(self):
        self.multicheck_widget.setCurrentWidget(self.checkbuttT)
        self.multicheck_widget.show()

    def choose_xypos(self):
        self.multicheck_widget.setCurrentWidget(self.checkbuttXY)
        self.multicheck_widget.show()

def main():
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()