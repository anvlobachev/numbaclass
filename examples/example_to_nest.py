import numpy as np
from numbaclass import numbaclass


@numbaclass(cache=True)
class ExampleToNest:
    def __init__(self, n):
        """
        n : count of arrays to remember len val
        """
        self.len_val = np.zeros(n, dtype=np.int64)

    def store_len(self, n, val):
        self.len_val[n] = val

    def check_len(self):
        print("Lengths: ", self.len_val)


# obj = ExampleToNest(2)
# obj.store_len(0, 3)
# obj.store_len(1, 2)
# obj.check_len()

# print(obj)
