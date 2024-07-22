from report import *


class WellKnownDB:
    verbose = True
    dict = {}

    @classmethod
    def list(cls):
        msg = f'Well-known entries\n'
        for key, value in cls.dict.items():
            msg += f"{key} == {value}\n"
        return msg

    @classmethod
    def get(cls, wellknown_key):
        value = cls.dict.get(wellknown_key, None)
        return value

    @classmethod
    def delete(cls, wellknown_key):
        if cls.get(wellknown_key) is None:
            return False
        else:
            cls.dict.pop(wellknown_key)
            return True

    @classmethod
    def add(cls, wellknown_key, uri_value):
        if cls.get(wellknown_key):
            return False
        else:
            cls.dict[wellknown_key] = uri_value
            return True



