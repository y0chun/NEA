import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


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
    print(f"The time taken is: {roundedtime}s")

def CalcXandYPosition(velo,anglep,elev,time):
    anginr = (np.pi/180)*anglep
    xpos = velo*np.cos(anginr) * time 
    ypos = (velo*np.sin(anginr) * time) + (0.5 * -g * time**2)
    roundedxpos = round(xpos, 2)
    roundedypos = round(ypos, 2)
    print(f"The x position is: {roundedxpos}m")
    print(f"The y position is: {roundedypos}m")

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

#g = float(input("Enter the gravitational field strength: "))
v = int(input("Enter the velocity: "))
a = int(input("Enter the angle of projection: "))
e = int(input("Enter the elevation: "))
t = int(input("Enter the time: "))
print()

CalcRange(v,a,e)
CalcMaxHeight(v,a,e)
CalcTimeTaken(v,a,e)
CalcXandYPosition(v,a,e,t)
#EulerMethod(v,a,e)

