import numpy as np
from numbaclass import numbaclass

from examples.example_incr import ExampleIncr


from numba import njit
from numba.core import types
from numba.experimental import structref
from numba.core.extending import overload_method, register_jitable

def ExampleNest(size):
    arr_ = np.zeros(size, dtype=np.float64)
    count = ExampleIncr(size)
    return ExampleNestNB(arr_, count)

@structref.register
class ExampleNestNBType(types.StructRef):
    def preprocess_fields(self, fields):
        return tuple((name, types.unliteral(typ)) for name, typ in fields)

class ExampleNestNB(structref.StructRefProxy):
    def __new__(
        cls,
        arr_,
        count
    ):
        return structref.StructRefProxy.__new__(
            cls,
            arr_,
            count
        )

    @property
    def arr_(self):
        return get__arr_(self)

    @property
    def count(self):
        return get__count(self)

    def update(self, val, index):
        return invoke__update(self, val, index)

structref.define_proxy(
    ExampleNestNB,
    ExampleNestNBType,
    [
	"arr_",
	"count"
    ],
)

@njit(cache=True)
def get__arr_(self):
    return self.arr_

@njit(cache=True)
def get__count(self):
    return self.count

@register_jitable
def the__update(self, val, index):
    """
    More comments
    """
    self.arr_[index] = val
    self.count.incr(index)


@njit(cache=True)
def invoke__update(self, val, index):
    return the__update(self, val, index)

@overload_method(ExampleNestNBType, "update", fastmath=False)
def ol__update(self, val, index):
    return the__update