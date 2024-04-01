import numpy as np
from numbaclass import numbaclass


from numba import njit
from numba.core import types
from numba.experimental import structref
from numba.core.extending import overload_method, register_jitable

def ExampleIncr(size):
    """
    __init__ will be converted to wrapper function,
    which will return jitted structref instance.
    Use any pure Python here.
    """
    arr_ = np.zeros(size, dtype=np.int64)
    arr_[:] = 3
    return ExampleIncrNB(arr_)

@structref.register
class ExampleIncrNBType(types.StructRef):
    def preprocess_fields(self, fields):
        return tuple((name, types.unliteral(typ)) for name, typ in fields)

class ExampleIncrNB(structref.StructRefProxy):
    def __new__(
        cls,
        arr_
    ):
        return structref.StructRefProxy.__new__(
            cls,
            arr_
        )

    @property
    def arr_(self):
        return get__arr_(self)

    def get_count(self, i):
        return invoke__get_count(self, i)

    def incr(self, i):
        return invoke__incr(self, i)

structref.define_proxy(
    ExampleIncrNB,
    ExampleIncrNBType,
    [
	"arr_"
    ],
)

@njit(cache=True)
def get__arr_(self):
    return self.arr_

@register_jitable
def the__get_count(self, i):
    return self.arr_[i]


@njit(cache=True)
def invoke__get_count(self, i):
    return the__get_count(self, i)

@register_jitable
def the__incr(self, i):
    self.arr_[i] += 1


@njit(cache=True)
def invoke__incr(self, i):
    return the__incr(self, i)

@overload_method(ExampleIncrNBType, "get_count", fastmath=False)
def ol__get_count(self, i):
    return the__get_count

@overload_method(ExampleIncrNBType, "incr", fastmath=False)
def ol__incr(self, i):
    return the__incr