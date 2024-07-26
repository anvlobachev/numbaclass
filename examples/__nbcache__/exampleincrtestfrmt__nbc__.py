



import numpy as np

from numba import njit
from numba.core import types
from numba.experimental import structref
from numba.core.extending import overload_method, register_jitable


class ExampleIncrTestfrmt(structref.StructRefProxy):
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

    @arr_.setter
    def arr_(self, value):
        return set__arr_(self, value)

    def check_me(self):
        return invoke__check_me(self)

    def incr(self, i, val):
        return invoke__incr(self, i, val)

@njit(cache=True)
def set__arr_(self, value):
    self.arr_=value

@njit(cache=True)
def get__arr_(self):
    return self.arr_

@register_jitable
def the__check_me(self):
    print(self.arr_)


@njit(cache=True)
def invoke__check_me(self):
    return the__check_me(self)

@register_jitable
def the__incr(self, i, val):
    """
    Doc
    """
    self.arr_[i] += val


@njit(cache=True)
def invoke__incr(self, i, val):
    return the__incr(self, i, val)


@structref.register
class ExampleIncrTestfrmtType(types.StructRef):
    def preprocess_fields(self, fields):
        return tuple((name, types.unliteral(typ)) for name, typ in fields)

structref.define_proxy(
    ExampleIncrTestfrmt,
    ExampleIncrTestfrmtType,
    [
	"arr_"
    ],
)

@overload_method(ExampleIncrTestfrmtType, "check_me", fastmath=False)
def ol__check_me(self):
    return the__check_me

@overload_method(ExampleIncrTestfrmtType, "incr", fastmath=False)
def ol__incr(self, i, val):
    return the__incr