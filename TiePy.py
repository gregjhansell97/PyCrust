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

def get_keys(obj):
    '''
    Determines some way to loop through an object and returns the keys
    to the indecies

    Args:
        obj: the object that can be iterated through
    '''
    if  issubclass(obj.__class__, list):
        return range(len(obj))
    else:
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
        "_TiePyWrapper__publish",
        "_TiePyWrapper__chain"]
    class_attributes = ["__dict__"]
    indexable_attributes = ["__setitem__", "__delitem__", "__getitem__"]

    #prevents tie_pyify from double wrapping itself, transfers ownership
    if has_attributes(tie_py_attributes, obj):
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
                #manual copying is needed to ensure that all items get set
                self.__callbacks = callbacks
                self.__publish = False #used to block callbacks when needed
                self.__chain = []
                #iterates through items of indexable object
                for key in get_keys(obj):
                #lists are struggling here because they would be initially empty
                    self.__setitem__(
                        key,
                        obj[key])

                self.__publish = True
            def __getitem__(self, key): #need to implement
                item = class_.__getitem__(self, key)
                if has_attributes(tie_py_attributes, item) and self not in item.__chain:
                    item.__chain.append(self)
                return item

            #when append gets called does set item get invoked?

            def __setitem__(self, key, value): #need to implement
                '''
                wrapper for set item class, invokes callbacks if needed

                Args:
                    key: the key to access the value
                    value: the value being assigned
                '''
                #if key doesn't change then don't do anything
                if value not in self.__chain and value is not self:
                    if key in get_keys(self):
                        if self[key] is value:
                            return value

                    callbacks = {} #copy of callbacks generated for child class
                    for id_ in self.__callbacks.keys():
                        owner, keys, cb = self.__callbacks[id_]
                        callbacks[id_] = (owner, keys + [key], cb)

                    value = tie_pyify(
                        value,
                        callbacks = callbacks)
                r = class_.__setitem__(
                    self,
                    key,
                    value)

                self.__run_callbacks(value, key)

                return r

            def __run_callbacks(self, value, key):
                '''
                given a value and key, invokes all the callbacks accordingly

                Args:
                    value: the value changed to
                    key: the key for that value
                '''
                if not self.__publish:
                    return
                for owner, keys, callback in self.__callbacks.values():
                    callback(
                        owner,
                        keys + [key],
                        value)

            def __delitem__(self, key): #need to implement
                '''
                wrapper for the delete items, unsubscribes common ids
                from it

                Args:
                    key: the key that is being deleted
                '''
                if has_attributes(tie_py_attributes, self[key]):
                    ids = list(self.__callbacks.keys())
                    self[key].__unsubscribe(ids)

                return class_.__delitem__(self, key)

            def __subscribe(self, id_, owner, keys, callback):
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
                '''
                a list of id's to unsubscribe the object from (remove callbacks), intended
                for internal use but if you're feeling confident try it out!

                Args:
                    ids ([int]): the list of ids that are being unsubscribed from
                '''
                for id_ in ids:
                   if id_ in self.__callbacks:
                       owner, _, _ = self.__callbacks[id_]
                       if owner is self and id_ not in get_id.available:
                           get_id.available.append(id_)
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
                if id_ in self.__callbacks:
                    self.__unsubscribe([id_])

        return TiePyWrapper(
            obj,
            callbacks = callbacks)
    else:
        return obj
