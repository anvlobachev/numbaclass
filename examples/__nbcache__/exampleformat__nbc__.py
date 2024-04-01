



import numpy as np




from numba import njit
from numba.core import types
from numba.experimental import structref
from numba.core.extending import overload_method, register_jitable

def ExampleFormat(n):
    """
    Numbaclass will convert __init__ to wrapper function,
    which will return jitted structref instance.
    Use pure Python and any modules here to process data for structref inputs.
    
    Note self. attributes have to be assigned with
    Numba compatible data types and objects.
    """
    
    prop1 = np.zeros(n, dtype=np.float64)
    prop2 = np.zeros(n, dtype=np.float64)
    
    tmp = 3 + 5
    prop1[:] = tmp
    return ExampleFormatNB(prop1, prop2)

@structref.register
class ExampleFormatNBType(types.StructRef):
    def preprocess_fields(self, fields):
        return tuple((name, types.unliteral(typ)) for name, typ in fields)

class ExampleFormatNB(structref.StructRefProxy):
    def __new__(
        cls,
        prop1,
        prop2
    ):
        return structref.StructRefProxy.__new__(
            cls,
            prop1,
            prop2
        )

    @property
    def prop1(self):
        return get__prop1(self)

    @property
    def prop2(self):
        return get__prop2(self)

    def check_me(self):
        return invoke__check_me(self)

    def incr_prop1(self, val):
        return invoke__incr_prop1(self, val)

structref.define_proxy(
    ExampleFormatNB,
    ExampleFormatNBType,
    [
	"prop1",
	"prop2"
    ],
)

@njit(cache=True)
def get__prop1(self):
    return self.prop1

@njit(cache=True)
def get__prop2(self):
    return self.prop2

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

@overload_method(ExampleFormatNBType, "check_me", fastmath=False)
def ol__check_me(self):
    return the__check_me

@overload_method(ExampleFormatNBType, "incr_prop1", fastmath=False)
def ol__incr_prop1(self, val):
    return the__incr_prop1