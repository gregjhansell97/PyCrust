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
    age_subscription = d.subscribe("age", callbacks.on_age_change)
    d.age += 1

    age_subscription.unsubscribe()
    d.age += 1

    assert callbacks.on_teach.count == 1
    assert callbacks.on_age_change.count == 1

def test_one_subscribe_invalid_attribute():
    d = ("bosco", 10)
    try:
        sub = d.subscribe("not_an_attr", None)
    except AttributeError:
        assert True
    except:
        assert False
    else:
        assert False
    

def test_subscription_out_of_scope():
    d = Dog("bosco", 10)
    callbacks = dog_callbacks()
    sub = d.subscribe("bark", callbacks.on_bark)
    del d
    try:
        sub.unsubscribe()
    except ReferenceError:
        pass
    except:
        assert False
    else:
        assert False

def test_multiple_subscribe():
    d = Dog("bosco", 10)
    callbacks = dog_callbacks()
    d.subscribe("teach", callbacks.on_teach)
    teach_subscription = d.subscribe("teach", callbacks.on_teach)
    d.subscribe("bark", callbacks.on_bark)
    d.teach("sit")
    teach_subscription.unsubscribe()
    d.teach("shake hand")
    d.bark()
    say_subscription = d.subscribe("say", callbacks.on_say)
    assert d.say("sit") == Dog.YES
    assert d.say("roll over") == Dog.NO
    assert callbacks.on_teach.count == 3
    assert callbacks.on_bark.count == 1
    assert callbacks.on_say.count == 2

