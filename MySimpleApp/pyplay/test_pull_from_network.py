#import pytest
import tempfile
import os.path
from .pull_from_network import PullFromNetwork
from .vlc_raw_play import VlcRawPlay
import pytest
#from create_desktop_icons import IconCreationStatus
from.support_defintions import TestYouTubeDownloadObj


#NONEXISTANT_YOUTUBE_VIDEO_URL = 'qwerty'
#EXISTANT_YOUTUBE_VIDEO_URL = '2PuFyjAs7JA' # https://www.youtube.com/watch?v=2PuFyjAs7JA
#EXISTANT_YOUTUBE_VIDEO_TITLE = '4K 2K 1080p 720p 480p video resolution test'
#EXISTANT_YOUTUBE_VIDEO_CHANNEL = 'JC'

MEDIA_FILE_EXTENSION = '.mp4'

TEST_YOUTUBE_VIDEO11 = TestYouTubeDownloadObj('2PuFyjAs7JA', 'Test Video 11sec', 'JC', 11,
                                              title='4K 2K 1080p 720p 480p video resolution test')

# This non-existant ref is based on the TEST_YOUTUBE_VIDEO11 but with a tweak o fthe last character
TEST_NON_EXISTANT = TestYouTubeDownloadObj('2PuFyjAs7JB', 'Non-existant', None, None, title='unspec')

TEST_CDVID_RISING = TestYouTubeDownloadObj('5T4rDrOI9DA', 'Rising Lion', 'The Bible Standard - Discover the Truth!', 1073,
                                           title='Breaking News! Operation “Rising Lion” Heralds the Rising of the Sun of Righteousness')

TEST_CDVID_TFTD_JUNE1 = TestYouTubeDownloadObj('Eo98jv6GSpI', 'TFTD-June1', 'The Bible Standard - Discover the Truth!', 233,
                                               title='Thought for June 1st " How long will you put off"  Joshua 18:3',
                                               cdvideo_url='https://christadelphianvideo.org/tftd/daily-readings-thought-for-june-1st-how-long-will-you-put-off/') #  How long will you put off



def create_test_folder():
    # create a temporary directory
    tmpdir = tempfile.TemporaryDirectory(dir="/tmp", prefix="simpli_").name
    os.mkdir(tmpdir, 0o777)  # we create the dest dir
    # print(f'XYZ Tempdir = {tmpdir}')
    if os.path.isdir(tmpdir) is False:
        raise ValueError('Failed to create temp directory')
    return tmpdir

