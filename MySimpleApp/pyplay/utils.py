import os
from my_enums import MediaType, MediaFormat
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
    elif pname.startswith('http:'):
        resp = True
    else:
        resp = False
    return resp


def detect_media(pname):
    ext = os.path.splitext(pname)[-1].lower()
    if ext == '.mp3':
        media_type = MediaType.AUDIO
        media_format = MediaFormat.MP3
    elif ext == '.mp4':
        media_type = MediaType.VIDEO
        media_format = MediaFormat.MP4
    elif ext == '.m4a':
        media_type = MediaType.AUDIO
        media_format = MediaFormat.M4A
    elif ext == '.jpg':
        media_type = MediaType.IMAGE
        media_format = MediaFormat.JPG
    elif ext == '.txt':
        media_type = MediaType.TEXT
        media_format = MediaFormat.TXT
    elif ext == '.iden':
        media_type = MediaType.IDENTITY
        media_format = MediaFormat.UNKNOWN
    else:
        media_type = MediaType.UNKNOWN
        media_format = MediaFormat.UNKNOWN
    return (media_type, media_format)

def media_type_from_format(format):
    if format in set(MediaFormat.TXT):
        mtype = MediaType.TEXT
    elif format in set(MediaFormat.JPG, MediaFormat.PNG):
        mtype = MediaType.IMAGE
    elif format in set(MediaFormat.M4A, MediaFormat.MP3):
        mtype = MediaType.AUDIO
    elif format in set(MediaFormat.MP4):
        mtype = MediaType.VIDEO
    else:
        mtype = MediaType.UNKNOWN


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

def print_list_tuples(list_name, header, first_tuple_name='Key', mapping='==>', second_tuple_name='Value'):
    print(f'\nList of: {header}')
    print(f'\t{first_tuple_name} {mapping} {second_tuple_name}')
    for key, value in list_name:
        print(f"\t{key} {mapping} {value}")
    print(f'===\n')

def print_dict(dict_name, header):
    sorted_dict = dict(sorted(dict_name.items()))
    print(f'\nDictionary of: {header}')
    for key, value in sorted_dict.items():
        print(f"\t{key} == {value}")
    print(f'===\n')

def create_prefixed_list(initial_text, final_text, prefix, postfix, array_entries):
    the_list = []
    the_list.append(str(initial_text))
    for i in array_entries:
        indent_entry = str(prefix) + str(i) + str(postfix)
        the_list.append(indent_entry)
    the_list.append(str(final_text))
    return the_list

def func_name():
    import traceback
    return traceback.extract_stack(None, 2)[0][2]

#def get_methods_in_class(class_name):
#    return [method for method in dir(class_name) if method.startswith('__') is False]
