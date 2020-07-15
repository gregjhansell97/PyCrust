# -*- coding: utf-8 -*-

import pytest
from pynoculars import observable

__author__ = "gregjhansell97"
__copyright__ = "gregjhansell97"
__license__ = "mit"


def get_callback():
    def cb(args, kwargs, retval):
        cb.invocations += 1
        cb.args = args
        cb.kwargs = kwargs
        cb.retval = retval

    cb.invocations = 0
    cb.args = None
    cb.kwargs = None
    cb.retval = None
    return cb


def get_function():
    @observable
    def f(arg, kwarg=None):
        return arg

    return f


class C:
    def __init__(self):
        self._p = 0

    @observable
    def method(self, arg, kwarg=None):
        return arg

    @observable
    def other_method(self, arg, kwarg=None):
        return arg

def assert_valid_invocations(f):
    """
    Runs a decorated function through several assert statements to verify
    functionality

    Args:
        f: decorated function
    """
    # confirm increments by one on invocation
    f(0, kwarg=2)
    # subscribe a callback to it
    cb = get_callback()
    f.subscribe(cb)
    assert cb.invocations == 0
    # function invocation
    f(0, kwarg=2)
    assert cb.invocations == 1
    # clear out invocation tally
    cb.invocations = 0
    # loop through and throw in some arguments
    for i in range(10):
        assert cb.invocations == i
        f(i, kwarg=i)
        assert cb.args[-1] == i
        assert cb.kwargs == {"kwarg": i}
        assert cb.retval == i
    cb.invocations = 0
    f.unsubscribe(cb)
    f(0, kwarg=1)
    assert cb.invocations == 0


def test_basic_function_decoration():
    # create a decorated function
    assert_valid_invocations(get_function())


def test_basic_method_decoration():
    c = C()
    C.method
    assert_valid_invocations(c.method)


def assert_multiple_functions(functions):
    # create callbacks for every f
    callbacks = [get_callback() for f in functions]
    # subscribe callbacks to functions
    for f, cb in zip(functions, callbacks):
        f.subscribe(cb)

    # invoke each method and confirm appropriate results
    for f, cb in zip(functions, callbacks):
        for i in range(10):
            assert cb.invocations == i
            f(i, kwarg=i)
            assert cb.args[-1] == i
            assert cb.kwargs == {"kwarg": i}
            assert cb.retval == i


def test_multiple_functions_function_decoration():
    functions = [get_function() for _ in range(10)]
    assert_multiple_functions(functions)


def test_multiple_methods_method_decoration():
    # create several instances
    instances = [C() for _ in range(10)]
    # check that accessing method gives you same method
    for c in instances:
        assert c.method is c.method
    # compare two separate instances and their methods
    for c1, c2 in zip(instances[0::2], instances[1::2]):
        assert c1.method is not c2.method
        assert c1.method != c2.method

    methods = [c.method for c in instances]
    methods += [c.other_method for c in instances]
    assert_multiple_functions(methods)
