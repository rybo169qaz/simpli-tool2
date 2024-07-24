



class InputParser:
    #initial_verbs = ['listw', 'listl', 'repl', 'help']

    repl_verb_list = ['q', 'h', 'select', 'list', 'add', 'delete']
    repl_resource_list = ['media', 'wdb', 'lfs']

    def __new__(cls):
        pass
        #cls.setglobal()


    @classmethod
    def get_repl_resources(cls):
        return cls.repl_resource_list

    @classmethod
    def get_repl_verbs(cls):
        return cls.repl_verb_list





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


