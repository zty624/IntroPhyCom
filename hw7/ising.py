import matplotlib.pyplot as plt
import numpy as np
import os
import re

def txt_list(path="./hw7"):
    return [f for f in os.listdir(path) if f.endswith('.txt') and f.startswith("lattice")]

def corr_func(m1:np.ndarray, m2:np.ndarray) -> np.ndarray:
    """
    calculate the correlation function between two matrices.
    $Cuv (r) = <su(R) * sv(R+r)>$
    """
    corr_matrix = np.zeros_like(m1)
    for i in range(m1.shape[0]):
        for j in range(m1.shape[1]):
            newm2 = np.roll(m2, -j, axis=1)
            newm2 = np.roll(newm2, -i, axis=0)
            corr_matrix[i, j] = np.sum(m1 * newm2) / m1.size
    return corr_matrix

if __name__ == "__main__":
    for i, file in enumerate(txt_list()):
        print(f"{i}. {file}")
    cmd = input("Select a file to plot corr func: ")

    filename = txt_list()[int(cmd)]
    match = re.search(r'lattice_(\d+)_', filename)
    if not match:
        raise ValueError("Lattice size not found in file name.")

    # read the file
    lattice_size = int(match.group(1))
    lattice_list = []
    minEnergy = -4 * lattice_size * lattice_size

    with open(os.path.join("./hw7", filename), "r") as f:
        lines = f.readlines()
        demo = np.zeros((lattice_size, lattice_size * 2))
        for i in range(0, len(lines), lattice_size + 2):
            for idx in range(lattice_size):
                line = lines[i + idx]
                # replace +/- by 1/-1
                line = line.replace("+", "1")
                line = line.replace("-", "-1")
                # convert to numpy array
                line_array = np.array([int(x) for x in line.split()])
                demo[idx, :] = line_array
            
            lattice_list.append(demo)
            demo = np.zeros((lattice_size, lattice_size * 2))

            # check the energy
            energy = int(lines[i + lattice_size].rstrip('\n'))
            if energy < minEnergy:
                print(f"New Energy found {energy} < {minEnergy} at {i}")
    
    for i in range(3):
        xygrid = np.meshgrid(np.arange(lattice_size), np.arange(lattice_size))
        plt.figure()
        plt.scatter(xygrid[0], xygrid[1], c=lattice_list[i][:, ::2].flatten(), cmap='RdBu', vmin=-1, vmax=1)
        plt.scatter(xygrid[0] + 0.5, xygrid[1] + 0.5, c=lattice_list[i][:, 1::2].flatten(), cmap='RdBu', vmin=-1, vmax=1)
        plt.colorbar()
        plt.clim(-1, 1)
        plt.xlabel("x")
        plt.ylabel("y")
        plt.savefig(f"hw7/figs/{lattice_size}_{i}.png")
        pass

    corr_matrix_mean = np.zeros((lattice_size, lattice_size))
    matrix_A_mean = np.zeros((lattice_size, lattice_size))
    matrix_B_mean = np.zeros((lattice_size, lattice_size))
    for i, lattice in enumerate(lattice_list):
        if np.sum(lattice) != 0:
            raise ValueError("lattice is not balanced")
        # matrix_A_mean += lattice[:, ::2]
        # matrix_B_mean += lattice[:, 1::2]
        matrix_A = lattice[:, ::2]
        matrix_B = lattice[:, 1::2]
        corr_matrix = corr_func(matrix_A, matrix_B)
        corr_matrix_mean += corr_matrix
    corr_matrix_mean /= len(lattice_list)

    plt.figure()
    plt.imshow(corr_matrix_mean, cmap='RdBu', vmin=-1, vmax=1, origin='lower',
                    extent=[0, lattice_size, 0, lattice_size], aspect='auto')
    # for (j, i), val in np.ndenumerate(corr_matrix_mean):
    #     plt.text(i + 0.5, j + 0.5, f'{val:.2f}', ha='center', va='center', fontsize=8)
    plt.colorbar()
    plt.clim(-1, 1)
    plt.title(f"Correlation function for size {lattice_size}")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.xticks(np.arange(0, lattice_size + 1))
    plt.yticks(np.arange(0, lattice_size + 1))
    plt.grid(which='both', color='gray', linestyle='--', linewidth=0.5)
    plt.savefig(f"hw7/figs/corr_matrix_{lattice_size}.png")
    plt.show()