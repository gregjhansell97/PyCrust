tie_py_attributes = [
    "_TiePyWrapper__callbacks",
    "_TiePyWrapper__publish"]
class_attributes = ["__dict__"]
indexable_attributes = ["__setitem__", "__delitem__", "__getitem__"]


def has_attributes(attributes, obj):
    return all([a in dir(obj) for a in attributes])

def get_id():
    if len(get_id.available) > 0:
        return get_id.available.pop()
    else:
        get_id.id += 1
        return get_id.id
get_id.available = []
get_id.id = -1

#PyNoculars
#TiePyrent??
#obj must be indexable
def get_keys(obj):
    '''
    Determines some way to loop through an object and returns the keys
    to the indecies

    Args:
        obj: the object that can be iterated through
    '''
    return obj.keys()

def tie_pyify(obj, callbacks={}):
    '''
    tie_pyify decorates an obj by adding the ability to monitor state changes
    through callbacks. An objects field variables also get wrapped. Indexable
    objects without the __dict__ attribute are copied over into new objects

    Args:
        obj: the object that is being tie-pied (adding monitoring information)
        callbacks: list of callbacks that get called on state change, helpful
            for transitioning an item over from one tie_pied object to another
        available: list of id's available on the callbacks list
    '''
    tie_py_attributes = [
        "_TiePyWrapper__callbacks", 
        "_TiePyWrapper__publish"]
    class_attributes = ["__dict__"]
    indexable_attributes = ["__setitem__", "__delitem__", "__getitem__"]

    #prevents tie_pyify from double wrapping itself, transfers ownership
    if has_attributes(tie_py_attributes, obj):
        #prevents recursive calls of items with the same callbacks (references to references)
        if obj._TiePyWrapper__callbacks is callbacks:
            return

        obj._TiePyWrapper__publish = False
        obj._TiePyWrapper__callbacks = {**obj._TiePyWrapper__callbacks, **callbacks}
        if has_attributes(indexable_attributes, obj):
            for k in get_keys(obj):
                obj[k] = tie_pyify(
                    obj[k], 
                    callbacks = callbacks)
        elif has_attributes(class_attributes, obj): 
            raise ValueError("Not on classes just yet")

        obj._TiePyWrapper__publish = True
        return obj

    #an object with __dict__
    if has_attributes(class_attributes, obj):
        raise ValueError("Not on classes just yet")

    elif has_attributes(indexable_attributes, obj):
        #if an object is indexable, would like to see deep copy
        class_ = obj.__class__
        class TiePyWrapper(class_):
            '''
            Decorates(design pattern not @) indexable objects that do not have
            the __dict__ attribute. The decoration monitors changes in index
            value. An index's index is also monitored (recursively a problem)

            Attributes:
                __callbacks (dict): the key is the id generated and the value is
                    a tuple of: (owner, keys, callback) where the owner is the
                    original object for the callback, key is the keys/attr needed
                    to get to the current dictionary value and callback is the
                    function called
                __publish (bool): should the callback be called or not, if false
                    the callback will not be invoked (internal changes)
            '''
            def __init__(self, obj, callbacks={}):
                #do not call super constructor, copying all values manually
                self.__callbacks = callbacks
                self.__publish = False #used to block callbacks when needed
                 
                #iterates through items of indexable object
                for key in get_keys(obj):
                    self.__setitem__(
                        key,
                        obj[key])

                self.__publish = True

            def __setitem__(self, key, value):
                '''
                wrapper for set item class, invokes callbacks if needed

                Args:
                    key: the key to access the value
                    value: the value being assigned
                '''
                #gotta be a way to try and access a key if there otherwise none
                #in a structure blind way
                if key in get_keys(self):
                    if self[key] is value:
                        return #nothing has changed

                callbacks = {} #copy of callbacks generated for child class
                for id_ in self.__callbacks.keys():
                    owner, keys, cb = self.__callbacks[id_]
                    callbacks[id_] = (owner, keys + [key], cb)

                value = tie_pyify(
                    value,
                    callbacks = callbacks)

                r =  class_.__setitem__(
                    self, 
                    key,
                    value)
                if self.__publish:
                    for owner, keys, callback in self.__callbacks.values():
                        callback(
                            owner, 
                            keys + [key], 
                            value)
                
                return r

            def __delitem__(self, key):
                '''
                wrapper for the delete items, unsubscribes common ids
                from it
                
                Args:
                    key: the key that is being deleted
                '''
                ids = self.__callbacks.keys()
                for key in get_keys(self):
                    if has_attributes(tie_py_attributes, self[key]):
                        self[key].__unsubscribe(ids)

                return class_.__delitem__(self, key)

            def __subscribe(self,id_, owner, keys, callback):
                '''
                gets drivin by the subscribe operator

                Args:
                    id_(int): the id of the callback
                    owner: the originator of the subscription
                    keys: the path from the owner to the value
                    callback(function): gets called on variable change 

               
                '''
                self.__callbacks[id_] = (owner, keys, callback)

                for key in get_keys(self):
                    if has_attributes(tie_py_attributes, self[key]):
                        self[key].__subscribe(id_, owner, keys + [key], callback)

            def subscribe(self, callback):
                '''
                on variable change, callback submitted is called, acting as a
                recursive driver for __subscribe

                Args:
                    callback (function(name, prior, current)): The function that gets
                        called when a field variable changes

                Returns:
                    int: the id of the subscriber
                '''
                id_ = get_id()
                self.__subscribe(id_, self, [], callback) #self og owner
                return id_

            def __unsubscribe(self, ids=[]):
                for id_ in ids:
                   if id_ in self.__callbacks:
                       del self.__callbacks[id_]
                for key in get_keys(self):
                    if has_attributes(tie_py_attributes, self[key]):
                        self[key].__unsubscribe(ids)

            def unsubscribe(self, id_):
                '''
                removes the callback function with that id_ from the subscription list

                Args:
                    id_: the id of the subscriber
                '''
                self.__unsubscribe([id_])
                if id_ not in get_id.available:
                    #this may interfere with partial subscriptions
                    get_id.available.append(id_)

        return TiePyWrapper(
            obj, 
            callbacks = callbacks)
    else:
        return obj
