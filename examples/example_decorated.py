import numpy as np
from numbaclass import numbaclass


@numbaclass(cache=False)
class ExampleDecorated:
    def __init__(self, n):
        """
        Numbaclass will convert __init__ to wrapper function,
        which will return jitted structref instance.
        It's safe to use pure Python and any modules here to fetch data and
        process values for structref inputs.

        Note that, instance properties with  must be
        compatible with Numba requirements.

        """

        self.prop1 = np.zeros(n, dtype=np.float64)
        self.prop2 = np.zeros(n, dtype=np.float64)

        self.prop1[:] = 7  # Property variation
        print("Init done")

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

    # No type hints
    def check_me(self):
        print(self.prop1)


obj = ExampleDecorated(4)
obj.incr_prop1(1)
obj.incr_prop1(3)
obj.check_me()

print(obj)
