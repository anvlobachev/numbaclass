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
        incr_val
    ):
        return structref.StructRefProxy.__new__(
            cls,
            arr_,
            incr_val
        )

    @property
    def arr_(self):
        return get__arr_(self)

    @property
    def incr_val(self):
        return get__incr_val(self)

    def get_count(self, i):
        return invoke__get_count(self, i)

    def incr(self, i):
        return invoke__incr(self, i)

@njit(cache=True)
def get__arr_(self):
    return self.arr_

@njit(cache=True)
def get__incr_val(self):
    return self.incr_val

@register_jitable
def the__get_count(self, i):
    return self.arr_[i]


@njit(cache=True)
def invoke__get_count(self, i):
    return the__get_count(self, i)

@register_jitable
def the__incr(self, i):
    self.arr_[i] += self.incr_val


@njit(cache=True)
def invoke__incr(self, i):
    return the__incr(self, i)


@structref.register
class ExampleIncrType(types.StructRef):
    def preprocess_fields(self, fields):
        return tuple((name, types.unliteral(typ)) for name, typ in fields)

structref.define_proxy(
    ExampleIncr,
    ExampleIncrType,
    [
	"arr_",
	"incr_val"
    ],
)

@overload_method(ExampleIncrType, "get_count", fastmath=False)
def ol__get_count(self, i):
    return the__get_count

@overload_method(ExampleIncrType, "incr", fastmath=False)
def ol__incr(self, i):
    return the__incr