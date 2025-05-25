from enum import Enum
from pydantic import BaseModel

class RespSuccess(Enum):
    FAILED = 1
    QUALIFIED = 2
    GOOD = 3

class RespQualifierCategory(Enum):
    REFUSED = 1
    FAILED = 2
    INDETERMINATE = 3
    GOOD = 4
    NOINFO = 5
    INVALID_RESOURCE = 6
    INVALID_VERB = 7
    WRONG_NUMBER_OF_PARAMS = 8
    OTHER = 9

class ResourceState(Enum):
    INACTIVE = 1
    ACTIVE = 2
    ACTIVE_NOT_PLAYING = 3
    ACTIVE_PLAYING = 4
    UNKNOWN = 5

class RespStateQual():
    """
    This holds the response information from a handler
    """
    def __init__(self, resp:RespSuccess, qual:RespQualifierCategory=RespQualifierCategory.NOINFO, state:ResourceState=ResourceState.UNKNOWN, qual_val:str=''):
        self.resp = resp
        self.qual = qual
        self.qual_val = qual_val
        self.state = state

    def __str__(self):
        resp_str = self.resp.name
        qual_str = self.qual.name
        qualval_str = str(self.qual_val)
        state_str = self.state.name

        full = f'Success={resp_str}, Qual={qual_str}({qualval_str}), State={state_str}'
        return full