import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


g = 9.81
dt = 0.01

a = np.single([1,1])
a[0] = a[0]*g)


def CalcRange(velo,anglep,elev):
    anginr = (np.pi/180)*anglep
    a = -g/2
    b = velo*np.sin(anginr)
    c = elev
    ux = velo*np.cos(anginr)
    t = (-b-math.sqrt(b**2-4*a*c)) / (2 * a)
    sx = ux*t
    roundedsx = round(sx, 2)
    print(f"The range is: {roundedsx}m")
