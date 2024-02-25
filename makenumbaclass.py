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

    def __init__(self, cls):

        self.cache = False

        self.classname = cls.__name__
        self.structrefname = cls.__name__ + "NB"
        self.init_args_names_ = []
        self.attrs_names_ = []

        self.methods_parts_ = []

        self.get_module_name = ""

        self.get_imports = ""
        self.get_init_code = ""
        self.get_methods_code_ = []

        self._gen_imports(cls)

        for itm in inspect.getmembers(cls):
            if "__init__" in itm[0]:
                self._gen_init(itm[1])
            if "__" not in itm[0]:
                self._parse_method(itm[1])

        self.get_nb_module = self._gen_final_module()

    def _gen_imports(self, src):
        src_module = inspect.getmodule(src)
        lines_ = inspect.getsourcelines(src_module)[0]

        for line in lines_:
            if "@numbaclass" in line and not line.lstrip().startswith("#"):
                break
            self.get_imports += line

        self.get_imports += "from numba import njit\n"
        self.get_imports += "from numba.core import types\n"
        self.get_imports += "from numba.experimental import structref\n"
        self.get_imports += (
            "from numba.core.extending import overload_method, register_jitable\n"
        )
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
        lines_ = inspect.getsourcelines(src)[0]  # We need only lines of code
        lines_[0] = f"def {self.classname}({', '.join(self.init_args_names_)}):\n"

        for n in range(1, len(lines_)):
            line = lines_[n]
            if line.startswith(self.TAB):
                line = line[len(self.TAB) :]
            # Retrieve attr instance names by "self." clause
            if "self." in line and not line.lstrip().startswith("#"):
                _name = line.split("self.")[1].split("=")[0].rstrip()
                if _name not in self.attrs_names_:
                    self.attrs_names_.append(_name)
                line = line.replace("self.", "")

            lines_[n] = line

        lines_.append(
            self.TAB + f"return {self.structrefname}({', '.join(self.attrs_names_)})\n"
        )

        self.get_init_code = "".join(lines_)
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

    def _gen_jit_methods_defs(self):
        _out = ""
        for _parts in self.methods_parts_:
            _args = ", ".join(_parts["args"])
            name = _parts["name"]
            _out += f"""
@njit(cache={self.cache})
def invoke__{name}({_args}):
    return the__{name}({_args})

@register_jitable
def the__{name}({_args}):
{"".join(_parts["code"])}\n"""

        return _out

    def _gen_preprocess_fields(self):

        _out = f"""
@structref.register
class {self.structrefname}Type(types.StructRef):
    def preprocess_fields(self, fields):
        return tuple((name, types.unliteral(typ)) for name, typ in fields)\n"""

        return _out

    def _gen_define_proxy(self):
        _args = ",\n".join([f'\t"{name}"' for name in self.attrs_names_])

        _out = f"""
structref.define_proxy(
    {self.structrefname},
    {self.structrefname}Type,
    [
{_args}
    ],
)\n"""
        return _out

    def _gen_overload_methods(self):
        methods_ = []
        for _parts in self.methods_parts_:
            name = _parts["name"]
            _args = ", ".join(_parts["args"])
            _meth = f"""
@overload_method({self.structrefname}Type, "{name}", fastmath=False)
def ol__{name}({_args}):
    return the__{name}"""
            methods_.append(_meth)

        return "\n".join(methods_)

    def _gen_final_module(self):

        _out = ""

        _out += self.get_imports
        _out += self.get_init_code

        _out += self._gen__new__()
        _out += self._gen_properties()
        _out += self._gen_methods_defs()
        _out += self._gen_jit_properties()
        _out += self._gen_jit_methods_defs()
        _out += self._gen_preprocess_fields()
        _out += self._gen_define_proxy()
        _out += self._gen_overload_methods()

        return _out
