import unittest

from collections import defaultdict
from tie_py import tie_pyify
from tie_py._enums import Action


class TestTiePyList(unittest.TestCase):
    '''
    runs tests on:

    '''
    callback = None

    def setUp(self):
        '''
        Called before every test function, must set static obj
        in the test function itself
        '''
        def callback(owner, path, value, action):
            self.assertTrue(callback.owner is owner)
            v = owner
            end_early = (action == Action.EXTEND or action == Action.CLEAR)
            try:
                for i in range(len(path) - end_early):
                    step = path[i]
                    v = v[step]
            except Exception as e:
                self.assertTrue(False)
            if action == Action.SET:
                self.assertTrue(value is v)
            if action == Action.EXTEND:
                self.assertEqual(v[path[-1]:], value) 
            if action == Action.CLEAR:
                self.assertEqual(len(v), 0)
                self.assertEqual(value, [])
            self.callback.count[action] += 1

        self.callback = callback
        self.callback.count = defaultdict(lambda: 0)
    def assert_count(self, action, expected_count):
        '''
        asserts the count is correct for a given action
        '''
        self.assertEqual(self.callback.count[action], expected_count)

    def test_one_layered_set(self):
        '''
        Testing one subscriber on a list that's already
        been made before hand
        '''
        x = [1, 2, 3]
        x = tie_pyify(x, {})
        self.callback.owner = x
        s_id = x.subscribe(self.callback)

        x[0] = 1
        self.assert_count(Action.SET, 0)
        x[0] = 0
        self.assert_count(Action.SET, 1)
        x[1] = 4
        self.assert_count(Action.SET, 2)
        x[2] = -100
        self.assert_count(Action.SET, 3)
        x[0] += 1
        self.assert_count(Action.SET, 4)
        #unsubscribing
        x.unsubscribe(s_id)
        x[2] = 25
        self.assert_count(Action.SET, 4)

    def test_one_layered_append(self):
        '''
        Testing one subscriber on a dictionary that's empty
        and new items will be added to it
        '''
        x = tie_pyify([], {})
        self.callback.owner = x
        s_id = x.subscribe(self.callback)

        x.append(0)
        self.assert_count(Action.SET, 1)
        x[0] = 12
        self.assert_count(Action.SET, 2)

        x.append(2)
        self.assert_count(Action.SET, 3)
        x[1] = 32
        self.assert_count(Action.SET, 4)

        x.append(3)
        self.assert_count(Action.SET, 5)

        #unsubscribing
        x.unsubscribe(s_id)
        x[0] = 25
        self.assert_count(Action.SET, 5)
        x.append(3)
        self.assert_count(Action.SET, 5)

    def test_one_layered_extend(self):
        x = tie_pyify([1, 2], {})
        self.callback.owner = x
        s_id = x.subscribe(self.callback)

        x.extend([4, 5])
        self.assert_count(Action.SET, 0)
        self.assert_count(Action.EXTEND, 1)

        x.extend([])
        self.assert_count(Action.EXTEND, 2)
    
        x.extend([1])
        self.assert_count(Action.EXTEND, 3)
 
        self.assertEqual(len(x), 5)
        self.assertEqual(x[0], 1)
        self.assertEqual(x[1], 2)
        self.assertEqual(x[2], 4)
        self.assertEqual(x[3], 5)
        self.assertEqual(x[4], 1)
       
        #unsubscribing
        x.unsubscribe(s_id)
        x.extend([2, 3])
        self.assert_count(Action.EXTEND, 3)
        self.assertEqual(x[-2:], [2, 3])

    def test_one_layered_iadd(self):
        x = tie_pyify([1, 2], {})
        self.callback.owner = x
        s_id = x.subscribe(self.callback)

        x += [4, 5]
        self.assert_count(Action.SET, 0)
        self.assert_count(Action.EXTEND, 1)

        x += []
        self.assert_count(Action.EXTEND, 2)
    
        x += [1]
        self.assert_count(Action.EXTEND, 3)
 
        self.assertEqual(len(x), 5)
        self.assertEqual(x[0], 1)
        self.assertEqual(x[1], 2)
        self.assertEqual(x[2], 4)
        self.assertEqual(x[3], 5)
        self.assertEqual(x[4], 1)
       
        #unsubscribing
        x.unsubscribe(s_id)
        x += [2, 3]
        self.assert_count(Action.EXTEND, 3)

    def test_one_layered_clear(self):
        x = tie_pyify([1, 2, 3, 4], {})
        self.callback.owner = x
        s_id = x.subscribe(self.callback)
        
        x.clear()
        self.assert_count(Action.CLEAR, 1)
        self.assertEqual(x, [])
        
        x.append(1)
        self.assert_count(Action.SET, 1)
        self.assert_count(Action.CLEAR, 1)
        self.assertEqual(x, [1])

        x.clear()
        self.assert_count(Action.CLEAR, 2)
        self.assertEqual(x, [])

        x.clear()
        self.assert_count(Action.CLEAR, 3)
        self.assertEqual(x, [])

        #unsubscribing
        x.unsubscribe(s_id)
        x.clear()
        self.assert_count(Action.CLEAR, 3)

    def test_one_layered_insert(self):
        pass    

    def _test_one_layered_with_multiple_subscribers(self):
        '''
        Testing multiple subscribers on a dictionary
        '''
        x = tie_pyify({}, {})
        self.callback.obj = x
        sub_count = 10 #must be larger than 3
        ids = [x.subscribe(self.callback) for _ in range(sub_count)]
        x["A"] = 0
        self.assertEqual(self.callback.count, sub_count)
        x["B"] = 4
        self.assertEqual(self.callback.count, 2*sub_count)
        x["C"] = -100
        self.assertEqual(self.callback.count, 3*sub_count)
        x["A"] += 1
        self.assertEqual(self.callback.count, 4*sub_count)
        #partially unsubscribing (removing 3 items)
        for i in range(sub_count - (sub_count - 3)):
            x.unsubscribe(ids.pop())
        x["B"] = 25
        self.assertEqual(
            self.callback.count,
            4*sub_count + (sub_count - 3))
        #completely unsubscribing
        for s_id in ids:
            x.unsubscribe(s_id)
        x["D"] = 98
        self.assertEqual(
            self.callback.count,
            4*sub_count + (sub_count - 3))

    def _test_one_layered_delete_operation(self):
        '''
        Testing delete operation to ensure the appropriate item gets published

        You shouldn't get a callback for deleting an item, though all of those items and it's
        children should be unsubscribed
        '''
        x = {"A": 1, "B": 2, "C": 3}
        x = tie_pyify(x, {})
        self.callback.obj = x
        s_id = x.subscribe(self.callback)

        del x["A"]
        self.assertEqual(self.callback.count, 0)
        del x["B"]
        self.assertEqual(self.callback.count, 0)
        #unsubscribing
        x.unsubscribe(s_id)
        del x["C"]
        self.assertEqual(self.callback.count, 0)

    def _test_multi_layered_general(self):
        '''
        Testing a multilevel dictionary
        '''
        x = {"A": {"B": 1, "C": {"D": 10}, }, "E": {"F": 30}}
        x = tie_pyify(x, {})
        self.callback.obj = x
        s_id = x.subscribe(self.callback)

        x["A"]["B"] = 10
        self.assertEqual(self.callback.count, 1)
        x["A"]["C"]["D"] = 25
        self.assertEqual(self.callback.count, 2)

        m = x["A"]
        m["B"] = 35
        self.assertEqual(x["A"]["B"], 35)
        self.assertEqual(self.callback.count, 3)

        m["B"] = {"GREG": 28}
        self.assertEqual(x["A"]["B"], m["B"])
        self.assertEqual(self.callback.count, 4)

        m["B"]["GREG"] = 29
        self.assertEqual(x["A"]["B"]["GREG"], m["B"]["GREG"])
        self.assertEqual(self.callback.count, 5)

        g = m
        m = {}
        m["NO"] = "YES"
        self.assertEqual(self.callback.count, 5)

        g["NO"] = "YES"
        self.assertEqual(self.callback.count, 6)

        g.unsubscribe(s_id)
        g["NO"] = "NO"
        self.assertEqual(self.callback.count, 6)

        x["A"]["NO"] = "Maybe"
        self.assertEqual(self.callback.count, 6)

        x["E"]["F"] = "39"
        self.assertEqual(self.callback.count, 7)

        x.unsubscribe(s_id)
        x["E"]["F"] = "12"
        self.assertEqual(self.callback.count, 7)

    def _test_multi_layered_delete_operation(self):
        x = {"A": {"B": 1, "C": {"D": 10, "G": 32}, "J": 67}, "E": {"F": 30}}
        x = tie_pyify(x, {})
        self.callback.obj = x
        s_id = x.subscribe(self.callback)

        del x["A"]["B"]
        self.assertEqual(self.callback.count, 0)
        self.assertTrue("B" not in x["A"])

        x["A"]["C"]["D"] = 98
        self.assertEqual(self.callback.count, 1)

        b = x["A"]
        del x["A"]
        b["D"] = 97
        self.assertEqual(self.callback.count, 1)

        x.unsubscribe(s_id)

    def _test_in_object_dict_moves(self):
        x = {"A": {"B": 1, "C": {"D": 10, "G": 32}, "J": 67}, "E": {"F": 30}}
        x = tie_pyify(x, {})
        self.callback.obj = x
        s_id = x.subscribe(self.callback)

        m = x["A"]["C"]
        x["H"] = 98
        self.assertEqual(self.callback.count, 1)


        x["H"] = m
        self.assertEqual(self.callback.count, 2)
        x["H"]["D"] = 99
        self.assertEqual(self.callback.count, 3)

        x["A"]["C"] = 45
        self.assertEqual(self.callback.count, 4)

        x["H"]["D"] = 73
        self.assertEqual(self.callback.count, 5)

        x["N"] = 42
        self.assertEqual(self.callback.count, 6)

	#challenge problem
        x["N"] = x
        self.assertEqual(self.callback.count, 7)
        x["N"]["N"]["N"]["N"] = 10
        self.assertEqual(self.callback.count, 8)

        #even more challenging
        x["A"]["B"] = x
        self.assertEqual(self.callback.count, 9)
        x["A"]["B"]["A"]["B"] = 29
        self.assertEqual(self.callback.count, 10)

    def _test_in_object_dict_moves_with_multiple_callbacks(self):
        x = {"A": {"B": 1, "C": {"D": 10, "G": 32}, "J": 67}, "E": {"F": 30}}
        x = tie_pyify(x, {})
        self.callback.obj = x
        s_id = x.subscribe(self.callback)

        def callback_1(obj, keys, value):
            self.assertTrue(callback_1.obj is obj)
            v = obj
            for k in keys:
                if k in v:
                    v = v[k]
                else:
                    v = None
            self.assertTrue(value is v)
            callback_1.count += 1
        callback_1.count = 0


        m = {"Z": 1}
        m = tie_pyify(m, {})
        callback_1.obj = m
        m_id = m.subscribe(callback_1)
        m["L"] = {"T": 98}
        self.assertEqual(callback_1.count, 1)

        x["A"]["J"] = m
        self.assertEqual(self.callback.count, 1)
        self.assertEqual(callback_1.count, 1)
        self.assertTrue(x["A"]["J"] == m)

        m["L"]["T"] = 99
        self.assertEqual(self.callback.count, 2)
        self.assertEqual(callback_1.count, 2)
