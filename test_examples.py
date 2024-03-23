import pytest


def test_pure_python_instance():

    from examples.example_class import ExampleClass

    try:
        purepy_cls = ExampleClass(5)
    except Exception as e:
        pytest.fail(f"Unexpected exception raised: {e}")


def test_conversion():

    from numbaclass.numbaclass import numbaclass
    from examples.example_class import ExampleClass

    # purepy_cls = ExampleClass(5)

    try:
        ExampleClassNB = numbaclass(_cls=ExampleClass, cache=True)
        numba_cls = ExampleClassNB(5)
    except Exception as e:
        pytest.fail(f"Unexpected exception raised: {e}")


def test_is_jittable():
    assert False


def test_is_overloaded():
    assert False


# if __name__ == "__main__":
#     test_conversion()
