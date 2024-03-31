import numpy as np
from numbaclass import numbaclass

from examples.example_incr import ExampleIncr


@numbaclass(cache=True)
class ExampleNest:
    def __init__(self, size):
        self.arr_ = np.zeros(size, dtype=np.float64)
        self.count = ExampleIncr(size)

    def update(self, val, index):
        """
        More comments
        """
        self.arr_[index] = val
        self.count.incr(index)


# obj = ExampleParent(3)
# obj.update(0.2, 0)
# obj.update(0.1, 0)
# print( obj.arr_[0] )
# print( obj.count.get_count(0) )
