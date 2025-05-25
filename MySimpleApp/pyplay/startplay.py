import sys
import inspect

#from sqlobject.converters import ClassType

#from MySimpleApp.pyplay.pytest_unittests.test_input_parse import TestXInputParser
from av_player import *
from media_identity import *
from my_argparse import *
import verb_handling
#import play_it
from report import *
from repl import Repl
#from storage_db import StorageDB
from well_known_db import *
import const_data
from environ import Environ
#from utils import get_methods_in_class

#import input_parse
from input_parse import *
from repl2 import replloop
from loguru import logger


required_version = (3,10)
actual_version = (sys.version_info.major, sys.version_info.minor)
if not actual_version >= required_version:
    sys.exit(f'Version is bad (required={required_version} ; actual={actual_version}')

# Global variable
Cwd = None
Dummy_Mode = False
Media_Player_Name = 'vlc'
Media_Player_Ffplay = None
Media_Player_Vlc = None
MPEG_Player_Path = None
Path_2_Files = None
Path_To_Local_Media = None
Run_Context_Bundle = 'undefined'
Verbose = False

PLAYER_TYPE = 'FFPLAY'  # 'VLC' 'FFPLAY'


def show_runtime_info():
    mod_mess(__name__ + ':show_runtime_info', f'unreliable')
    if Run_Context_Bundle:
        mod_mess(__name__, f'running in a PyInstaller bundle ')
    else:
        mod_mess(__name__, 'running in a normal Python process')
    mod_mess(__name__, f'Path to media player == {MPEG_Player_Path}\n')


def show_passed_args(the_args):
    mod_mess(__name__, f"show_passed_args")
    mod_mess(__name__, f"verbose == {the_args.verbose}")
    mod_mess(__name__, f"dummy == {the_args.dummy}")
    mod_mess(__name__, f"info == {the_args.info}")
    mod_mess(__name__, f"player == {the_args.player}")
    mod_mess(__name__, f"Repeat interval == {the_args.repeat}")
    mod_mess(__name__, f"Action == {the_args.action}")
    mod_mess(__name__, f"CLIargs == {the_args.cliargs}")
    mod_mess(__name__, f"\n")


def show_help():
    wanted_text = '''
    help               This text
    listl              List local media and then exit.
    listw              List wellknown names and then exit
    repl     (Default) Move into command and control mode (Read Execute Print Loop)
    '''
    mod_mess(__name__, f'{wanted_text}')

global MEDIA_PLAYER_FFPLAY

def populate_wellknown(the_db):
    for entry in const_data.well_known_uris:
        (wellknown, mid) = entry
        the_db.add(wellknown, mid)

def list_welknown():
    print(f'not displaying\n')
    return
    new_array = []
    new_array.append('Well-known == Value')
    new_array.append('===================')
    the_list_obj = WellKnownDB.list()
    for i in the_list_obj:
        my_key, my_value = i
        combi = f"{my_key} == {my_value}"
        new_array.append(combi)

    new_msg = utils.create_prefixed_list('\nList of well-known entries', 'End of list\n', '\t', '\n', new_array)
    for x in new_msg:
        print(f'{x}')

def local_func(local_in):
    iny = local_in
    mylocal = 99
    return 77

tim = 'abc'

def do_unit_tests():

    def call_the_methods(class_instance, wanted_methods):
        for x in wanted_methods:
            getattr(class_instance, x)()

    def perform_class_test(module_name, class_name_to_test):
        print(f'vvv===== START TEST {module_name} {class_name_to_test}')

        funcy = getattr(module_name, class_name_to_test)
        valinfunc = getattr(funcy, 'mylocal')

        tc = funcy(class_name_to_test)
        tc_methods_list = [method for method in dir(funcy) if method.startswith('__') is False]
        call_the_methods(tc, tc_methods_list)
        print(f'^^^==== END TEST {class_name_to_test}\n')

    if False:
        print('{}\n{}: START UNIT TESTS'.format('v' * 80, func_name()))
        myx = callable(getattr('startplay', 'local_func'))
        print(f'TIM IS {myx}\n')

        print(f'+++++')
        perform_class_test('local_func', 'iny')

    tc = TestInputParser()
    tc_methods_list = [method for method in dir(TestInputParser) if method.startswith('__') is False]
    call_the_methods(tc, tc_methods_list)

    tmi = TestMediaIdentity()
    tmi_methods_list = [method for method in dir(TestMediaIdentity) if method.startswith('__') is False]
    call_the_methods(tmi, tmi_methods_list)

    twk = TestWellKnownDB()
    twk_methods_list = [method for method in dir(TestWellKnownDB) if method.startswith('__') is False]
    call_the_methods(twk, twk_methods_list)

    #perform_class_test('input_parse', 'simple_func')

    print('{}\n{}: END UNIT TESTS'.format('^' * 80, func_name()))

