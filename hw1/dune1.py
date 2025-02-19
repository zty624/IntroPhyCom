import matplotlib.pyplot as plt
import numpy as np

from dune import *

if __name__ == "__main__":
    dune = np.zeros((LENGTH,LENGTH), dtype=np.int8)
    iter_num = 20000
    scores = np.zeros(iter_num)
    densities = np.zeros(iter_num)
    for i in range(iter_num):
        (score, density) = iterate(dune)
        scores[i] = score
        densities[i] = density
        if i % 1000 == 0:
            print(f"Iteration {i}: Score = {score}, Density = {density:.2f}")
    
    # plot
    x_array = np.arange(iter_num)
    fig, ax1 = plt.subplots(figsize=(12, 8))
    plt.rcParams['font.size'] = 14

    color = 'tab:blue'
    ax1.set_xlabel('Iteration')
    ax1.set_ylabel('Score', color=color)
    ax1.plot(x_array, scores, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Density', color=color)
    ax2.plot(x_array, densities, color=color)
    ax2.axhline(y=2.08, color='gray', linestyle='--', label='Density = 1')
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title("Dune Simulation")
    plt.grid(True)
    fig.tight_layout()
    plt.savefig("dune_simulation.png")
    plt.show()