# Variations with comments, annotations and hints for
# testing purposes.

# from numbaclass import numbaclass
import numpy as np


class ExampleFormat:
    def __init__(self, prop1):
        self.prop1 = prop1


    def incr_prop1(
        self,
        val: int,
        # Multiline args
        # Multiline args
    ) -> None:  # Trailing comment and annotations
        """
        Doc
        """
        self.prop1[:] += val

    # No type hints
    def check_me(self):
        print(self.prop1)


def init(n):
    """
    This is init wrapper for jittable classes.
    Use it if pure python routines is needed to prepare inputs for jitted class.

    If jitted class is initialized inside other jitted function 
    use decorated (by @numbaclass) class directly.

    """

    prop1 = np.zeros(n, dtype=np.float64)
    
    obj = ExampleFormat(prop1)
    
    return obj


obj = ExampleFormat(np.zeros(5, dtype=np.float64))
obj.incr_prop1(1)
# obj.incr_prop1(3)
# obj.check_me()

# print(obj)
