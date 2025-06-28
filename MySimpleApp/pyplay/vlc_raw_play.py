import os
import time
import vlc

class VlcRawPlay:
    '''
    Very basic VLC player to use for testing
    '''

    def __init__(self, file_location):
        self.file_location = file_location

    def get_loc(self):
        return self.file_location

    def play_it(self, delay_length=5):
        '''
        Plays local media. This is primarily for test purposes
        :return:
        True if found and played
        False if no local media
        '''
        if not os.path.isfile(self.file_location):
            print(f'File {self.file_location} does not exist')
            return False

        # creating vlc media player object
        media_player = vlc.MediaPlayer()

        # media object
        media = vlc.Media(self.file_location)

        # setting media to the media player
        media_player.set_media(media)

        # start playing video
        media_player.play()

        # wait so the video can be played for 5 seconds
        # irrespective for length of video
        time.sleep(delay_length) # 5
        return True
