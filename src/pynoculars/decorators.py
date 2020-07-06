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
def observable(f):
    """
    Decorator description
    """
    # need to attach information to the function
    print("HERE")
    def wrapper(*args, **kwargs):
        print("pre-processing")
        f(*args, **kwargs)
        print("post-processing")
    wrapper.attached_data = {}
    return wrapper
