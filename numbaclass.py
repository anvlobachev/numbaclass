import inspect
import functools

import importlib

import os

import imp
from makenumbaclass import MakeNumbaClass


def numbaclass(_cls=None, cache=None, writeout=None):
    """
    cache flag for both:
      @numbaclass decorator and
      @njit(cache=...) flag inside generated StructRef


    TODO: Issue with matching __init__ arguments and instance attrnames

    TODO: Decide on postfix in name of converted class, TestExampleNB

    TODO: Check if cached_MakeNumbaClass(cls) is using cache
    TODO: Replace imp with importlib.util.module_from_spec (?)

    TODO: Explore more on: Importing a Dynamically Generated Module

    """
    # Set defaults flags
    if cache is None:
        cache = True
    if writeout is None:
        writeout = False

    @functools.lru_cache(maxsize=32)
    def cached_MakeNumbaClass(cls):
        return MakeNumbaClass(cls)

    def deco(cls):

        if cache:
            print("Get cached output")
            nbc = cached_MakeNumbaClass(cls)
        else:
            print("Generate new output")
            nbc = MakeNumbaClass(cls)

        if writeout:
            # Construct filepath for generated module
            _absfile = inspect.getabsfile(cls)
            _newabsfile = os.path.join(
                os.path.split(_absfile)[0], f"{nbc.get_module_name}.py"
            )

            with open(_newabsfile, "w") as file:
                file.write(nbc.get_nb_module)
                print("Numbaclass module saved: ", nbc.get_module_name)

        _nb_module_code = compile(nbc.get_nb_module, nbc.get_module_name, "exec")
        _numbaclass = imp.new_module(nbc.get_module_name)

        exec(_nb_module_code, _numbaclass.__dict__)
        _tocall = getattr(_numbaclass, nbc.classname)

        def _initcall(*args, **kwargs):
            return _tocall(*args, **kwargs)

        return _initcall

    if _cls is None:
        return deco
    else:
        return deco(_cls)
