import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation

v = 10
ap = 40
e = 0
g = 9.8                                                                                                             
theta = (np.pi/180)*ap                                                               

x_data = []
y_data = []

fig, ax = plt.subplots()

ax.set_xlim(0,25)
ax.set_ylim(0,25)

line, = ax.plot(0,0)

def animation_frame(t):
    x_data.append(v * np.cos(theta) * t)
    y_data.append(v * np.sin(theta) * t - (0.5) * g * (t)**2 + e)

    line.set_data(x_data, y_data)
    return line,

animation = FuncAnimation(fig, func = animation_frame, frames = np.arange(0, 10, 0.01), interval = 10)
plt.show()




