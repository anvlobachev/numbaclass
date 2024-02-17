# numbaclass

Allows python class to be compiled with Numba.\
Converted class can be used inside other jitted or non-jitted functions simultaneously.

### Use @numbaclass decorator

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

### Installation

```bash
pip install numbaclass
```

### Use Guides

* Inside \_\_init\_\_() define attributes, prepare and process data in a regular python way, use any libraries.
* Other dunder methods will be ignored, don't override.
* Class methods must use Numba compatibe routines.
  * tip 1
  * tip 2

\Consider also:

### How it works

Under the hood decorator rewrites class to Numba StructRef object.

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
