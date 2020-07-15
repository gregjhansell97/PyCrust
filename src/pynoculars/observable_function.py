# -*- coding: utf-8 -*-

import asyncio
import concurrent.futures
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

# observable cannot be attached to a property... need to create a separate 
# function that does this... perhaps observe. Should get other machinery up 
# first, perhaps version 0.2.0. This is gonna be version 0.1.0

# TODO create a parent class that handles subscriptions of both functions
# and methods

class ObservableFunctor:
    """
    The class wraps functions and extends their functionality. It maintains a 
    collection of subscribers. These subscribers are notified on invocation
    of the wrapped function. New subscribers can be created with the subscribe
    method; old subscribers can be removed with the unsubscribe method.
    """
    def __init__(self, func):
        self._callbacks = []
        self._func = func  # function being wrapped

    def __call__(self, *args, **kwargs):
        # makes the class callable
        retval = self._func(*args, **kwargs)
        for cb in self._callbacks:
            cb(args, kwargs, retval)

    def __get__(self, instance, cls):
        if instance is not None:
            # handles binding function to instance (method creation)
            # retrieves bound method
            method = self._func.__get__(instance, cls)
            # attempts to access functor corresponding to that
            try:
                return instance._pyno_methods_table[method]
            except AttributeError:
                instance._pyno_methods_table = {}
                # store functor in methods table
                instance._pyno_methods_table[method] = ObservableFunctor(method)
            except KeyError:
                instance._pyno_methods_table[method] = ObservableFunctor(method)
            return instance._pyno_methods_table[method]
        else:
            return self

    def subscribe(self, callback, executor=None, loop=None):
        """
        Registers a callback to receive a notification when the wrapped function
        is successfully invoked. Currently executor and loop do nothing, but
        that will change in later versions, so I want to make it part of the 
        interface now

        Args:
            callback: notified on function invocation, will receive same
                arguments as the wrapped function
            executor (concurrent.futures.Executor): executes callback in thread 
                executor specified
            loop (asyncio.AbstractEventLoop): asyncio eventloop if executor not 
                specified
        """
        self._callbacks.append(callback)

    def unsubscribe(self, callback):
        """
        Removes a registered callback

        Args:
            callback: callback being removed
        """
        self._callbacks.remove(callback)

observable = ObservableFunctor
