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

    def incr(self, i):
        self.arr_[i] += 1

    def get_count(self, i):
        return self.arr_[i]
