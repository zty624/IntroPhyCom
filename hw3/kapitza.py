import matplotlib.pyplot as plt
import numpy as np

from ode.rk45 import *

def eqas(t, vars, g=1, l=1, a=0.1, w=20):
    res = np.zeros(2)
    res[0] = eqa1(t, vars)
    res[1] = eqa2(t, vars, g, l, a, w)
    return res

def eqa1(t, vars):
    return vars[1]

def eqa2(t, vars, g, l, a, w):
    return (-g/l + a * w * w / l * np.cos(w * t)) * np.sin(vars[0])

def ui(t0state=np.array([np.pi/2, 0]), g=1, l=1, a=0.1, w=5):
    def eqas_para(t, vars):
        return eqas(t, vars, g, l, a, w)
    fig, axes = plt.subplots(1, 2, figsize=(8, 4))
    ax1, ax2 = axes

    # plot the trajectory
    ax1.set_xlim(-1, 1)
    ax1.set_ylim(-1, 1)
    ax1.set_aspect('equal')
    ax1.set_title('Trajectory')
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    ax1.grid()

    # plot the t-theta plot
    ax2.set_xlim(0, 10)
    ax2.set_ylim(-np.pi, np.pi)
    ax2.set_title('Theta-t')
    ax2.set_xlabel('t')
    ax2.set_ylabel('theta')
    ax2.grid()

    dt = 0.001

    # lists to store the trajectory and theta values
    x_vals, y_vals = [], []
    t_vals, theta_vals = [], []

    # circle to represent the pendulum
    circle, = ax1.plot([], [], 'bo', markersize=10, alpha = 0.02)
    line, = ax2.plot([], [], 'r-')

    for t, y in RK45FixedIterator(eqas_para, t0state, 0, 10, step=dt):
        theta = y[0]
        xx = np.sin(y[0])
        yy = -np.cos(y[0])
        x_vals.append(xx)
        y_vals.append(yy)
        t_vals.append(t)
        if abs(theta) > np.pi:
            theta = (theta + np.pi) % (2 * np.pi) - np.pi
        theta_vals.append(theta)

        circle.set_data(x_vals, y_vals)
        line.set_data(t_vals, theta_vals)

    plt.show()
    # plt.savefig(f"hw3/figs/w={w}.png")

if __name__ == "__main__":
    for i in range(5, 30, 5):
        ui(np.array([np.pi * 4 / 5,0]), w=i)