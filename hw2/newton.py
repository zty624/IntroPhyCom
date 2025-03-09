import matplotlib.pyplot as plt
import numpy as np

roots = [
    1 + 0j,
    -0.5 + (np.sqrt(3)/2)*1j,
    -0.5 - (np.sqrt(3)/2)*1j
]

def f(z):
    return z ** 3 - 1

def diff_f(z):
    return 3 * z ** 2

def newton_method(z0:np.ndarray, eps=1e-2):
    z = z0
    while np.any(np.abs(f(z)) > eps):
        z = z - f(z) / diff_f(z)
    return z

def mapping(cntr_x, cntr_y, hfw, step, filename):
    x_min = cntr_x - hfw
    x_max = cntr_x + hfw
    y_min = cntr_y - hfw
    y_max = cntr_y + hfw
    x = np.arange(x_min, x_max + step, step)
    y = np.arange(y_min, y_max + step, step)
    X, Y = np.meshgrid(x, y)
    Z = X + Y * 1j
    res = newton_method(Z)

    arg = np.abs(res[:, :, np.newaxis] - roots)
    result = np.argmin(arg, axis=2)

    plt.figure(figsize=(10, 10))
    plt.rcParams['font.size'] = 16
    plt.scatter(X, Y, c=result, cmap="tab10", s=1)
    plt.xlabel("Re")
    plt.ylabel("Im")
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.title(f"Newton Fractal Center: ({cntr_x}, {cntr_y}), Width: {2*hfw}")
    plt.savefig("hw2/" + filename)
    plt.close()

if __name__ == "__main__":
    print("1")
    mapping(0.0, 0.0, 1.0, 0.002, "newton_0_0.png")
    print("2")
    mapping(-0.8, 0.0, 0.25, 0.0005, "newton_-0.8_0.png")
    print("3")
    mapping(-0.56, 0.18, 0.1, 0.0002, "newton_-0.56_0.18.png")