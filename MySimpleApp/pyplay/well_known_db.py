import os.path

from report import *
import json


class WellKnownDB:
    '''
    This holds a simple key value pair mapping
    '''
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

    def dump_to_file(self, dest_file):
        if os.path.isfile(dest_file):
            return False
        json_data = json.dumps(self.dict, sort_keys=True, indent=2)
        the_file = open(dest_file, 'w')
        the_file.write(json_data)
        the_file.close()
        return True

    def load_from_file(self,src_file):
        if not os.path.isfile(src_file):
            return False
        if self.num_entries() != 0:
            return False
        with open(src_file, 'r') as file:
            data = json.load(file)
        #print(f'DATA IS {data}')
        for key in data:
            #print(f'KEY={key}  , VALUE={data[key]}')
            self.add(key, data[key])


        return True

from utils import func_name
class TestWellKnownDB:

    def __init__(self):
        print(f'\nINITIALISING TestWellKnownDB')

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

    def test_dump_to_file(self):
        print('Testing {}.{}'.format(__name__, func_name()))
        wdb_d2f = WellKnownDB()

        # check that it fails if the file exists AND the file is unchanged
        dummy1 = 'tempy1.json'
        with open(dummy1, 'w') as fp:
            pass
        ts = os.path.getmtime(dummy1)
        if not os.path.isfile((dummy1)):
            raise Exception("failed to create the file")
        resp = wdb_d2f.dump_to_file(dummy1)
        assert resp == False, "Should return False if file alreday exusts"
        assert os.path.isfile(dummy1) == True, "The file should still exist"
        assert ts == os.path.getmtime(dummy1), "The file should not have been modified"

        # check that file is created if it does not exist
        dummy2 = 'tempy2.json'
        if os.path.exists(dummy2):
            os.remove(dummy2)
        resp = wdb_d2f.dump_to_file(dummy2)
        assert resp == True, "Provided the file did not exist then it should always return true"
        assert os.path.isfile(dummy2) == True, "The file should exist"

        # check that the dictionary that is written to the file is:
        # valid json, has correct fields, will come out sorted by keyname
        dummy3 = 'temp3.json'
        if os.path.exists(dummy3):
            os.remove(dummy3)
        wdb_d2f.add('zzz', 'rst.mp3')
        wdb_d2f.add('tttt', '/blurb/abc.mp4')
        wdb_d2f.add('bcdef', 'https:/super.com/somewhere/abc.mp3')

        wdb_d2f.dump_to_file(dummy3)
        file = open(dummy3, "r")
        actual_contents = file.read()
        expected_json = '{\n  "bcdef": "https:/super.com/somewhere/abc.mp3",\n  "tttt": "/blurb/abc.mp4",\n  "zzz": "rst.mp3"\n}'
        #print(f'EXPECTED: {expected_json}')
        #print(f'ACTUAL  : {actual_contents}')
        assert actual_contents == expected_json, 'JSON not in expected format'


    def test_load_from_file(self):
        print('Testing {}.{}'.format(__name__, func_name()))
        wdb_lff = WellKnownDB()
        # fail if file does not exist
        non_existant = 'qwerty.mp4'
        if os.path.exists(non_existant):
            os.remove(non_existant)
        resp = wdb_lff.load_from_file(non_existant)
        assert resp == False, "if attempt load non-existant file then return error"

        # fail if wdb is not empty;
        dummy2 = "temp_load2"
        raw_json = '{\n  "bcdef": "https:/super.com/somewhere/abc.mp3",\n  "tttt": "/blurb/abc.mp4",\n  "zzz": "rst.mp3"\n}'
        with open(dummy2, 'w') as fp:
            fp.write(raw_json)
        fp.close()
        wdb_lff.add('abc', 'the-link')
        resp2  = wdb_lff.load_from_file(dummy2)
        assert resp2 == False, "do not allow load of file if WDB is not empty"

        # content of populated WDB
        wdb_lff3 = WellKnownDB()
        dummy3 = "temp_load3"
        raw_json3 = '{\n  "abc": "/sam/dummy.mp3",\n  "pqr": "/abc.mp4",\n  "tttt": "http:acme.com/my_media/file.mp3"\n}'
        with open(dummy3, 'w') as fp3:
            fp3.write(raw_json3)
        fp3.close()
        resp3 = wdb_lff3.load_from_file(dummy3)
        assert resp3 == True, "It should be valid to load an empty DB from file"
        expected_json = '{\n}'
        derived_value = wdb_lff3.get("abc")
        #print(f'DERIVED = {derived_value}')
        assert "/sam/dummy.mp3" == derived_value, "Entry expected"
        assert "/abc.mp4" == wdb_lff3.get("pqr"), "Entry expected"
        assert "http:acme.com/my_media/file.mp3" == wdb_lff3.get("tttt"), "Entry expected"

        # content of empty WDB
        wdb_lff4 = WellKnownDB()
        dummy4 = "temp_load4"
        raw_json4 = '{}'
        with open(dummy4, 'w') as fp4:
            fp4.write(raw_json4)
        fp4.close()
        resp4 = wdb_lff4.load_from_file(dummy4)
        assert resp4 == True, "It should be valid to load an empty DB from file"
        assert wdb_lff4.num_entries() == 0, "should have no entries if empty db file"

