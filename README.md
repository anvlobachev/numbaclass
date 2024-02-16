# numbaclass

Allows python class to be compiled with Numba.\
Converted class can be used inside other jitted and/or
interpreted functions simultaneously.

Use @numbaclass decorator on your class:

```python
from numbaclass import numbaclass
import numpy as np

@numbaclass
class TestClass:
    def __init__(self, num):
        self.a = np.zeros(num, dtype=np.float64)
        self.b = np.zeros(num, dtype=np.float64)
    
    def process():
        for i in range(1000):
            pass
```

todo: Class must use Numba compatibe methods and syntax.
Some reminders to consider:

\
Installation

```bash
pip install numbaclass
```

## How it works

Under the hood decorator rewrites class to Numba StructRef object.
