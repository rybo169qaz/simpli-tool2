import pytest
import const_data
import utils
from environ import Environ


class MediaIdentity:
    def __init__(self, uri, verbose=False, dummy=False):
        self.uri = uri
        self.media_type = None
        self.media_location = None
        self.media_streamed = None
        self.media_identity = None
        self.verbose = verbose
        self.dummy = dummy
        self.valid = False
        self._populate()

    def _populate(self):
        uri = self.uri
        (is_found, media_tuple) = self._match_well_known_url()

        if self.verbose:
            print(f'URI=={uri} : Found={is_found} , MEDIA_IS == {media_tuple[3]}')
        if is_found:
            (media_type, media_location, media_streamed, media_identity) = media_tuple

        else:
            media_type = utils.detect_media(uri)
            if utils.is_absolute_path(uri):
                media_location = 'usb'
                media_streamed = False
                if self.verbose:
                    print(f'URI was deemed ABSOLUTE')
            elif utils.is_remote_path(uri):
                media_location = 'remote'
                media_streamed = True
                if self.verbose:
                    print(f'URI was deemed REMOTE')
            else:
                media_location = 'test'
                media_streamed = False
            media_identity = uri

        self.media_type = media_type
        self.media_location = media_location
        self.media_streamed = media_streamed
        self.media_identity = media_identity

    def med_type(self):
        return self.media_type

    def med_location(self):
        return self.media_location

    def med_streamed(self):
        return self.media_streamed

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
            (wellknown, mtype, mloc, mstream, mid) = entry
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


def test_media_streamed_A():
    mi = MediaIdentity('testsilentvideo')
    assert mi.med_streamed() == True

def test_media_streamed_B():
    mi = MediaIdentity('testsilentvideo')
    assert mi.med_streamed() == False


def test_media_identity():
    mi = MediaIdentity('abc.txt')
    assert mi.med_identity() == True




