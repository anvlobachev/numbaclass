import numpy as np
from numbaclass import numbaclass



from numba import njit
from numba.core import types
from numba.experimental import structref
from numba.core.extending import overload_method, register_jitable


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

    @arr_.setter
    def arr_(self, value):
        return set__arr_(self, value)

    @total_count.setter
    def total_count(self, value):
        return set__total_count(self, value)

    def get_count(self, i):
        return invoke__get_count(self, i)

    def incr(self, i, val):
        return invoke__incr(self, i, val)

@njit(cache=True)
def set__arr_(self, value):
    self.arr_=value

@njit(cache=True)
def set__total_count(self, value):
    self.total_count=value

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