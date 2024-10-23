from beaker.cache import clsmap
from my_enums import *
from report import exit_with_message

class InputParser:
    validated = False

    repl_verb_list = ['q', 'h', 'select', 'list', 'add', 'delete']
    verb_info = dict({'q': 'quits the repl loop. No other arguments required.',
                      'h': 'shows this help information. No other arguments required.',
                      'select': 'selects the specified media (only applicable to resource == media)',
                      'list': 'list all the items in teh resource',
                      'add': 'add a new entry to the resource',
                      'delete': 'delete the specified entry'
                      }
        )

    repl_resource_list = ['media', 'wdb', 'lfs']
    resource_info = dict({
                      'media': 'selects the specified media (only applicable to resource == media)',
                      'wdb': 'well-known database',
                      'lfs': 'local file system Media folder'
                      }
        )

    verb_res_combos = list([
        ('media'     , 'select'    , ''                        , 'Select a specific media file.' ),
        ('wdb'       , 'list'      , ''                        , 'Lists all the entries in the wellknown DB'  ),
        ('wdb'       , 'add'       , '-w <wellknown> -u <uri>' , 'Adds an entry to the wellknown db'),
        ('wdb'       , 'delete'    , '-w <wellknown>'          , 'Deletes specified entry from the wellknown db'),
    ])


    @classmethod
    def get_repl_resources(cls):
        return cls.repl_resource_list

    @classmethod
    def get_resources(cls):
        return list(cls.resource_info.keys())

    @classmethod
    def get_repl_verbs(cls):
        return cls.repl_verb_list

    @classmethod
    def get_verbs(cls):
        return list(cls.verb_info.keys())

    @classmethod
    def get_description_of_resource(cls, resourcename):
        return cls.resource_info[resourcename]

    @classmethod
    def get_description_of_verb(cls, verbname):
        return cls.verb_info[verbname]


    @classmethod
    def get_verb_help(cls):
        verblist = cls.get_verbs()
        mesg = ''
        for verb in verblist:
            desc = cls.get_description_of_verb(verb)
            mesg += '\n\t' + verb + ' == ' + desc
        return mesg

    @classmethod
    def get_resource_help(cls):
        reslist = cls.get_resources()
        mesg = ''
        for resy in reslist:
            desc = cls.get_description_of_resource(resy)
            mesg += '\n\t' + resy + ' == ' + desc
        return mesg

    @classmethod
    def get_attrib_of_verb_res(cls, wanted_verb, wanted_resource):
        found = False
        assoc_args = None
        assoc_desc = None
        for entry in cls.verb_res_combos:
            (res, vrb, args, desc) = entry
            if res == wanted_resource and vrb == wanted_verb:
                assoc_args = args
                assoc_desc = desc
                found = True
                break

        if found:
            return (assoc_args, assoc_desc)
        else:
            return None

    @classmethod
    def get_table_of_res_verb_combinations(cls, verb_first=False):
        def format_line(r, v, a, desc):
            pack = '   |   '
            if verb_first:
                x = '\t{0:15}     {1:12}      {2:25}    {3}\n'.format(v, r, a, desc)
                #y = f'\t{r:12}     {v:15}      {a:25}    {desc}\n'
            else:
                #print('{}\n{}: START UNIT TESTS'.format('v' * 80, func_name()))
                x = ('\t{0:12} {pack} {1:15}      {2:25}    {3}\n').format(r, v, a, desc)
                #y = f'\t{r:12} {pack} {v:15} {pack} {a:25}    {desc}\n'
            # if x != y:
            #     errinfo = f'\nnon match\nvvv\nX\n{x}\nY\n{y}\n=====\n'
            #     exit_with_message(errinfo, 55)
            return x

        table_text = '\n' + format_line('Resources', 'Valid Verbs', 'Arguments', 'Description')
        for entry in cls.verb_res_combos:
            (res, vrb, args, desc) = entry
            table_text += format_line(res, vrb, args, desc)
        table_text += '\n'
        return table_text

def simple_func(myarg):
    simple_value = 3
    print(f'CALLED   simple_func')

