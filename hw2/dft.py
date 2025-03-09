import numpy as np
from numpy import complex128 as comp
from numba import jit
import time

def dft(x:np.ndarray, rev:int=1) -> np.ndarray:
    sign = 1 if rev == 1 else -1
    length = len(x)
    res = np.zeros(length, dtype=comp)
    tr_mat_index = np.ones((length, length), dtype=comp)
    for i in range(length):
        tr_mat_index[i,:] *= i
        tr_mat_index[:,i] *= i
    tr_mat = np.exp(sign * 2j * np.pi * tr_mat_index / length, dtype=comp)
    res = np.dot(tr_mat, x) / np.sqrt(len(x), dtype=comp)
    return res

@jit(nopython=True)
def fftjit(x: np.ndarray, rev: int = 1) -> np.ndarray:
    x = x.astype(np.complex128)
    n = x.size
    if (n & (n - 1)) != 0:
        new_n = 1
        while new_n < n:
            new_n <<= 1
        zeros = np.zeros(new_n - n, dtype=np.complex128)
        x = np.concatenate((x, zeros))
        n = new_n
    if n == 1:
        return x
    even = fftjit(x[::2], rev)
    odd = fftjit(x[1::2], rev)
    base = np.exp(rev * 2j * np.pi * np.arange(n // 2) / n)
    return np.concatenate((even + base * odd, even - base * odd))

def fft(x: np.ndarray, rev: int = 1) -> np.ndarray:
    n = x.size
    if n == 1:  return x
    if (n & (n - 1)) != 0:
        new_n = 1 << (n.bit_length())
        x = np.concatenate([x, np.zeros(new_n - n, dtype=x.dtype)])
        n = new_n
    even = fft(x[::2], rev)
    odd = fft(x[1::2], rev)
    base = np.exp(rev * 2j * np.pi * np.arange(n // 2, dtype=comp) / n)
    return np.concatenate([even + base * odd, even - base * odd])

def _timestamp(txt=""):
    global last
    cur = time.time()
    if 'last' in globals() and txt:
        inv = cur - last
        print(f"{txt}: {inv:.6f} s")
        last = cur
        return inv
    else:
        last = cur
        return 

def _dft_test():
    sample = np.random.rand(1 << 4)
    res = dft(sample, -1)
    res_np = np.fft.fft(sample)
    res_np_nor = res_np / np.sqrt(len(res_np))
    diff = np.sum(np.abs(res - res_np_nor))

    import matplotlib.pyplot as plt
    plt.figure(figsize=(10,4))
    plt.plot(np.arange(len(res)), np.abs(res), label="dft")
    plt.plot(np.arange(len(res)), np.abs(res_np), label="np.fft")
    plt.title(f"error: {diff:.3e}")
    plt.legend()
    plt.savefig("hw2/figs/dftcheck.png")
    plt.show()

def _fft_test():
    times = []
    errs = []
    for i in range(5, 25):
        print(1 << i)
        sample = np.random.rand(1 << i)
        _timestamp()
        res = np.fft.fft(sample)
        res = np.fft.ifft(sample)
        times.append(_timestamp("usage"))
        errs.append(np.sum(np.abs(res - sample)))
    
    with open("hw2/fft_results.txt", "r") as f:
        data = f.read()
    cresults = np.array(data.split(), dtype=np.float128).reshape(-1,5)

    fig, axes = plt.subplots(1,2, figsize=(14, 6))
    plt.rcParams['font.size'] = 14
    plt.tight_layout(pad=3)

    axes[0].plot(np.arange(5, 25), times, label="np.fft")
    axes[0].plot(np.arange(5, 25), cresults[:,1], label="fft")
    axes[0].plot(np.arange(5, 25), cresults[:,3], label="iterate fft")
    axes[0].set_xlabel("log2 of sample size")
    axes[0].set_ylabel("time/s")
    axes[0].set_yscale("log")
    axes[0].legend()

    axes[1].plot(np.arange(5, 25), errs, label="np.fft")
    axes[1].plot(np.arange(5, 25), cresults[:,2], label="fft")
    axes[1].plot(np.arange(5, 25), cresults[:,4], label="iterate fft")
    axes[1].set_xlabel("log2 of sample size")
    axes[1].set_ylabel("error")
    axes[1].set_yscale("log")
    axes[1].legend()
    plt.savefig("hw2/figs/ffttime.png")
    plt.show()

def _test():
    '''return a np.ndarray with shape (9, 9)'''
    res = np.zeros((11, 12), dtype=np.float128)
    for index in range(4, 15):
        sample = np.random.rand(1 << index)
        print("sample size:", len(sample))
        _timestamp()
        dft_res = dft(sample, 1)
        res[index - 4, 0] = _timestamp("dft usage")
        idft_res = dft(dft_res, -1)
        res[index - 4, 1] = _timestamp("idft usage")
        res[index - 4, 2] = np.sum(np.abs(idft_res - sample))
        print("errs:", res[index - 4, 2])
        
        _timestamp()
        fft_res = fft(sample, 1) / np.sqrt(len(sample), dtype=comp)
        res[index - 4, 3] = _timestamp("fft usage")
        ifft_res = fft(fft_res, -1) / np.sqrt(len(sample), dtype=comp)
        res[index - 4, 4] = _timestamp("ifft usage") 
        res[index - 4, 5] = np.sum(np.abs(ifft_res - sample))
        print("errs:", res[index - 4, 5])

        _timestamp()
        dft_res = fftjit(sample, 1) / np.sqrt(len(sample), dtype=comp)
        res[index - 4, 6] = _timestamp("jit fft usage")
        ifft_res = fftjit(fft_res, -1) / np.sqrt(len(sample), dtype=comp)
        res[index - 4, 7] = _timestamp("jit ifft usage") 
        res[index - 4, 8] = np.sum(np.abs(ifft_res - sample))
        print("errs:", res[index - 4, 8])

        _timestamp()
        dft_res = np.fft.fft(sample)
        res[index - 4, 9] = _timestamp("np.fft usage")
        idft_res = np.fft.ifft(dft_res)
        res[index - 4, 10] = _timestamp("np.ifft usage")
        res[index - 4, 11] = np.sum(np.abs(idft_res - sample))
        print("errs:", res[index - 4, 11])

    return res

def data():
    path = "hw2/waveform.dat"
    with open(path, "r") as f:
        data = f.read()
    data = np.array(data.split(), dtype=np.float128).reshape(-1, 2)
    length = data.shape[0]
    x = data[:, 0]
    y = data[:, 1]
    res = np.fft.fft(y)
    resmod = np.abs(res)
    freqs = np.fft.fftfreq(length, d=(x[1] - x[0]))
    print(resmod[resmod > 100])     # local max

    plt.figure(figsize=(20,6))
    plt.tight_layout(pad=2)
    plt.rcParams['font.size'] = 20
    plt.plot(freqs, resmod, label="dft")
    plt.xlabel("frequency")
    plt.ylabel("amplitude")
    plt.yscale("log")
    plt.legend()
    # plt.savefig("hw2/figs/fftshow.png")
    plt.xlim(-10, 10)
    plt.xticks(np.arange(-10, 11, 1))
    # plt.show()
    plt.close()

    # frequency filtering
    res[resmod < 100] = 0
    y_filt = np.fft.ifft(res)
    plt.figure(figsize=(20, 6))
    plt.tight_layout(pad=2)
    plt.rcParams['font.size'] = 20
    plt.scatter(x[:3000], y[:3000], s=4, alpha=1, label="original")
    plt.plot(x[:3000], y_filt[:3000], label="filtered", c='r', linewidth=3)
    plt.xlabel("t/s")
    plt.xticks(np.arange(0, 3.1, 0.2))

    plt.ylabel("y")
    plt.legend()
    plt.savefig("hw2/figs/fftretrive.png")
    # plt.show()
    plt.close()

if __name__ == "__main__":
    cresults = [2.09e-5, 2.21e-5, 3.11e-5, 7.28e-5, 0.0001, 0.00021, 0.000459, 0.00128, 0.0021, 0.0045, 0.012]

    import matplotlib.pyplot as plt


    _fft_test()    
    import sys
    sys.exit(0)
    _dft_test()
    data()
    res = _test()

    fig, axes = plt.subplots(1,2, figsize=(14, 6))
    plt.rcParams['font.size'] = 14
    plt.tight_layout(pad=3)

    axes[0].plot(np.arange(4, 15), res[:, 0] + res[:, 1], label="dft")
    axes[0].plot(np.arange(4, 15), res[:, 3] + res[:, 4], label="fft")
    axes[0].plot(np.arange(4, 15), res[:, 6] + res[:, 7], label="jit.fft")
    axes[0].plot(np.arange(4, 15), res[:, 9] + res[:, 10], label="np.fft")
    axes[0].plot(np.arange(4, 15), cresults, label="c++ fft")
    axes[0].set_xlabel("log2 of sample size")
    axes[0].set_ylabel("time/s")
    axes[0].set_yscale("log")
    axes[0].legend()

    axes[1].plot(np.arange(4, 15), res[:, 2], label="dft")
    axes[1].plot(np.arange(4, 15), res[:, 5], label="np.fft")
    axes[1].plot(np.arange(4, 15), res[:, 8], label="fft")
    axes[1].plot(np.arange(4, 15), res[:, 11], label="jit fft")
    axes[1].set_xlabel("log2 of sample size")
    axes[1].set_ylabel("error")
    axes[1].set_yscale("log")
    axes[1].legend()

    plt.savefig("hw2/figs/time.png")
    plt.show()