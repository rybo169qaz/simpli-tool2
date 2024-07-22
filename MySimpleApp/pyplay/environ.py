import os
from report import *
import platform

class Environ:
    myc = 'Environ'
    print(f'Environ - initial -start')
    PYPLAY_DIR = 'pyplay'
    MEDIA_PATH = 'Media'

    MEDIA_PLAYER_FFPLAY = 'ffplay'
    WINDOWS_FFPLAY_PATH = r'E:\DOWNLOAD\Computing\SOFTWARE\FFMPEG\ffmpeg-2022-09-15-git-3f0fac9303-full_build\bin'
    LINUX_FFPLAY_PATH = r'/usr/bin'

    MEDIA_PLAYER_VLC = 'vlc'  # 'vlc' 'cvlc'
    WINDOWS_VLC_PATH = r'C:\Program Files\VideoLAN\VLC'  # WINDOWS_VLC_PATH = r'C:\Program Files (x86)\VideoLAN\VLC'
    LINUX_VLC_PATH = r'/snap/bin'

    MPEG_Player_Path = None

    environ_cwd = None
    environ_path_2_files = None
    environ_path_to_local_media = None
    environ_platform_name = None

    environ_media_player_ffplay = None
    environ_media_player_vlc = None

    print(f'Environ - initial -end')

    def __new__(cls):
        cls.setglobal()

    @classmethod
    def setglobal(cls):
        print(f'({cls.myc} : setglobal): STARTING')

        #def set_global_variable():
        cls.environ_cwd = os.getcwd()
        mod_mess(__name__, f'CWD: {cls.environ_cwd} ')


        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            Run_Context_Bundle = True
            cls.environ_path_2_files = getattr(sys, '_MEIPASS')
            mod_mess(__name__, f'running in a PyInstaller bundle ')
            cls.environ_path_to_local_media = os.path.join(cls.environ_path_2_files, cls.MEDIA_PATH)

        else:
            Run_Context_Bundle = False
            cls.environ_path_2_files = cls.environ_cwd
            mod_mess(__name__, 'running in a normal Python process')
            cls.environ_path_to_local_media = os.path.join(cls.environ_path_2_files, cls.PYPLAY_DIR, cls.MEDIA_PATH)

        mod_mess(__name__, f'Path_2_files=={cls.environ_path_2_files}')
        mod_mess(__name__, f'Using Path_To_Local_Media == {cls.environ_path_to_local_media}')

        cls.environ_platform_name = platform.system()
        mod_mess(__name__, f'Using Platform_Name == {cls.environ_platform_name}')

        if cls.environ_platform_name == 'Linux':
            cls.environ_media_player_ffplay = os.path.join(cls.LINUX_FFPLAY_PATH, cls.MEDIA_PLAYER_FFPLAY)
            environ_media_player_vlc = os.path.join(cls.LINUX_VLC_PATH, cls.MEDIA_PLAYER_VLC)
        else:
            executable = cls.MEDIA_PLAYER_FFPLAY + '.exe'
            cls.environ_media_player_ffplay = os.path.join(cls.WINDOWS_FFPLAY_PATH, executable)
            environ_media_player_vlc = os.path.join(cls.WINDOWS_VLC_PATH, cls.MEDIA_PLAYER_VLC)
        print(f'({cls.myc} : setglobal): ENDING')

    @classmethod
    def list(cls):
        msg = f'Well-known entries\n'
        for key, value in cls.dict.items():
            msg += f"{key} == {value}\n"
        return msg

    @classmethod
    def get_cwd(cls):
        return cls.environ_cwd

    @classmethod
    def get_path_to_local_media(cls):
        return cls.environ_path_to_local_media

    @classmethod
    def get_platform_name(cls):
        return cls.environ_platform_name


