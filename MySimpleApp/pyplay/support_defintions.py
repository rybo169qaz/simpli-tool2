
class TestYouTubeDownloadObj():
    """
    This holds the data required for a youtube video
    """
    def __init__(self, src, friend, chan, dur, title, cdvideo_url=None):
        self.src = src
        self.friend = friend
        self.chan = chan
        self.dur = dur
        self.title = title
        self.cdvideo_url = cdvideo_url
        self.prefix_url = 'https://www.youtube.com/watch?v=' # ''
        self.local_file_prefix = 'yt_'

