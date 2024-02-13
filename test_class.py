import numpy as np

from numbaclass import numbaclass


@numbaclass
class TestClass:
    def __init__(self, a):

        self.prop1 = np.zeros(a, dtype=np.float64)
        self.prop2 = np.zeros(a, dtype=np.float64)

    def incr_prop1(self):
        """
        More comments
        """
        self.prop1[:] += 1


obj = TestClass(3)
obj.incr_prop1()

print(obj.prop1)
