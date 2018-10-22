from enum import Enum

class Action(Enum):
    '''
    every modfication to a tie_pyified object has an action tied to it
    '''
    SET = 0
    DELETE = 1
    APPEND = 2
    EXTEND = 3
