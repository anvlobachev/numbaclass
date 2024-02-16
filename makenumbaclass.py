import inspect


class MakeNumbaClass:
    """
    class IndicatorAtr(structref.StructRefProxy):
    def __new__(
        cls,
        arg1,
    ):
        return structref.StructRefProxy.__new__(
            cls,
            arg1,
        )


    """

    NBPREFIX = "NB"
    TAB = "    "

    def __init__(self):

        self.cache = False

        self.classname = None
        self.init_args_names_ = []
        self.attrs_names_ = []

        self.methods_parts_ = []

        self.get_module_name = ""

        self.get_imports = ""
        self.get_init_code = ""
        self.get_methods_code_ = []

    def _gen_imports(self, src):
        src_module = inspect.getmodule(src)
        lines_ = inspect.getsourcelines(src_module)[0]

        for line in lines_:
            if "@numbaclass" in line and not line.lstrip().startswith("#"):
                break
            self.get_imports += line

        self.get_imports += "from numba import njit\n"
        self.get_imports += "from numba.experimental import structref\n"
        self.get_imports += "\n"

    def _gen_init(self, src):
        """
        Takes class __init__ method source code as argument.
        Creates function which inits inputs and
        returns Numba StructRef object.
        """
        #  Don't include 'self' argument, skip first item [1:]
        self.init_args_names_ = list(inspect.getfullargspec(src).args[1:])
        # getsourcelines docs: Return a list of source lines and starting line number for an object.
        _codelines = inspect.getsourcelines(src)[0]  # We need only lines of code
        _codelines[0] = f"def {self.classname}({', '.join(self.init_args_names_)}):\n"

        for n in range(1, len(_codelines)):
            line = _codelines[n]
            if line.startswith(self.TAB):
                line = line[len(self.TAB) :]
            # Retrieve attr instance names by "self." clause
            if "self." in line and not line.lstrip().startswith("#"):
                _name = line.split("self.")[1].split("=")[0].rstrip()
                if _name not in self.attrs_names_:
                    self.attrs_names_.append(_name)
                line = line.replace("self.", "")

            _codelines[n] = line

        # _codelines.append(
        #     self.TAB
        #     + f"return {self.NBPREFIX}{self.classname}({', '.join(self.attrs_names_)})\n"
        # )
        _codelines.append(self.TAB + f"return 'Some output'\n")

        self.get_init_code = "".join(_codelines)
        self.get_module_name = self.classname.lower() + "_nb"

    def _gen__new__(self):

        _args1 = ",\n".join([f"\t\t{name}" for name in self.attrs_names_])
        _args2 = ",\n".join([f"\t\t\t{name}" for name in self.attrs_names_])

        _out = f"""
class {self.classname}{self.NBPREFIX}(structref.StructRefProxy):
    def __new__(
        cls,\n{_args1}
    ):
        return structref.StructRefProxy.__new__(
            cls,\n{_args2}
        )\n"""
        return _out

    def _gen_properties(self):
        _out = ""
        for name in self.attrs_names_:
            _out += f"""
    @property
    def {name}(self):
        return get__{name}(self)\n"""
        return _out

    def _gen_jit_properties(self):
        _out = ""
        for name in self.attrs_names_:
            _out += f"""
@njit(cache={self.cache})
def get__{name}(self):
    return self.{name}\n"""
        return _out

    def _parse_method(self, src):
        """
        Collect methods parts for latter use
        """
        _parts = {"name": "", "args": [], "code": []}

        _parts["name"] = src.__name__
        _parts["args"] = list(inspect.getfullargspec(src).args)

        lines_ = inspect.getsourcelines(src)[0]  # We need only lines of code

        for n in range(0, len(lines_)):
            if lines_[n].startswith("    "):
                lines_[n] = lines_[n][len(self.TAB) :]
        _parts["code"] = lines_[1:]

        self.methods_parts_.append(_parts)

    def _gen_methods_defs(self):
        _out = ""

        for _parts in self.methods_parts_:
            _args = ", ".join(_parts["args"])
            name = _parts["name"]
            _out += f"""
    def {name}({_args}):
        return invoke__{name}({_args})\n"""
        return _out

    def _gen_final_module(self):

        _out = ""

        _out += self.get_imports
        _out += self.get_init_code

        _out += self._gen__new__()
        _out += self._gen_properties()
        _out += self._gen_methods_defs()
        _out += self._gen_jit_properties()

        # TODO: Add here _gen_jit_methods_defs()

        return _out
