import os
from report import *
import platform
import utils

class Environ:
    myc = 'Environ'
    #print(f'Environ - initial -start')
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
    environ_dict = {}

    #print(f'Environ - initial -end')

    def __new__(cls):
        cls.setglobal()
        #cls.show_environment_key_values()

    @classmethod
    def setglobal(cls):
        print(f'({cls.myc} : setglobal): STARTING')

        versInfo = str(sys.version_info.major) + '.' + str(sys.version_info.minor)
        cls.environ_dict['pythonVersion'] = versInfo
        cls.environ_dict['pythonInterpreter'] = sys.executable


        #def set_global_variable():
        cls.environ_cwd = os.getcwd()
        cls.environ_dict['currentWorkingDirectory'] = os.getcwd()
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

        cls.environ_dict['runContextBundlePyInstaller'] = Run_Context_Bundle
        cls.environ_dict['pathToFiles'] = cls.environ_path_2_files
        cls.environ_dict['pathToLocalMedia'] = cls.environ_path_to_local_media

        mod_mess(__name__, f'Path_2_files=={cls.environ_path_2_files}')
        mod_mess(__name__, f'Using Path_To_Local_Media == {cls.environ_path_to_local_media}')

        cls.environ_platform_name = platform.system()
        cls.environ_dict['platformName'] = cls.environ_platform_name
        mod_mess(__name__, f'Using Platform_Name == {cls.environ_platform_name}')


        if cls.environ_platform_name == 'Linux':
            cls.environ_media_player_ffplay = os.path.join(cls.LINUX_FFPLAY_PATH, cls.MEDIA_PLAYER_FFPLAY)
            environ_media_player_vlc = os.path.join(cls.LINUX_VLC_PATH, cls.MEDIA_PLAYER_VLC)
        else:
            executable = cls.MEDIA_PLAYER_FFPLAY + '.exe'
            cls.environ_media_player_ffplay = os.path.join(cls.WINDOWS_FFPLAY_PATH, executable)
            environ_media_player_vlc = os.path.join(cls.WINDOWS_VLC_PATH, cls.MEDIA_PLAYER_VLC)

        cls.environ_dict['media_player_ffplay'] = cls.environ_media_player_ffplay



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


    @classmethod
    def show_environment_key_values(cls):
        utils.print_dict(cls.environ_dict, 'Environment values')


