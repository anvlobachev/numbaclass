import inspect


def numbaclass(func):
    def wrapper(*args, **kwargs):
        # Lets test retrieving sourcse code of function
        _source = inspect.getsource(func)
        print(_source)

    return wrapper


@numbaclass
def test_func():
    z = 0
    for i in range(5):
        z += 1
    print(z)


# test_func()
