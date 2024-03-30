import pytest
from numba import njit


def test_pure_python_instance_sanity_check():

    try:
        from examples.example_class import ExampleClass

        purepy_cls = ExampleClass(5)
        purepy_cls.incr_prop1(5)
        purepy_cls.check_me()

    except Exception as e:
        pytest.fail(f"Exception raised: {e}")


def test_converted_without_typos():

    from examples.example_class import ExampleClass

    try:
        from numbaclass import numbaclass

        ExampleClassNB = numbaclass(_cls=ExampleClass, cache=True)
        numba_cls = ExampleClassNB(5)
    except Exception as e:
        pytest.fail(f"Exception raised: {e}")


def test_can_run_inside_jitted_function():
    """
    Note, that instance object ( numba_cls ) created
    outside jitted function.
    """

    from numbaclass import numbaclass
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
        pytest.fail(f"Exception raised: {e}")


def test_can_run_nested_structrefs():

    try:
        from examples.example_parent import ExampleParent

        numba_cls = ExampleParent(2, 3)
        numba_cls.action()
        numba_cls.check_me()

    except Exception as e:
        pytest.fail(f"Exception raised: {e}")

    # assert False


# test_can_run_nested_structrefs()
