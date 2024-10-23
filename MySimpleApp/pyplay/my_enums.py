from enum import Enum


class SourceLoc(Enum):
    LOCAL = 1
    NETWORK = 2
    TESTLOCAL = 3

class MediaForm(Enum):
    FILE = 1
    STREAMED = 2

class MediaType(Enum):
    TEXT = 1
    MPEG = 2
    IDENTITY = 3
    UNKNOWN = 4
    VIDEO = 5
    IMAGE = 6
    AUDIO = 7

class MediaFormat(Enum):
    TXT = 1
    PDF = 2
    JPG = 3
    PNG = 4
    MP3 = 5
    MP4 = 6
    M4A = 7
    UNKNOWN = 8

class MediaMaster(Enum):
    MASTER = 1
    DERIVED = 2
