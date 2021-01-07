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

        self.is_sim_mode = True

        self.setWindowTitle("Simulation Mode")

        main_layout = QVBoxLayout()
        header_layout = QHBoxLayout()
        simdisplay_layout = QVBoxLayout()
        slider_layout = QHBoxLayout()
        graph_layout = QVBoxLayout()
        input_layout = QVBoxLayout()

        self.qwindowbutton = QPushButton("Switch to Question Mode")
        self.qwindowbutton.pressed.connect(self.switch_mode)

        self.rangedisplay = QLabel("Final Range: ")
        self.timedisplay = QLabel("Final Time Taken: ")

        self.veloinp_sm = QLineEdit(self)
        self.velolabel_sm = QLabel("Enter your velocity:")
        self.anglespin_sm = QDoubleSpinBox(cleanText = None, decimals = 2, maximum = 90, minimum = 0, prefix = None, singleStep = 1, stepType = None, suffix = None, value = 0)
        self.anglelabel_sm = QLabel("Enter your angle:")
        self.elevinp_sm = QLineEdit(self)
        self.elevlabel_sm = QLabel("Enter your elevation:")

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

        self.figure_sm = Figure(figsize=(5,10),dpi=100)
        self.canvas_sm = FigureCanvas(self.figure_sm)
        
        self.animbutton = QPushButton("Start")
        self.animbutton.pressed.connect(self.final_graph)
        self.animbutton.pressed.connect(self.display_range_time)

        simdisplay_layout.addWidget(self.rangedisplay)
        simdisplay_layout.addWidget(self.timedisplay)
        simdisplay_layout.setAlignment(Qt.AlignRight)

        header_layout.addWidget(self.qwindowbutton)
        header_layout.addLayout(simdisplay_layout)

        slider_layout.addWidget(self.view)
        slider_layout.addWidget(self.elevslider)
        slider_layout.addWidget(self.canvas_sm)

        graph_layout.addLayout(slider_layout)
        graph_layout.addWidget(self.animbutton)

        input_layout.addWidget(self.velolabel_sm)
        input_layout.addWidget(self.veloinp_sm)
        input_layout.addWidget(self.anglelabel_sm)
        input_layout.addWidget(self.anglespin_sm)
        input_layout.addWidget(self.elevlabel_sm)
        input_layout.addWidget(self.elevinp_sm)

        main_layout.addLayout(header_layout)
        main_layout.addLayout(graph_layout)
        main_layout.addLayout(input_layout)

        self.veloinp_sm.editingFinished.connect(self.input_velocity)
        self.anglespin_sm.editingFinished.connect(self.input_angle)
        self.elevinp_sm.editingFinished.connect(self.input_elevation)

        self.sim_widget = QWidget()
        self.sim_widget.setLayout(main_layout)

        select_layout = QHBoxLayout()
        input_layout = QVBoxLayout()
        ans_layout = QHBoxLayout()
        interface_layout = QVBoxLayout()
        whole_layout = QHBoxLayout()

        graph_layout = QVBoxLayout()

        self.selectgvalue = QPushButton("Select G Value")
        self.swindowbutton = QPushButton("Switch to Simulation Mode")
        self.swindowbutton.pressed.connect(self.switch_mode)

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

        self.veloinp_qm = QLineEdit(self)
        self.velolabel_qm = QLabel("Enter your velocity:")
        self.angleinp_qm = QLineEdit(self)
        self.anglelabel_qm = QLabel("Enter your angle:")
        self.elevinp_qm = QLineEdit(self)
        self.elevlabel_qm = QLabel("Enter your elevation:")
        self.timeinp_qm = QLineEdit(self)
        self.timelabel_qm = QLabel("Enter your time:")
        self.ansinp_qm = QLineEdit(self)
        self.anslabel_qm = QLabel("Enter your answer:")

        self.figure_qm = Figure(figsize=(5,10),dpi=100)
        self.canvas_qm = FigureCanvas(self.figure_qm)

        self.correctans = QLabel("Correct")
        self.falseans = QLabel("False")
        self.ansdisplay_widget = QStackedWidget()

        self.checkbuttR = QPushButton("Check Range")
        self.checkbuttH = QPushButton("Check Max Height")
        self.checkbuttT = QPushButton("Check Time Taken")
        self.checkbuttXY = QPushButton("Check XY Position")
        self.multicheck_widget = QStackedWidget()

        select_layout.addWidget(self.selectrange)
        select_layout.addWidget(self.selectmaxheight)
        select_layout.addWidget(self.selecttimetaken)
        select_layout.addWidget(self.selectxypos)

        input_layout.addWidget(self.velolabel_qm)
        input_layout.addWidget(self.veloinp_qm)
        input_layout.addWidget(self.anglelabel_qm)
        input_layout.addWidget(self.angleinp_qm)
        input_layout.addWidget(self.elevlabel_qm)
        input_layout.addWidget(self.elevinp_qm)
        input_layout.addWidget(self.timelabel_qm)
        input_layout.addWidget(self.timeinp_qm)

        ans_layout.addWidget(self.anslabel_qm)
        ans_layout.addWidget(self.ansinp_qm)
        
        #self.selectgvalue.pressed.connect(self.showgvalue)

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

        self.veloinp_qm.editingFinished.connect(self.input_velocity)
        self.angleinp_qm.editingFinished.connect(self.input_angle)
        self.elevinp_qm.editingFinished.connect(self.input_elevation)
        self.timeinp_qm.editingFinished.connect(self.input_time)

        self.checkbuttR.pressed.connect(self.check_rangeans)
        self.checkbuttH.pressed.connect(self.check_maxheightans)
        self.checkbuttT.pressed.connect(self.check_timetakenans)
        self.checkbuttXY.pressed.connect(self.check_xypos)

        interface_layout.addWidget(self.selectgvalue)
        interface_layout.addWidget(self.swindowbutton)
        interface_layout.addWidget(self.selectlabel)
        interface_layout.addLayout(select_layout)
        interface_layout.addLayout(input_layout)
        interface_layout.addLayout(ans_layout)
        interface_layout.addWidget(self.multicheck_widget)

        whole_layout.addLayout(interface_layout)
        whole_layout.addWidget(self.canvas_qm)

        self.que_widget = QWidget()
        self.que_widget.setLayout(whole_layout)

        self.main_widget = QStackedWidget()
        self.main_widget.addWidget(self.sim_widget)
        self.main_widget.addWidget(self.que_widget)

        self.setCentralWidget(self.main_widget)

        self.figure_sm.canvas.mpl_connect('pick_event', onpick)

    def final_graph(self):
        self.figure_sm.clear()
        self.ax = self.figure_sm.add_subplot()
        t = np.linspace(0, CalcTimeTaken(calclist[0], calclist[1], calclist[2]), 75)
        line, = self.ax.plot((float(self.veloinp_sm.text()) * np.cos((np.pi/180)*float(self.anglespin_sm.text())) * t), (float(self.veloinp_sm.text()) * np.sin((np.pi/180)*float(self.anglespin_sm.text())) * t - (0.5) * g * (t)**2 + float(self.elevinp_sm.text())), 'b.', linewidth=1, pickradius=3)
        self.canvas_sm.draw() 

    def onpick(event):
        thisline = event.artist
        xdata = thisline.get_xdata()
        ydata = thisline.get_ydata()
        ind = event.ind
        xpoints = xdata[ind]
        ypoints = ydata[ind]
        print(round(xpoints[0],2), round(ypoints[0],2))

    def animate(self):
        if self.is_sim_mode == True:
            if CalcRange(calclist[0], calclist[1], calclist[2]) > CalcMaxHeight(calclist[0], calclist[1], calclist[2]):
                limit = CalcRange(calclist[0], calclist[1], calclist[2])
            else:
                limit = CalcMaxHeight(calclist[0], calclist[1], calclist[2])
            try:
                self.cl = self.figure_sm.clf()
                self.ax = self.figure_sm.add_subplot()
                self.circle = Circle((0,0), 0.3) 
                self.ax.add_artist(self.circle) 
                self.ax.set_xlim([0,limit+(limit*0.1)]) 
                self.ax.set_ylim([0,limit+(limit*0.1)])
                self.animation1 = animation.FuncAnimation(self.figure_sm,self.animate_loop_sm,frames=np.arange(0, CalcTimeTaken(float(self.veloinp_sm.text()), float(self.anglespin_sm.text()), float(self.elevinp_sm.text())), 0.01),interval=10,repeat=False)
                self.animation2 = animation.FuncAnimation(self.figure_sm,self.animate_trailloop_sm,frames=np.arange(0, CalcTimeTaken(float(self.veloinp_sm.text()), float(self.anglespin_sm.text()), float(self.elevinp_sm.text())),0.01),interval=10,repeat=False)
                self.canvas_sm.draw()
            except:
                print("Error")
        else:
            try:
                self.cl = self.figure_qm.clf()
                self.ax = self.figure_qm.add_subplot()
                self.circle = Circle((0,0), 0.3) 
                self.ax.add_artist(self.circle) 
                self.ax.set_xlim([0,limit]+(limit*0.1)) 
                self.ax.set_ylim([0,limit]+(limit*0.1))
                self.animation = animation.FuncAnimation(self.figure_qm,self.animate_loop_qm,frames=np.arange(0, CalcTimeTaken(float(self.veloinp_qm.text()), float(self.angleinp_qm.text()), float(self.elevinp_qm.text())), 0.01),interval=10,repeat=False)
                self.canvas_qm.draw()
            except:
                print("Error")
        
    def animate_loop_sm(self,t):
        self.circle.center=(float(self.veloinp_sm.text()) * np.cos((np.pi/180)*float(self.anglespin_sm.text())) * t, float(self.veloinp_sm.text()) * np.sin((np.pi/180)*float(self.anglespin_sm.text())) * t - (0.5) * g * (t)**2 + float(self.elevinp_sm.text()))
        return self.circle
    
    def animate_trailloop_sm(self,t):
        interval_t = round(t*100,0)
        ln, = self.ax.plot([], [], 'b.')
        xdata, ydata = [], []
        if interval_t % 5 == 0:
            xdata.append(float(self.veloinp_sm.text()) * np.cos((np.pi/180)*float(self.anglespin_sm.text())) * t)
            ydata.append(float(self.veloinp_sm.text()) * np.sin((np.pi/180)*float(self.anglespin_sm.text())) * t - (0.5) * g * (t)**2 + float(self.elevinp_sm.text()))
            ln.set_data(xdata, ydata)
            return ln,
            self.canvas_sm.show()
    
    def animate_loop_qm(self,t):
        self.circle.center=(float(self.veloinp_qm.text()) * np.cos((np.pi/180)*float(self.angleinp_qm.text())) * t, float(self.veloinp_qm.text()) * np.sin((np.pi/180)*float(self.angleinp_qm.text())) * t - (0.5) * g * (t)**2 + float(self.elevinp_qm.text()))
        return self.circle, 
    
    def switch_mode(self):
        if self.is_sim_mode == True:
            self.main_widget.setCurrentWidget(self.que_widget)
            self.setWindowTitle("Question Mode")
            self.is_sim_mode = False
        else:
            self.main_widget.setCurrentWidget(self.sim_widget)
            self.setWindowTitle("Simulation Mode")
            self.is_sim_mode = True

    def input_velocity(self):
        if self.is_sim_mode == True:
            calclist[0] = float(self.veloinp_sm.text())
        else:
            calclist[0] = float(self.veloinp_qm.text())

    def input_angle(self):
        if self.is_sim_mode == True:
            calclist[1] = float(self.anglespin_sm.text())
        else:
            calclist[1] = float(self.angleinp_qm.text())

    def input_elevation(self):
        if self.is_sim_mode == True:
            calclist[2] = float(self.elevinp_sm.text())
            rounded_elev = round(float(self.elevinp_sm.text()), 0)
            self.elevslider.setValue(int(rounded_elev))
        else:
            calclist[2] = float(self.elevinp_qm.text())

    def input_time(self):
        calclist[3] = float(self.timeinp_qm.text())
    
    def get_elevation(self):
        elevation = str(self.elevslider.value())
        self.elevinp_sm.setText(elevation)
        calclist[2] = float(self.elevinp_sm.text())
    
    def display_range_time(self):
        self.rangedisplay.setText(f'Final Range: {str(CalcRange(calclist[0], calclist[1], calclist[2]))}')
        self.timedisplay.setText(f'Final Time Taken: {str(CalcTimeTaken(calclist[0], calclist[1], calclist[2]))}')
    
    '''
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
    '''

    def calculate_range(self):
        CalcRange(calclist[0], calclist[1], calclist[2])
    
    def check_rangeans(self):
        if float(self.ansinp_qm.text()) == CalcRange(calclist[0], calclist[1], calclist[2]):
            self.ansdisplay_widget.setCurrentWidget(self.correctans)
            self.ansdisplay_widget.show()
            self.animate()
        else:
            self.ansdisplay_widget.setCurrentWidget(self.falseans)
            self.ansdisplay_widget.show()
    
    def calculate_maxheight(self):
        CalcMaxHeight(calclist[0], calclist[1], calclist[2])

    def check_maxheightans(self):
        if float(self.ansinp_qm.text()) == CalcMaxHeight(calclist[0], calclist[1], calclist[2]):
            self.ansdisplay_widget.setCurrentWidget(self.correctans)
            self.ansdisplay_widget.show()
            self.animate()
        else:
            self.ansdisplay_widget.setCurrentWidget(self.falseans)
            self.ansdisplay_widget.show()

    def calculate_timetaken(self):
        CalcTimeTaken(calclist[0], calclist[1], calclist[2])

    def check_timetakenans(self):
        if float(self.ansinp_qm.text()) == CalcTimeTaken(calclist[0], calclist[1], calclist[2]):
            self.ansdisplay_widget.setCurrentWidget(self.correctans)
            self.ansdisplay_widget.show()
            self.animate()
        else:
            self.ansdisplay_widget.setCurrentWidget(self.falseans)
            self.ansdisplay_widget.show()

    def calculate_xypos(self):
        CalcXYPosition(calclist[0], calclist[1], calclist[2], calclist[3])

    def check_xypos(self):
        if float(self.ansinp_qm.text()) == CalcXYPosition(calclist[0], calclist[1], calclist[2], calclist[3]):
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