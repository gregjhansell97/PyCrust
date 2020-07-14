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

# TODO create a parent class that handles subscriptions of both functions 
# and methods
class _ObservableFunctor:
    pass

class ObservableMethod:
    """
    """
    def __init__(self, instance, method):
        pass
    def __call__(self, *args, **kwargs):
        pass
    def subscribe(self, callback, executor=None, loop=None):
        pass

        

class ObservableFunctor:
    """
    The class wraps functions and extends their functionality. It maintains a 
    collection of subscribers. These subscribers are notified on invocation
    of the wrapped function. New subscribers can be created with the subscribe
    method; old subscribers can be removed with the unsubscribe method.
    """
    def __init__(self, func):
        self._func = func # function being wrapped
        self._cbs = [] # list of callbacks

    def __call__(self, *args, **kwargs):
        # makes the class callable
        retval = self._func(*args, **kwargs)
        for callback in self._cbs:
            callback(args, kwargs, retval)

    def __get__(self, instance, class_):
        if instance is not None:
            print(instance, class_)
            # TODO: return an observable method that no longer has self bound
            # to it... (woah that would be cool)
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
        self._cbs.append(callback)

    def unsubscribe(self, callback):
        """
        Removes a registered callback

        Args:
            callback: callback being removed
        """
        self._cbs.remove(callback)

def observable(f):
    return ObservableFunctor(f)

'''POTENTIAL
def observable(f):
    """
    Decorator that replaces the function with an ObservableFunction instance
    """
    # cannot just provide a functor, needs to be another function so it can 
    # become a method
    def wrapper(*args, **kwargs):
        wrapper._pynoculars_agent(*args, **kwargs)
    # link observable functor to wrapper
    agent = ObservableFunctor(f)
    wrapper._pynoculars_agent = agent
    wrapper.subscribe = agent.subscribe
    wrapper.unsubscribe = agent.unsubscribe
    return wrapper
'''
