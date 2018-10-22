# pynoculars

## Overview
Provides a way to monitor changes in member variables of a class. Monitoring is
implemented using callbacks. When a member variable is changed, a callback is
invoked which indicates what member variable was changed and how it was changed.

### Monitor
A class that needs to be monitored inherits from the Monitor class. The only
requirement is that Monitor's init() is invoked in all constructors

### tie_pyification
tie_pyificiation is the process that changes dicts/lists/sets/custom objects
into tie_py versions that can be monitored. For built in objects like dicts,
lists and sets, this processes creates a new object rather a reference. For
custom objects, the reference is maintained but __dict__ is copied. There is
more information about tie_pyification in tie_py/README.md

### Deep Change
When a class inherits from Monitor, all of its member variables are recursively
tie_pyified, ensuring that a member variables' member variables are also
tie_pyified.

### Callback
Callbacks have four named parameters:
1. owner (obj): The master object that owns the member variable.
2. path (list): Path from the owner to the value.
4. value (obj) The value after change was applied (None if deleted).
5. action (enum) The action performed (ex: deletion, setting, append). Current
enums defined are: Set, Delete, Append, Extend

### Subscription
Subscription takes in a callback and returns an id. The id can be used to
unsubscribe.

## Examples
``` python
from pynoculars import Monitor

class Simple(Monitor):
    def __init__(self):
        Monitor.__init__(self)
        self.x = 10

def callback_foo(owner, path, value, action):
    pass

obj = Simple()
id_ = obj.subscribe(callback_foo)
obj.x = 10 #no callback invoked, nothing happened
obj.x = 9 #callback invoked, something happened
obj.unsubscribe(id_)
```

## Versions
python >= 3.4.0

## Installation
Clone repo for now. I still need to figure out how to get on PIP!

## History
Wow can't believe you made it this far. Okay you history buffs here it goes. The
original idea was implemented (poorly) in a 7 hour hackathon. The tie_py part is
a relic of that hackathon. I couldn't think of a good name for the module and I
was wearing a tie dye shirt...
