#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from pynoculars import observable

__author__ = "gregjhansell97"
__copyright__ = "gregjhansell97"
__license__ = "mit"


@observable
class Animal:
    def __init__(self, name="animal", age=10):
        self._name = name
        self._age = age
    def set_name(self, name):
        self._name = name


def test_one_subscribe():
    def callback(name: str):
        if(obj.set_name == method):
            pass
    a = Animal()
    a.set_name("greg")
    a.subscribe(Animal.set_name, callback)

def test_multiple_subscribe():
    pass
    '''
    def callback(name: str):
        pass
    animals = [Animal() for i in range(10)]
    #for a in animals:
    #    a.subscribe(Animal.set_name, callback)
    '''


