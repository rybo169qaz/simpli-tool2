import pytest
import utils
import const_data
from my_enums import *
from report import mod_mess
import my_enums
#from MySimpleApp.pyplay.my_enums import MediaType

from environ import Environ


class MediaIdentity:
    def __init__(self, uri, verbose=False, dummy=False):
        self.uri = uri
        self.media_type = None
        self.media_location = None
        self.media_form = None
        self.media_format = None
        self.media_identity = None
        self.verbose = verbose
        self.dummy = dummy
        self.valid = False
        self._populate()

    def _populate(self):
        uri = self.uri
        (is_found, media_tuple) = self._match_well_known_url()

        if self.verbose:
            mod_mess(__name__, f'URI=={uri} : Found={is_found} , MEDIA_IS == {media_tuple[3]}')

        if is_found:
            (mtype, mlocation, mform, media_identity) = media_tuple
        else:
            (mtype, mformat) = utils.detect_media(uri)

            if utils.is_absolute_path(uri):
                mlocation = SourceLoc.LOCAL
                mform = MediaForm.FILE
                if self.verbose:
                    print(f'URI was deemed ABSOLUTE')

            elif utils.is_remote_path(uri):
                mlocation = SourceLoc.NETWORK
                mform = MediaForm.STREAMED
                if self.verbose:
                    print(f'URI was deemed REMOTE')

            else:
                mlocation = SourceLoc.TESTLOCAL
                mform = MediaForm.FILE

            media_identity = uri

        self.media_type = mtype
        self.media_location = mlocation
        self.media_form = mform
        self.media_identity = media_identity
        self.media_format = mformat

    def get_media_type(self):
        return self.media_type

    def get_media_location(self):
        return self.media_location

    def get_media_form(self):
        return self.media_form

    def get_media_format(self):
        return self.media_format

    def med_identity(self):
        return self.media_identity

    def _match_well_known_url(self):
        media_type = None
        media_location = None
        media_streamed = None
        media_identity = None

        uri = self.uri
        resp = True

        found = False
        if self.verbose:
            print(f'Looking for match of {uri}\n')

        for entry in const_data.well_known_uris:
            (wellknown, mid) = entry
            #(wellknown, mtype, mloc, mstream, mid) = entry
            if uri == wellknown:
                media_type = mtype
                media_location = mloc
                media_streamed = mstream
                if media_location == 'remote':
                    if self.verbose:
                        print("Remote\n")
                    media_identity = mid
                else:
                    if self.verbose:
                        print("Local\n")
                    #media_identity = input_parse.get_full_uri(mid)
                    media_identity = utils.get_full_uri_to_media(mid)

                found = True
                if self.verbose:
                    print(f' Matched {uri} in loop')
                break

        if found is False:
            resp = False
            if self.verbose:
                print(f'not found in if-then strcut')

        if self.verbose:
            print(f'match_well_known: MATCH={resp}, MEDIA_IDENTITY={media_identity}')
        media_details = (media_type, media_location, media_streamed, media_identity)
        return (resp, media_details)



from utils import func_name
class TestMediaIdentity:

    def test_get_media_type(self):
        print('Testing {}.{}'.format(__name__, func_name()))
        assert MediaType.TEXT == MediaIdentity('abc.txt').get_media_type()
        assert MediaType.AUDIO == MediaIdentity('abc.mp3').get_media_type()
        assert MediaType.VIDEO == MediaIdentity('/tmp/Fish123.mp4').get_media_type()
        assert MediaType.AUDIO == MediaIdentity('cat/dog.mp3').get_media_type()
        assert MediaType.VIDEO == MediaIdentity('abc.mp4').get_media_type()
        assert MediaType.IMAGE == MediaIdentity('mypicture.jpg').get_media_type()

    def test_get_media_location(self):
        print('Testing {}.{}'.format(__name__, func_name()))
        assert SourceLoc.TESTLOCAL == MediaIdentity('abc.txt').get_media_location() # relative path is deemed to be test area
        assert SourceLoc.LOCAL == MediaIdentity('/p/q/r.txt').get_media_location()
        assert SourceLoc.NETWORK == MediaIdentity('http://widget.co.uk/a/b/c').get_media_location()
        assert SourceLoc.NETWORK == MediaIdentity('https://widget.co.uk/x/y/z.mp4').get_media_location()
        assert SourceLoc.NETWORK == MediaIdentity('http://widget.co.uk/a/b/c').get_media_location()

    def test_get_media_form(self):
        print('Testing {}.{}'.format(__name__, func_name()))
        assert MediaForm.FILE == MediaIdentity('/p/q/r.mp3').get_media_form()
        assert MediaForm.FILE == MediaIdentity('/abc.mp4').get_media_form()
        assert MediaForm.STREAMED == MediaIdentity('https://mycompany.co.uk/a/b/c/d/e/f/g/h.mp3').get_media_form()

    def test_get_media_format(self):
        print('Testing {}.{}'.format(__name__, func_name()))
        assert MediaFormat.TXT == MediaIdentity('/p/q/r.txt').get_media_format()
        assert MediaFormat.JPG == MediaIdentity('/p/q/r.jpg').get_media_format()
        assert MediaFormat.MP4 == MediaIdentity('/p/q/r.mp4').get_media_format()
        assert MediaFormat.M4A == MediaIdentity('/p/q/r.m4a').get_media_format()