def main():

    Environ()
    Environ.show_environment_key_values()

    mod_mess(__name__, f'Python script invoked: {sys.argv[0]}')
    cmndline_args = sys.argv[1:]
    action_cmnd = None
    args_to_pass = None
    delim_char = ','
    try:
        delim_index = cmndline_args.index(delim_char)
        action_cmnd = cmndline_args[0:delim_index]
        args_to_pass = cmndline_args[delim_index+1:]
        print(f'DELIM ({delim_char}) INDEX == {delim_index}')
    except ValueError:
        print(f'No delimchar ({delim_char})')
        action_cmnd = cmndline_args


    print(f'ACTION COMMAND == {action_cmnd}')
    print(f'PASS COMMAND == {args_to_pass}')

    mod_mess(__name__, f'Commandline arguments: {cmndline_args}')

    parser3 = argparse.ArgumentParser(description='A simple program to demonstrate argparse usage')
    parser = MyArgParse(description='Parses the commandline')

    # Adding arguments
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose mode')
    parser.add_argument('-d', '--dummy', action='store_true', help='Pretend to do the action')
    parser.add_argument('-i', '--info', action='store_true', help='Request descriptive info on a particular topic')

    # parser.add_argument('-l', "--location", required=False, type=str,
    #                     default='test',
    #                     choices=['test', 'usb', 'remote'],
    #                     help='The repo identity')

    parser.add_argument('-p', '--player', required=False, type=str,
                        default='ffmpeg',
                        choices=['vlc', 'plug', 'ffmpeg', 'chromium'],
                        help='The media player')

    # parser.add_argument('-f', '--format', required=False, type=str,
    #                     default='cmdstr',
    #                     choices=['cmdstr', 'qr', 'camera'],
    #                     help='The media player')

    # parser.add_argument('-k', "--known", required=False, type=str,
    #                     default='unspecified',
    #                     help='A wellknown file is being specified.\n '
    #                          'To see all well-known data then use the list verb (no additional params reqd) \n'
    #                          'These are local to to the tool unless they include  remote  in their name.')

    # parser.add_argument('-q', "--qrloc", required=False, type=str,
    #                     default='unspecified',
    #                     help='The file containing the QR code\n ')

    parser.add_argument('-r', '--repeat', required=False, type=int,
                        default=5,
                        help='Repeat interval. 0 == no repeat; positive values are delay in seconds\n')

    parser.add_argument("action", type=str, choices=['listw', 'listl', 'repl', 'repl2', 'help', 'unit'],
                        default = 'repl',
                        help='The action')

    parser.add_argument('-c', '--cliargs', required=False, type=str,
                        default="",
                        help='CLI args to pas to the REPL\n')

    args = parser.parse_args(args=action_cmnd)
    show_passed_args(args)

    # Accessing parsed arguments
    global Dummy_Mode
    if args.dummy:
        Dummy_Mode = True

    global Media_Player_Name
    Media_Player_Name = args.player

    global Verbose
    if args.verbose:
        Verbose = True
    Verbose = True

    repeat_interval = args.repeat

    player_obj = AvPlayer(args.player, Verbose, Dummy_Mode)
    player_obj.discover()
    print(f'GOT HEERE A')


    if Verbose:
        mod_mess(__name__, f'Verbose mode enabled')

        mod_mess(__name__, f'ENV CWD == {Environ.get_cwd()}')
        #mod_mess(__name__, f'CWD == {Cwd}')
        #assert Environ.get_cwd() == Cwd

        play = player_obj.get_tool_name()
        mod_mess(__name__, f"player == {play}")
        playtool = player_obj.get_media_player_path()
        mod_mess(__name__, f"player-path == {playtool}")

        show_runtime_info()

    if args.info:
        my_docs.help_info()

    the_action = args.action
    mod_mess(__name__, f'Action = {the_action}')


    #populate_wellknown()
    #list_welknown()


    if the_action == 'help':
        print('HELP')
        show_help()
        exit_with_message(f'Command completed', 0)


    elif the_action == 'listl':
        print('list local')
        #verb_handling.list_all_media()
        verb_handling.print_all_media()

        exit_with_message(f'LIST LOCAL Command completed', 0)

    elif the_action == 'listw':
        print('list wellknown')
        verb_handling.list_well_known()
        exit_with_message(f'LIST WELL KNOWN Command completed', 0)

    elif the_action == 'unit':
        do_unit_tests()
        exit_with_message(f'UNIT TESTS COMPLETED', 0)

    elif the_action == 'repl':
        print(f'DOING repl')
        # assume repl
        dbfile = 'alpha-db.yaml'
        welldb = WellKnownDB()
        populate_wellknown(welldb)
        stor_obj = None # StorageDB(dbfile)
        repl_obj = Repl(welldb, player_obj, stor_obj, repeat=True, interval=3, verbose=True, dummy=False)
        repl_obj.repl_loop(initial_cmd=args_to_pass)
        exit_with_message(f'Command completed (qr)', 0)

    elif the_action == 'repl2':
        logger.debug(f'ACTIONING repl2. The passed string is "{args.cliargs}"')
        #print(f'DOING repl2. The passed string is "{args.cliargs}"')
        replloop(args.cliargs)


    exit(0)


if __name__ == "__main__":
    main()
