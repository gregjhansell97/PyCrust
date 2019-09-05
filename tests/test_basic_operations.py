#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from pynoculars import observable

__author__ = "gregjhansell97"
__copyright__ = "gregjhansell97"
__license__ = "mit"


@observable
class Dog:
    YES = 1
    NO = 2
    def __init__(self, name="dogo", age=0):
        self.name = name
        self.age = age
        self.commands = set()
    def bark(self):
        return "wuff"
    def teach(self, cmd:str):
        self.commands.add(cmd.lower())
    def say(self, cmd:str):
        if cmd.lower() in self.commands:
            return Dog.YES
        else:
            return Dog.NO
    def set_name(self, name):
        self._name = name

def countable(func):
    def wrapper(*args, **kwargs):
        wrapper.count += 1
        func(*args, **kwargs)
    wrapper.count = 0
    return wrapper

#TODO test fixtures

def test_one_subscribe():
    @countable
    def on_teach(dog, retval, cmd:str):
        assert cmd in dog.commands
    @countable
    def on_age_change(dog, old_value, new_value):
        assert old_value + 1 == new_value
    d = Dog("bosco", 10)
    d.teach("sit")
    d.subscribe("teach", on_teach)
    d.teach("roll over")
    d.age = 11
    d.subscribe("age", on_age_change)
    d.age += 1
    assert on_teach.count == 1
    assert on_age_change.count == 1

def test_multiple_subscribe():
    @countable
    def on_teach(dog, retval, cmd:str):
        assert cmd in dog.commands
    @countable
    def on_bark(dog, retval):
        assert retval == "wuff"
    @countable
    def on_say(dog, retval, cmd:str):
        if cmd.lower() in dog.commands:
            assert retval == Dog.YES
        else:
            assert retval == Dog.NO
    d = Dog("bosco", 10)
    d.subscribe("teach", on_teach)
    d.subscribe("bark", on_bark)
    d.teach("sit")
    d.bark()
    d.subscribe("say", on_say)
    assert d.say("sit") == Dog.YES
    assert d.say("roll over") == Dog.NO
    assert on_teach.count == 1
    assert on_bark.count == 1
    assert on_say.count == 2

# TODO test subscription type

    '''
    def callback(name: str):
        pass
    animals = [Animal() for i in range(10)]
    #for a in animals:
    #    a.subscribe(Animal.set_name, callback)
    '''


