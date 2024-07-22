import shutil
import time
import os
import platform
#import vlc
#from input_parse import *
from report import *
import utils

MEDIA_PLAYER_FFPLAY = 'ffplay'
WINDOWS_FFPLAY_PATH = r'E:\DOWNLOAD\Computing\SOFTWARE\FFMPEG\ffmpeg-2022-09-15-git-3f0fac9303-full_build\bin'
LINUX_FFPLAY_PATH = r'/usr/bin'

MEDIA_PLAYER_VLC = 'vlc'  # 'vlc' 'cvlc'
WINDOWS_VLC_PATH = r'C:\Program Files\VideoLAN\VLC'  # WINDOWS_VLC_PATH = r'C:\Program Files (x86)\VideoLAN\VLC'
#LINUX_VLC_PATH = r'/snap/bin'
LINUX_VLC_PATH = r'/usr/bin'


class AvPlayer:
    def __init__(self, media_player, verbose=True, dummy=True):
        self.plat = None
        self.player = media_player
        self.display_name = None
        self.media_player_path = None
        self.verbose = verbose
        self.dummy = dummy
        self.vlc = None
        self.ffplay = None
        self.chromium = None
        self.player_handle = None
        self.discover()
        self.populate()
        mod_mess(__name__, f'Instantaited AvPlayer')
        bill = 'pqr'
        mod_mess(__name__, f"INIT {bill}")

    def discover(self):
        self.vlc = shutil.which('vlc')
        self.cvlc = shutil.which('cvlc')
        self.ffplay = shutil.which('ffplay')
        self.chromium = shutil.which('chromium')
        if self.verbose:
            mod_mess(__name__, f'Discovered CHROMIUM : {self.chromium}')
            mod_mess(__name__, f'Discovered FFPLAY   : {self.ffplay}')
            mod_mess(__name__, f'Discovered VLC      : {self.vlc} \t{self.cvlc}')

    def populate(self):

        if self.player == 'vlc':
            self.display_name = 'VLC'
        elif self.player == 'plug':
            self.display_name = 'VLCPLUG'
        elif self.player == 'ffmpeg':
            self.display_name = 'FFMPEG'
        elif self.player == 'chromium':
            self.display_name = 'CHROMIUM'
        else:
            self.display_name = 'UNKNOWN_PLAYER'

        if self.verbose:
            mod_mess(__name__, f'Using media player {self.display_name}')

        self.plat = platform.system()
        medpath = None
        if self.player == 'ffmpeg':
            if self.plat == 'Linux':
                if True:
                    medpath = self.ffplay
                else:
                    medpath = os.path.join(LINUX_FFPLAY_PATH, MEDIA_PLAYER_FFPLAY)
            else:
                medpath = os.path.join(WINDOWS_FFPLAY_PATH, MEDIA_PLAYER_FFPLAY + '.exe')
                print(
                    f'medpath derived from: WINDOWS_FFPLAY_PATH="{WINDOWS_FFPLAY_PATH}" , '
                    f'MEDIA_PLAYER_FFPLAY="{MEDIA_PLAYER_FFPLAY}" , .exe')

        elif self.player == 'vlc':

            if self.plat == 'Linux':
                if True:
                    medpath = os.path.join(LINUX_VLC_PATH, MEDIA_PLAYER_VLC)
                else:
                    medpath = os.path.join(WINDOWS_VLC_PATH, MEDIA_PLAYER_VLC + '.exe')
            else:
                medpath = os.path.join(WINDOWS_VLC_PATH, MEDIA_PLAYER_VLC + '.exe')
                print(f'medpath derived from: WINDOWS_VLC_PATH="{WINDOWS_VLC_PATH}" , '
                      f'MEDIA_PLAYER_VLC="{MEDIA_PLAYER_VLC}" , .exe')
        elif self.player == 'plug':

            if self.plat == 'Linux':
                if True:
                    medpath = os.path.join(LINUX_VLC_PATH, MEDIA_PLAYER_VLC)
                else:
                    print(f'CANNOT PLAY ON WINDOWS')

            else:
                print(f'Windows not supported for plug')

        elif self.player == 'chromium':
            medpath = self.chromium
        self.media_player_path = medpath

    def get_tool_name(self):
        return self.display_name

    def get_media_player_path(self):
        return self.media_player_path

    def play_text(self, media_path, step_info, line_start=1, line_total=-1):
        if self.verbose: print(f'play_test: start={line_start}, count={line_total}, stepInfo={step_info}')

        if self.dummy:
            print(f'NOT PLAYING TEXT FILE {media_path}')
            return 0

        if self.verbose: print(f'PLAYING TEXT FILE {media_path}')
        utils.starting_media('TEXT')
        media_object = open(media_path, "r")
        line_num = 0
        line_count = 0
        for line in media_object:
            line_num += 1
            started = True if (line_num >= line_start) else False
            ended = True if (line_num >= (line_start + line_total)) else False
            # active = started
            # print(f'LINE:  {line_num} : started={started} , ended={ended}')
            if started and (not ended):
                line_count += 1
                # print(f'LINE:  {line_num}, lineCount={line_count} : started={started} , ended={ended}')
                line_prefix = "LINE:" + str(line_num) + "\t"
                print(line_prefix, end=" ", flush=True)
                word_count = 0
                words = line.split()
                for the_word in words:
                    word_count += 1
                    time.sleep(step_info)
                    # print(f'\tWORD: {word_count} : {the_word}')
                    print(the_word, end=" ", flush=True)
                print('')
        media_object.close()
        utils.stopping_media('TEXT')

    def _play_vlc_plugin(self, path_to_file):
        print(f'(vlc plugin) attempt to play')
        MyClass = 'vlc.MediaPlayer'
        methods_list = [method for method in dir(MyClass) if callable(
            getattr(MyClass, method)) and not method.startswith("__")]
        print(f'vvvv\n{methods_list}\n^^^\n')

        # creating vlc media player object
        media_player = vlc.MediaPlayer()

        # media object
        media = vlc.Media(path_to_file)

        # setting media to the media player
        media_player.set_media(media)

        run_period1 = 3
        pause_period1 = 2
        run_period2 = 3
        pause_period2 = 2

        media_player.play() # start playing video

        time.sleep(run_period1)
        media_player.pause()

        time.sleep(pause_period1)
        media_player.play()

        time.sleep(run_period2)
        media_player.pause()

        time.sleep(pause_period2)
        media_player.play()

        time.sleep(5)
        media_player.set_media(media)
        media_player.play()

    def play_media(self, mpeg_streamed, pname, start_time=0, duration=-1, volume=50):
        av_player = self.get_tool_name()
        av_path = self.get_media_player_path()
        if self.verbose:
            print(f'\nplay_mpeg: \n\tMediaPlayer={av_player}\n\tPath={av_path} \n', flush=True)
            print(f'\tfile={pname} \n\tstreamed={mpeg_streamed}\n\tstart={start_time}, \n\tduration={duration}, \n\tvol={volume}', flush=True)

        if self.dummy:
            print(f'Dummy Mode is True - so not playing')
            return

        # print(f'Using Media player == {MPEG_Player_Path}', flush=True)
        complex_args = True
        stop_time = start_time + duration
        mpegcmd = " "

        if av_player == 'FFMPEG':
            ffmpeg_reqd = " -autoexit "
            file_arg = "-i " + pname + " "

            if mpeg_streamed or start_time == -1:
                start_arg = ''
            else:
                start_hms = utils.convert_sec_to_HHMMSS(start_time)
                start_arg = "-ss " + f'{start_hms} '

            if mpeg_streamed or duration == -1:
                duration_arg = ''
            else:
                duration_arg = "-t " + utils.convert_sec_to_HHMMSS(duration)

            if complex_args:
                mpegcmd += f' {ffmpeg_reqd} {duration_arg} {start_arg} {file_arg} '
            else:
                mpegcmd += file_arg

        elif av_player == 'VLC':
            file_arg = pname + " "
            if mpeg_streamed:
                start_arg = ' '
            else:
                start_arg = "--start-time " + f'{start_time} '

            if mpeg_streamed or duration == -1:
                stop_arg = ''
            else:
                stop_arg = "--stop-time " + f'{stop_time} '

            close_on_finish_arg = " vlc://quit "
            if complex_args:
                mpegcmd = start_arg + stop_arg +  file_arg + close_on_finish_arg
            else:
                mpegcmd = file_arg

        elif av_player == 'VLCPLUG':
            self._play_vlc_plugin(pname)
            return



        else: # is chromium
            file_arg = pname + " "
            if mpeg_streamed:
                start_arg = ' '
            else:
                start_arg = "--start-time " + f'{start_time} '


            if mpeg_streamed or duration == -1:
                stop_arg = ''
            else:
                stop_arg = "--stop-time " + f'{stop_time} '
            print(f'Ignoring start and stop time')
            start_arg = ' '
            stop_arg = ''

            open_in_new_instance = " --new-window "
            close_on_finish_arg = " "
            if complex_args:
                mpegcmd = start_arg + stop_arg + open_in_new_instance + file_arg + close_on_finish_arg
            else:
                mpegcmd = file_arg

        cmd_args = mpegcmd
        #mpeg_player_protected = create_protected_path(av_path)
        mpeg_player_protected = utils.create_protected_path(av_path)
        mpegfullcmd = f'{mpeg_player_protected} {cmd_args}'
        if self.verbose: print(f'\nCMD ARGS: {cmd_args}\n', flush=True)


        if self.verbose:
            print(f'FULL CMD: {mpegfullcmd}', flush=True)

        if self.dummy:
            print(f'Dummy mode - NOT INVOKING')
        else:
            utils.starting_media('MPEG')
            os.system(mpegfullcmd)
            utils.stopping_media('MPEG')


