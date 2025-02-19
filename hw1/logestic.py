import matplotlib.pyplot as plt
import numpy as np

def iterate(x, mu):
    return 1 - mu * x ** 2

def iterate2(x, mu):
    return np.cos(x) - mu * x **2

def generate_array(x0, mu, n, extend=False):
    x_iter = x0
    array = []
    for i in range(n):
        x_iter = iterate2(x_iter, mu) if extend else iterate(x_iter, mu)
        array.append(x_iter)
    return array

def plot_x_n(num=100, extend=False):
    params = [(0.5, 0.2), (1, 0.2), (1.5, 0.2), (.5, .7), (1, .7), (1.5, .7)]
    fig, ax = plt.subplots(2, 3, figsize=(20, 10))
    plt.rcParams['font.size'] = 14
    fig.tight_layout(pad=4.0)

    for (i, (mu, x0)) in enumerate(params):
        x_array = [i for i in range(num)]
        y_array = generate_array(x0, mu, 100, extend=extend)
        ax[i//3, i%3].plot(x_array, y_array)
        ax[i//3, i%3].set_title(f"mu = {mu}, x0 = {x0}")
        ax[i//3, i%3].set_xlabel("n")
        ax[i//3, i%3].set_ylabel("x")
    # plt.savefig("x_n.png")
    plt.show()

def plot_mu_x(extend=False):
    fig, ax = plt.subplots(3, 2, figsize=(15, 15))
    fig.tight_layout(pad=5.0)
    plt.rcParams['font.size'] = 14
    mu_array = np.linspace(-0.5,2,500)
    x0_array = [0.1, 0.3, 0.5, 0.7, 0.9, 1]

    for (i, x0) in enumerate(x0_array):
        show_x_array = []
        show_y_array = []
        for mu in mu_array:
            array = generate_array(x0, mu, 200, extend=extend)
            show_x_array.extend([mu for i in range(200)])
            show_y_array.extend(array)
            
        ax[i//2, i%2].scatter(show_x_array, show_y_array, s=0.2, label=f"x0={x0:.2f}")
        ax[i//2, i%2].set_xlabel("$\mu$")
        ax[i//2, i%2].set_ylabel("$x$")
        ax[i//2, i%2].set_xlim((-0.5,2))
        ax[i//2, i%2].set_ylim((-1.1,1.1))
        ax[i//2, i%2].set_title(f"x0={x0:.2f}")
        ax[i//2, i%2].grid()

    # plt.savefig("mu_x_new.png")
    plt.show()

def plot_x0_x(extend=False):
    fig, ax = plt.subplots(2, 2, figsize=(15, 15))
    fig.tight_layout(pad=5.0)
    plt.rcParams['font.size'] = 14
    x0_array = np.linspace(0,1,200)
    mu_array = [0.5, 0.8, 1.4, 1.8]

    for (i, mu) in enumerate(mu_array):
        show_x_array = []
        show_y_array = []
        for x0 in x0_array:
            array = generate_array(x0, mu, 200, extend=extend)
            show_x_array.extend([x0 for i in range(200)])
            show_y_array.extend(array)
            
        ax[i//2, i%2].scatter(show_x_array, show_y_array, s=0.2, label=f"mu={mu:.2f}")
        ax[i//2, i%2].set_xlabel("$x_0$")
        ax[i//2, i%2].set_ylabel("$x$")
        ax[i//2, i%2].set_xlim((0,1))
        ax[i//2, i%2].set_ylim((0,1))
        ax[i//2, i%2].set_title(f"mu={mu:.2f}")
        ax[i//2, i%2].grid()
    
    plt.savefig("x0_x.png")
    plt.show()

if __name__ == "__main__":

    # plot_x_n(extend=True)
    plot_mu_x(True)
    # plot_x0_x(False)