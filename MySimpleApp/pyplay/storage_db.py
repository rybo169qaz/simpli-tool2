from report import *
import yamldb
import os

class StorageDB:
    def __init__(self, storage_file, verbose=True, dummy=True):
        self.storage_file = storage_file
        self.verbose = verbose
        self.dummy = dummy
        self.db = None
        self.valid = False
        self.dummy = 'ABC: StorageDB is not working'

    def _prepare(self):
        if not os.path.isfile(self.storage_file):
            exit_with_message('DB file does not exist', 67)

        self.db = yamldb.YamlDB(filename=self.storage_file)
        self.db.load()
        #self.valid = True

    def list_wellknown(self):
        if self.valid is False:
            return self.dummy
        listw = self.db.search('wellknown' + '.*')
        return listw

    def add_wellknown(self, wk, argstring):
        if self.valid is False:
            return self.dummy
        key = 'wellknown.' + wk
        resp = self.db[key] = argstring
        print(f'Add wellknown: wk = {wk} , args = {argstring}, resp = {resp}')

    def del_wellknown(self, wk):
        if self.valid is False:
            return self.dummy
        key = 'wellknown.' + wk
        resp = self.db.delete(key)
        print(f'Del wellknown: wk = {wk} , resp = {resp}')

    def get_wellknown(self, wk):
        if self.valid is False:
            return self.dummy
        key = 'wellknown.' + wk
        the_item = self.db.get(key, default=None)
        print(f'Get wellknown: wk = {wk} , resp = >>{the_item}<<')
        return the_item