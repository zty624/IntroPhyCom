import matplotlib.pyplot as plt
import numpy as np

path = "hw10/output.txt"
data_dict = {}

with open(path, "r") as f:
    p = None
    while True:
        line = f.readline()
        if not line:
            break
        if line.startswith("p"):
            p = int(line.lstrip("p = ").rstrip("\n"))
            data_dict[p] = []
        else:
            data_dict[p].append(list(map(float, line.rstrip("\n").split())))

length = len(data_dict)
l_sqr = int(np.ceil(length ** 0.5))

fig, axes = plt.subplots(l_sqr, l_sqr, figsize=(16, 16))
plt.tight_layout(pad=3)
idx = 0
for key, value in data_dict.items():
    data_dict[key] = np.array(value)
    axes[idx // l_sqr, idx % l_sqr].hist(data_dict[key][:, 0], bins=50, range=(0, 1), alpha=0.5, label=f"p = {key}", density=True)
    axes[idx // l_sqr, idx % l_sqr].legend()
    axes[idx // l_sqr, idx % l_sqr].set_title(f"p = {key}")
    axes[idx // l_sqr, idx % l_sqr].set_xlabel("Similarity")
    axes[idx // l_sqr, idx % l_sqr].set_ylabel("Density")
    idx += 1
plt.show()
