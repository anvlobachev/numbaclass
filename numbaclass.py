import inspect


def numbaclass(func):
    """
    TODO: Is to consider functools?
    """

    def wrapper(*args, **kwargs):
        # Lets test retrieving sourcse code of function
        _source = inspect.getsource(func)
        _source = inspect.getmembers(func)
        # _source = inspect.getsourcelines(func)
        # for i in range(3):
        #     _out = inspect.getblock(_source)
        #     print(_out)
        for itm in _source:
            print(itm)
            # if itm[0] == "method1":
            if "__" not in itm[0]:
                _src = inspect.getsource(itm[1])

                _sign = inspect.signature(itm[1])
                _argspec = inspect.getfullargspec(itm[1])

                print(itm[1].__name__)
                print(_sign)
                print(_argspec)
                print(_src)
                print(inspect.getblock(_src))

    return wrapper
