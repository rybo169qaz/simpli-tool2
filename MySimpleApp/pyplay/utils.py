import os
from environ import Environ


def convert_sec_to_HHMMSS(seconds):
    (my_whole_mins, my_seconds_in_minute) = divmod(seconds, 60)
    (my_whole_hours, my_mins_in_hour) = divmod(my_whole_mins, 60)
    hms = f'{my_whole_hours:02}:{my_mins_in_hour:02}:{my_seconds_in_minute:02}'
    #print(f'SECONDS={seconds}  ==  {hms}')
    return hms


def is_absolute_path(pname):
    resp = os.path.isabs(pname)
    #print(f'ABS == {resp} \t Path == {pname}')
    return resp


def is_remote_path(pname):
    if pname.startswith('https:'):
        resp = True
    else:
        resp = False
    return resp


def detect_media(pname):
    ext = os.path.splitext(pname)[-1].lower()
    if ext == '.mp3':
        media_type = 'MPEG'
    elif ext == '.mp4':
        media_type = 'MPEG'
    elif ext == '.m4a':
        media_type = 'MPEG'
    elif ext == '.txt':
        media_type = 'TEXT'
    elif ext == '.iden':
        media_type = 'IDENTITY'
    else:
        media_type = 'UNKNOWN'
    return media_type


def get_full_uri_to_media(file):
    #global Path_To_Local_Media
    #assert Environ.get_path_to_local_media() == Path_To_Local_Media
    #assert Environ.get_path_to_local_media() == 'abc'
    if is_absolute_path(file):
        full = file
    else:
        full = os.path.join(Environ.get_path_to_local_media(), file)
    return full


def create_protected_path(pathname):
    #assert Environ.get_platform_name() == Platform_Name
    #assert Environ.get_platform_name() == 97
    if Environ.get_platform_name() == 'Windows':
        new_path = f'"{pathname}" '
    else:
        new_path = pathname
    return new_path


def media_delim(is_start, media_type):
    the_char = 'v' if is_start else '^'
    print( media_type + ' ' + the_char * 60)

def starting_media(media_type):
    media_delim(True, media_type)

def stopping_media(media_type):
    media_delim(False, media_type)


def print_dict(dict_name):
    print(f'PRINT DICT START\n')
    for key, value in dict_name.items():
        print(f"{key} == {value}")
    print(f'PRINT DICT END\n')