# inhouse
from tie_py import tie_pyify
from tests.base_dict import TestTiePyBaseDict

class TestTiePyBasicDict(TestTiePyBaseDict):

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

        You shouldn't get a callback for deleting an item, though all of those
        items and it's children should be unsubscribed
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
