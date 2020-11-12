import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

g = 9.8
e = 0

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_title('click on points')
t = np.linspace(0, 2.884, 100)

line, = ax.plot((20 * np.cos((np.pi/180)*45) * t), (20 * np.sin((np.pi/180)*45) * t - (0.5) * g * (t)**2 + e), ':', linewidth=1, picker=3) 
#circle = Circle((0,0), 0.3) 
#ax.add_artist(circle)
#circle.center=(40.8,0)

def onpick(event):
    thisline = event.artist
    xdata = thisline.get_xdata()
    ydata = thisline.get_ydata()
    ind = event.ind
    xpoints = xdata[ind]
    ypoints = ydata[ind]
    print(round(xpoints[0],2), round(ypoints[0],2))

fig.canvas.mpl_connect('pick_event', onpick)

plt.show()