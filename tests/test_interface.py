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

def assert_valid_invocations(f):
    """
    Runs a decorated function through several assert statements to verify
    functionality

    Args:
        f: decorated function
    """
    # confirm increments by one on invocation
    f()
    # subscribe a callback to it
    cb = get_callback()
    f.subscribe(cb) 
    assert cb.invocations == 0
    # function invocation
    f()
    assert cb.invocations == 1
    # clear out invocation tally
    cb.invocations = 0
    # loop through and throw in some arguments
    for i in range(10):
        assert cb.invocations == i
        f(i, count=i)
        assert cb.args == (i, )
        assert cb.kwargs == {"count": i}
        assert cb.retval == None
    cb.invocations = 0
    f.unsubscribe(cb)
    f()
    assert cb.invocations == 0

def test_basic_basic_function_decoration():
    # create a decorated function
    @observable
    def f(*args, **kwargs):
        f.invocations += 1
    f.invocations = 0
    assert_valid_invocations(f)
    
def test_method_decoration():
    # you may run into issues where the decorator is tied to the function not
    # each individual function. So if you have two instances of "C" and 
    # you call subscribe for just one of their methods, you may see it on 
    # both...
    class C:
        @observable
        def method(self, *args, **kwargs):
            pass
    c = C()
    print(C.method)
    assert_valid_invocations(c.method)
    # TODO: write full testing impl

def test_property_decoration():
    class C:
        @property
        @observable
        def x(self):
            pass

        @x.setter
        @observable
        def x(self):
            pass
    # TODO: write full testing impl
