# Variations with comments, annotations and hints for
# testing purposes.

# from numbaclass import numbaclass
import numpy as np

class ExampleIncrTestfrmt:
    def __init__(self, arr_):
        self.arr_ = arr_

    def incr(
        self,
        i: int,
        val: int,
        # Multiline args
        # Multiline args
    ) -> None:  # Trailing comment and annotations
        """
        Doc
        """
        self.arr_[i] += val

    # No type hints
    def check_me(self):
        print(self.arr_)


def init(n):
    """
    This is init wrapper for jittable classes.
    Use it if pure python routines is needed to prepare inputs for jitted class.

    If jitted class is initialized inside other jitted function 
    use decorated (by @numbaclass) class directly.

    """

    prop1 = np.zeros(n, dtype=np.float64)
    obj = ExampleIncrTestfrmt(prop1)
    return obj


# obj = ExampleFormat(np.zeros(5, dtype=np.float64))
# obj.incr_prop1(1)
# obj.incr_prop1(3)
# obj.check_me()

# print(obj)
