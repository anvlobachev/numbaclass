import inspect
import importlib

import os

import imp
from makenumbaclass import MakeNumbaClass


def numbaclass(cls):
    """
    TODO: Consider functools?
    TODO: Explore more on: Importing a Dynamically Generated Module
    TODO: Replace with importlib.util.module_from_spec (?)

    """
    nbc = MakeNumbaClass(cls)

    _nb_module_src = nbc._gen_final_module()

    writeout = True
    if writeout:
        # Construct filepath for generated module
        _absfile = inspect.getabsfile(cls)
        _absdir = os.path.split(_absfile)[0]
        _newabsfile = os.path.join(_absdir, f"{nbc.get_module_name}.py")

        with open(_newabsfile, "w") as file:
            file.write(_nb_module_src)
            print("Numbaclass module saved: ", nbc.get_module_name)

    _nb_module_code = compile(_nb_module_src, nbc.get_module_name, "exec")
    _numbaclass = imp.new_module(nbc.get_module_name)

    exec(_nb_module_code, _numbaclass.__dict__)
    _tocall = getattr(_numbaclass, nbc.classname)

    # print(nbc.methods_parts_)

    def wrapper(*args, **kwargs):
        return _tocall(*args, **kwargs)

    return wrapper
