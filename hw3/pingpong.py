import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Pool
from ode.rk45 import *
import os

CPUNUM = os.cpu_count() - 2

G = 10
A = 0.02
W = 4 * np.pi

def worker(y0):
    print(f'Processing y0={y0:.1f}...')
    t_vals, y_vals, v_vals, ct_vals, cy_vals, cv_vals = simu(0, 2000, 0.001, y0, 0)
    print(f'Finished y0={y0:.1f}!')
    return (
        np.array(t_vals), 
        np.array(y_vals),
        np.array(v_vals),
        np.array(ct_vals),
        np.array(cy_vals),
        np.array(cv_vals)
    )

# vars: y, vy
def eqas(t, vars, g=G, gamma=0.02):
    res = np.zeros(2)
    res[0] = eqa1(t, vars)
    res[1] = eqa2(t, vars, g, gamma)
    return res
def eqa1(t, vars):
    return vars[1]
def eqa2(t, vars, g, gamma):
    return -g - gamma * vars[1]

class BallCrash(Event):
    def __init__(self, kill = False):
        super().__init__(kill)
    
    def detect(self, t, y4, y5, err):
        return y4[0] < (A * np.sin(W * t))
    
    def handle(self, t, y4, y5, err):
        y4[1] = -y4[1] + 2 * A * W * np.cos(W * t)  # bounce
        y4[0] = A * np.sin(W * t) + 1e-8
        return t, y4, y5, err

def autosimu(ts, te, err, y0, v0):
    t_vals = [ts]
    y_vals = [y0]
    v_vals = [v0]
    ct_vals = []
    cy_vals = []
    cv_vals = []
    
    while t_vals[-1] < te:
        for t, y in RK45AutoIterator(eqas, np.array([y_vals[-1], v_vals[-1]], dtype=np.float64), t_vals[-1], te, tol=err):
            t_vals.append(t)
            # crush logic
            if y[0] < (A * np.sin(W * t)):  # crush
                ct_vals.append(t)
                cy_vals.append(y[0])
                cv_vals.append(y[1])

                y[1] = -y[1] + 2 * A * W * np.cos(W * t)  # bounce
                y_vals.append(A * np.sin(W * t) + 1e-6)
                v_vals.append(y[1])
                break
            else:
                y_vals.append(y[0])
                v_vals.append(y[1])
    return t_vals, y_vals, v_vals, ct_vals, cy_vals, cv_vals

def simu(ts, te, step, y0, v0):
    t_vals = np.zeros(int((te - ts) / step) + 1, dtype = np.float64)
    y_vals = np.zeros(int((te - ts) / step) + 1, dtype = np.float64)
    v_vals = np.zeros(int((te - ts) / step) + 1, dtype = np.float64)
    ct_vals = np.zeros_like(t_vals, dtype = np.float64)
    cy_vals = np.zeros_like(y_vals, dtype = np.float64)
    cv_vals = np.zeros_like(v_vals, dtype = np.float64)
    t_vals[0] = ts
    y_vals[0] = y0
    v_vals[0] = v0

    index = 0

    for t, y in RK45FixedIterator(eqas, np.array([y_vals[0], v_vals[0]], dtype=np.float64), ts, te, events=[BallCrash()], step=step):
        index += 1
        t_vals[index] = t
        y_vals[index] = y[0]
        v_vals[index] = y[1]
        
        # record crush
        if v_vals[index] > 0 and v_vals[index - 1] < 0:
            ct_vals[index] = t_vals[index - 1]
            cy_vals[index] = y_vals[index - 1]
            cv_vals[index] = v_vals[index - 1]
        
    return t_vals, y_vals, v_vals, ct_vals, cy_vals, cv_vals


if __name__ == "__main__":
    fig, axes = plt.subplots(1, 2, figsize=(20,10))
    plt.rcParams['font.size'] = 16

    x = np.linspace(0, 10, 1000)
    y_racket = A * np.sin(W * x)
    axes[0].plot(x, y_racket, 'r-', label='Racket')
    axes[0].axhline(0, color='black', lw=1)

    y0_list = np.arange(0.1, 5, 0.2)
    with Pool(processes=CPUNUM) as pool:
        results = pool.map(worker, y0_list)

    for idx, (t_vals, y_vals, v_vals, ct_vals, cy_vals, cv_vals) in enumerate(results):
        mask = (t_vals >= 1990) & (t_vals <= 2000)
        axes[0].plot(t_vals[mask] - 1990, y_vals[mask], 
                    alpha=0.5,
                    label=f'y0={y0_list[idx]:.1f}')

        mask_collision = (ct_vals != 0) & (ct_vals >= 1800)
        axes[1].scatter(cy_vals[mask_collision], 
                       cv_vals[mask_collision], 
                       s=5, 
                       alpha=0.2)

    axes[0].set(xlabel='Time (s)', ylabel='Height (m)', title='Last 10s Trajectory')
    axes[1].set(xlabel='Height (m)', ylabel='Velocity (m/s)', title='Phase Space')
    # for ax in axes: 
    #     ax.grid()
    #     ax.legend()
    plt.tight_layout(pad=5)
    plt.show()