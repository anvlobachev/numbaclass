## Numbaclass

Add @numbaclass decorator to Python class, to compile it with Numba, using StructRef feature.\
Decorated class will work inside other jitted or non-jitted functions.

```python
import numpy as np
from numbaclass import numbaclass

@numbaclass
class TestExample:
    def __init__(self, n):
        self.a = np.zeros(n, dtype=np.float64)
        self.b = np.zeros(n, dtype=np.float64)
    
    def process():
        for i in range(1000):
            pass
```

Because @numbaclass relies on Numba StructRef, the above example, under the hood, will be converted to this:

```python
import numpy as np
 
from numba import njit 
from numba.experimental import structref 

def TestExampleNB(n): 
    a = np.zeros(n, dtype=np.float64) 
    b = np.zeros(n, dtype=np.float64) 
    return 

# TODO: Inclue full result
```

A lot of wrappers and boilerplate code, which @numbaclass helps to avoid.

## Use Guides

* Inside \_\_init\_\_() define attributes, prepare and process data in a regular python way, use any libraries.
* Other dunder methods will be ignored, don't override.
* Class methods must use Numba compatibe routines.
  * tip 1
  * tip 2

## Installation

```bash
pip install numbaclass
```

## Configure details

Disable conversion globally via Environment variable.

Write out intermediate StructRef output to file with flag:
@numbaclass(write=True)

Cache flag, one for conversion and jitted code.
@numbaclass(cache=True)
