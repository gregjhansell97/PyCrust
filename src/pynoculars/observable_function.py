# -*- coding: utf-8 -*-

from abc import abstractmethod, ABC
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


# TODO create an abstract base class
class AbstractObservableFunctor(ABC):
    """
    The class wraps functions and extends their functionality. It maintains a 
    collection of subscribers. These subscribers are notified on invocation
    of the wrapped function. New subscribers can be created with the subscribe
    method; old subscribers can be removed with the unsubscribe method.
    """

    @abstractmethod
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
        raise NotImplementedError

    @abstractmethod
    def unsubscribe(self, callback):
        """
        Removes a registered callback

        Args:
            callback: callback being removed
        """
        raise NotImplementedError


class ObservableFunctor(AbstractObservableFunctor):
    def __init__(self, func):
        self._func = func  # function being wrapped
        self._cbs = []  # list of callbacks

    def __call__(self, *args, **kwargs):
        # makes the class callable
        retval = self._func(*args, **kwargs)
        for callback in self._cbs:
            callback(args, kwargs, retval)

    def __get__(self, instance, class_):
        if instance is not None:
            print(instance, class_)
            return ObservableMethod(instance, ObservableFunctor(self._func))
        else:
            return self

    def subscribe(self, callback, executor=None, loop=None):
        self._cbs.append(callback)

    def unsubscribe(self, callback):
        self._cbs.remove(callback)


class ObservableMethod(AbstractObservableFunctor):
    def __init__(self, instance, functor):
        self._instance = instance
        self._functor = functor

    def __call__(self, *args, **kwargs):
        self._functor(self._instance, *args, **kwargs)

    def subscribe(self, *args, **kwargs):
        self._functor.subscribe(*args, **kwargs)

    def unsubscribe(self, *args, **kwargs):
        self._functor.unsubscribe(*args, **kwargs)


def observable(f):
    return ObservableFunctor(f)
