import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.artist import Artist
from matplotlib.animation import FuncAnimation

import numpy as np


G_ACCELERATION = np.array([0, -9.81]) # Gravitational acceleration; g = 9.81 m/s^2

DT = 0.001 # Time step; ∆t = 0.001 s

STEPS_PER_FRAME = 10 # Number of steps per animation frame

class Particle:
    def __init__(self, r0, v0, mass):
        """ Create a new Particle with the given position, velocity, and mass. """
        self.r = r0
        self.v = v0
        self.m = mass

    def step(self, dt):
        """ Calculate the new position and velocity of the particle after a given time step.
            Use the rectangle rule to step velocity and then position. """
        self.v = self.v + G_ACCELERATION * dt
        self.r = self.r + self.v * dt

def init_particle():
    return Particle(np.array([0,0]), np.array([6,6]), 1)

fig, ax = plt.subplots()
paths = ax.scatter([0], [0])

p = init_particle()

def init():
    """ Called at beginning of animation. """
    # Set up the plot
    ax.axis('equal')
    ax.set_xlim(0, 10)
    ax.set_ylim(-5,5)
    ax.set_xlabel("x (meters)")
    ax.set_ylabel("y (meters)")
    ax.axhline(y=0, color='k')
    ax.axvline(x=0, color='k')

    # Initialize the particle and move the drawn circle to its location
    p = init_particle()
    paths.set_offsets([p.r[0], p.r[1]])
    return paths

def update(frame):
    """ Called on every animation frame """
    # Loop a given number of times, stepping the particle on each iteration
    for _ in range(STEPS_PER_FRAME):
        p.step(DT)

    # Move the drawn circle to the particle's location
    paths.set_offsets([p.r[0], p.r[1]])
    return paths

# Create the animation, with a frame delay of 100 milliseconds and a length of 20 frames
ani = FuncAnimation(fig, update, frames=30, interval=1, init_func=init)

plt.show()