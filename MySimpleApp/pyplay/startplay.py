import sys

from av_player import *
from media_identity import *
from my_argparse import *
import verb_handling
#import play_it
from report import *
from repl import Repl
#from storage_db import StorageDB
from well_known_db import WellKnownDB
import const_data
from environ import Environ


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

def populate_wellknown():
    for entry in const_data.well_known_uris:
        (wellknown, mtype, mloc, mstream, mid) = entry
        WellKnownDB.add(wellknown, mid)

        # mod_mess(pfx, WellKnownDB.list())
        # WellKnownDB.add('apple', 'myapple.mp3')
        # WellKnownDB.add('berry', 'myberry.mp4')
        # mod_mess(pfx, WellKnownDB.list())
        # WellKnownDB.delete('apple')
        # mod_mess(pfx, WellKnownDB.list())

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


def main():

    Environ()

    mod_mess(__name__, f'Python script invoked: {sys.argv[0]}')
    mod_mess(__name__, f'Commandline arguments: {sys.argv[1:]}')

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

    parser.add_argument("action", type=str, choices=['listw', 'listl', 'repl', 'help'],
                        default = 'repl',
                        help='The action')

    args = parser.parse_args()
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

    populate_wellknown()

    list_welknown()


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

    dbfile = 'alpha-db.yaml'
    stor_obj = None # StorageDB(dbfile)
    repl_obj = Repl(player_obj, stor_obj, repeat=True, interval=3, verbose=True, dummy=False)
    repl_obj.repl_loop()
    exit_with_message(f'Command completed (qr)', 0)

    exit(0)


if __name__ == "__main__":
    main()
