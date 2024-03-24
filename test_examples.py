import pytest
from numba import njit


def test_pure_python_instance_sanity_check():

    try:
        from examples.example_class import ExampleClass

        purepy_cls = ExampleClass(5)
        purepy_cls.incr_prop1(5)
        purepy_cls.check_me()

    except Exception as e:
        pytest.fail(f"Unexpected exception raised: {e}")


def test_convered_without_typos():

    from examples.example_class import ExampleClass

    try:
        from numbaclass.numbaclass import numbaclass

        ExampleClassNB = numbaclass(_cls=ExampleClass, cache=True)
        numba_cls = ExampleClassNB(5)
    except Exception as e:
        pytest.fail(f"Unexpected exception raised: {e}")


# def test_is_jittable():
#     assert False


def test_can_run_inside_jitted_function():

    from numbaclass.numbaclass import numbaclass
    from examples.example_class import ExampleClass

    try:
        ExampleClassNB = numbaclass(_cls=ExampleClass, cache=True)
        numba_cls = ExampleClassNB(5)

        @njit
        def run_in_jit(numba_cls):

            numba_cls.incr_prop1(5)
            numba_cls.check_me()

        run_in_jit(numba_cls)

    except Exception as e:
        pytest.fail(f"Unexpected exception raised: {e}")


# if __name__ == "__main__":
#     test_conversion()
