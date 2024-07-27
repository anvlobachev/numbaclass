import pytest
from numba import njit
import numpy as np

# @pytest.mark.skip(reason="temporary")
def test_example_incr_testfrmt_pure_python():

    try:
        from examples.example_incr_testfrmt import ExampleIncrTestfrmt

        purepy_cls = ExampleIncrTestfrmt(np.zeros(5, dtype=np.float64))
        purepy_cls.incr(0, 1)
        purepy_cls.check_me()

    except Exception as e:
        pytest.fail(f"Exception raised: {e}")



def test_example_incr_testfrmt_converted_without_typos():

    from examples.example_incr_testfrmt import ExampleIncrTestfrmt

    try:
        from numbaclass import numbaclass

        ExampleClassNB = numbaclass(_cls=ExampleIncrTestfrmt, cache=True)
        numba_cls = ExampleClassNB(5)
    except Exception as e:
        pytest.fail(f"Exception raised: {e}")


def test_example_incr_testfrmt_can_run_inside_jitted_function():
    """
    Note, instance object ( numba_cls ) created
    outside jitted function.
    """

    import numpy as np
    from numbaclass import numbaclass
    from examples.example_incr_testfrmt import ExampleIncrTestfrmt

    try:
        ExampleClassNB = numbaclass(_cls=ExampleIncrTestfrmt, cache=True)
        numba_cls = ExampleClassNB(
                                     np.zeros(5, dtype=np.float64 )
                                   )

        @njit
        def run_in_jit(numba_cls):

            numba_cls.incr(0, 1)
            numba_cls.check_me()

        run_in_jit(numba_cls)

    except Exception as e:
        pytest.fail(f"Exception raised: {e}")


# @pytest.mark.skip(reason="temporary")
def test_example_incr_pure_python():
    try:
        from examples import example_incr

        numba_cls = example_incr.init(3)
        numba_cls.incr(0, 1)
        numba_cls.incr(1, 1)
        numba_cls.get_count(0)

    except Exception as e:
        pytest.fail(f"Exception raised: {e}")


def test_example_incr_converted_without_typos():

    from examples.example_incr import ExampleIncr

    try:
        from numbaclass import numbaclass

        ExampleClassNB = numbaclass(_cls=ExampleIncr, cache=True)
        numba_cls = ExampleClassNB(np.zeros(5, dtype=np.int64), 0)
    except Exception as e:
        pytest.fail(f"Exception raised: {e}")


# @pytest.mark.skip(reason="temporary")
def test_can_mutate_from_jitted():

    try:
        from numbaclass import numbaclass
        from examples.example_incr import ExampleIncr

        ExampleClassNB = numbaclass(_cls=ExampleIncr, cache=False)
        numba_cls = ExampleClassNB(np.zeros(3, dtype=np.float64), 0)

        @njit
        def jitted_func(cls):
            cls.incr(0, 1)
            cls.incr(1, 1)
            cls.total_count = 0
            cls.get_count(0)

        jitted_func(numba_cls)

    except Exception as e:
        pytest.fail(f"Exception raised: {e}")


# @pytest.mark.skip(reason="Implement setters generation")
def test_can_mutate_from_purepy():

    try:
        from numbaclass import numbaclass
        from examples.example_incr import ExampleIncr

        ExampleClassNB = numbaclass(_cls=ExampleIncr, cache=False)
        numba_cls = ExampleClassNB(np.zeros(3, dtype=np.float64), 0)

        def python_func(cls):
            cls.incr(0, 1)
            cls.incr(1, 1)
            cls.total_count = 0
            cls.get_count(0)

        python_func(numba_cls)

    except Exception as e:
        pytest.fail(f"Exception raised: {e}")


@pytest.mark.skip(reason="temporary")
def test_can_run_nested_structrefs():

    try:

        from numbaclass import numbaclass

        from examples import example_nest 

        numba_cls = example_nest.init(3)
        numba_cls.update(10.1, 0)
        numba_cls.update(5.3, 1)
        numba_cls.update(6.01, 2)
        numba_cls.update(2.01, 2)
        numba_cls.update(1.01, 2)
        numba_cls.count.get_count(2)

    except Exception as e:
        pytest.fail(f"Exception raised: {e}")