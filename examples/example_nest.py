import numpy as np
from numbaclass import numbaclass

from examples.example_incr import ExampleIncr


@numbaclass(cache=True)
class ExampleParent:
    def __init__(self, incr: ExampleIncr):
        self.incr = incr

    def evaluate_loop(self, passes):
        """
        More comments
        """
        for i in range(passes):
            pass
            # self.arr_[index] = val
            # self.count.incr(index)


def init(arr_size):
    """
    Pure python init helper function.
    size: Provide size of one-dim array to store counts for child class ExampleIncr
    """
    from examples import example_incr
    
    incr = example_incr.init(arr_size)
    return ExampleParent(incr)

# obj = ExampleParent(3)
# obj.update(0.2, 0)
# obj.update(0.1, 0)
# print( obj.arr_[0] )
# print( obj.count.get_count(0) )