@pytest.mark.pullnetwork
class TestPullFromNetwork:

    def test_provided_args_retained_existent(self):
        tyt = TEST_YOUTUBE_VIDEO11
        tmpdir = create_test_folder()
        pfn1 = PullFromNetwork(tyt.prefix_url  + tyt.src, tmpdir)
        assert pfn1.source_url() == tyt.prefix_url  + tyt.src
        assert pfn1.destination_dir() == tmpdir

    def test_provided_args_retained_nonexistent(self):
        tyt = TEST_NON_EXISTANT
        tmpdir = create_test_folder()
        pfn1 = PullFromNetwork(tyt.prefix_url  + tyt.src, tmpdir)
        assert pfn1.source_url() == tyt.prefix_url  + tyt.src
        assert pfn1.destination_dir() == tmpdir

    def test_remote_exists_existent(self):
        tyt = TEST_YOUTUBE_VIDEO11
        pfn1 = PullFromNetwork(tyt.prefix_url  + tyt.src, create_test_folder())
        assert pfn1.media_exists_remote() == True

    def test_remote_exists_nonexistent(self):
        tyt = TEST_NON_EXISTANT
        pfn1 = PullFromNetwork(tyt.prefix_url  + tyt.src, create_test_folder())
        assert pfn1.media_exists_remote() == False

    def test_get_youtube_meta_valid(self):
        tyt = TEST_YOUTUBE_VIDEO11
        pfn1 = PullFromNetwork(tyt.prefix_url  + tyt.src, create_test_folder())
        assert pfn1.get_youtube_meta('id') == tyt.src
        assert pfn1.get_youtube_meta('channel') == tyt.chan
        assert pfn1.get_youtube_meta('duration') == tyt.dur
        assert pfn1.get_youtube_meta('title') == tyt.title

        tyt2 = TEST_CDVID_RISING
        pfn2 = PullFromNetwork(tyt2.prefix_url + tyt2.src, create_test_folder())
        assert pfn2.get_youtube_meta('id') == tyt2.src
        assert pfn2.get_youtube_meta('channel') == tyt2.chan
        assert pfn2.get_youtube_meta('duration') == tyt2.dur
        assert pfn2.get_youtube_meta('title') == tyt2.title

        tyt3 = TEST_CDVID_TFTD_JUNE1
        pfn3 = PullFromNetwork(tyt3.prefix_url + tyt3.src, create_test_folder())
        assert pfn3.get_youtube_meta('id') == tyt3.src
        assert pfn3.get_youtube_meta('channel') == tyt3.chan
        assert pfn3.get_youtube_meta('duration') == tyt3.dur
        assert pfn3.get_youtube_meta('title') == tyt3.title

    def test_get_youtube_meta_invalid(self):
        tyt = TEST_NON_EXISTANT
        pfn1 = PullFromNetwork(tyt.prefix_url  + tyt.src, create_test_folder())
        assert pfn1.get_youtube_meta('id') is None

    def test_get_media_valid(self):
        tyt = TEST_YOUTUBE_VIDEO11      #tyt = TEST_CDVID_TFTD_JUNE1
        tmpdir = create_test_folder()
        pfn1 = PullFromNetwork(tyt.prefix_url  + tyt.src, tmpdir)
        assert len(os.listdir(tmpdir)) == 0 # check that dest dir is empty

        assert pfn1.get_media() == True
        assert pfn1.get_filename() == tyt.local_file_prefix + tyt.src + MEDIA_FILE_EXTENSION
        assert pfn1.media_is_local() == True
        assert pfn1.get_file_path() == tmpdir + '/' + pfn1.get_filename() # ensures that generated file is within the specified destdir
        assert os.path.isfile(pfn1.get_file_path()) == True # check that the file exists
        assert len(os.listdir(tmpdir)) == 1  # check that dest dir has only one file
        #VlcRawPlay(pfn1.get_file_path()).play_it(4)

    def test_get_media_invalid(self):
        tyt = TEST_NON_EXISTANT
        tmpdir = create_test_folder()
        pfn1 = PullFromNetwork(tyt.prefix_url  + tyt.src, tmpdir)
        assert len(os.listdir(tmpdir)) == 0  # initial condition check

        assert pfn1.get_media() is False
        assert pfn1.media_is_local() == False
        assert pfn1.get_file_path() is None
        assert len(os.listdir(tmpdir)) == 0  # check that dest dir is empty


    def test_remove_local_when_invalid(self):
        tyt = TEST_NON_EXISTANT
        temp_dir = create_test_folder()
        pfn1 = PullFromNetwork(tyt.prefix_url + tyt.src, temp_dir)
        pfn1.get_media()
        assert pfn1.media_is_local() == False # precondition
        assert len(os.listdir(temp_dir)) == 0

        pfn1.remove_local_copy()
        assert pfn1.media_is_local() == False
        assert pfn1.get_file_path() is None
        assert len(os.listdir(temp_dir)) == 0  # check that dest dir is empty

    def test_remove_local_when_valid_and_exists_locally(self):
        tyt = TEST_YOUTUBE_VIDEO11
        temp2_dir = create_test_folder()
        pfn2 = PullFromNetwork(tyt.prefix_url + tyt.src, temp2_dir)
        pfn2.get_media()
        assert pfn2.media_is_local() == True    # precondition
        assert len(os.listdir(temp2_dir)) == 1  # precondition

        pfn2.remove_local_copy()
        assert pfn2.media_is_local() == False
        assert pfn2.get_file_path() is None
        assert len(os.listdir(temp2_dir)) == 0

    def test_remove_local_when_valid_but_not_local(self):
        tyt = TEST_YOUTUBE_VIDEO11
        temp4_dir = create_test_folder()
        pfn4 = PullFromNetwork(tyt.prefix_url + tyt.src, temp4_dir)
        pfn4.get_youtube_meta('title')
        assert pfn4.media_is_local() == False  # precondition
        assert len(os.listdir(temp4_dir)) == 0  # precondition

        pfn4.remove_local_copy()
        assert pfn4.media_is_local() == False
        assert len(os.listdir(temp4_dir)) == 0


def main():
    print('DONE')

if __name__ == "__main__":
    main()