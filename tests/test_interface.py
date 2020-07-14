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

    @property
    def prop(self):
        return self._p

    @prop.setter
    def prop(self, p):
        self._p = p


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
    methods = [c.method for c in instances]
    assert_multiple_functions(methods)


def test_property_decoration():
    def callback(*args, **kwargs):
        print(args)
        print(kwargs)
    c = C()
    c.prop.subscribe(callback)
    c.prop = 10

    # TODO: write full testing impl
