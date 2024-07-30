## Numbaclass

Add @numbaclass decorator to Python class, to compile it with Numba experimental [StructRef](https://numba.readthedocs.io/en/stable/extending/high-level.html#implementing-mutable-structures).

* Converted class will work inside other jitted or non-jitted functions in pure Python.
* Classed can be nested.
* Supports Numba cache

```python
import numpy as np
from numbaclass import numbaclass

@numbaclass(cache=True)
class ExampleIncr:
    def __init__(self, arr_, incr_val):
        self.arr_ = arr_
        self.incr_val = incr_val

    def incr(self, i):
        self.arr_[i] += self.incr_val

    def get_count(self, i):
        return self.arr_[i]
```

Because @numbaclass relies on Numba StructRef, the above example, under the hood, converts to this:
<details>
<summary>Click to expand <br />&nbsp;</summary>

```python
import numpy as np

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
```

</details>

Every method gets wrapped with @njit (same as @jit(nopython=True))

By default, cache flag is False. @numbaclass(cache=False) will not store files and caches.\
Set @numbaclass(cache=True) to save generated code and numba compiled cache to
\_\_nbcache\_\_ folder, neighbouring \_\_pycache\_\_.

## Installation

```bash
git clone git@github.com:anvlobachev/numbaclass.git
cd numbaclass
python -m pip install .

```

## Configure

Disable conversion globally via environment variable:\
"NUMBACLS_BYPASS" = "1"

## Use Guides and Tips

* Decorator expects one Python class within module.

* "self." attributes within \_\_init\_\_ must be assigned with Numba compatible data types or objects.

* ~~Scalar variable will be treated as constant by StructRef. To be able to update the value, it's advisable to use array of one item size.~~ Probably overcome this.

@numbaclass is usefull for arranging code for compute intensive, repetative operations with a state.

Decorated class stays clean from additional code, which is needed using StructRef directily.
In case of Numba's own @jitclass decorator, caching and nesting is not supported.
While @numbaclass utilizes StructRef to cache compiled code and allows to constuct nested classes.

## Todos

* ~~Add setters~~
* Move from Alfa to Beta release
* Check changes of source vs cached before generate.
* Implement literal_unroll mock.
* Implement with object() mock to call pure Python from jitted code.
