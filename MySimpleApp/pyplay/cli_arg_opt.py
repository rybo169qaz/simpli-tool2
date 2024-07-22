import argparse

from my_argparse import *
from report import *
from my_docs import *


class CliArgOpt:
    def __init__(self, the_string, verbose=True):
        self.the_string = the_string
        self.verbose = verbose
        self.parse_obj = None
        self.arg_list = None
        self.arg_dict = None
        self.args = None
        self.parse_problem = False
        self._process_string(the_string)

    def _process_string(self, my_string):
        #self.parse_obj = MyArgParse(description='Parse repl commands')
        self.parse_obj = argparse.ArgumentParser(description='Parse repl commands', exit_on_error=False)
        pars = self.parse_obj

        pars.add_argument("verb", type=str, choices=['q', 'select', 'start', 'stop',
                                                     'dbadd', 'dbdel', 'dbget', 'dblist', 'list', 'help'],
                          help='The verb')


        pars.add_argument('-r', "--resource", type=str, choices=['media', 'db' 'system'],
                          default='system',
                          required = False,
                          help='The resource')

        pars.add_argument('-w', "--wellknown", required=False, type=str,
                            default = None,
                            help = 'The well-known id\n ')

        pars.add_argument('-u', "--uri", required=False, type=str,
                            default = None,
                            help = 'The local identity\n ')

        pars.add_argument('-k', "--key", required=False, type=str,
                          default=None,
                          help='The key for wellknown db\n ')

        pars.add_argument('-v', "--value", required=False, type=str,
                          default=None,
                          help='The value for wellknown db\n ')

        self.arg_list = my_string.split(" ")
        try:
            self.args = pars.parse_args(self.arg_list, None)
            self.arg_dict = vars(self.args)
            print(f'')
            for key, value in self.arg_dict.items():
                print(f"{key.capitalize()} == {value}.")
        except argparse.ArgumentError:
            self.parse_problem = True
            if self.verbose:
                print(f'PROBLEM PARSING >>{argparse.ArgumentError}<<')

    def bad_parse(self):
        if self.verbose:
            print(f'Parse problem == {self.parse_problem}')
        resp = (self.parse_problem, self.arg_list)
        return resp

    def get_verb(self):
        try:
            tmp = self.args.verb
        except:
            if self.verbose:
                print(f'problem parsing verb >>{argparse.ArgumentError}<<')
            tmp = None
        return tmp

    def get_resource(self):
        try:
            tmp = self.args.resource
        except:
            if self.verbose:
                print(f'problem parsing resource >>{argparse.ArgumentError}<<')
            tmp = None
        return tmp

    def get_wellknown(self):
        return self.args.wellknown

    def get_db_key(self):
        return self.args.key

    def get_db_value(self):
        return self.args.value

    def get_uri(self):
        return self.args.uri

    def validate_verb_res(self):
        resp = True
        res = self.args.resource
        vrb = self.args.verb

        if res == 'media':
            if vrb not in ['select']:
                help_info('verbres')
            resp = False

        elif res == 'db':
            if vrb not in ['list']:
                help_info('verbres')
            resp = False
        else:
            # invalid resource
            resp = False
            exit_with_message(f'INTERNAL ERROR - BAD resource >>{res}<<', 123)

        mod_mess('validate_verb_res', f'== {resp}')
        return resp


