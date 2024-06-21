


from numbaclass import numbaclass
import numpy as np


from numba import njit
from numba.core import types
from numba.experimental import structref
from numba.core.extending import overload_method, register_jitable


class ExampleFormat(structref.StructRefProxy):
    def __new__(
        cls,
        prop1
    ):
        return structref.StructRefProxy.__new__(
            cls,
            prop1
        )

    @property
    def prop1(self):
        return get__prop1(self)

    def check_me(self):
        return invoke__check_me(self)

    def incr_prop1(self, val):
        return invoke__incr_prop1(self, val)

@njit(cache=True)
def get__prop1(self):
    return self.prop1

@register_jitable
def the__check_me(self):
    print(self.prop1)


@njit(cache=True)
def invoke__check_me(self):
    return the__check_me(self)

@register_jitable
def the__incr_prop1(self, val):
    """
    Doc
    """
    self.prop1[:] += val


@njit(cache=True)
def invoke__incr_prop1(self, val):
    return the__incr_prop1(self, val)


@structref.register
class ExampleFormatType(types.StructRef):
    def preprocess_fields(self, fields):
        return tuple((name, types.unliteral(typ)) for name, typ in fields)

structref.define_proxy(
    ExampleFormat,
    ExampleFormatType,
    [
	"prop1"
    ],
)

@overload_method(ExampleFormatType, "check_me", fastmath=False)
def ol__check_me(self):
    return the__check_me

@overload_method(ExampleFormatType, "incr_prop1", fastmath=False)
def ol__incr_prop1(self, val):
    return the__incr_prop1