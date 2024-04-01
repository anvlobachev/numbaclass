# Variations with comments, annotations and hints for
# testing purposes.

# from numbaclass import numbaclass
import numpy as np


# @numbaclass
# @numbaclass(cache=True)
class ExampleFormat:
    def __init__(self, n):
        """
        Numbaclass will convert __init__ to wrapper function,
        which will return jitted structref instance.
        Use pure Python and any modules here to process data for structref inputs.

        Note self. attributes have to be assigned with
        Numba compatible data types and objects.
        """

        self.prop1 = np.zeros(n, dtype=np.float64)  # self. in comment
        self.prop2 = np.zeros(n, dtype=np.float64)

        tmp = 3 + 5
        self.prop1[:] = tmp  # Property variation

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


# obj = ExampleFormat(4)
# obj.incr_prop1(1)
# obj.incr_prop1(3)
# obj.check_me()

# print(obj)
