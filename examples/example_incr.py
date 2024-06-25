import numpy as np
from numbaclass import numbaclass


# @numbaclass(cache=True)
class ExampleIncr:
    def __init__(self, arr_):
        self.arr_ = arr_

    def incr(self, i, val):
        self.arr_[i] += val

    def get_count(self, i):
        return self.arr_[i]


def init(size):
    """
    size: Provide size of one-dim array to store counts
    """
    arr_ = np.zeros(size, dtype=np.int64)
    arr_[:] = 3
    return ExampleIncr(arr_)


if __name__ == "__main__":
    obj = init(3)
    obj.incr(0)
    obj.incr(0)
    print(obj.get_count(0))
