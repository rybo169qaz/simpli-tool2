import copy
import json
import os
from yt_dlp import YoutubeDL

# these for the testing
import tempfile


if __name__ == "__main__":
    from vlc_raw_play import VlcRawPlay
    from support_defintions import TestYouTubeDownloadObj
else:
    from .vlc_raw_play import VlcRawPlay
    from .support_defintions import TestYouTubeDownloadObj


'''

Examples
    https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#output-template-examples
    
Convert command line to API
   https://github.com/yt-dlp/yt-dlp/blob/master/devscripts/cli_to_api.py
   
CODE 
    https://github.com/yt-dlp/yt-dlp/blob/c54ddfba0f7d68034339426223d75373c5fc86df/yt_dlp/YoutubeDL.py#L457

STACKOVERFLOW Using yt-dlp in a Python script, how do I download a specific section of a video?
    https://stackoverflow.com/questions/73516823/using-yt-dlp-in-a-python-script-how-do-i-download-a-specific-section-of-a-video
    
#
# examples
#   https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#output-template-examples
'''
YOUTUBE_PREFIX = 'https://www.youtube.com/watch?v='
DEBUG_ACTIVE = False

def print_headed_dictionary(the_dict, the_title):
    if the_dict is None:
        print(f'Dictionary {the_title} is None')
    else:
        # pretty_dict = json.dumps(the_dict.__dict__, indent=4)
        pretty_dict = json.dumps(the_dict, indent=4)
        print(f'\nSTART Printing {the_title}')
        print(f'{pretty_dict}')
        print(f'END Printing {the_title} metadata')


class PullFromNetwork:
    '''
    Obtains media from the network.
    Currently ONLY YouTube is supported.
    The directory is populated with 2 items:
        the media file
        a metadata file containing: URL, Title, Channel
    '''

    def __init__(self, src_url, dest_dir):
        #def __init__(self, yt_obj: YouTubeDownloadObj) :
            # self.ytube_obj = copy.deepcopy(yt_obj)
            # self.src_url = yt_obj.src_url #src_url
            # self.dest_dir = yt_obj.dest_dir #dest_dir

        self.src_url = src_url
        self.dest_dir = dest_dir

        self.failure = None

        self.started_analyse_meta = False
        self.full_youtube_metadata = None
        self.refined_meta = None  # Dictionary of wanted attributes

        self.started_analyse_for_download = False
        self.downloaded = False
        self.media_filename = None #populated when downloaded is True

        self.path_prefix = "."
        self.file_prefix = "yt_"
        self.FILE_FORMAT_STRING = f'{self.file_prefix}%(id)s.%(ext)s'
        self.FILE_EXTENSION = 'mp4'

    def source_url(self):
        return self.src_url

    def destination_dir(self):
        return self.dest_dir

    def get_required(self, download_media) -> bool:
        '''
        gets metadata and (depending upon download_media flag) the media file
        :param download_media:
        :return:
            True if it extracts data without a problem
            False if there is an error
        '''

        self.started_analyse_meta = True
        if download_media:
            self.started_analyse_for_download = True

        opfile = f'{self.dest_dir}/{self.FILE_FORMAT_STRING}'
        ydl_opts = {
            'format': self.FILE_EXTENSION,
            # 'outtmpl': "./yt_%(id)s.%(ext)s",
            'outtmpl': opfile,
        }
        respy = False

        try:
            meta = YoutubeDL(ydl_opts).extract_info(self.src_url, download=download_media)
            self.full_youtube_metadata = copy.deepcopy(meta)

            keys_to_extract = ['id', 'title', 'duration', 'channel', 'filesize_approx',
                               'fulltitle', 'description', 'duration', 'ext']
            # The following are currently unwanted : url  duration_string

            self.refined_meta = dict({})
            for key, value in self.full_youtube_metadata.items():
                if DEBUG_ACTIVE:
                    print(f'Checking key=={key}')
                if key in keys_to_extract:
                    #print(f'\tDesire to extract key=={key} and write in value >>{value}<<')
                    self.refined_meta[key] = value
                    # setattr(self.refined_meta, key, value) # is used for setting attributs in objects
                    if DEBUG_ACTIVE:
                        print(f'\tExtracted key=={key}')

            if download_media:
                id_part = self.refined_meta['id']  # .id
                ext_part = self.refined_meta['ext']  # .ext
                self.media_filename = f'{self.file_prefix}{id_part}.{ext_part}'
                self.downloaded = True
            respy = True

        except Exception as exc:  # DownloadError
            self.failure = exc
            print(f"Exception Name: {type(exc).__name__}")
            print(f"Exception Desc: {exc}")

        return respy

    def print_full_metadata(self):
        print_headed_dictionary(self.full_youtube_metadata, 'Full Metadata')

    def print_refined_metadata(self):
        print_headed_dictionary(self.refined_meta, 'Refined Metadata')

    def get_metadata(self) -> dict:
        if self.refined_meta is None:
            if self.get_required(False):
                resp = self.refined_meta
            else:
                resp = None
        else:
            resp = self.refined_meta
        return resp

    def get_media(self) -> bool:
        '''
        Provides the path to the media file if it exists
        :return:
        <path-to-file> :
        None : If the url is not valid
        '''
        if self.started_analyse_for_download is False:
            self.get_required(True)
        return False if self.get_file_path() is None else True


    def get_filename(self):
        '''
        the filename within the directory
        :return:
            If the file is downloaded returns filename with in dir
            None if it is not downloaded
        '''
        #return (self.media_filename + self.FILE_EXTENSION) if self.downloaded else None
        return self.media_filename if self.downloaded else None

    def get_file_path(self):
        '''
        Provides details on the location of the media file
        :return:
        Returns the local filepath if the file has been downloaded ELSE returns None
        '''
        #resp = self.media_path if self.downloaded else None
        resp = f'{self.dest_dir}/{self.media_filename}' if self.downloaded else None

        return resp

    def get_youtube_meta(self, field_name):
        if self.started_analyse_meta is False:
            self.get_required(False)

        if self.refined_meta is None:
            resp = None
            #raise Exception('the refined_meat shoudl be configured')
        else:
            if field_name in self.refined_meta:
                resp = self.refined_meta[field_name]
            else:
                resp = None
        return resp

    def media_exists_remote(self):
        '''
        Enables determination of whether the specified media is available on the internet.
        :return:
        True if it does exist
        False if it does not exist
        '''
        if self.started_analyse_meta is False:
            self.get_required(False)
        return False if self.refined_meta is None else True

    # def pull_media(self):
    #     '''
    #     Download the specified media
    #     :return:
    #     True if the file has been downloaded
    #     False if it is currently not downloaded (also if non-existant on internet)
    #     '''
    #     mycwd = os.getcwd()
    #     print(f'CWD=={mycwd}')
    #     full_url = self.src_url # YOUTUBE_PREFIX + self.src_url
    #     print(f'Attempting to download: Youtube={self.src_url} ; Full URL== {full_url}')
    #
    #     paths_arg = {'paths': 'home'}
    #     output_arg = "%(title)s.%(ext)s"
    #
    #     yt_opts = dict({})
    #     yt_opts['output'] = output_arg
    #     yt_opts['restrict-filenames'] = True
    #
    #     ydl = YoutubeDL(yt_opts)
    #     url_list = [full_url]
    #     try:
    #         yresp = ydl.download(url_list)
    #         self.downloaded = True
    #         print(f'Finished download of {url_list}')
    #         resp = True
    #     except Exception as exc:  # DownloadError
    #
    #         print(f"Exception Name2: {type(exc).__name__}")
    #         print(f"Exception Desc2: {exc}")
    #         resp = False
    #
    #     return resp # (isvalid, is_writing, is_written)

    def media_is_local(self):
        '''
        Indicates if copy of media is local
        :return:
        True is media is already local
        false if media is not local
        '''
        if self.downloaded:
            return True
        else:
            return False

    def remove_local_copy(self):
        the_file = self.get_file_path()
        if the_file is not None:
            if os.path.exists(the_file):
                os.remove(the_file)
                if os.path.exists(the_file):
                    raise FileNotFoundError # Probably being paranoid
                self.downloaded = False
            else:
                raise FileNotFoundError # we should never find this to be the case


