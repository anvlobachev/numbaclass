import inspect


class MakeNumbaClass:
    """ """

    # NBPREFIX = "NB"

    NBPREFIX = ""
    TAB = "    "
    TAB2 = TAB + TAB
    TAB3 = TAB + TAB + TAB

    def __init__(self, cls, cache):

        self._MAKE_SETTERS = True

        self.cache = cache

        self.classname = cls.__name__
        self.structrefname = cls.__name__ + self.NBPREFIX
        self.init_args_names_ = []
        self.attrs_names_ = []

        self.methods_parts_ = []

        self.get_imports = ""
        self.get_methods_code_ = []

        self.get_module_name = self.classname.lower() + "__nbc__"

        self.src_module = inspect.getmodule(cls)
        self._gen_imports(cls)

        for itm in inspect.getmembers(cls):
            if "__init__" in itm[0]:
                #  Don't include 'self' argument, skip first item [1:]
                self.attrs_names_ = list(inspect.getfullargspec(itm[1]).args[1:])

            if "__" not in itm[0]:
                self._parse_method(itm[1])

        self.get_nb_module = self._gen_final_module()

    def _gen_imports(self, src):
        # src_module = inspect.getmodule(src)
        lines_ = inspect.getsourcelines(self.src_module)[0]

        for line in lines_:
            # Remove inline comments
            if "#" in line:
                line = line.split("#")[0].strip() + "\n"

            # TODO: Fix in case @numbaclass is renamed
            if line.startswith("@numbaclass") or line.startswith("class "):
                break

            self.get_imports += line

        self.get_imports += "from numba import njit\n"
        self.get_imports += "from numba.core import types\n"
        self.get_imports += "from numba.experimental import structref\n"
        self.get_imports += (
            "from numba.core.extending import overload_method, register_jitable\n"
        )
        self.get_imports += "\n"

    def _remove_definition(self, src, lines_):
        """
        Removes function definition from list of lines
        """

        for line in lines_[:]:

            lines_.remove(line)
            # Remove inline comments
            if "#" in line:
                line = line.split("#")[0].strip() + "\n"

            # End of difinition
            if ":\n" in line:
                break

    def _gen__new__(self):
        _args1 = ",\n".join([f"{self.TAB2}{name}" for name in self.attrs_names_])
        _args2 = ",\n".join([f"{self.TAB3}{name}" for name in self.attrs_names_])

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


    # TODO Issue #15
    #  
    def _gen_setters(self):
        if not self._MAKE_SETTERS:
            return ""
        _out = ""
        for name in self.attrs_names_:
            _out += f"""
    @{name}.setter
    def {name}(self, value):
        return set__{name}(self, value)\n"""
        return _out


    def _gen_jit_setters(self):
        if not self._MAKE_SETTERS:
            return ""
        _out = ""
        for name in self.attrs_names_:
            _out += f"""
@njit(cache={self.cache})
def set__{name}(self, value):
    self.{name}=value\n"""
        return _out    


    def _parse_method(self, src):
        """
        Collect methods parts for latter use
        """
        _parts = {"name": "", "args": [], "numba_type_signature": "", "code": []}

        _parts["name"] = src.__name__
        _parts["args"] = list(inspect.getfullargspec(src).args)

        lines_, line_num_from_module = inspect.getsourcelines(
            src
        )  # We need only lines of code

        # NOTE: Issue #4, Implement type infer:
        #   Implemented extraction of signature from comment line
        #   But, explicit signature is not working in case of structref
        #   because of 'self' statement in short.

        # module_lines_ = inspect.getsourcelines(self.src_module)[0]
        # _sign = module_lines_[line_num_from_module - 2]
        # if "#" in _sign:
        #     _sign = _sign.split("#")[1].strip()
        #     _parts["numba_type_signature"] = _sign

        self._remove_definition(src, lines_)

        for n in range(0, len(lines_)):
            if lines_[n].startswith("    "):
                lines_[n] = lines_[n][len(self.TAB) :]
        _parts["code"] = lines_

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
            _signature = ""
            ## Issue #4, Implement type infer.
            # _signature = _parts["numba_type_signature"]
            # if len(_signature) != 0:
            #     _signature = "'" + _signature + "'" + ", "

            name = _parts["name"]
            _out += f"""
@register_jitable
def the__{name}({_args}):
{"".join(_parts["code"])}

@njit({_signature}cache={self.cache})
def invoke__{name}({_args}):
    return the__{name}({_args})\n"""

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

        _out = (
            self.get_imports,
            self._gen__new__(),
            self._gen_properties(),
            self._gen_setters(),   # Issue #15
            self._gen_methods_defs(),
            # 
            self._gen_jit_setters(),
            self._gen_jit_properties(),
            self._gen_jit_methods_defs(),
            "\n",
            self._gen_preprocess_fields(),
            self._gen_define_proxy(),
            self._gen_overload_methods(),
        )

        return "".join(_out)
