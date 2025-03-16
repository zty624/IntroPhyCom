import numpy as np
from typing import Callable, Tuple

class RK45Coefficients:
    '''base class of RK45 coeffs'''
    def __init__(self):
        self.a: np.ndarray  # 节点系数
        self.b: np.ndarray  # 权重系数矩阵
        self.c: np.ndarray  # 4阶解系数
        self.d: np.ndarray  # 5阶解系数
    
    def get(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        return self.a, self.b, self.c, self.d

class DormandPrince(RK45Coefficients):
    def __init__(self):
        super().__init__()
        self.a = np.array([0, 1/5, 3/10, 4/5, 8/9, 1])
        self.b = np.array([
            [0, 0, 0, 0, 0, 0],
            [1/5, 0, 0, 0, 0, 0],
            [3/40, 9/40, 0, 0, 0, 0],
            [44/45, -56/15, 32/9, 0, 0, 0],
            [19372/6561, -25360/2187, 64448/6561, -212/729, 0, 0],
            [9017/3168, -355/33, 46732/5247, 49/176, -5103/18656, 0]
        ])
        self.c = np.array([35/384, 0, 500/1113, 125/192, -2187/6784, 11/84])
        self.d = np.array([5179/57600, 0, 7571/16695, 393/640, -92097/339200, 187/2100])

class CashKarp(RK45Coefficients):
    def __init__(self):
        super().__init__()
        self.__a = np.array([0, 1/5, 3/10, 3/5, 1, 7/8])
        self.__b = np.array([
            [0, 0, 0, 0, 0, 0],
            [1/5, 0, 0, 0, 0, 0],
            [3/40, 9/40, 0, 0, 0, 0],
            [3/10, -9/10, 6/5, 0, 0, 0],
            [-11/54, 5/2, -70/27, 35/27, 0, 0],
            [1631/55296, 175/512, 575/13824, 44275/110592, 253/4096, 0]
        ])
        self.__c = np.array([37/378, 0, 250/621, 125/594, 0, 512/1771])
        self.__d = np.array([2825/27648, 0, 18575/48384, 13525/55296, 277/14336, 1/4])

class Event:
    def __init__(self, kill: bool = False) -> None:
        self.kill = kill
    
    def detect(self, t: np.float64, y4: np.ndarray, y5: np.ndarray, err: np.float64) -> bool:
        raise NotImplementedError

    def handle(self, t: np.float64, y4: np.ndarray, y5: np.ndarray, err: np.float64) -> None:
        raise NotImplementedError

class RK45Iterator():
    def __init__(self,
                 f: Callable[[np.float64, np.ndarray], np.ndarray],
                 y0: np.ndarray,
                 t0: np.float64,
                 t1: np.float64,
                 events: list[Event] = [],
                 constants: RK45Coefficients = DormandPrince()) -> None:
        self.f = f
        self.y0 = y0
        self.t0 = t0
        self.t1 = t1
        self.events = events
        self.constants = constants
        self.a, self.b, self.c, self.d = self.constants.get()

        self.t = t0
        self.y = y0
        self.i = 0
    
    def __iter__(self):
        return self
    
    def __next__(self) -> Tuple[np.float64, np.ndarray]:
        raise NotImplementedError
    
    def iterate(self, step) -> Tuple[np.ndarray, np.ndarray, np.float64]:
        k = np.zeros((6, len(self.y)))
        k[0] = self.f(self.t, self.y)
        for i in range(1, 6):
            sum_bk = sum(self.b[i][j] * k[j] for j in range(i))
            k[i] = self.f(self.t + self.a[i] * step,
                          self.y + step * sum_bk)

        y4 = self.y + step * np.dot(self.c, k)
        y5 = self.y + step * np.dot(self.d, k)
        error = np.linalg.norm(y5 - y4) / np.sqrt(len(self.y))
        return (y4, y5, error)
    
    def _event_check(self, y4:np.ndarray, y5:np.ndarray, err:np.float64) -> None:
        for event in self.events:
            if event.detect(self.t, y4, y5, err):
                if event.kill:
                    raise StopIteration
                else:
                    self.t, y4, y5, err = event.handle(self.t, y4, y5, err)
        self.y = y4.copy()
    
class RK45FixedIterator(RK45Iterator):
    def __init__(self, f, y0, t0, t1, events = [], constants = DormandPrince(),
                 step:float = 1e-3):
        super().__init__(f, y0, t0, t1, events, constants)
        self.step = step
        self.n = int((t1 - t0) / step)
    
    def __next__(self) -> Tuple[np.float64, np.ndarray]:
        if self.i >= self.n:
            raise StopIteration
        self.i += 1
        self.t = self.t0 + (self.i) * self.step
        y4, y5, err = self.iterate(self.step)
        self._event_check(y4, y5, err)
        return (self.t, self.y)

class RK45AutoIterator(RK45Iterator):
    def __init__(self, f, y0, t0, t1, events = [], constants = DormandPrince(),
                 step:np.float64 = 1e-3,
                 tol:np.float64 = 1e-6,
                 max_step:np.float64 = np.inf,
                 min_step:np.float64 = 1e-12):
        super().__init__(f, y0, t0, t1, events, constants)
        self.tol = tol
        self.step = step
        self.max_step = max_step
        self.min_step = min_step

    def __next__(self) -> Tuple[float, np.ndarray]:
        if self.step < self.min_step or self.step > self.max_step:
            raise StopIteration

        y4, y5, error = self.iterate(self.step)
        if error < self.tol:
            self.t += self.step
            self.y = y5.copy()
            delta = 0.9 * (self.tol / error)**0.2
            self.step = min(self.max_step, self.step * delta)
            return (self.t, self.y)
        else:
            delta = 0.9 * (self.tol / error)**0.25
            self.step = max(0.1 * self.step, self.step * delta)
            return self.__next__()