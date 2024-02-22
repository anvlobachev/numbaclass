import numpy as np

from numbaclass import numbaclass


@numbaclass
class TestExample:
    def __init__(self, n):
        """
        Init routines
        """

        self.prop1 = np.zeros(n, dtype=np.float64)
        self.prop2 = np.zeros(n, dtype=np.float64)
        print("Init done")

    def incr_prop1(self):
        """
        More comments
        """
        self.prop1[:] += 1

    def check_me(self):
        print(self.prop1)


obj = TestExample(3)
obj.incr_prop1()
obj.check_me()


print(obj)
