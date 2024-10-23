#import input_parse
from input_parse import InputParser
#from MySimpleApp.pyplay.input_parse import InputParser

from const_data import TEST_REMOTE_AUDIO_MEAST_ABSALOM, TEST_REMOTE_AUDIO_MEAST_AMOS
from report import *

TOOLNAME = 'play'


def help_info(clue='general'):

    def general_help():
        msg = '''
        Help on using the tool.
        The tool runs in a loop: reading command line; processing command and repeating in a loop (REPL).
            REPL == Read Execute Print/Process Loop 
        Use 'q' to quit the loop
        Use 'h' to display general help.
        '''

        return msg

    def syntax_help():
        msg = '''
        Syntax:
            <verb> <resource> [<optional args>]
        
        '''
        return msg

    def verb_help():
        msg = '\n\tVERBS'
        msg += InputParser.get_verb_help() + '\n'
        return msg

    def resource_help():
        msg = '\n\tRESOURCES'
        msg += InputParser.get_resource_help() + '\n'
        return msg

    def verb_resource_help():
        #msg = InputParser.get_table_of_res_verb_combinations(False)
        msg = InputParser.get_table_of_res_verb_combinations(True)
        return msg

    descrip = clue

    if descrip == 'verb':
        verb_info = verb_help()
        return verb_info

    if descrip == 'resource':
        res_info = resource_help()
        return res_info
        #mod_mess(__name__, f'{res_info}')

    if descrip == 'verbres':
        verbres_info = verb_resource_help()
        return verbres_info

    if descrip == 'syntax':
        syntax_info = syntax_help()
        return syntax_info

    if descrip == 'general':
        general_info = general_help()
        syntax_info = syntax_help()
        verbres_info = verb_resource_help()
        full_text =  general_info + syntax_info + verbres_info
        return full_text


    if False:
        print(f'=========================')

        PACK = '\t\t\t\t\t'
        print(f'Help for {descrip}')
        print(f'Syntax:\n\t./{TOOLNAME} ')
        print(f'\t\tselect \n\t\t\t--known <known_media> ')
        print(f'{PACK}where\t <known_media> = [')
        print(f'{PACK}testtext | testproverbs | testjosephus')
        print(f'{PACK}testaudio | testcountingaudio | remoteaudio1 | remoteaudio2')
        print(f'{PACK}testvideo | testsilentvideo | testmoosevideo')
        print(f'{PACK}]')
        print(f'\t\t\t -p [vlc | ffmpeg] \tThis specifies which media player will be used.')

    if False:
        print(f'\t\t-m <media file> \t\tPlay the given media file')
        print(f'\t\t-r <url to remote media source> \t\tPlay the given remote link')
        print('Remote\n')
        print('daily broadcasts on alternative hours followed by music     http://165.22.38.83:8000/liquidsoap \n')
        print('the gospel          http://165.22.38.83:8000/preaching \n')
        print('archive stream      http://165.22.38.83:8000/liquidcopy \n')
        print(f'\tAbsalom     MH                      {TEST_REMOTE_AUDIO_MEAST_ABSALOM} ')
        print('\tActs        A.Johnson               http://165.22.38.83/archives/ActsA.Johnson.mp3 ')
        print(f'\tAmos        Graham Jackman          {TEST_REMOTE_AUDIO_MEAST_AMOS} ')
        print('\n\tlisten again        http://165.22.38.83/archives')

def print_help_info(clue=None):
    the_text = help_info(clue)
    mod_mess(__name__, f'{the_text}')
