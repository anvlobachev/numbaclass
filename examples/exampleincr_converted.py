import numpy as np
from numbaclass import numbaclass


from numba import njit
from numba.core import types
from numba.experimental import structref
from numba.core.extending import overload_method, register_jitable

"""
Test setters

"""


class ExampleIncr(structref.StructRefProxy):
    def __new__(
        cls,
        arr_,
        total_count
    ):
        return structref.StructRefProxy.__new__(
            cls,
            arr_,
            total_count
        )

    @property
    def arr_(self):
        return get__arr_(self)

    @property
    def total_count(self):
        return get__total_count(self)

    def get_count(self, i):
        return invoke__get_count(self, i)

    def incr(self, i, val):
        return invoke__incr(self, i, val)

@njit(cache=True)
def get__arr_(self):
    return self.arr_

@njit(cache=True)
def get__total_count(self):
    return self.total_count

@register_jitable
def the__get_count(self, i):
    return self.arr_[i]


@njit(cache=True)
def invoke__get_count(self, i):
    return the__get_count(self, i)

@register_jitable
def the__incr(self, i, val):
    self.arr_[i] += val
    self.total_count += val


@njit(cache=True)
def invoke__incr(self, i, val):
    return the__incr(self, i, val)


@structref.register
class ExampleIncrType(types.StructRef):
    def preprocess_fields(self, fields):
        return tuple((name, types.unliteral(typ)) for name, typ in fields)

structref.define_proxy(
    ExampleIncr,
    ExampleIncrType,
    [
	"arr_",
	"total_count"
    ],
)

@overload_method(ExampleIncrType, "get_count", fastmath=False)
def ol__get_count(self, i):
    return the__get_count

@overload_method(ExampleIncrType, "incr", fastmath=False)
def ol__incr(self, i, val):
    return the__incr



if __name__ == "__main__":

    arr_ = np.zeros(3, dtype=np.int64)
    obj = ExampleIncr(arr_, 0)

    obj.incr(0, 1)
    obj.incr(0, 1)
    print(obj.get_count(0))
    print("obj.total_count: ", obj.total_count )
    # reset total_count
    
    # obj.total_count = 0
    print("obj.total_count: ", obj.total_count )