from enum import Enum
import time
import vlc
from loguru import logger
from resp_state_qual import *


class Presenter:
    # https://www.olivieraubert.net/vlc/python-ctypes/doc/
    PREFIX = 'pyplay/Media/'

    def __init__(self):
        self.current_handle = None
        self.actual_uri = None
        self.state = ResourceState.UNKNOWN
        self.vlc_obj = vlc.Instance()
        self.player = self.vlc_obj.media_player_new()
        self.media = None
        self.handle_map = dict({})
        self.__populate_map__()

    def __add_handle__(self, handle, uri):
        this_func = 'Add handle'
        if uri.startswith('https'):
            assign_val = uri
        else:
            assign_val = Presenter.PREFIX + uri
        self.handle_map[handle] = assign_val
        logger.debug(f'{this_func}: handle={handle} ; uri={assign_val}')


    def __populate_map__(self):
        self.__add_handle__('moose', 'Nursing_moose_calf.mp4')
        self.__add_handle__('pot', 'pot-on-wheel.mp4')
        self.__add_handle__('spoken', 'spoken_1-20_seconds.m4a')
        self.__add_handle__('testvideo', 'test-video.mp4')
        self.__add_handle__('hymn', 'Hymn-372_Who-is-on.mp3')
        self.__add_handle__('resurrect', 'https://christadelphianvideo.org/studyvideo/the-truth-about-jesus-resurrection-fiction-or-fact-biblical-evidence-%f0%9f%94%a5/')

    def __map_handle_to_uri__(self, handle):
        this_func = 'map_handle_to_uri'
        resp = self.handle_map.get(handle)
        retval = None
        if resp is None:
            # no mapping found
            logger.debug(f'{this_func}: handle={self.current_handle} NOT found in dict')
            retval = handle
        else:
            # use the mapped value
            logger.debug(f'{this_func}: handle={self.current_handle} FOUND in dict=={resp}')
            retval = resp
        return retval

    def select_media(self, handle):
        this_func = 'Presenter Media-Select'
        self.current_handle = handle
        self.actual_uri = self.__map_handle_to_uri__(handle)

        logger.debug(f'{this_func}: handle={self.current_handle} ; actual_uri={self.actual_uri}')
        self.media = self.vlc_obj.media_new(self.actual_uri)
        self.player.set_media(self.media)
        return RespStateQual(RespSuccess.GOOD)

    def start_play(self):
        this_func = 'Presenter Media-Play'
        logger.debug(f'{this_func}: Begin: {self.current_handle}')
        vlc_resp = self.player.play()

        if vlc_resp == 0:
            self.state = ResourceState.ACTIVE
            resp = RespStateQual(resp=RespSuccess.GOOD, state=self.state)
            logger.debug(f'{this_func}: GOOD')
        else:
            self.state = ResourceState.INACTIVE
            resp = RespStateQual(resp=RespSuccess.FAILED, state=self.state)
            logger.debug(f'{this_func}: BAD')
        return resp

    def stop_play(self):
        this_func = 'Presenter Media-Stop'
        logger.debug(f'{this_func}: Begin: {self.current_handle}')
        self.player.stop()
        self.state = ResourceState.INACTIVE
        return RespStateQual(RespSuccess.GOOD, state=self.state)

    def get_duration(self):
        this_func = 'Presenter Media-Duration'
        logger.debug(f'{this_func}: Begin: ')
        duration = self.player.get_length()
        volume = self.player.audio_get_volume()
        print(f'Duration=={duration}')
        print(f'Volume=={volume}')
        return RespStateQual(RespSuccess.GOOD)

    def pause(self):
        this_func = 'Presenter Media-Pause'
        logger.debug(f'{this_func}: Begin: ')
        self.player.pause()
        return RespStateQual(RespSuccess.GOOD, state=self.state)

    def close(self):
        this_func = 'Presenter Media-Close'
        logger.debug(f'{this_func}: Begin: ')
        self.player.release()
        return RespStateQual(RespSuccess.GOOD, state=self.state)

    def is_playing(self):
        this_func = 'Presenter Media-IsPlaying'
        logger.debug(f'{this_func}: ')
        vlc_resp = self.player.is_playing()
        if vlc_resp == 1:
            self.state = ResourceState.ACTIVE_PLAYING
            resp = RespStateQual(RespSuccess.GOOD, state=self.state)
        elif vlc_resp == 0:
            self.state = ResourceState.ACTIVE_NOT_PLAYING
            resp = RespStateQual(RespSuccess.GOOD, state=self.state)
        else:
            resp = RespStateQual(resp=RespSuccess.FAILED, qual=RespQualifierCategory.OTHER, qual_val=str(vlc_resp))
        return resp