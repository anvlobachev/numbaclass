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
        Numbaclass will convert __init__ to wrapper for structref.
        Safely perform routines in pure Python here to setup inputs for structref.

        .self properties must be compatible with Numba requirements
        """

        self.prop1 = np.zeros(n, dtype=np.float64)
        self.prop2 = np.zeros(n, dtype=np.float64)

        self.prop1[:] = 7  # Property variation
        print("Init done")

    # (pyobject, int64,)
    # (float64[:], int64,)
    #
    def incr_prop1(
        self,
        val: int,
        # Multiline args
        # Multiline args
    ) -> None:  # Trailing comment and annotations
        """
        More comments
        """
        self.prop1[:] += val

    def check_me(self):
        print(self.prop1)


obj = TestExample(4)
obj.incr_prop1(1)
obj.incr_prop1(3)
obj.check_me()


print(obj)
