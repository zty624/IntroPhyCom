import matplotlib.pyplot as plt
import numpy as np
import os
import re

output_dir = "./hw8/output"
regex = r"box(\d+)_temp(\d+\.\d+).txt"

def output_list(path="./hw8"):
    return [f for f in os.listdir(path) if f.endswith('.txt')]

def read(filename):
    res_ls = []
    with open(os.path.join(output_dir, filename), "r") as f:
        lines = f.readlines()
        params = lines[0].rstrip("\n").split(" ")
        boxsize = int(params[2])

        for i in range(0, len(lines), boxsize + 2):
            params = lines[i].rstrip("\n").split(" ")
            res_ls.append(list(map(int, params[3:])))
    return res_ls

if __name__ == "__main__":
    data = {8: {}, 16: {}, 32: {}}

    data_ls = output_list(output_dir)
    for datapath in data_ls:
        # match
        match = re.match(regex, datapath)
        if match:
            boxsize = int(match.group(1))
            temp = float(match.group(2))
            data[boxsize][temp] = read(datapath)
    
    temp_np = np.arange(1.5, 3.0, 0.1, endpoint=True)
    m2_np   = np.zeros((len(temp_np), 3))
    c_np    = np.zeros((len(temp_np), 3))
    chi_np  = np.zeros((len(temp_np), 3))
    for (boxsize, value) in data.items():
        match boxsize:
            case 8: idx = 0;
            case 16: idx = 1;
            case 32: idx = 2;
        for (temp, data) in value.items():
            temp_idx = int((temp - 1.5) / 0.1)
            data_np = np.array(data)
            e_np = data_np[:, 0]; m_np = data_np[:, 1]
            e_mean = np.mean(e_np); e2_mean = np.mean(e_np ** 2)
            m_mean = np.mean(m_np); m2_mean = np.mean(m_np ** 2)
            m_absmean = np.mean(np.abs(m_np))
            m2_np[idx, temp_idx] = m2_mean
            c_np[idx, temp_idx] = (e2_mean - e_mean ** 2) / (temp ** 2)
            chi_np[idx, temp_idx] = (m2_mean - m_absmean ** 2) / temp

    # Plotting
    plt.figure()
    m2_hist, m2_bins = np.histogram(m2_np, bins=200, density=True)
    plt.plot(m2_bins[:-1], m2_hist, label="m2 histogram")
    plt.show()


    # energy_hist, bins = np.histogram(energy_list,
    #                                  bins=200,
    #                                  density=True,
    #                                  range=(min(energy_list) - 1, max(energy_list) + 1))
    # plt.figure()
    # plt.plot(bins[:-1], energy_hist, label="Energy histogram")
    # plt.xlabel("Energy")
    # plt.ylabel("Frequency")
    # plt.title(f"Energy distribution for {filename}")
    # plt.show()



    #     lines = f.readlines()

    #     demo = np.zeros((lattice_size, lattice_size * 2))
    #     for i in range(0, len(lines), lattice_size + 2):
    #         for idx in range(lattice_size):
    #             line = lines[i + idx]
    #             # replace +/- by 1/-1
    #             line = line.replace("+", "1")
    #             line = line.replace("-", "-1")
    #             # convert to numpy array
    #             line_array = np.array([int(x) for x in line.split()])
    #             demo[idx, :] = line_array
            
    #         lattice_list.append(demo)
    #         demo = np.zeros((lattice_size, lattice_size * 2))

    #         # check the energy
    #         energy = int(lines[i + lattice_size].rstrip('\n'))
    #         if energy < minEnergy:
    #             print(f"New Energy found {energy} < {minEnergy} at {i}")
    
    # for i in range(3):
    #     xygrid = np.meshgrid(np.arange(lattice_size), np.arange(lattice_size))
    #     plt.figure()
    #     plt.scatter(xygrid[0], xygrid[1], c=lattice_list[i][:, ::2].flatten(), cmap='RdBu', vmin=-1, vmax=1)
    #     plt.scatter(xygrid[0] + 0.5, xygrid[1] + 0.5, c=lattice_list[i][:, 1::2].flatten(), cmap='RdBu', vmin=-1, vmax=1)
    #     plt.colorbar()
    #     plt.clim(-1, 1)
    #     plt.xlabel("x")
    #     plt.ylabel("y")
    #     plt.savefig(f"hw7/figs/{lattice_size}_{i}.png")
    #     pass

    # corr_matrix_mean = np.zeros((lattice_size, lattice_size))
    # matrix_A_mean = np.zeros((lattice_size, lattice_size))
    # matrix_B_mean = np.zeros((lattice_size, lattice_size))
    # for i, lattice in enumerate(lattice_list):
    #     if np.sum(lattice) != 0:
    #         raise ValueError("lattice is not balanced")
    #     # matrix_A_mean += lattice[:, ::2]
    #     # matrix_B_mean += lattice[:, 1::2]
    #     matrix_A = lattice[:, ::2]
    #     matrix_B = lattice[:, 1::2]
    #     corr_matrix = corr_func(matrix_A, matrix_B)
    #     corr_matrix_mean += corr_matrix
    # corr_matrix_mean /= len(lattice_list)

    # plt.figure()
    # plt.imshow(corr_matrix_mean, cmap='RdBu', vmin=-1, vmax=1, origin='lower',
    #                 extent=[0, lattice_size, 0, lattice_size], aspect='auto')
    # # for (j, i), val in np.ndenumerate(corr_matrix_mean):
    # #     plt.text(i + 0.5, j + 0.5, f'{val:.2f}', ha='center', va='center', fontsize=8)
    # plt.colorbar()
    # plt.clim(-1, 1)
    # plt.title(f"Correlation function for size {lattice_size}")
    # plt.xlabel("x")
    # plt.ylabel("y")
    # plt.xticks(np.arange(0, lattice_size + 1))
    # plt.yticks(np.arange(0, lattice_size + 1))
    # plt.grid(which='both', color='gray', linestyle='--', linewidth=0.5)
    # plt.savefig(f"hw7/figs/corr_matrix_{lattice_size}.png")
    # plt.show()