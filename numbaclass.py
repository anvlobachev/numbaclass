import inspect


def numbaclass(cls):
    """
    TODO: Is to consider functools?

    """

    nbc = MakeNumbaClass()
    nbc.classname = cls.__name__

    for itm in inspect.getmembers(cls):
        # print(itm)

        if "__init__" in itm[0]:
            zz = nbc.construct_init(itm[1])
            print(zz)

        if "__" not in itm[0]:
            _src = inspect.getsourcelines(itm[1])
            _sign = inspect.signature(itm[1])
            _argspec = inspect.getfullargspec(itm[1])

            print(itm[1].__name__)
            print(_sign)
            print(_argspec)
            print(_src)

    def wrapper(*args, **kwargs):
        return cls(*args, **kwargs)

    return wrapper


class MakeNumbaClass:

    NBPREFIX = "NB_"
    TAB = "    "

    def __init__(self):

        self.classname = None
        self.init_args_names_ = set()
        self.attrs_names_ = set()
        self.methods_names_ = set()

    def construct_init(self, src):
        """
        Takes class __init__ method source code as argument.
        Creates function which inits inputs and
        returns Numba StructRef object.
        """

        attrs_names_ = self.attrs_names_
        init_args_names_ = self.init_args_names_

        init_args_names_ = set(
            inspect.getfullargspec(src).args[1:]
        )  # Don't include 'self' argument

        # getsourcelines docs: Return a list of source lines and starting line number for an object.
        _codelines = inspect.getsourcelines(src)[0]  # We need only lines of code

        _codelines[0] = f"def {self.classname}({', '.join(init_args_names_)}):\n"

        for n in range(1, len(_codelines)):

            line = _codelines[n]
            if line == "\n":
                continue

            line = line.lstrip()

            if "self." in line:
                # Don't want to instantiate class only to
                # get instance attributes names.
                # Retrieve them by "self." clause
                _attr_name = line.split("self.")[1].split("=")[0].rstrip()

                attrs_names_.add(_attr_name)

                line = line.replace("self.", "")

            _codelines[n] = self.TAB + line

        _codelines.append(" ")
        _codelines[-1] = (
            self.TAB
            + f"return {self.NBPREFIX}{self.classname}({', '.join(attrs_names_)})\n"
        )

        return "".join(_codelines)

    def construct_method(self, src):
        """
        Takes custom method source code and
        generates Numba aware wrappers
        """

        return
