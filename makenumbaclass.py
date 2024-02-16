import inspect


class MakeNumbaClass:

    NBPREFIX = "NB_"
    TAB = "    "

    def __init__(self):

        self.classname = None
        self.init_args_names_ = set()
        self.attrs_names_ = set()
        self.methods_names_ = set()

        self.get_module_name = ""

        self.get_imports = ""
        self.get_init_code = ""
        self.get_methods_code_ = []

    def gen_imports(self, src):
        src_module = inspect.getmodule(src)
        lines_ = inspect.getsourcelines(src_module)[0]

        for line in lines_:
            if "@numbaclass" in line:
                break
            self.get_imports += line

    def gen_init(self, src):
        """
        Takes class __init__ method source code as argument.
        Creates function which inits inputs and
        returns Numba StructRef object.
        """
        #  Don't include 'self' argument, skip first item [1:]
        self.init_args_names_ = set(inspect.getfullargspec(src).args[1:])
        # getsourcelines docs: Return a list of source lines and starting line number for an object.
        _codelines = inspect.getsourcelines(src)[0]  # We need only lines of code
        _codelines[0] = f"def {self.classname}({', '.join(self.init_args_names_)}):\n"

        for n in range(1, len(_codelines)):
            line = _codelines[n]
            if line.startswith(self.TAB):
                line = line[len(self.TAB) :]
            # Retrieve attr instance names by "self." clause
            if "self." in line:
                self.attrs_names_.add(line.split("self.")[1].split("=")[0].rstrip())
                line = line.replace("self.", "")

            _codelines[n] = line

        # _codelines.append(
        #     self.TAB
        #     + f"return {self.NBPREFIX}{self.classname}({', '.join(self.attrs_names_)})\n"
        # )
        _codelines.append(self.TAB + f"return 'Some output'\n")

        self.get_init_code = "".join(_codelines)

        self.get_module_name = self.classname.lower() + "nb"

    def gen_method(self, src):
        """
        Takes custom method source code and
        generates Numba aware wrappers
        """
        lines_ = inspect.getsourcelines(src)[0]  # We need only lines of code

        for n in range(0, len(lines_)):

            if lines_[n].startswith(self.TAB):
                lines_[n] = lines_[n][len(self.TAB) :]

        self.get_methods_code_.append("".join(lines_))

    def gen_final_module(self):

        _out = ""

        _out += self.get_imports
        _out += self.get_init_code

        return _out
