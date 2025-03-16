import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

def eqa(t, t0, y0, v0):
    return y(t, t0, y0, v0) - 0.02 * np.sin(4 * np.pi * t)

def y(t, t0, y0, v0, g=10, gamma=0.02):
    return y0 - g / gamma * (t - t0) + (v0 + g / gamma) / gamma * (1 - np.exp(-gamma * (t - t0)))

def v(t, t0, y0, v0, g=10, gamma=0.02):
    return - g / gamma + (v0 + g / gamma) * np.exp(-gamma * (t - t0))

def loop(ts, te, y0, v0):
    ct_vals = []
    cy_vals = []
    cv_vals = []

    # solve eqa by newton method
    t = ts
    while t < te:
        dt = t + 1  # initial guess for Newton's method
        res = sp.optimize.newton(eqa, dt, args=(t, y0, v0), tol=1e-8)
        if t >= te:
            break
        ct_vals.append(t)
        cy_vals.append(y(res, t, y0, v0))
        cv_vals.append(v(res, t, y0, v0))
        # crush logic
        y0 = y(res, t, y0, v0)
        v0 = -v0 + 2 * 0.02 * np.cos(4 * np.pi * res)  # bounce
        y0 = 0.02 * np.sin(4 * np.pi * res) + 1e-8  # avoid crush

        t = res
        print(f"t={t:.2f}", end='\r')
    
    return np.array(ct_vals), np.array(cy_vals), np.array(cv_vals)

if __name__ == "__main__":
    ct_vals, cy_vals, cv_vals = loop(0, 2000, 0.3, 0)

    mask = (ct_vals >= 1990) & (ct_vals <= 2000)
    plt.plot(ct_vals[mask] - 1990, cy_vals[mask], 
             alpha=0.5,
             label=f'y0')

    mask_collision = (ct_vals != 0) & (ct_vals >= 1800)
    plt.scatter(cy_vals[mask_collision], 
                cv_vals[mask_collision], 
                s=5, 
                alpha=0.2)

    plt.set(xlabel='Height (m)', ylabel='Velocity (m/s)', title='Phase Space')
    plt.tight_layout(pad=5)
    plt.show()