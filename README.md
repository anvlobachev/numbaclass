## Numbaclass

Add @numbaclass decorator to Python class, to compile it with Numba.

* Converted class will work inside other jitted or non-jitted functions in pure Python.
* Classed can be nested.
* Support Numba cache

```python
import numpy as np
from numbaclass import numbaclass

@numbaclass
class ExampleClass:
    def __init__(self, n):
        self.a = np.zeros(n, dtype=np.float64)
        self.b = np.zeros(n, dtype=np.float64)
    
    def process():
        for i in range(1000):
            pass
```

Because @numbaclass relies on Numba StructRef, the above example, under the hood, converts to this:
<details>
<summary>Click to expand <br />&nbsp;</summary>

```python
import numpy as np
 
from numba import njit 
from numba.experimental import structref 

def ExampleClassNB(n): 
    a = np.zeros(n, dtype=np.float64) 
    b = np.zeros(n, dtype=np.float64) 
    return 

# TODO: Inclue full result
```

</details>

Using flag @numbaclass(cache=True), generated code will be saved to \_\_numbacls\_\_ dir within decorated class location.

## Use Guides and Tips

* Inside \_\_init\_\_() define attributes, prepare and process data in a regular python way, use any libraries.
* Other dunder methods will be ignored, don't override.
* Class methods must use Numba compatibe routines.
  * tip 1
  * tip 2
*

## Installation

```bash
pip install numbaclass
```

## Configure details

Disable conversion globally via Environment variable: "NUMBACLS_BYPASS" = "1"

@numbaclass(cache=True) flag will be translated to Numba @njit(cache=True).\
Also converted to StructRef class will be saved to \_\_pycache\_\_ folder.\
Default value: False
