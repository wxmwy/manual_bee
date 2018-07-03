import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pygame
import array
import random
import sys
import bee_utils

def data_gen(t=0):
    while True:
        f = open("score.txt")
        t = int(f.readline())
        y = int(f.readline())
        f.close()
        yield t, y


def init():
    ax.set_ylim(0, 30)
    ax.set_xlim(0, 10)
    del xdata[:]
    del ydata[:]
    line.set_data(xdata, ydata)
    return line



def run(data):
    # update the data
    t, y = data
    xdata.append(t)
    ydata.append(y)
    xmin, xmax = ax.get_xlim()

    if t >= xmax:
        ax.set_xlim(xmin, 2 * xmax)
        ax.figure.canvas.draw()
    line.set_data(xdata, ydata)
    return line

def make:
    fig, ax = plt.subplots()
    line, = ax.plot([], [], lw=2)
    ax.grid()
    xdata, ydata = [], []
    ani = animation.FuncAnimation(fig, run, data_gen, blit=False, interval=5,
                              repeat=False, init_func=init)
plt.show()

