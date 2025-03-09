import matplotlib.pyplot as plt
import numpy as np

DATA = np.fromfile('waveform.dat', dtype=np.float32, sep='	').reshape(-1, 2)

if __name__ == "__main__":
    fig, axes = plt.subplots(2, 1, figsize=(10, 8)) 
    fig.tight_layout(pad=3.0)

    axes[0].plot(DATA[:, 0], DATA[:, 1])
    axes[0].set_xlabel("x")
    axes[0].set_ylabel("f(x)")
    axes[0].set_title("Original Data")



    plt.show()
