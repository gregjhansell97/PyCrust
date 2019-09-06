#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from dog import Dog
from fixtures import dog_callbacks

__author__ = "gregjhansell97"
__copyright__ = "gregjhansell97"
__license__ = "mit"

def test_one_subscribe():
    d = Dog("bosco", 10)
    d.teach("sit")
    callbacks = dog_callbacks()
    d.subscribe("teach", callbacks.on_teach)
    d.teach("roll over")
    d.age = 11
    d.subscribe("age", callbacks.on_age_change)
    d.age += 1
    assert callbacks.on_teach.count == 1
    assert callbacks.on_age_change.count == 1

def test_multiple_subscribe():
    d = Dog("bosco", 10)
    callbacks = dog_callbacks()
    d.subscribe("teach", callbacks.on_teach)
    d.subscribe("bark", callbacks.on_bark)
    d.teach("sit")
    d.bark()
    d.subscribe("say", callbacks.on_say)
    assert d.say("sit") == Dog.YES
    assert d.say("roll over") == Dog.NO
    assert callbacks.on_teach.count == 1
    assert callbacks.on_bark.count == 1
    assert callbacks.on_say.count == 2

