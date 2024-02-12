import numpy as np

from numbaclass import numbaclass


@numbaclass
class TestClass:
    def __init__(self, a):
        self.b = a
        self.prop1 = None
        self.prop2 = None
        self.prop3 = None

        self.prop1 = np.zeros(10, dtype=np.float64)
        self.prop2 = np.zeros(10, dtype=np.float64)
        self.prop3 = np.zeros(10, dtype=np.float64)

        print("Class Init")
        return

    def method1(self):
        """
        More comments
        """
        # Some
        self.prop1[:] = 1
        print(self.prop1)


obj = TestClass(1)
