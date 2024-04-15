import numpy as np
from numbaclass import numbaclass

from examples.example_incr import ExampleIncr


from numba import njit
from numba.core import types
from numba.experimental import structref
from numba.core.extending import overload_method, register_jitable


class ExampleNest(structref.StructRefProxy):
    def __new__(
        cls,
        size
    ):
        return structref.StructRefProxy.__new__(
            cls,
            size
        )

    @property
    def size(self):
        return get__size(self)

    def update(self, val, index):
        return invoke__update(self, val, index)

@njit(cache=True)
def get__size(self):
    return self.size

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


@structref.register
class ExampleNestType(types.StructRef):
    def preprocess_fields(self, fields):
        return tuple((name, types.unliteral(typ)) for name, typ in fields)

structref.define_proxy(
    ExampleNest,
    ExampleNestType,
    [
	"size"
    ],
)

@overload_method(ExampleNestType, "update", fastmath=False)
def ol__update(self, val, index):
    return the__update