def test_dictprint(description: str, url: str, file_handle: str ='xxx'):
    d = {"name": "shakshi", "age": 21}
    #print(json.dumps(d, indent=4))
    #print(json.dumps(d.__dict__, indent=4))
    #

    pfx = 'simpli_' + file_handle + '_'
    tempdir = tempfile.TemporaryDirectory(dir="/tmp", prefix=pfx).name
    print(f'\n\nTEST DICR: {description} (using YouTube URL={url} , destdir={tempdir})')
    os.mkdir(tempdir, 0o777)  # we create the dest dir
    pfn1 = PullFromNetwork(url, tempdir)
    print_headed_dictionary(d, 'testdict')
    x = pfn1.get_metadata()

def analyse(description: str, url: str, file_handle: str ='xxx'):
    pfx = 'simpli_' + file_handle + '_'
    tempdir = tempfile.TemporaryDirectory(dir="/tmp", prefix=pfx).name
    print(f'\n\nITEM: {description} (using YouTube URL={url} , destdir={tempdir})')
    os.mkdir(tempdir, 0o777)  # we create the dest dir
    pfn1 = PullFromNetwork(url, tempdir)
    pfn1.get_required(True)
    #pfn1.print_full_metadata()
    #pfn1.print_refined_metadata()

    is_remote = pfn1.media_exists_remote()
    print(f'\n\nMedia exists remote = {is_remote}')
    if is_remote:
        #pfn1.print_full_metadata()
        pfn1.print_refined_metadata()

        file_location = pfn1.get_file_path()
        print(f'File expected at {file_location}')

        play_obj = VlcRawPlay(pfn1.get_file_path())
        play_obj.play_it()

    print(f'\nEND\n\n')

def basic_test():
    TEST_YT_VID11 = TestYouTubeDownloadObj('2PuFyjAs7JA', 'Test Video 11sec', 'JC', 11,
                                                  title='4K 2K 1080p 720p 480p video resolution test')


    #test_dictprint(TEST_YT_VID11.friend, TEST_YT_VID11.src)
    analyse(TEST_YT_VID11.friend, TEST_YT_VID11.src)

    #analyse('short 11 second yt video', '2PuFyjAs7JA') # ref_url1 = 'https://www.youtube.com/watch?v=2PuFyjAs7JA'
    #analyse('CDvideo TFTD June 1st', 'https://youtu.be/nK3jQv9iZ_g')
    #analyse('Non-existant', 'https://youtu.be/bc987qwe')
    #analyse('Operation Rising lion', 'https://www.youtube.com/watch?v=5T4rDrOI9DA')

if __name__ == "__main__":
    basic_test()