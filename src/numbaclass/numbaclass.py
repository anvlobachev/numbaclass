import inspect
import functools

import importlib

import os


# from numbaclass.makenumbaclass import MakeNumbaClass
from .makenumbaclass import MakeNumbaClass
from importlib.machinery import SourceFileLoader


def numbaclass(_cls=None, cache=None):
    """
    FIXME: Ensure right order of structref setup at MakeNumbaClass
    TODO: Issue with matching __init__ arguments and instance attrnames

    """

    NUMBACLS_BYPASS = 0
    if (_numbacls_bypass := os.getenv("NUMBACLS_BYPASS")) is not None:
        NUMBACLS_BYPASS = int(_numbacls_bypass)

    # Set defaults flags
    if cache is None:
        cache = False

    # TODO: File cache (?)
    def cached_MakeNumbaClass(cls, cache):
        return MakeNumbaClass(cls, cache)

    def deco(cls):

        if cache:
            # print("Get cached output")
            nbc = cached_MakeNumbaClass(cls, cache)
        else:
            # print("Generate new output")
            nbc = MakeNumbaClass(cls, cache)

        if cache:
            # Construct filepath for generated module
            _absfile = inspect.getabsfile(cls)
            print("_absfile: ", _absfile)

            # _cachedir = os.path.join(os.path.split(_absfile)[0], "__numbacls__")
            _cachedir = os.path.split(_absfile)[0]

            if not os.path.isdir(_cachedir):
                os.mkdir(_cachedir)

            _newabsfile = os.path.join(_cachedir, f"{nbc.get_module_name}.py")
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

    def deco_bypass(cls):
        print(
            f"@numbaclass conversion bypassed: {cls.__name__}, NUMBACLS_BYPASS = {NUMBACLS_BYPASS}"
        )
        return cls

    if _cls is None:
        if NUMBACLS_BYPASS:
            return deco_bypass
        return deco
    else:
        if NUMBACLS_BYPASS:
            return _cls
        return deco(_cls)
