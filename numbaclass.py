import inspect
import importlib

import imp
from makenumbaclass import MakeNumbaClass


def numbaclass(cls):
    """
    TODO: Is to consider functools?

    # TODO: Explore more on: Importing a Dynamically Generated Module
    # TODO: Replace with importlib.util.module_from_spec (?)

    """
    nbc = MakeNumbaClass()
    nbc.classname = cls.__name__
    nbc.gen_imports(cls)

    for itm in inspect.getmembers(cls):
        if "__init__" in itm[0]:
            nbc.gen_init(itm[1])
        if "__" not in itm[0]:
            nbc.gen_method(itm[1])

    _nb_module_src = nbc.gen_final_module()

    with open(f"{nbc.get_module_name}.py", "w") as file:
        file.write(_nb_module_src)
        print("Numbaclass module saved: ", nbc.get_module_name)

    _nb_module_code = compile(_nb_module_src, nbc.get_module_name, "exec")
    _numbaclass = imp.new_module(nbc.get_module_name)

    exec(_nb_module_code, _numbaclass.__dict__)
    _tocall = getattr(_numbaclass, nbc.classname)

    def wrapper(*args, **kwargs):
        return _tocall(*args, **kwargs)

    return wrapper
