import numpy as np
from numbaclass import numbaclass


@numbaclass(cache=True)
class ExampleIncr:
    def __init__(self, size):
        """
        __init__ will be converted to wrapper function,
        which will return jitted structref instance.
        Use any pure Python here.
        """
        self.arr_ = np.zeros(size, dtype=np.int64)
        self.arr_[:] = 3  # Arbitrary assign

        self.incr_val = 1

    def incr(self, i):
        self.arr_[i] += self.incr_val

    def get_count(self, i):
        return self.arr_[i]
