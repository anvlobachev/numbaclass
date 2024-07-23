import numpy as np
from numbaclass import numbaclass


@numbaclass(cache=True)
class ExampleIncr:
    def __init__(self, arr_, total_count):
        self.arr_ = arr_
        self.total_count = total_count

    def incr(self, i, val):
        self.arr_[i] += val
        self.total_count += val

    def get_count(self, i):
        return self.arr_[i]


def init(size):
    """
    Pure python init helper function.
    size: Provide size of one-dim array to store counts
    """
    arr_ = np.zeros(size, dtype=np.int64)
    return ExampleIncr(arr_, 0)


if __name__ == "__main__":
    obj = init(3)
    obj.incr(0, 1)
    obj.incr(0, 1)
    print(obj.get_count(0))
    print("obj.total_count: ", obj.total_count )
    # reset total_count

    obj.total_count = 0
    print("obj.total_count: ", obj.total_count )

