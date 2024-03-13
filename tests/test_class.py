from numbaclass import numbaclass
import numpy as np

# import os
# os.environ["NUMBACLS_BYPASS"] = "0"
# from numba.extending import overload, register_jitable
# from numba import njit


@numbaclass(cache=True)
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

    # void(int64,)
    # (pyobject, int64,)
    # (float64[:], int64,)
    #
    def incr_prop1(
        self,
        val: int,
        #
        #
        #
    ) -> None:  # Trailing comment and annotations
        """
        More comments
        """
        self.prop1[:] += val

    # New line
    #
    def check_me(self):
        print(self.prop1)


obj = TestExample(4)
obj.incr_prop1(1)
obj.incr_prop1(3)
obj.check_me()


print(obj)