from utils import func_name
class TestInputParser:

    def __init__(self):
        print(f'INITIALISING TestInputParser')

    def test_verbs(self):
        print('Testing {}.{}'.format(__name__, func_name()))
        expected_verbs = ['q', 'h', 'select', 'list', 'add', 'delete']
        assert InputParser.get_repl_verbs() == expected_verbs
        assert InputParser.get_verbs() == expected_verbs


    def test_resources(self):
        print('Testing {}.{}'.format(__name__, func_name()))
        expected_resources = ['q', 'h', 'select', 'list', 'add', 'delete']
        assert InputParser.get_repl_verbs() == expected_resources
        assert InputParser.get_verbs() == expected_resources


    def test_verb_descriptions(self):
        print('Testing {}.{}'.format(__name__, func_name()))
        simplified_quit = ' '.join(InputParser.get_description_of_verb('q').replace('/t', ' ').split())
        assert 'quit' in simplified_quit, 'Missing q(uit) entry'

        simplified_help = ' '.join(InputParser.get_description_of_verb('h').replace('/t', ' ').split())
        assert 'help' in simplified_help, 'Missing h(elp) entry'

        simplified_select = ' '.join(InputParser.get_description_of_verb('select').replace('/t', ' ').split())
        assert 'select' in simplified_select, 'Missing select entry'


    def test_verb_help(self):
        print('Testing {}.{}'.format(__name__, func_name()))
        help_info = InputParser.get_verb_help()

        # check that for each verb there is a row    <verb> ==
        for the_verb in InputParser.get_verbs():
            #print(f'analyzing help for verb {the_verb}')
            reqd = f'{the_verb} == '
            assert reqd in help_info, f'No mention of verb {the_verb}'

    def test_resource_help(self):
        print('Testing {}.{}'.format(__name__, func_name()))
        res_help_info = InputParser.get_resource_help()

        # check that for each verb there is a row    <verb> ==
        for the_res in InputParser.get_resources():
            #print(f'analyzing help for res {the_res}')
            reqd = f'{the_res} == '
            assert reqd in res_help_info, f'No mention of resource {the_res}'
            # check that indentation of all == are the same

    def test_get_attrib_of_verb_res(self):
        print('Testing {}.{}'.format(__name__, func_name()))
        resp = InputParser.get_attrib_of_verb_res('add', 'wdb')
        if resp is None:
            #print('BAD')
            pass
        (add_wdb_arg, add_wdb_desc) = resp
        assert add_wdb_arg == '-w <wellknown> -u <uri>', 'Bad match on attributes'
        assert '-w' in add_wdb_arg, 'Missing -w attrib for add wdb'
        assert '-u' in add_wdb_arg, 'Missing -u attrib for add wdb'

        all_res = InputParser.get_resources()
        all_verb = InputParser.get_verbs()
        for entry in InputParser.verb_res_combos:
            (res, vrb, args, desc) = entry
            assert res in all_res, f'Invalid resource ({res}) in config data'
            assert vrb in all_verb, f'Invalid resource ({vrb}) in config data'




# import os
# import platform
# import sys
# from report import *
# import pytest
# import utils
# from environ import Environ
#
# PYPLAY_DIR = 'pyplay'
# MEDIA_PATH = 'Media'
#
# MEDIA_PLAYER_FFPLAY = 'ffplay'
# WINDOWS_FFPLAY_PATH = r'E:\DOWNLOAD\Computing\SOFTWARE\FFMPEG\ffmpeg-2022-09-15-git-3f0fac9303-full_build\bin'
# LINUX_FFPLAY_PATH = r'/usr/bin'
#
# MEDIA_PLAYER_VLC = 'vlc'  # 'vlc' 'cvlc'
# WINDOWS_VLC_PATH = r'C:\Program Files\VideoLAN\VLC'  # WINDOWS_VLC_PATH = r'C:\Program Files (x86)\VideoLAN\VLC'
# LINUX_VLC_PATH = r'/snap/bin'
#
# MPEG_Player_Path = None
#
# def set_global_variable():
#     global Cwd
#     Cwd = os.getcwd()
#     mod_mess(__name__, f'CWD: {Cwd} ')
#
#     global Path_2_Files
#     global Path_To_Local_Media
#     if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
#         Run_Context_Bundle = True
#         Path_2_Files = getattr(sys, '_MEIPASS')
#         mod_mess(__name__, f'running in a PyInstaller bundle ')
#         Path_To_Local_Media = os.path.join(Path_2_Files, MEDIA_PATH)
#
#     else:
#         Run_Context_Bundle = False
#         Path_2_Files = Cwd
#         mod_mess(__name__, 'running in a normal Python process')
#         Path_To_Local_Media = os.path.join(Path_2_Files, PYPLAY_DIR, MEDIA_PATH)
#
#     mod_mess(__name__, f'Path_2_files=={Path_2_Files}')
#     mod_mess(__name__, f'Using Path_To_Local_Media == {Path_To_Local_Media}')
#
#     global Platform_Name
#     Platform_Name = platform.system()
#     mod_mess(__name__, f'Using Platform_Name == {Platform_Name}')
#
#     global Media_Player_Ffplay
#     global Media_Player_Vlc
#     if Platform_Name == 'Linux':
#         Media_Player_Ffplay = os.path.join(LINUX_FFPLAY_PATH, MEDIA_PLAYER_FFPLAY)
#         Media_Player_Vlc = os.path.join(LINUX_VLC_PATH, MEDIA_PLAYER_VLC)
#     else:
#         executable = MEDIA_PLAYER_FFPLAY + '.exe'
#         Media_Player_Ffplay = os.path.join(WINDOWS_FFPLAY_PATH, executable)
#         Media_Player_Vlc = os.path.join(WINDOWS_VLC_PATH, MEDIA_PLAYER_VLC)

# def set_av_player(player):
#     global MPEG_Player_Path
#     if player == 'vlc':
#         MPEG_Player_Path = Media_Player_Vlc
#     else:
#         MPEG_Player_Path = Media_Player_Ffplay

# def get_av_player():
#     return MPEG_Player_Path

# def is_absolute_path(pname):
#     resp = os.path.isabs(pname)
#     #print(f'ABS == {resp} \t Path == {pname}')
#     return resp


# def create_protected_path(pathname):
#     #assert Environ.get_platform_name() == Platform_Name
#     #assert Environ.get_platform_name() == 97
#     if Environ.get_platform_name() == 'Windows':
#         new_path = f'"{pathname}" '
#     else:
#         new_path = pathname
#     return new_path
#
# def media_delim(is_start, media_type):
#     the_char = 'v' if is_start else '^'
#     print( media_type + ' ' + the_char * 60)
#
# def starting_media(media_type):
#     media_delim(True, media_type)
#
# def stopping_media(media_type):
#     media_delim(False, media_type)


