from numbaclass import numbaclass
import numpy as np


@numbaclass(cache=True, writeout=True)
class TestExample:
    def __init__(
        self,
        n,
        #
        #
        #
        # z
    ):
        """
        Init routines2
        Init routines3
        """

        self.prop1 = np.zeros(n, dtype=np.float64)
        self.prop2 = np.zeros(n, dtype=np.float64)
        print("Init done")

    def incr_prop1(
        self,
        #
        #
        #
        #
    ):
        """
        More comments
        """
        self.prop1[:] += 1

    def check_me(self):
        print(self.prop1)


obj = TestExample(4)
obj.incr_prop1()
obj.incr_prop1()
obj.check_me()


print(obj)
