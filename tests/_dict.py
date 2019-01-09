# external modules
import unittest
from collections import defaultdict

# inhouse
from tie_py import tie_pyify

class TestTiePyDicts(unittest.TestCase):
    '''
    runs tests on:

    '''
    callback = None

    def setUp(self):
        '''
        Called before every test function, must set static obj
        in the test function itself
        '''
        def callback(owner, path, method, args):
            path = list(path) 
            self.assertTrue(callback.owner is owner)
            
            #follows the path down
            v = owner
            while len(path) > 0:
                k = path.pop(0)
                if k in v:
                    v = v[k]
                else:
                    self.assertTrue(False)
            if method == dict.__setitem__:
                obj, key, value = args
                self.assertTrue(obj is v)
                self.assertTrue(key in v)
                self.assertTrue(value is v[key])
            elif method == dict.__delitem__:
                obj, key = args
                self.assertTrue(obj is v)
                self.assertTrue(key not in v)
                self.assertTrue(len(path) == 0)
            else:
                self.assertTrue(False)
    
            self.callback.count[method] += 1

        self.callback = callback
        self.callback.count = defaultdict(lambda: 0)

    def assert_count(self, method, expected_count):
        '''
        asserts the count is correct for a given action
        '''
        self.assertEqual(self.callback.count[method], expected_count)

    def test_one_layered_pre_initialized(self):
        '''
        Testing one subscriber on a dictionary that's already
        been made before hand (no new keys)
        '''
        x = {"A": 1, "B": 2, "C": 3}
        x = tie_pyify(x)
        self.callback.owner = x
        s_id = x.subscribe(self.callback)

        x["A"] = 0
        self.assert_count(dict.__setitem__, 1)

        x["B"] = 4
        self.assert_count(dict.__setitem__, 2)

        x["C"] = -100
        self.assert_count(dict.__setitem__, 3)

        x["A"] += 1
        self.assert_count(dict.__setitem__, 4)

        #unsubscribing
        x.unsubscribe(s_id)
        x["B"] = 25
        self.assert_count(dict.__setitem__, 4)

    def test_one_layered_initially_empty(self):
        '''
        Testing one subscriber on a dictionary that's empty
        and new items will be added to it
        '''
        x = tie_pyify({})
        self.callback.owner = x
        s_id = x.subscribe(self.callback)

        x["A"] = 0
        self.assert_count(dict.__setitem__, 1)

        x["B"] = 4
        self.assert_count(dict.__setitem__, 2)

        x["C"] = -100
        self.assert_count(dict.__setitem__, 3)

        x["A"] += 1
        self.assert_count(dict.__setitem__, 4)

        #unsubscribing
        x.unsubscribe(s_id)
        x["B"] = 25
        x["D"] = 98
        self.assert_count(dict.__setitem__, 4)

    def test_one_layered_with_multiple_subscribers(self):
        '''
        Testing multiple subscribers on a dictionary
        '''
        x = tie_pyify({})
        self.callback.owner = x
        sub_count = 10 #must be larger than 3
        ids = [x.subscribe(self.callback) for _ in range(sub_count)]
        
        x["A"] = 0
        self.assert_count(dict.__setitem__, sub_count)

        x["B"] = 4
        self.assert_count(dict.__setitem__, 2*sub_count)

        x["C"] = -100
        self.assert_count(dict.__setitem__, 3*sub_count)

        x["A"] += 1
        self.assert_count(dict.__setitem__, 4*sub_count)

        #partially unsubscribing (removing 3 items)
        for i in range(sub_count - (sub_count - 3)):
            x.unsubscribe(ids.pop())

        x["B"] = 25
        self.assert_count(dict.__setitem__, 4*sub_count + (sub_count - 3))

        #completely unsubscribing
        for s_id in ids:
            x.unsubscribe(s_id)

        x["D"] = 98
        self.assert_count(
            dict.__setitem__,
            4*sub_count + (sub_count - 3))

    def test_one_layered_delete_operation(self):
        '''
        Testing delete operation to ensure the appropriate item gets published

        You shouldn't get a callback for deleting an item, though all of those items and it's
        children should be unsubscribed
        '''
        x = {"A": 1, "B": 2, "C": 3}
        x = tie_pyify(x)
        self.callback.owner = x
        s_id = x.subscribe(self.callback)

        del x["A"]
        self.assert_count(dict.__delitem__, 1)
        self.assert_count(dict.__setitem__, 0)
        self.assertTrue("A" not in x)

        del x["B"]
        self.assert_count(dict.__delitem__, 2)
        self.assertTrue("B" not in x)

        #unsubscribing
        x.unsubscribe(s_id)

        del x["C"]
        self.assert_count(dict.__delitem__, 2)
        self.assertTrue("C" not in x)

    def test_multi_layered_general(self):
        '''
        Testing a multilevel dictionary
        '''
        x = {"A": {"B": 1, "C": {"D": 10}, }, "E": {"F": 30}}
        x = tie_pyify(x)
        self.callback.owner = x
        s_id = x.subscribe(self.callback)

        x["A"]["B"] = 10
        self.assert_count(dict.__setitem__, 1)
        x["A"]["C"]["D"] = 25
        self.assert_count(dict.__setitem__, 2)

        m = x["A"]
        m["B"] = 35
        self.assertEqual(x["A"]["B"], 35)
        self.assert_count(dict.__setitem__, 3)

        m["B"] = {"GREG": 28}
        self.assertEqual(x["A"]["B"], m["B"])
        self.assert_count(dict.__setitem__, 4)

        m["B"]["GREG"] = 29
        self.assertEqual(x["A"]["B"]["GREG"], m["B"]["GREG"])
        self.assert_count(dict.__setitem__, 5)

        g = m
        m = {}
        m["NO"] = "YES"
        self.assert_count(dict.__setitem__, 5)

        g["NO"] = "YES"
        self.assert_count(dict.__setitem__, 6)

        g["NO"] = "YES"
        self.assert_count(dict.__setitem__, 6)

        x["A"]["NO"] = "Maybe"
        self.assert_count(dict.__setitem__, 7)

        x["E"]["F"] = "39"
        self.assert_count(dict.__setitem__, 8)

        x.unsubscribe(s_id)

        x["E"]["F"] = "12"
        self.assert_count(dict.__setitem__, 8)

    def test_multi_layered_delete_operation(self):
        x = {"A": {"B": 1, "C": {"D": 10, "G": 32}, "J": 67}, "E": {"F": 30}}
        x = tie_pyify(x)
        self.callback.owner = x
        s_id = x.subscribe(self.callback)

        del x["A"]["B"]
        self.assert_count(dict.__delitem__, 1)
        self.assertTrue("B" not in x["A"])

        x["A"]["C"]["D"] = 98
        self.assert_count(dict.__setitem__, 1)

        b = x["A"]
        del x["A"]
        self.assert_count(dict.__delitem__, 2)
        self.assertTrue("A" not in x)

        b["D"] = 97
        self.assert_count(dict.__setitem__, 1)

        x.unsubscribe(s_id)

    def test_in_object_dict_moves(self):
        x = {"A": {"B": 1, "C": {"D": 10, "G": 32}, "J": 67}, "E": {"F": 30}}
        x = tie_pyify(x)
        self.callback.owner = x
        s_id = x.subscribe(self.callback)

        m = x["A"]["C"]
        x["H"] = 98
        self.assert_count(dict.__setitem__, 1)

        x["H"] = m
        self.assert_count(dict.__setitem__, 2)

        x["H"]["D"] = 99
        self.assert_count(dict.__setitem__, 3)

        x["A"]["C"] = 45
        self.assert_count(dict.__setitem__, 4)

        x["H"]["D"] = 73
        self.assert_count(dict.__setitem__, 5)

        x["N"] = 42
        self.assert_count(dict.__setitem__, 6)

	#challenge problem
        x["N"] = x
        self.assert_count(dict.__setitem__, 7)
        x["N"]["N"]["N"]["N"] = 10
        self.assert_count(dict.__setitem__, 8)

        #even more challenging
        x["A"]["B"] = x
        self.assert_count(dict.__setitem__, 9)
        x["A"]["B"]["A"]["B"] = 29
        self.assert_count(dict.__setitem__, 10)

        x.unsubscribe(s_id)

    def test_multiple_keys_to_same_object(self):
        x = {"A": {"B": 1, "C": {"D": 10, "G": 32}, "J": 67}, "E": {"F": 30}}
        x = tie_pyify(x)
        self.callback.owner = x
        s_id = x.subscribe(self.callback)

        m = x["A"]["C"]
        x["H"] = 98
        self.assert_count(dict.__setitem__, 1)

        x["H"] = m
        self.assert_count(dict.__setitem__, 2)
 
        x["H"]["D"] = 99
        self.assert_count(dict.__setitem__, 3)

        del x["H"]
        x["A"]["C"]["D"] = 120
        self.assert_count(dict.__setitem__, 4)
    
    def test_in_object_dict_moves_with_multiple_callbacks(self):
        x = {"A": {"B": 1, "C": {"D": 10, "G": 32}, "J": 67}, "E": {"F": 30}}
        x = tie_pyify(x)
        self.callback.owner = x
        s_id = x.subscribe(self.callback)

        def callback_1(owner, path, method, args):
            self.assertTrue(callback_1.owner is owner)
            v = owner
            path = list(path)
            while len(path) > 0:
                k = path.pop(0)
                if k in v:
                    v = v[k]
                else:
                    self.assertTrue(False)
            if method == dict.__setitem__:
                obj, key, value = args
                self.assertTrue(obj is v)
                self.assertTrue(key in v)
                self.assertTrue(value is v[key])
            elif action == dict.__delitem__:
                obj, key = args
                self.assertTrue(obj is v)
                self.assertTrue(key not in v)
            else:
                self.assertTrue(False)
            callback_1.count[method] += 1
        callback_1.count = defaultdict(lambda: 0)

        def assert_count_1(action, expected_count):
            self.assertEqual(callback_1.count[action], expected_count)


        m = {"Z": 1}
        m = tie_pyify(m)
        callback_1.owner = m
        m_id = m.subscribe(callback_1)
        m["L"] = {"T": 98}
        assert_count_1(dict.__setitem__, 1)

        x["A"]["J"] = m
        self.assert_count(dict.__setitem__, 1)
        assert_count_1(dict.__setitem__, 1)
        self.assertTrue(x["A"]["J"] == m)

        m["L"]["T"] = 99
        self.assert_count(dict.__setitem__, 2)
        assert_count_1(dict.__setitem__, 2)
