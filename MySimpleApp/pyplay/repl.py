import os.path

import utils
from my_argparse import *
from input_parse import InputParser
import play_it
from my_docs import *
from process_qr import ProcessQR
from cli_arg_opt import CliArgOpt
import verb_handling
from well_known_db import WellKnownDB

class Repl:
    def __init__(self, player_object, store_object=None, repeat=True, interval=1, verbose=True, dummy=True):
        self.player_object = player_object
        self.store_object = store_object
        self.repeat = repeat
        self.interval = interval
        self.verbose = verbose
        self.dummy = dummy
        self.cwd = os.getcwd()
        self.qr_dir = 'Input-Images'
        self.qr_file = 'snap.qr'
        #self.qr_file = 'testsilentvideo.qr'
        self.file_path = '../Input-Images/' + self.qr_file

        print(f'Instantiated Repl (QR file == {self.file_path}, dummy={self.dummy}')


    def _read_keyboard(self, msg):
        prefix = msg + '(q ==quit ; f == qr file) >>>'
        entered = input(prefix)
        return entered

    def _read_image(self, msg):
        prefix = msg + ' Full path == ' + self.file_path
        print('READ IMAGE')
        if 'Input-Images' in self.file_path:
            print(f'valid file path')
        else:
            print(f'INVALID file path')
            msg = 'INVALID FILE PATH - NOT PROGRESSING (' + self.file_path + ')'
            exit_with_message(msg, 999)

        raw = None
        qrobj = ProcessQR(self.file_path, True)
        if qrobj.image_file_exists():
            raw = qrobj.get_raw()
            extra = ' found. raw>>' + raw + '<<'
            os.remove(self.file_path)
        else:
            extra = ' NOT found.'
        print(prefix + extra)
        return raw

    def _read_input(self, msg):
        inp = self._read_keyboard(msg)
        if inp == 'f':
            inp = self._read_image(msg)
            source = 'qrfile'
        else:
            source = 'keyboard'
        return (source, inp)

    def handle_media(self, verb, option_dict):
        fn = __name__ + ':' + 'handle_media'
        mod_mess(fn, f'Handling verb={verb}')

        utils.print_dict(option_dict, 'Provided options')
        well_known = option_dict.get('wellknown', None)
        uri = option_dict.get('uri', None)

        if well_known is not None:
            play_it.play_wellknown(self.player_object, well_known, True)
        elif uri is not None:
            mod_mess(__name__, 'playing media via uri is not supported')
        else:
            exit_with_message('Only well known is supported', 67)

    def handle_local_file_system(self, verb):
        fn = __name__ + ':' + 'handle_local_file_system'
        mod_mess(fn, f'Handling verb={verb}')
        if verb == 'list':
            media_info = 'Media in local file system'
            media_info += verb_handling.list_all_media()
            mod_mess(__name__, media_info)

        else:
            exit_with_message(f'Unknown verb ({verb}', 96)


    def handle_wdb(self, verb, option_dict):
        fn = __name__ + ':' + 'handle_wdb'
        mod_mess(fn, f'Handling verb={verb}')
        utils.print_dict(option_dict, 'Provided options')

        if verb == 'list':
            utils.print_list_tuples(WellKnownDB.list(), 'Shortcuts (aka well-known)',
                'Shortcut',
                '==>',
                'Actual location')

        elif verb == 'add':
            well_known = option_dict.get('wellknown', None)
            uri = option_dict.get('uri', None)
            is_success = WellKnownDB.add(well_known, uri)
            if is_success:
                print(f'Sucessfully added entry')
            else:
                print(f'Failed to add  entry')


        elif verb == 'delete':
            well_known = option_dict.get('wellknown', None)
            is_success = WellKnownDB.delete(well_known)
            if is_success:
                print(f'Successfully deleted entry')
            else:
                print(f'Failed to delete entry')

        else:
            exit_with_message(f'Unknown verb ({verb}', 96)


    def repl_loop(self):
        #infoobj = info_blob.InfoBlob(self.entry_type)


        #verb_list = ['q', 'h', 'select', 'list', 'add', 'delete']
        verb_list = InputParser.get_repl_verbs()

        #resource_list = ['media', 'wdb', 'lfs']
        resource_list = InputParser.get_repl_resources()

        verb_parse = argparse.ArgumentParser(description='Parse VERB', exit_on_error=False)
        #verb_parse.add_argument("verb", type=str, choices=['q', 'select', 'list', 'h'], help='The verb')
        verb_parse.add_argument("verb", type=str, choices=verb_list, help='The verb')

        res_parse = argparse.ArgumentParser(description='Parse RESOURCE', exit_on_error=False)
        #res_parse.add_argument("resource", type=str, choices=['media', 'db' 'system'], default='system', help='The resource')
        res_parse.add_argument("resource", type=str, choices=resource_list, default='system',
                               help='The resource')

        opt_parse = argparse.ArgumentParser(description='Parse OPTIONS', exit_on_error=False)
        opt_parse.add_argument('-w', "--wellknown", required=False, type=str,
                          default=None,
                          help='The well-known id\n ')

        opt_parse.add_argument('-u', "--uri", required=False, type=str,
                          default=None,
                          help='The local identity\n ')



        cont_loop = True
        loop_count =1
        while cont_loop:
            msg = '(' + str(loop_count) + ')'
            src, data_entered = self._read_input(msg)
            if data_entered is not None:

                if True:
                    my_arg_list = data_entered.split(" ")

                    mod_mess('verb check', my_arg_list)
                    the_verb = my_arg_list[0] if len(my_arg_list) > 0 else None
                    if the_verb is None:
                        # no data provided
                        continue

                    if the_verb not in verb_list:
                        info_text = f'Bad VERB >>{the_verb}<<\n' + help_info('verb')
                        mod_mess(__name__, f'{info_text}')
                        continue

                    if the_verb == 'q':
                        print(f'QUITing')
                        break

                    elif the_verb == 'h':
                        info_text = help_info('general')
                        mod_mess(__name__, f'{info_text}')
                        continue

                    else:
                        del my_arg_list[0]
                        mod_mess('resource check', my_arg_list)
                        the_res = my_arg_list[0] if len(my_arg_list) > 0 else None
                        if the_res is None:
                            info_text = f'Missing RESOURCE \n' + help_info('resource')
                            mod_mess(__name__, f'{info_text}')
                            continue

                        if the_res not in resource_list:
                            info_text = f'Bad RESOURCE >>{the_res}<<\n' + help_info('resource')
                            mod_mess(__name__, f'{info_text}')
                            continue

                        del my_arg_list[0]
                        mod_mess('option checks', my_arg_list)
                        parsed = opt_parse.parse_args(my_arg_list, None)

                        opt_dict = vars(parsed)
                        #self.print_dict(opt_dict)

                        my_dict = {}
                        my_dict['wellknown'] = parsed.wellknown
                        my_dict['uri'] = parsed.uri

                        #self.print_dict(my_dict)


                        if the_res == 'media':
                            self.handle_media(the_verb, opt_dict)

                        elif the_res == 'wdb':
                            print(f'about to handle wdb')
                            self.handle_wdb(the_verb, opt_dict)
                            print(f'handled wdb')


                        elif the_res == 'lfs':
                            self.handle_local_file_system(the_verb)

                        else:
                            exit_with_message('INTERNAL ERROR - bad resource', 99)

                        mod_mess(__name__, 'CONTINUING')
                        continue

                else: # never
                    exit_with_message('SHOULD NOT GET HERE', 156)
                    input_obj = CliArgOpt(data_entered)

                    verb = input_obj.get_verb()
                    if verb is None:
                        help_info('verb')
                        print(f'VERB BAD : CONTINUE')
                        continue

                    (bad, arg_list) = input_obj.bad_parse()
                    if bad:
                        info_text = f'Bad VERB or RESOURCE argument. Arg list == >>{arg_list}<<\n'
                        info_text += help_info('syntax')
                        info_text += help_info('verb')
                        info_text += help_info('resource')
                        mod_mess(__name__, f'{info_text}')
                        # continue

                    res = input_obj.get_resource()
                    if res is None:
                        help_info('resource')
                        print(f'RESOURCE BAD : CONTINUE')
                        #continue

                    mod_mess(__name__, f'VERB={verb} , RESOURCE={res}')
                    valid_combo = input_obj.validate_verb_res()
                    if not valid_combo:
                        info_text = f'Bad VERB-RESOURCE combination. Arg list == >>{arg_list}<<\n'
                        info_text += help_info('syntax')
                        info_text += help_info('verbres')
                        mod_mess(__name__, f'{info_text}')
                        continue

                    well_known = input_obj.get_wellknown()
                    uri = input_obj.get_uri()

                    if verb == 'q':
                        print(f'QUITing')
                        break

                    elif verb == 'select':
                        if well_known is not None:
                            play_it.play_wellknown(self.player_object, well_known, True)
                        else:
                            exit_with_message('Only well known is supported', 67)

                    elif verb == 'dbadd':
                        the_key = input_obj.get_db_key()
                        the_value = input_obj.get_db_value()
                        print(f'DB ADD: key={the_key} , value >>{the_value}<<')
                        self.store_object.add_wellknown(the_key, the_value)

                    elif verb == 'dbdel':
                        the_key = input_obj.get_db_key()
                        print(f'DB DEL: key={the_key} ')
                        self.store_object.del_wellknown(the_key)

                    elif verb == 'dbget':
                        the_key = input_obj.get_db_key()
                        the_entry = self.store_object.get_wellknown(the_key)
                        print(f'DB GET: key={the_key} , value >>{the_entry}<<')

                    elif verb == 'dblist':
                        the_list = self.store_object.list_wellknown()
                        print(f'DB LIST: ')
                        for entry in the_list:
                            print(f'ENTRY: value >>{entry}<<')

                    else:
                        msg = 'unknown verb (' + verb + ')'
                        exit_with_message(msg, 69)

            else:
                print(f'Data was None')

            if not self.repeat:
                print(f'EXITING ONE-SHOT')
                break

            #print(f'Sleeping {self.interval}')
            #time.sleep(self.interval)
            loop_count += 1
        if self.verbose:
            print(f'Exiting repl')