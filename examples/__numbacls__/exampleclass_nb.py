
import numpy as np




from numba import njit
from numba.core import types
from numba.experimental import structref
from numba.core.extending import overload_method, register_jitable

def ExampleClass(n):
    """
    Numbaclass will convert __init__ to wrapper function,
    which will return jitted structref instance.
    It's safe to use pure Python and any modules here to fetch data and
    process values for structref inputs.

    Note that, instance properties with  must be
    compatible with Numba requirements.

    """

    prop1 = np.zeros(n, dtype=np.float64)
    prop2 = np.zeros(n, dtype=np.float64)

    prop1[:] = 7  # Property variation
    print("Init done")
    return ExampleClassNB(prop1, prop2)

@structref.register
class ExampleClassNBType(types.StructRef):
    def preprocess_fields(self, fields):
        return tuple((name, types.unliteral(typ)) for name, typ in fields)

class ExampleClassNB(structref.StructRefProxy):
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
    ExampleClassNB,
    ExampleClassNBType,
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
    More comments
    """
    self.prop1[:] += val


@njit(cache=True)
def invoke__incr_prop1(self, val):
    return the__incr_prop1(self, val)

@overload_method(ExampleClassNBType, "check_me", fastmath=False)
def ol__check_me(self):
    return the__check_me

@overload_method(ExampleClassNBType, "incr_prop1", fastmath=False)
def ol__incr_prop1(self, val):
    return the__incr_prop1