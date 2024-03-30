import numpy as np
from numbaclass import numbaclass

from examples.example_to_nest import ExampleToNest


@numbaclass(cache=True)
class ExampleParent:
    def __init__(self, n, m):
        self.arr1 = np.zeros(n, dtype=np.float64)
        self.arr2 = np.zeros(m, dtype=np.float64)
        self.nested_struct = ExampleToNest(2)

    def action(self):
        """
        More comments
        """
        self.nested_struct.store_len(0, len(self.arr1))
        self.nested_struct.store_len(1, len(self.arr2))

    # No type hints
    def check_me(self):
        print("self.nested_struct: ", self.nested_struct)


# obj = ExampleParent(4, 5)
# obj.action()
# obj.check_me()
