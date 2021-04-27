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

class MathsCalculations:
    def __init__(self, V, TH, E, T, G, X, Y, DP):
        self.velo = V
        self.anglep = TH
        self.elev = E
        self.time = T
        self.g = G
        self.xpos = X
        self.ypos = Y
        self.dp = DP

    def SetVelocity(self, n):
        self.velo = n
    
    def SetAngleOfProjection(self, n):
        self.anglep = n
    
    def SetElevation(self, n):
        self.elev = n

    def SetTime(self, n):
        self.time = n

    def SetXPosition(self, n):
        self.xpos = n
    
    def SetYPosition(self, n):
        self.ypos = n
    
    def SetGravFieldStrength(self, n):
        self.g = n
    
    def SetDecimalPoint(self,n):
        self.dp = n
        
    def GetVelocity(self):
        return self.velo
    
    def GetAngleOfProjection(self):
        return self.anglep
    
    def GetElevation(self):
        return self.elev
    
    def GetGravFieldStrength(self):
        return self.g
    
    def GetTime(self):
        return self.time

    def GetXPosition(self):
        return self.xpos
    
    def GetYPosition(self):
        return self.ypos

    def GetDecimalPoint(self):
        return self.dp

    def CalcRange(self,v,th,e):
        anginr = (np.pi/180)*self.anglep
        a = -(self.g)/2
        b = self.velo*np.sin(anginr)
        c = self.elev
        ux = self.velo*np.cos(anginr)
        t = (-b-math.sqrt(b**2-4*a*c)) / (2 * a)
        sx= ux*t
        roundedsx = round(sx, self.dp)
        return roundedsx

    def CalcMaxHeight(self,v,th,e):
        anginr = (np.pi/180)*self.anglep
        uy = self.velo*np.sin(anginr)
        e = self.elev
        hmax = ((uy**2/(2*self.g))) + e
        roundedhmax = round(hmax, self.dp)
        return roundedhmax

    def CalcTimeTaken(self,v,th,e):
        anginr = (np.pi/180)*self.anglep
        a = -(self.g)/2
        b = self.velo*np.sin(anginr)
        c = self.elev
        self.time = (-b-math.sqrt(b**2-4*a*c)) / (2 * a)
        roundedtime = round(self.time, self.dp)
        return roundedtime

    def CalcXYPosition(self,v,th,e,t):
        anginr = (np.pi/180)*self.anglep
        e = self.elev
        t = self.time
        ux = self.velo*np.cos(anginr)
        sx = ux*t
        uy = self.velo*np.sin(anginr)
        sy = (uy * t) + (0.5 * -(self.g) * t**2) + e
        roundedsx = round(sx, self.dp)
        roundedsy = round(sy, self.dp)
        return roundedsx, roundedsy
    
    def CalcVeloAndDirec(self,v,th,e,t):
        anginr = (np.pi/180)*self.anglep
        e = self.elev
        t = self.time
        ux = self.velo*np.cos(anginr)
        vx = ux
        uy = self.velo*np.sin(anginr)
        vy = uy + -self.g*t
        V = np.sqrt(vx**2 + vy**2)
        D = np.arctan(vy/vx) * 180/np.pi
        roundedV = round(V, self.dp)
        roundedD = round(D,self.dp)
        return roundedV, roundedD

    def CalcInitialVelocity(self,th,e,t,x,y):
        anginr = (np.pi/180)*anglep
        e = self.elev
        t = self.time
        sx = self.xpos
        sy = self.ypos
        if self.ypos == None:
            U = sx / (t*np.cos(anginr))
        if self.xpos == None:
            U = (sy - (-1/2*g*t**2)) / (t*np.sin(anginr))
        roundedU = round(U,self.dp)
        return roundedU

    def CalcAngleOfProjection(self,v,e,t,x,y):
        angind = 180/np.pi
        e = self.elev
        t = self.time
        sx = self.xpos
        sy = self.ypos
        if self.ypos == None:
            AOP = angind * np.arccos(sx / (velo * t))
        if self.xpos == None:
            AOP = angind * np.arcsin((sy - (-1/2*g*t**2)) / (velo * t))
        if self.ypos != None and self.xpos != None:
            AOP = angind * np.arccos(sx / (velo * t))
        roundedAOP = round(AOP,self.dp)
        return roundedAOP

class GDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setWindowTitle("G Value Selection")

        g_layout = QHBoxLayout()

        self.gnpebutt = QRadioButton("9.8")
        self.gnpeobutt = QRadioButton("9.81")

        self.ginp = QLineEdit(self)
        self.glabel = QLabel("Enter your g value:")
        self.gconfirm = QPushButton("Confirm")

        g_layout.addWidget(self.gnpebutt)
        g_layout.addWidget(self.gnpeobutt)
        g_layout.addWidget(self.glabel)
        g_layout.addWidget(self.ginp)
        g_layout.addWidget(self.gconfirm)

        self.gnpebutt.pressed.connect(self.set_npegvalue)
        self.gnpeobutt.pressed.connect(self.set_npeogvalue)
        self.ginp.editingFinished.connect(self.resetgbutt)
        self.gconfirm.pressed.connect(self.set_newgvalue)
        self.setLayout(g_layout)

    def set_newgvalue(self):
        MathsCalculations.SetGravFieldStrength(self,float(self.ginp.text()))

    def resetgbutt(self):
        self.gnpebutt.setChecked(False)
        self.gnpeobutt.setChecked(False)
    
    def set_npegvalue(self):
        MathsCalculations.SetGravFieldStrength(self,9.8)

    def set_npeogvalue(self):
        MathsCalculations.SetGravFieldStrength(self,9.81)

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__( *args, **kwargs)

        self.set_gvalue()
        self.is_sim_mode = True

        self.setWindowTitle("Simulation Mode")

        main_layout = QVBoxLayout()
        header_layout = QHBoxLayout()
        simdisplay_layout = QVBoxLayout()
        slider_layout = QHBoxLayout()
        graph_layout = QVBoxLayout()
        input_layout = QVBoxLayout()
        velocity_layout = QHBoxLayout()
        angle_layout = QHBoxLayout()
        elevation_layout = QHBoxLayout()
        bottom_layout = QHBoxLayout()

        self.qwindowbutton = QPushButton("Switch to Question Mode")
        self.qwindowbutton.pressed.connect(self.switch_mode)
        
        self.dpinp_sm = QLineEdit(self)
        self.dpinp_sm.setFixedSize(20,20)
        self.dplabel_sm = QLabel("Enter the amount of decimal places: ")
        self.dplabel_sm.setContentsMargins(20,0,0,0)

        self.gvaluebutton = QPushButton("Select G Value")
        self.gvaluebutton.pressed.connect(self.show_gdialog)

        self.rangedisplay = QLabel("Final Range: ")
        self.timedisplay = QLabel("Final Time Taken: ")

        self.veloinp_sm = QLineEdit(self)
        self.velolabel_sm = QLabel("Enter your velocity:")
        self.anglespin_sm = QDoubleSpinBox(cleanText = None, decimals = 2, maximum = 90, minimum = 0, prefix = None, singleStep = 1, stepType = None, suffix = None, value = 0)
        self.anglelabel_sm = QLabel("Enter your angle:")
        self.elevinp_sm = QLineEdit(self)
        self.elevlabel_sm = QLabel("Enter your elevation:")

        self.veloinp_sm.setFixedSize(60,20)
        self.anglespin_sm.setFixedSize(60,20)
        self.elevinp_sm.setFixedSize(60,20)

        self.elevslider = QSlider(Qt.Vertical)
        self.elevslider.setMinimum(0)
        self.elevslider.setMaximum(100)
        self.elevslider.setSingleStep(1)
        self.elevslider.sliderReleased.connect(self.get_elevation)
        
        self.sliderlabel = QGraphicsScene(self)
        self.sliderlabel.addText("Adjust elevation") 
        self.view = QGraphicsView(self.sliderlabel)
        self.view.setMaximumSize(40,100)
        self.view.rotate(270)
        self.view.show()

        self.figure_sm = Figure(figsize=(5,10),dpi=100)
        self.canvas_sm = FigureCanvas(self.figure_sm)
        self.canvas_sm.setFixedSize(480,480)

        start_layout = QVBoxLayout()
        
        self.animbutton = QPushButton("Start")
        self.switchgraph = QPushButton("Finalise")

        start_layout.addWidget(self.animbutton)
        start_layout.addWidget(self.switchgraph)

        self.animbutton.pressed.connect(self.animate)
        self.animbutton.pressed.connect(self.display_range_time)
        self.switchgraph.pressed.connect(self.final_graph)

        self.animbutton.setFixedSize(100,20)
        self.switchgraph.setFixedSize(100,20)

        simdisplay_layout.addWidget(self.rangedisplay)
        simdisplay_layout.addWidget(self.timedisplay)
        simdisplay_layout.addWidget(self.gvaluebutton)
        simdisplay_layout.setContentsMargins(25,0,0,0)

        header_layout.addStretch()
        header_layout.addWidget(self.qwindowbutton)
        header_layout.addWidget(self.dplabel_sm)
        header_layout.addWidget(self.dpinp_sm)
        header_layout.addLayout(simdisplay_layout)
        header_layout.addStretch()
        header_layout.setContentsMargins(0,25,0,25)

        slider_layout.addStretch()
        slider_layout.addWidget(self.view)
        slider_layout.addWidget(self.elevslider)
        slider_layout.addWidget(self.canvas_sm)
        slider_layout.addStretch()

        graph_layout.addLayout(slider_layout)

        velocity_layout.addStretch()
        velocity_layout.addWidget(self.velolabel_sm)
        velocity_layout.addWidget(self.veloinp_sm)
        velocity_layout.addStretch()

        angle_layout.addStretch()
        angle_layout.addWidget(self.anglelabel_sm)
        angle_layout.addWidget(self.anglespin_sm)
        angle_layout.addStretch()

        elevation_layout.addStretch()
        elevation_layout.addWidget(self.elevlabel_sm)
        elevation_layout.addWidget(self.elevinp_sm)
        elevation_layout.addStretch()

        input_layout.addLayout(velocity_layout)
        input_layout.addLayout(angle_layout)
        input_layout.addLayout(elevation_layout)

        bottom_layout.addStretch()
        bottom_layout.addLayout(input_layout)
        bottom_layout.addLayout(start_layout)
        bottom_layout.addStretch()

        main_layout.addLayout(header_layout)
        main_layout.addLayout(graph_layout)
        main_layout.addLayout(bottom_layout)

        self.veloinp_sm.editingFinished.connect(self.input_velocity)
        self.anglespin_sm.editingFinished.connect(self.input_angle)
        self.elevinp_sm.editingFinished.connect(self.input_elevation)
        self.dpinp_sm.editingFinished.connect(self.input_decimalpoint)

        self.sim_widget = QWidget()
        self.sim_widget.setLayout(main_layout)

        select_layout = QVBoxLayout()
        select_row1_layout = QHBoxLayout()
        select_row2_layout = QHBoxLayout()
        input_layout = QVBoxLayout()
        ans_layout = QHBoxLayout()
        interface_layout = QVBoxLayout()
        whole_layout = QHBoxLayout()

        graph_layout = QVBoxLayout()

        self.selectgvalue = QPushButton("Select G Value")
        self.swindowbutton = QPushButton("Switch to Simulation Mode")
        self.selectgvalue.pressed.connect(self.show_gdialog)
        self.swindowbutton.pressed.connect(self.switch_mode)

        self.selectgvalue.setFixedSize(200,20)
        self.swindowbutton.setFixedSize(200,20)

        self.dplabel_qm = QLabel("Enter the amount of decimal places: ")
        self.dpinp_qm = QLineEdit(self)
        self.dpinp_qm.setFixedSize(20,20)

        self.selectlabel = QLabel("Select a target value from the following:")
        self.selectlabel.setFixedSize(250,20)
        self.selectrange = QPushButton("Range")
        self.selectmaxheight = QPushButton("Max Height")
        self.selecttimetaken = QPushButton("Time Taken")
        self.selectinitvelo = QPushButton("Initial Velocity")
        self.selectang = QPushButton("Angle of Projection")
        self.selectgivenvd = QPushButton("Velocity and Direction at given time")
        self.selectxypos = QPushButton("X & Y Position")
       
        self.veloinp_qm = QLineEdit(self)
        self.velolabel_qm = QLabel("Enter your velocity:")

        self.angleinp_qm = QLineEdit(self)
        self.anglelabel_qm = QLabel("Enter your angle:")

        self.elevinp_qm = QLineEdit(self)
        self.elevlabel_qm = QLabel("Enter your elevation:")

        self.timeinp_qm = QLineEdit(self)
        self.timelabel_qm = QLabel("Enter your time:")

        self.xposinp_qm = QLineEdit(self)
        self.xposlabel_qm = QLabel("Enter your x position:")

        self.yposinp_qm = QLineEdit(self)
        self.yposlabel_qm = QLabel("Enter your y position:")

        self.ansinp_qm = QLineEdit(self)
        self.anslabel_qm = QLabel("Enter your answer:")

        self.anslabel_qm.setFixedSize(300,20)

        self.figure_qm = Figure(figsize=(5,10),dpi=100)
        self.canvas_qm = FigureCanvas(self.figure_qm)
        self.canvas_qm.setFixedSize(480,480)

        self.correctans = QLabel("Correct")
        self.falseans = QLabel("False")
        self.ansdisplay_widget = QStackedWidget()

        self.checkbuttR = QPushButton("Check Range")
        self.checkbuttH = QPushButton("Check Max Height")
        self.checkbuttT = QPushButton("Check Time Taken")
        self.checkbuttXY = QPushButton("Check XY Position")
        self.checkbuttIV = QPushButton("Check Initial Velocity")
        self.checkbuttAOP = QPushButton("Check Angle of Projection")
        self.checkbuttVD = QPushButton("Check Velocity and Direction")

        self.is_xpos = True
        self.is_velo = True

        self.checkbuttX = QPushButton("X Position")
        self.checkbuttY = QPushButton("Y Position")
        self.checkbuttV = QPushButton("Velocity")
        self.checkbuttD = QPushButton("Direction")

        self.multicheck_widget = QStackedWidget()
        self.multicheck_widget.setFixedSize(200,30)

        select_row1_layout.addWidget(self.selectrange)
        select_row1_layout.addWidget(self.selectmaxheight)
        select_row1_layout.addWidget(self.selecttimetaken)
        select_row1_layout.addWidget(self.selectxypos)
        select_row2_layout.addWidget(self.selectinitvelo)
        select_row2_layout.addWidget(self.selectang)
        select_row2_layout.addWidget(self.selectgivenvd)

        select_layout.addStretch()
        select_layout.addLayout(select_row1_layout)
        select_layout.addLayout(select_row2_layout)
        select_layout.addStretch()

        veloinp_layout = QHBoxLayout()
        angleinp_layout = QHBoxLayout()
        elevinp_layout = QHBoxLayout()
        xposinp_layout = QHBoxLayout()
        yposinp_layout = QHBoxLayout()
        timeinp_layout = QHBoxLayout()
        dpinp_layout = QHBoxLayout()

        veloinp_layout.addStretch()
        veloinp_layout.addWidget(self.velolabel_qm)
        veloinp_layout.addWidget(self.veloinp_qm)
        veloinp_layout.addStretch()
    
        angleinp_layout.addStretch()
        angleinp_layout.addWidget(self.anglelabel_qm)
        angleinp_layout.addWidget(self.angleinp_qm)
        angleinp_layout.addStretch()

        elevinp_layout.addStretch()
        elevinp_layout.addWidget(self.elevlabel_qm)
        elevinp_layout.addWidget(self.elevinp_qm)
        elevinp_layout.addStretch()

        xposinp_layout.addStretch()
        xposinp_layout.addWidget(self.xposlabel_qm)
        xposinp_layout.addWidget(self.xposinp_qm)
        xposinp_layout.addStretch()

        yposinp_layout.addStretch()
        yposinp_layout.addWidget(self.yposlabel_qm)
        yposinp_layout.addWidget(self.yposinp_qm)
        yposinp_layout.addStretch()

        timeinp_layout.addStretch()
        timeinp_layout.addWidget(self.timelabel_qm)
        timeinp_layout.addWidget(self.timeinp_qm)
        timeinp_layout.addStretch()

        dpinp_layout.addStretch()
        dpinp_layout.addWidget(self.dplabel_qm)
        dpinp_layout.addWidget(self.dpinp_qm)
        dpinp_layout.addStretch()

        input_layout.addLayout(veloinp_layout)
        input_layout.addLayout(angleinp_layout)
        input_layout.addLayout(elevinp_layout)
        input_layout.addLayout(xposinp_layout)
        input_layout.addLayout(yposinp_layout)
        input_layout.addLayout(timeinp_layout)
        input_layout.setSpacing(20)
        input_layout.setContentsMargins(0,25,0,0)

        ans_layout.addStretch()
        ans_layout.addWidget(self.anslabel_qm)
        ans_layout.addWidget(self.checkbuttX)
        ans_layout.addWidget(self.checkbuttY)
        ans_layout.addWidget(self.checkbuttV)
        ans_layout.addWidget(self.checkbuttD)
        self.checkbuttX.hide()
        self.checkbuttY.hide()
        self.checkbuttV.hide()
        self.checkbuttD.hide()
        ans_layout.addWidget(self.ansinp_qm)
        ans_layout.addStretch()
        ans_layout.setContentsMargins(0,20,0,20)

        self.ansdisplay_widget.addWidget(self.correctans)
        self.ansdisplay_widget.addWidget(self.falseans)
        ans_layout.addWidget(self.ansdisplay_widget)
        self.ansdisplay_widget.hide()

        self.multicheck_widget.addWidget(self.checkbuttR)
        self.multicheck_widget.addWidget(self.checkbuttH)
        self.multicheck_widget.addWidget(self.checkbuttT)
        self.multicheck_widget.addWidget(self.checkbuttXY)
        self.multicheck_widget.addWidget(self.checkbuttIV)
        self.multicheck_widget.addWidget(self.checkbuttAOP)
        self.multicheck_widget.addWidget(self.checkbuttVD)
        self.multicheck_widget.show()

        self.selectrange.pressed.connect(self.choose_range)
        self.selectmaxheight.pressed.connect(self.choose_maxheight)
        self.selecttimetaken.pressed.connect(self.choose_timetaken)
        self.selectxypos.pressed.connect(self.choose_xypos)
        self.selectinitvelo.pressed.connect(self.choose_initialvelocity)
        self.selectang.pressed.connect(self.choose_angleofprojection)
        self.selectgivenvd.pressed.connect(self.choose_velocitydirection)

        self.veloinp_qm.editingFinished.connect(self.input_velocity)
        self.angleinp_qm.editingFinished.connect(self.input_angle)
        self.elevinp_qm.editingFinished.connect(self.input_elevation)
        self.xposinp_qm.editingFinished.connect(self.input_xpos)
        self.yposinp_qm.editingFinished.connect(self.input_ypos)
        self.timeinp_qm.editingFinished.connect(self.input_time)
        self.dpinp_qm.editingFinished.connect(self.input_decimalpoint)

        self.checkbuttR.pressed.connect(self.check_rangeans)
        self.checkbuttH.pressed.connect(self.check_maxheightans)
        self.checkbuttT.pressed.connect(self.check_timetakenans)
        self.checkbuttXY.pressed.connect(self.check_xypos)
        self.checkbuttVD.pressed.connect(self.check_veloanddirec)
        self.checkbuttIV.pressed.connect(self.check_initialvelocity)
        self.checkbuttAOP.pressed.connect(self.check_angleofprojection)

        self.checkbuttX.pressed.connect(self.xpos_selection)
        self.checkbuttY.pressed.connect(self.ypos_selection)
        self.checkbuttV.pressed.connect(self.v_selection)
        self.checkbuttD.pressed.connect(self.d_selection)

        interface_layout.addStretch()
        interface_layout.addWidget(self.selectgvalue)
        interface_layout.addWidget(self.swindowbutton)
        interface_layout.addLayout(dpinp_layout)
        interface_layout.addWidget(self.selectlabel)
        interface_layout.addLayout(select_layout)
        interface_layout.addLayout(input_layout)
        interface_layout.addLayout(ans_layout)
        interface_layout.addWidget(self.multicheck_widget)
        interface_layout.addStretch()

        whole_layout.addLayout(interface_layout)
        whole_layout.addWidget(self.canvas_qm)

        self.que_widget = QWidget()
        self.que_widget.setLayout(whole_layout)

        self.main_widget = QStackedWidget()
        self.main_widget.addWidget(self.sim_widget)
        self.main_widget.addWidget(self.que_widget)

        self.setCentralWidget(self.main_widget)

    def set_gvalue(self):
        initialg = 9.81
        MathsCalculations.SetGravFieldStrength(self,initialg)

    def show_gdialog(self):
        gdlg = GDialog()
        gdlg.exec_()

    def final_graph(self):
        if MathsCalculations.CalcRange(self, MathsCalculations.GetVelocity(self), MathsCalculations.GetAngleOfProjection(self), MathsCalculations.GetElevation(self)) > MathsCalculations.CalcMaxHeight(self, MathsCalculations.GetVelocity(self), MathsCalculations.GetAngleOfProjection(self), MathsCalculations.GetElevation(self)):
                limit = MathsCalculations.CalcRange(self, MathsCalculations.GetVelocity(self), MathsCalculations.GetAngleOfProjection(self), MathsCalculations.GetElevation(self))
        else:
            limit = MathsCalculations.CalcMaxHeight(self, MathsCalculations.GetVelocity(self), MathsCalculations.GetAngleOfProjection(self), MathsCalculations.GetElevation(self))
        self.cl = self.figure_sm.clear()
        self.ax = self.figure_sm.add_subplot()
        self.ax.set_xlim([0,limit+(limit*0.1)]) 
        self.ax.set_ylim([0,limit+(limit*0.1)])
        t = np.linspace(0, MathsCalculations.CalcTimeTaken(self, MathsCalculations.GetVelocity(self), MathsCalculations.GetAngleOfProjection(self), MathsCalculations.GetElevation(self)), 50)
        line, = self.ax.plot((float(self.veloinp_sm.text()) * np.cos((np.pi/180)*float(self.anglespin_sm.text())) * t), (float(self.veloinp_sm.text()) * np.sin((np.pi/180)*float(self.anglespin_sm.text())) * t - (0.5) * MathsCalculations.GetGravFieldStrength(self) * (t)**2 + float(self.elevinp_sm.text())), 'b.', linewidth=1, pickradius=3)
        self.canvas_sm.draw()

    def onpick(event):
        graph_point = event.artist
        xdata = graph_point.get_xdata()
        ydata = graph_point.get_ydata()
        ind = event.ind
        xpoints = xdata[ind]
        ypoints = ydata[ind]
        print(round(xpoints[0],2), round(ypoints[0],2))

    def animate(self):
        if MathsCalculations.CalcRange(self, MathsCalculations.GetVelocity(self), MathsCalculations.GetAngleOfProjection(self), MathsCalculations.GetElevation(self)) > MathsCalculations.CalcMaxHeight(self, MathsCalculations.GetVelocity(self), MathsCalculations.GetAngleOfProjection(self), MathsCalculations.GetElevation(self)):
                limit = MathsCalculations.CalcRange(self, MathsCalculations.GetVelocity(self), MathsCalculations.GetAngleOfProjection(self), MathsCalculations.GetElevation(self))
        else:
            limit = MathsCalculations.CalcMaxHeight(self, MathsCalculations.GetVelocity(self), MathsCalculations.GetAngleOfProjection(self), MathsCalculations.GetElevation(self))
        if self.is_sim_mode == True:
            try:
                self.cl = self.figure_sm.clf()
                self.ax = self.figure_sm.add_subplot()
                self.circle = Circle((0,0), 0.3) 
                self.ax.add_artist(self.circle) 
                self.ax.set_xlim([0,limit+(limit*0.1)])
                self.ax.set_ylim([0,limit+(limit*0.1)])
                self.animation1 = animation.FuncAnimation(self.figure_sm,self.animate_loop_sm,frames=np.arange(0, MathsCalculations.CalcTimeTaken(self, float(self.veloinp_sm.text()), float(self.anglespin_sm.text()), float(self.elevinp_sm.text())), 0.01),interval=10,repeat=False)
                self.animation2 = animation.FuncAnimation(self.figure_sm,self.animate_trailloop_sm,frames=np.arange(0, MathsCalculations.CalcTimeTaken(self, float(self.veloinp_sm.text()), float(self.anglespin_sm.text()), float(self.elevinp_sm.text())),0.01),interval=10,repeat=False)
                self.canvas_sm.draw()
            except:
                print("Error")
        else:
            try:
                self.cl = self.figure_qm.clf()
                self.ax = self.figure_qm.add_subplot()
                self.circle = Circle((0,0), 0.3) 
                self.ax.add_artist(self.circle) 
                self.ax.set_xlim([0,limit+(limit*0.1)])
                self.ax.set_ylim([0,limit+(limit*0.1)])
                self.animation3 = animation.FuncAnimation(self.figure_qm,self.animate_loop_qm,frames=np.arange(0, MathsCalculations.CalcTimeTaken(self, float(self.veloinp_qm.text()), float(self.angleinp_qm.text()), float(self.elevinp_qm.text())), 0.01),interval=10,repeat=False)
                self.animation4 = animation.FuncAnimation(self.figure_qm,self.animate_trailloop_qm,frames=np.arange(0, MathsCalculations.CalcTimeTaken(self, float(self.veloinp_qm.text()), float(self.angleinp_qm.text()), float(self.elevinp_qm.text())),0.01),interval=10,repeat=False)
                self.canvas_qm.draw()
            except:
                print("Error")
        
    def animate_loop_sm(self,t):
        self.circle.center=(float(self.veloinp_sm.text()) * np.cos((np.pi/180)*float(self.anglespin_sm.text())) * t, float(self.veloinp_sm.text()) * np.sin((np.pi/180)*float(self.anglespin_sm.text())) * t - (0.5) * MathsCalculations.GetGravFieldStrength(self) * (t)**2 + float(self.elevinp_sm.text()))
        return self.circle
    
    def animate_trailloop_sm(self,t):
        interval_t = round(t*100,0)
        ln, = self.ax.plot([], [], 'b.')
        self.xdata, self.ydata = [], []
        if interval_t % 7 == 0:
            self.xdata.append(float(self.veloinp_sm.text()) * np.cos((np.pi/180)*float(self.anglespin_sm.text())) * t)
            self.ydata.append(float(self.veloinp_sm.text()) * np.sin((np.pi/180)*float(self.anglespin_sm.text())) * t - (0.5) * MathsCalculations.GetGravFieldStrength(self) * (t)**2 + float(self.elevinp_sm.text()))
            ln.set_data(self.xdata, self.ydata)
            return ln,
            self.canvas_sm.show()
    
    def animate_loop_qm(self,t):
        self.circle.center=(float(self.veloinp_qm.text()) * np.cos((np.pi/180)*float(self.angleinp_qm.text())) * t, float(self.veloinp_qm.text()) * np.sin((np.pi/180)*float(self.angleinp_qm.text())) * t - (0.5) * MathsCalculations.GetGravFieldStrength(self) * (t)**2 + float(self.elevinp_qm.text()))
        return self.circle
    
    def animate_trailloop_qm(self,t):
        interval_t = round(t*100,0)
        ln, = self.ax.plot([], [], 'b.')
        self.xdata, self.ydata = [], []
        if interval_t % 7 == 0:
            self.xdata.append(float(self.veloinp_qm.text()) * np.cos((np.pi/180)*float(self.angleinp_qm.text())) * t)
            self.ydata.append(float(self.veloinp_qm.text()) * np.sin((np.pi/180)*float(self.angleinp_qm.text())) * t - (0.5) * MathsCalculations.GetGravFieldStrength(self) * (t)**2 + float(self.elevinp_qm.text()))
            ln.set_data(self.xdata, self.ydata)
            return ln,
            self.canvas_qm.show()
    
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
            MathsCalculations.SetVelocity(self,float(self.veloinp_sm.text()))
        else:
            MathsCalculations.SetVelocity(self,float(self.veloinp_qm.text()))

    def input_angle(self):
        if self.is_sim_mode == True:
            MathsCalculations.SetAngleOfProjection(self,float(self.anglespin_sm.text()))
        else:
            MathsCalculations.SetAngleOfProjection(self,float(self.angleinp_qm.text()))

    def input_elevation(self):
        if self.is_sim_mode == True:
            MathsCalculations.SetElevation(self,float(self.elevinp_sm.text()))
            rounded_elev = round(float(self.elevinp_sm.text()), 0)
            self.elevslider.setValue(int(rounded_elev))
        else:
            MathsCalculations.SetElevation(self,float(self.elevinp_qm.text()))

    def input_xpos(self):
        MathsCalculations.SetXPosition(self,float(self.xposinp_qm.text()))

    def input_ypos(self):
        MathsCalculations.SetYPosition(self,float(self.yposinp_qm.text()))

    def input_time(self):
        MathsCalculations.SetTime(self,float(self.timeinp_qm.text()))
        
    def input_decimalpoint(self):
        if self.is_sim_mode == True:
            MathsCalculations.SetDecimalPoint(self,int(self.dpinp_sm.text()))
            self.dpinp_qm.setText(str(self.dpinp_sm.text()))
        else:
            MathsCalculations.SetDecimalPoint(self,int(self.dpinp_qm.text()))
            self.dpinp_sm.setText(str(self.dpinp_qm.text()))

    def xpos_selection(self):
        self.is_xpos = True

    def ypos_selection(self):
        self.is_xpos = False

    def v_selection(self): 
        self.is_velo = True

    def d_selection(self):
        self.is_velo = False
    
    def get_elevation(self):
        elevation = str(self.elevslider.value())
        self.elevinp_sm.setText(elevation)
        MathsCalculations.SetElevation(self,float(self.elevinp_sm.text()))
    
    def display_range_time(self):
        self.rangedisplay.setText(f'Final Range: {str(MathsCalculations.CalcRange(self, MathsCalculations.GetVelocity(self), MathsCalculations.GetAngleOfProjection(self), MathsCalculations.GetElevation(self)))}')
        self.timedisplay.setText(f'Final Time Taken: {str(MathsCalculations.CalcTimeTaken(self, MathsCalculations.GetVelocity(self), MathsCalculations.GetAngleOfProjection(self), MathsCalculations.GetElevation(self)))}')

    def calculate_range(self):
        MathsCalculations.CalcRange(self, MathsCalculations.GetVelocity(self), MathsCalculations.GetAngleOfProjection(self), MathsCalculations.GetElevation(self))
    
    def check_rangeans(self):
        if float(self.ansinp_qm.text()) == MathsCalculations.CalcRange(self, MathsCalculations.GetVelocity(self), MathsCalculations.GetAngleOfProjection(self), MathsCalculations.GetElevation(self)):
            self.ansdisplay_widget.setCurrentWidget(self.correctans)
            self.ansdisplay_widget.show()
            self.animate()
        else:
            self.ansdisplay_widget.setCurrentWidget(self.falseans)
            self.ansdisplay_widget.show()
    
    def calculate_maxheight(self):
        MathsCalculations.CalcMaxHeight(self, MathsCalculations.GetVelocity(self), MathsCalculations.GetAngleOfProjection(self), MathsCalculations.GetElevation(self))

    def check_maxheightans(self):
        if float(self.ansinp_qm.text()) == MathsCalculations.CalcMaxHeight(self, MathsCalculations.GetVelocity(self), MathsCalculations.GetAngleOfProjection(self), MathsCalculations.GetElevation(self)):
            self.ansdisplay_widget.setCurrentWidget(self.correctans)
            self.ansdisplay_widget.show()
            self.animate()
        else:
            self.ansdisplay_widget.setCurrentWidget(self.falseans)
            self.ansdisplay_widget.show()

    def calculate_timetaken(self):
        MathsCalculations.CalcTimeTaken(MathsCalculations.GetVelocity(self), MathsCalculations.GetAngleOfProjection(self), MathsCalculations.GetElevation(self))

    def check_timetakenans(self):
        if float(self.ansinp_qm.text()) == MathsCalculations.CalcTimeTaken(self, MathsCalculations.GetVelocity(self), MathsCalculations.GetAngleOfProjection(self), MathsCalculations.GetElevation(self)):
            self.ansdisplay_widget.setCurrentWidget(self.correctans)
            self.ansdisplay_widget.show()
            self.animate()
        else:
            self.ansdisplay_widget.setCurrentWidget(self.falseans)
            self.ansdisplay_widget.show()

    def calculate_xypos(self):
        MathsCalculations.CalcXYPosition(self, MathsCalculations.GetVelocity(self), MathsCalculations.GetAngleOfProjection(self), MathsCalculations.GetElevation(self), MathsCalculations.GetTime(self))

    def check_xypos(self):
        if self.is_xpos == True:
            if float(self.ansinp_qm.text()) == MathsCalculations.CalcXYPosition(self, MathsCalculations.GetVelocity(self), MathsCalculations.GetAngleOfProjection(self), MathsCalculations.GetElevation(self), MathsCalculations.GetTime(self))[0]:
                self.ansdisplay_widget.setCurrentWidget(self.correctans)
                self.ansdisplay_widget.show()
                print(MathsCalculations.CalcXYPosition(self, MathsCalculations.GetVelocity(self), MathsCalculations.GetAngleOfProjection(self), MathsCalculations.GetElevation(self), MathsCalculations.GetTime(self))[0])
                self.animate()
            else:
                self.ansdisplay_widget.setCurrentWidget(self.falseans)
                print(MathsCalculations.CalcXYPosition(self, MathsCalculations.GetVelocity(self), MathsCalculations.GetAngleOfProjection(self), MathsCalculations.GetElevation(self), MathsCalculations.GetTime(self))[0])
                self.ansdisplay_widget.show()
        else:
            if float(self.ansinp_qm.text()) == MathsCalculations.CalcXYPosition(self, MathsCalculations.GetVelocity(self), MathsCalculations.GetAngleOfProjection(self), MathsCalculations.GetElevation(self), MathsCalculations.GetTime(self))[1]:
                self.ansdisplay_widget.setCurrentWidget(self.correctans)
                print(MathsCalculations.CalcXYPosition(self, MathsCalculations.GetVelocity(self), MathsCalculations.GetAngleOfProjection(self), MathsCalculations.GetElevation(self), MathsCalculations.GetTime(self))[1])
                self.ansdisplay_widget.show()
                self.animate()
            else:
                self.ansdisplay_widget.setCurrentWidget(self.falseans)
                print(MathsCalculations.CalcXYPosition(self, MathsCalculations.GetVelocity(self), MathsCalculations.GetAngleOfProjection(self), MathsCalculations.GetElevation(self), MathsCalculations.GetTime(self))[1])
                self.ansdisplay_widget.show()


    def calculate_veloanddirec(self):
        MathsCalculations.CalcVeloAndDirec(self, MathsCalculations.GetVelocity(self), MathsCalculations.GetAngleOfProjection(self), MathsCalculations.GetElevation(self), MathsCalculations.GetTime(self))

    def check_veloanddirec(self):
        if self.is_velo == True:
            if float(self.ansinp_qm.text()) == MathsCalculations.CalcVeloAndDirec(self, MathsCalculations.GetVelocity(self), MathsCalculations.GetAngleOfProjection(self), MathsCalculations.GetElevation(self), MathsCalculations.GetTime(self))[0]:
                self.ansdisplay_widget.setCurrentWidget(self.correctans)
                self.ansdisplay_widget.show()
                print(MathsCalculations.CalcVeloAndDirec(self, MathsCalculations.GetVelocity(self), MathsCalculations.GetAngleOfProjection(self), MathsCalculations.GetElevation(self), MathsCalculations.GetTime(self))[0])
                self.animate()
            else:
                self.ansdisplay_widget.setCurrentWidget(self.falseans)
                print(MathsCalculations.CalcVeloAndDirec(self, MathsCalculations.GetVelocity(self), MathsCalculations.GetAngleOfProjection(self), MathsCalculations.GetElevation(self), MathsCalculations.GetTime(self))[0])
                self.ansdisplay_widget.show()
        else:
            if float(self.ansinp_qm.text()) == MathsCalculations.CalcVeloAndDirec(self, MathsCalculations.GetVelocity(self), MathsCalculations.GetAngleOfProjection(self), MathsCalculations.GetElevation(self), MathsCalculations.GetTime(self))[1]:
                self.ansdisplay_widget.setCurrentWidget(self.correctans)
                self.ansdisplay_widget.show()
                print(MathsCalculations.CalcVeloAndDirec(self, MathsCalculations.GetVelocity(self), MathsCalculations.GetAngleOfProjection(self), MathsCalculations.GetElevation(self), MathsCalculations.GetTime(self))[1])
                self.animate()
            else:
                self.ansdisplay_widget.setCurrentWidget(self.falseans)
                print(print(MathsCalculations.CalcVeloAndDirec(self, MathsCalculations.GetVelocity(self), MathsCalculations.GetAngleOfProjection(self), MathsCalculations.GetElevation(self), MathsCalculations.GetTime(self))[0]))
                self.ansdisplay_widget.show()

    def calculate_initialvelocity(self):
        MathsCalculations.CalcInitialVelocity(self, MathsCalculations.GetAngleOfProjection(self), MathsCalculations.GetElevation(self), MathsCalculations.GetTime(self), MathsCalculations.GetXPosition(self), MathsCalculations.GetYPosition(self))

    def check_initialvelocity(self):
        if float(self.ansinp_qm.text()) == MathsCalculations.CalcInitialVelocity(self, MathsCalculations.GetAngleOfProjection(self), MathsCalculations.GetElevation(self), MathsCalculations.GetTime(self), MathsCalculations.GetXPosition(self), MathsCalculations.GetYPosition(self)):
            self.ansdisplay_widget.setCurrentWidget(self.correctans)
            self.ansdisplay_widget.show()
            self.animate()
        else:
            self.ansdisplay_widget.setCurrentWidget(self.falseans)
            self.ansdisplay_widget.show()

    def calculate_angleofproejction(self):
        MathsCalculations.CalcAngleOfProjection(self, MathsCalculations.GetVelocity(self), MathsCalculations.GetElevation(self), MathsCalculations.GetTime(self), MathsCalculations.GetXPosition(self), MathsCalculations.GetYPosition(self))
    
    def check_angleofprojection(self):
        if float(self.ansinp_qm.text()) == MathsCalculations.CalcAngleOfProjection(self, MathsCalculations.GetVelocity(self), MathsCalculations.GetElevation(self), MathsCalculations.GetTime(self), MathsCalculations.GetXPosition(self), MathsCalculations.GetYPosition(self)):
            self.ansdisplay_widget.setCurrentWidget(self.correctans)
            self.ansdisplay_widget.show()
            self.animate()
        else:
            self.ansdisplay_widget.setCurrentWidget(self.falseans)
            self.ansdisplay_widget.show()

    def choose_range(self):
        self.multicheck_widget.setCurrentWidget(self.checkbuttR)
        self.multicheck_widget.show()
        self.checkbuttX.hide()
        self.checkbuttY.hide()
        self.checkbuttV.hide()
        self.checkbuttD.hide()

    def choose_maxheight(self):
        self.multicheck_widget.setCurrentWidget(self.checkbuttH)
        self.multicheck_widget.show()
        self.checkbuttX.hide()
        self.checkbuttY.hide()
        self.checkbuttV.hide()
        self.checkbuttD.hide()

    def choose_timetaken(self):
        self.multicheck_widget.setCurrentWidget(self.checkbuttT)
        self.multicheck_widget.show()
        self.checkbuttX.hide()
        self.checkbuttY.hide()
        self.checkbuttV.hide()
        self.checkbuttD.hide()

    def choose_xypos(self):
        self.multicheck_widget.setCurrentWidget(self.checkbuttXY)
        self.multicheck_widget.show()
        self.checkbuttX.show()
        self.checkbuttY.show()
        self.checkbuttV.hide()
        self.checkbuttD.hide()
    
    def choose_initialvelocity(self):
        self.multicheck_widget.setCurrentWidget(self.checkbuttIV)
        self.multicheck_widget.show()
        self.checkbuttX.hide()
        self.checkbuttY.hide()
        self.checkbuttV.hide()
        self.checkbuttD.hide()
    
    def choose_angleofprojection(self):
        self.multicheck_widget.setCurrentWidget(self.checkbuttAOP)
        self.multicheck_widget.show()
        self.checkbuttX.hide()
        self.checkbuttY.hide()
        self.checkbuttV.hide()
        self.checkbuttD.hide()
    
    def choose_velocitydirection(self):
        self.multicheck_widget.setCurrentWidget(self.checkbuttVD)
        self.multicheck_widget.show()
        self.checkbuttV.show()
        self.checkbuttD.show()
        self.checkbuttX.hide()
        self.checkbuttY.hide()
    
def main():
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
