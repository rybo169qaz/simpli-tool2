from report import *


class WellKnownDB:
    def __init__(self, verbose=True):
        self.verbose = verbose
        self.dict = {}

    def list(self):
        msg = f'Well-known entries\n'
        the_list = []
        for key, value in self.dict.items():
            the_entry = (key, value)
            the_list.append(the_entry)
            #msg += f"{key} == {value}\n"
        return the_list

    def num_entries(self):
        nume = len(self.list())
        #mod_mess(__file__, f'numentries={nume}')
        return nume

    def get(self, wellknown_key):
        value = self.dict.get(wellknown_key, None)
        return value

    def delete(self, wellknown_key):
        if self.get(wellknown_key) is None:
            return False
        else:
            self.dict.pop(wellknown_key)
            return True

    def add(self, wellknown_key, uri_value):
        if self.get(wellknown_key):
            return False
        else:
            self.dict[wellknown_key] = uri_value
            return True


from utils import func_name
class TestWellKnownDB:

    def __init__(self):
        print(f'INITIALISING TestWellKnownDB')

    def test_numentries(self):
        print('Testing {}.{}'.format(__name__, func_name()))
        wdb_num = WellKnownDB()
        assert wdb_num.num_entries() == 0
        wdb_num.add('a', 'uri-a')
        assert wdb_num.num_entries() == 1
        wdb_num.add('b', 'uri-b')
        assert wdb_num.num_entries() == 2
        wdb_num.add('c', 'uri-c')
        assert wdb_num.num_entries() == 3

    def test_add(self):
        print('Testing {}.{}'.format(__name__, func_name()))
        wdb_add = WellKnownDB()

        resp2 = wdb_add.add('xyz', 'https://super.com/a/b/c')
        assert resp2 == True
        assert wdb_add.num_entries() == 1

        # attempting to add an entry with the same key
        resp3 = wdb_add.add('xyz', 'other')
        assert resp3 == False
        assert wdb_add.num_entries() == 1

        # attempting to add an entry with same content but different key
        resp4 = wdb_add.add('pqr', 'https://super.com/a/b/c')
        assert resp4 == True
        assert wdb_add.num_entries() == 2

    def test_delete(self):
        print('Testing {}.{}'.format(__name__, func_name()))
        wdb_del = WellKnownDB()

        wdb_del.add('abc', 'data-abc')
        wdb_del.add('def', 'data-def')
        wdb_del.add('jkl', 'data-jkl')
        assert wdb_del.num_entries() == 3

        assert True == wdb_del.delete('def')
        assert wdb_del.num_entries() == 2

        assert False == wdb_del.delete('def') # deleting non existant entry
        assert wdb_del.num_entries() == 2

        assert True == wdb_del.delete('abc')  # deleting valid entry
        assert wdb_del.num_entries() == 1

        assert True == wdb_del.delete('jkl')  # deleting valid entry
        assert wdb_del.num_entries() == 0

        assert False == wdb_del.delete('XYZ')  # deleting non-existant
        assert wdb_del.num_entries() == 0



    def test_get(self):
        print('Testing {}.{}'.format(__name__, func_name()))
        wdb_get = WellKnownDB()

        wdb_get.add('abc', 'data-abc')
        wdb_get.add('def', 'data-def')
        wdb_get.add('jkl', 'data-jkl')
        assert 'data-def' == wdb_get.get('def')

        wdb_get.delete('def')
        wdb_get.add('def', 'new-content')
        assert 'new-content' == wdb_get.get('def')

        assert 'data-jkl' == wdb_get.get('jkl')


    def test_list(self):
        print('Testing {}.{}'.format(__name__, func_name()))
        wdb_list = WellKnownDB()

        wdb_list.add('abc', 'data-abc')
        wdb_list.add('def', 'data-def')
        wdb_list.add('jkl', 'data-jkl')

        expected = [
            ('abc', 'data-abc'),
            ('def', 'data-def'),
            ('jkl', 'data-jkl')
        ]
        assert expected == wdb_list.list()
