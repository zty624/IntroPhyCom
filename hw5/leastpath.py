from typing import Tuple
import subprocess
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Pool, cpu_count

NUM = 30000
NMAX = 100

def cppmain(n: list):
    process = subprocess.Popen(
        ["./main"],
        stdin   = subprocess.PIPE,
        stdout  = subprocess.PIPE,
        text=True
    )
    stdin = " ".join(map(str, n))
    stdout, _ = process.communicate(input=stdin)
    output = stdout.strip().split()
    output = list(map(int, output))
    process.kill()
    return output

def pymain(n:int) -> Tuple[float, int]:
    heap = np.random.rand(n, n)
    path = np.zeros_like(heap, dtype=np.int32)

    for i in range(heap.shape[0] - 1, 0, -1):
        path[i-1][:i] = heap[i][:i] > heap[i][1:i+1]
        addindex = np.arange(i) + path[i-1][:i]
        heap[i-1][:i] += heap[i, addindex]

    x = 0
    for i in range(heap.shape[0] - 1):
        x = int(x)
        x += path[i][x]
    return heap[0][0], x

def worker(i):
    print(f"Size: {i}")
    data = [i] * NUM
    return cppmain(data)

if __name__ == "__main__":
    pool = Pool(cpu_count() - 1)

    results = pool.map(worker, range(1, NMAX + 1))
    data = np.array(results)

    pool.close()
    pool.join()

    x = np.arange(data.shape[0])
    y = np.std(data, axis=1)
    logx = np.log10(x)[2:]
    logy = np.log10(y)[2:]

    A = np.vstack([logx, np.ones_like(logx)]).T
    m, c = np.linalg.lstsq(A, logy, rcond=None)[0]
    print(f"m: {m:.6f}, c: {c:.6f}")

    # show std
    fig = plt.figure(figsize=(8,6))
    plt.rcParams["font.size"] = 16
    plt.plot(logx, m * logx + c, label=f"linear fit: y = {m:.3f}x + {c:.3f}")
    plt.plot(logx, logy, label="simulation")
    # plt.plot(x,y)
    plt.xlabel("log N")
    plt.ylabel("log w(N)")
    # plt.xlabel("N")
    # plt.ylabel("w(N)")
    # plt.xscale("log")
    # plt.yscale("log")
    plt.grid()
    plt.legend()
    plt.savefig("stdlog.png")
    plt.show()