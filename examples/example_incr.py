import numpy as np
from numbaclass import numbaclass


@numbaclass(cache=True)
class ExampleIncr:
    def __init__(self, arr_, incr_val):
        self.arr_ = arr_
        self.incr_val = incr_val

    def incr(self, i):
        self.arr_[i] += self.incr_val

    def get_count(self, i):
        return self.arr_[i]


def init(size):
    arr_ = np.zeros(size, dtype=np.int64)
    arr_[:] = 3
    incr_val = 1
    return ExampleIncr(arr_, incr_val)


if __name__ == "__main__":
    obj = init(3)
    obj.incr(0)
    obj.incr(0)
    print(obj.get_count(0))
