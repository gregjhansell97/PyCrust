import unittest
from TiePy import tie_pyify

class TestTiePySimpleDicts(unittest.TestCase):
    '''
    runs tests on:
        
    '''
    callback = None

    def setUp(self):
        '''
        Called before every test function, must set static obj
        in the test function itself
        '''
        def callback(obj, keys, value):
            self.assertTrue(callback.obj is obj)
            v = obj
            for k in keys:
                if k in v:
                    v = v[k]
                else:
                    v = None
            self.assertTrue(value is v)
            self.callback.count += 1

        self.callback = callback
        self.callback.count = 0 #called 0 times
        self.callback = callback

    def test_one_layered_pre_initialized(self):
        '''
        Testing one subscriber on a dictionary that's already
        been made before hand (no new keys)
        '''
        x = {"A": 1, "B": 2, "C": 3}
        x = tie_pyify(x, {})
        self.callback.obj = x
        s_id = x.subscribe(self.callback)
        
        x["A"] = 0
        self.assertEqual(self.callback.count, 1)
        x["B"] = 4
        self.assertEqual(self.callback.count, 2)
        x["C"] = -100
        self.assertEqual(self.callback.count, 3)
        x["A"] += 1
        self.assertEqual(self.callback.count, 4)
        #unsubscribing
        x.unsubscribe(s_id)
        x["B"] = 25
        self.assertEqual(self.callback.count, 4)
    
    def test_one_layered_initially_empty(self):
        '''
        Testing one subscriber on a dictionary that's empty
        and new items will be added to it
        '''
        x = tie_pyify({}, {})
        self.callback.obj = x
        s_id = x.subscribe(self.callback)
        
        x["A"] = 0
        self.assertEqual(self.callback.count, 1)
        x["B"] = 4
        self.assertEqual(self.callback.count, 2)
        x["C"] = -100
        self.assertEqual(self.callback.count, 3)
        x["A"] += 1
        self.assertEqual(self.callback.count, 4)
        #unsubscribing
        x.unsubscribe(s_id)
        x["B"] = 25
        x["D"] = 98
        self.assertEqual(self.callback.count, 4)

    def test_one_layered_with_multiple_subscribers(self):
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
    
    def test_one_layered_delete_operation(self):
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
    
    def test_multi_layered_general(self):
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

    def test_multi_layered_delete_operation(self):
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

    def test_in_object_dict_moves(self):
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

        


class TestTiePyComplexDict(unittest.TestCase):
    
    def setUp(self):
        pass

    def getCallbacks(count):
        callbacks = []
        for _ in range(count): 
            def callback(obj, keys, value):
                self.assertTrue(callback.obj is obj)
                v = obj
                for k in keys:
                    if k in v:
                        v = v[k]
                    else:
                        v = None
                self.assertTrue(value is v)
                callback.count += 1
            callback.count = 0
            callback.obj = None
            callbacks.append(callback)
    
    def test_multi_layered_ownership(self):
        pass

class TestTiePyLists(unittest.TestCase):

    def test_one_layered_pre_initialized(self):
        pass

if __name__ == "__main__":
    unittest.main()
