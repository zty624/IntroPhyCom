import matplotlib.pyplot as plt
import numpy as np

from dune import *

if __name__ == "__main__":
    length_list = [8, 16, 32, 64]
    scores_list = []

    for length in length_list:
        dune = np.zeros((length,length), dtype=np.int8)
        iter_num = 100000
        scores = np.zeros(iter_num)
        for i in range(iter_num):
            (score, density) = iterate(dune, length)
            scores[i] = score
            if i % 10000 == 0:
                print(f"LENGTH {length}, Iteration {i}: Score = {score}, Density = {density:.2f}", end="\r")
        
        scores_list.append(scores)

    fig, ax = plt.subplots(2,2, figsize=(16,16))
    plt.tight_layout(pad=5.0)
    plt.rcParams['font.size'] = 14

    for (i, length) in enumerate(length_list):
        scores = scores_list[i][10000:]
        scores = scores[scores > 0]
        ax[i//2, i%2].hist(np.log10(scores), bins=100, density=True, alpha=0.5, color='red', label=f"LENGTH={length}")
        ax[i//2, i%2].set_title(f"LENGTH={length}")
        ax[i//2, i%2].set_xlabel('log(Score)')
        ax[i//2, i%2].set_ylabel('Density')
        ax[i//2, i%2].set_yscale('log')
        # ax[i//2, i%2].set_xscale('log')
        # ax[i//2, i%2].set_xlim((1,1000))
        ax[i//2, i%2].grid(True)
    
    plt.savefig("ScoreDist.png")
    plt.show()