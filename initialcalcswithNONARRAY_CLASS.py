import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

matplotlib.use('Qt5Agg')

from PyQt5 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


g = 9.81
dt = 0.01

class QuestionMode:

    def __init__(self,velo,anglep,elev,time):
        self.velo = velo
        self.anglep = anglep
        self.elev = elev
        self.time = time

    def CalcRange(self):
        anginr = (np.pi/180)*self.anglep
        a = -g/2
        b = self.velo*np.sin(anginr)
        c = self.elev
        ux = self.velo*np.cos(anginr)
        t = (-b-math.sqrt(b**2-4*a*c)) / (2 * a)
        sx= ux*t
        roundedsx = round(sx, 2)
        print(f"The range is: {roundedsx}m")

    def CalcMaxHeight(self):
        anginr = (np.pi/180)*self.anglep
        uy = self.velo*np.sin(anginr)
        e = self.elev
        hmax = ((uy**2/(2*g))) + e
        roundedhmax = round(hmax, 2)
        print(f"The maximum height is: {roundedhmax}m")

    def CalcTimeTaken(self):
        anginr = (np.pi/180)*self.anglep
        a = -g/2
        b = self.velo*np.sin(anginr)
        c = self.elev
        time = (-b-math.sqrt(b**2-4*a*c)) / (2 * a)
        roundedtime = round(time, 2)
        print(f"The time taken is: {roundedtime}s")

    def CalcXPosition(self):
        anginr = (np.pi/180)*self.anglep
        xpos = self.velo*np.cos(anginr) * self.time 
        roundedxpos = round(xpos, 2)
        print(f"The x position is: {roundedxpos}m")

    def CalcYPosition(self):
        anginr = (np.pi/180)*self.anglep
        ypos = (self.velo*np.sin(anginr) * self.time) + (0.5 * -g * self.time**2)
        roundedypos = round(ypos, 2)
        print(f"The y position is: {roundedypos}m")

    '''
    def EulerMethod(velo,anglep,elev):
        anginr = (np.pi/180)*anglep
        y = elev
        vy = velo*np.sin(anginr)
        t = 0
        while y > 0:
            y += vy * dt
            vy += -g * dt 
            t += dt
            print(y)
    '''

#g = float(input("Enter the gravitational field strength: "))
v = int(input("Enter the velocity: "))
a = int(input("Enter the angle of projection: "))
e = int(input("Enter the elevation: "))
t = int(input("Enter the time: "))
print()

answ = QuestionMode(v,a,e,t)

answ.CalcRange()
answ.CalcMaxHeight()
answ.CalcTimeTaken()
answ.CalcXPosition()
answ.CalcYPosition()
#EulerMethod(v,a,e)

