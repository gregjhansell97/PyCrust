# pynoculars

***

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
custom objects, the reference is maintained but __dict__ is copied.

### Deep Change
When a class inherits from Monitor, all of its member variables are recursively
tie_pyified, ensuring that a member variables' member variables are also
tie_pyified.

### Callback
Callbacks have four named parameters:
#### owner (obj)
The master object that owns the member variable.
#### path (list)
Path from the owner to the value.
#### old (obj)
The value before change was applied.
#### new (obj)
The value after change was applied (None if deleted).
#### action (enum)
The action performed (ex: deletion, setting, append). Current enums defined:
1. Set
2. Delete
3. Append
4. Extend

### Subscription
Subscription takes in a callback and returns an id. The id can be used to
unsubscribe.

***

## Examples
``` python
from pynoculars import Monitor

class Simple(Monitor):
    def __init__(self):
        Monitor.__init__(self)
        self.x = 10

def callback_foo(owner, path, old, new, action):
    pass

obj = Simple()
id_ = obj.subscribe(callback_foo)
obj.x = 10 #no callback invoked, nothing happened
obj.x = 9 #callback invoked, something happened
obj.unsubscribe(id_)
```
***

## Compatability
python >= 3.4.0

***
## History
Original idea was implemented (poorly) in a 7 hour hackathon
Provides call back solutions for field variables and functions that need to be monitored by other objects
