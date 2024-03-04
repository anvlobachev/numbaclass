import inspect
import functools

import importlib

import os


from makenumbaclass import MakeNumbaClass
from importlib.machinery import SourceFileLoader


def numbaclass(_cls=None, cache=None, writeout=None):
    """
    cache flag for both:
      @numbaclass decorator and
      @njit(cache=...) flag inside generated StructRef


    TODO: Issue with matching __init__ arguments and instance attrnames

    TODO: Decide on postfix in name of converted class, TestExampleNB

    TODO: Explore more on: Importing a Dynamically Generated Module

    DONE: Implement cache, issue #1
    # https://numba.discourse.group/t/hacking-numba-cache-dir-and-userprovidedcachelocator-to-package-jit-cache-in-egg/895/3

    """
    # Set defaults flags
    if cache is None:
        cache = True
    # if writeout is None:
    #     writeout = False

    # TODO: File cache (?)
    def cached_MakeNumbaClass(cls, cache):
        return MakeNumbaClass(cls, cache)

    def deco(cls):

        if cache:
            print("Get cached output")
            nbc = cached_MakeNumbaClass(cls, cache)
        else:
            print("Generate new output")
            nbc = MakeNumbaClass(cls, cache)

        if cache:
            # Construct filepath for generated module
            _absfile = inspect.getabsfile(cls)
            print("_absfile: ", _absfile)
            _newabsfile = os.path.join(
                os.path.split(_absfile)[0], f"{nbc.get_module_name}.py"
            )

            with open(_newabsfile, "w") as file:
                file.write(nbc.get_nb_module)
                print("Numbaclass module saved: ", nbc.get_module_name)

            _numbaclass = SourceFileLoader(
                nbc.get_module_name, _newabsfile
            ).load_module()

        else:
            module_spec = importlib.machinery.ModuleSpec(nbc.get_module_name, None)
            _numbaclass = importlib.util.module_from_spec(module_spec)
            exec(nbc.get_nb_module, _numbaclass.__dict__)

        _tocall = getattr(_numbaclass, nbc.classname)

        def _initcall(*args, **kwargs):
            return _tocall(*args, **kwargs)

        return _initcall

    if _cls is None:
        return deco
    else:
        return deco(_cls)
