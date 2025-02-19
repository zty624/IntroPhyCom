import numpy as np

LENGTH = 32

def islegal(coor, length=LENGTH):
    (row, col) = coor
    if row < 0 or row >= length or col < 0 or col >= length:
        return False
    return True

def neighbors(coors, length=LENGTH):
    res = []
    for coor in coors:
        res_list = [(coor[0]-1, coor[1]), (coor[0]+1, coor[1]),
                    (coor[0], coor[1]-1), (coor[0], coor[1]+1)]
        for i in res_list:
            if islegal(i, length):
                res.append(i)
    return res

def depletion(dune, init_coor, length=LENGTH):
    coors = [init_coor]
    score = 0
    while len(coors) > 0:
        (row, col) = coors.pop(0)
        if dune[row, col] < 4:
            continue
        dune[row, col] -= 4
        score += 1
        for (row_n, col_n) in neighbors([(row, col)], length):
            dune[row_n, col_n] += 1
        coors.extend(neighbors([(row, col)], length))
    return score

def iterate(dune, length=LENGTH):
    """put a block on the length"""
    row = np.random.randint(0, length)
    col = np.random.randint(0, length)
    dune[row, col] += 1
    score = depletion(dune, (row, col), length)
    density = np.sum(dune) / (length * length)
    return (score, density)
