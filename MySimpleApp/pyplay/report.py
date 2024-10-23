import sys
from inspect import currentframe

# Global Constants
MEDIA_TYPE_SET = {'TEXT', 'MPEG', 'IDENTITY'}
VERB_LIST = ['help', 'select', 'start', 'stop']
MEDIATYPE_LIST = ['media', 'id']



def lineno():
    cf = currentframe()
    return cf.f_back.f_lineno

def mod_mess(module, message):

    full_text = f"({module}): {message}"
    print(full_text)

def exit_with_message(msg, exception, loc='Unknown', linenum='?'):
    print('-' * 60)
    common_text = f'Exiting application:\n\tReason:{msg}\n\tLocation={loc} #{linenum}'
    if isinstance(exception, Exception):
        print(f'{common_text}\n\tException Text:{exception}')
        sys.exit("error 999")
    else:
        #print(f'Exiting application:\n\tReason:{msg}\n{loc}\n\tExiting with code {exception}')
        print(f'{common_text}\n\tExiting with code:{exception}')
        sys.exit(exception)


def file_is_readable(pname):
    try:
        media_object = open(pname, "r")
        media_object.close()
        resp = True
    except Exception as e:
        resp = False
    return resp

def test_file_is_readable_A():
    assert file_is_readable('repl.py') == True

def test_file_is_readable_B():
    assert file_is_readable('abc.txt') == False