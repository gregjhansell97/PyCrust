from enum import Enum

class Action(Enum):
    '''
    every modfication to a tie_pyified object has an action tied to it
    '''
    CLEAR = 1
    DELETE = 2
    EXTEND = 3
    SET = 4
