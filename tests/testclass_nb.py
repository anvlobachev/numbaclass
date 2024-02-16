import numpy as np

from numbaclass import numbaclass


def TestClass(a):
    """
    Init routines
    """

    prop1 = np.zeros(a, dtype=np.float64)
    prop2 = np.zeros(a, dtype=np.float64)
    print("Init done")
    return 'Some output'
