import matplotlib.pyplot as plt
import numpy as np

from dune import *

if __name__ == "__main__":
    length_list = [16, 32, 48, 64]
    scores_list = []

    for length in length_list:
        dune = np.zeros((length,length), dtype=np.int8)
        iter_num = 100000
        scores = np.zeros(iter_num)
        for i in range(iter_num):
            (score, _) = iterate(dune, length)
            scores[i] = score
            if i % 10000 == 0:
                print(f"LENGTH {length}, Iteration {i}: Score = {score}", end="\r")
        
        scores_list.append(scores)

    fig = plt.figure(figsize=(12, 8))
    # plt.tight_layout(pad=5.0)
    plt.rcParams['font.size'] = 14

    for (i, length) in enumerate(length_list):
        scores = scores_list[i][10000:]
        bins = np.logspace(np.log10(1), np.log10(np.max(scores)), 100)
        hist, bin_edges = np.histogram(scores[scores > 0], bins=bins)
        # hist, bin_edges = np.histogram(scores[scores > 0], bins=100)
        hist = hist / len(scores)
        plt.plot(bin_edges[:-1], hist, label=f"LENGTH={length}")

    plt.xlabel('Score')
    plt.ylabel('Density')
    plt.xscale('log')
    plt.yscale('log')
    plt.grid(True)
    plt.legend()
    plt.savefig("ScoreDist.png")
    plt.show()