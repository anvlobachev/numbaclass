import numpy as np

from numbaclass import numbaclass


@numbaclass
class TestClass:
    def __init__(self, a):
        """
        Init routines
        """

        self.prop1 = np.zeros(a, dtype=np.float64)
        self.prop2 = np.zeros(a, dtype=np.float64)
        print("Init done")

    def incr_prop1(self):
        """
        More comments
        """
        self.prop1[:] += 1

    def check_me(self):
        # print("Me checked")
        return "Me checked"


obj = TestClass(3)
# obj.incr_prop1()

print(obj)
