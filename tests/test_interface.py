# -*- coding: utf-8 -*-

import pytest
from pynoculars.decorators import observable

__author__ = "gregjhansell97"
__copyright__ = "gregjhansell97"
__license__ = "mit"


def test_function_decoration():
    @observable
    def func():
        pass
    # TODO: write full testing impl

def test_function_decoration_with_args_and_kwargs():
    @observable
    def func(x, y=0):
        pass
    # TODO: write full testing impl

def test_function_decoration_with_undefined_number_args_and_kwargs():
    @observable
    def func(*args, **kwargs):
        pass
    # TODO: write full testing impl

def test_method_decoration():
    # you may run into issues where the decorator is tied to the function not
    # each individual function. So if you have two instances of "C" and 
    # you call subscribe for just one of their methods, you may see it on 
    # both...
    class C:
        @observable
        def method(self):
            pass
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
