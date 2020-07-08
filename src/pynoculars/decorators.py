# -*- coding: utf-8 -*-
"""
Module level description
"""

import logging

from pynoculars import __version__

__author__ = "gregjhansell97"
__copyright__ = "gregjhansell97"
__license__ = "mit"


# okay here is the decorator and these are temporary comments
# ex:
# @observable
# def example():
#     ...
# may want to create a instance thats tied to f that stores everything.

class ObservableFunction:
    """
    Agent description
    """
    def __init__(self, f):
        self.func = f

    def __call__(self, *args, **kwargs):
        print("pre-processing")
        self.func(*args, **kwargs)
        print("post-processing")

    def subscribe(self, callback, loop=None, executor=None):
        """
        Subscribe description
        """
        pass 
    # TODO write unsubscribe code

def observable(f):
    """
    Decorator description
    """
    return ObservableFunction(f)

