import os
import platform
import sys
from report import *

# Test Text
TEST_TEXT = 'test-job.txt'
TEST_SAME_TEXT = 'test-job-same.txt'
TEST_PROVERBS_TEXT = "Proverbs_KJV.txt"
TEST_JOSEPHUS_TEXT = "Life-Flavius-Josephus.txt"

# Test Audio
TEST_MP3 = "Hymn-372_Who-is-on.mp3"
TEST_SPOKEN_NUMBERS_M4A_AUDIO = "spoken_1-20_seconds.m4a"

# Test Video
TEST_VIDEO = "test-video.mp4"
TEST_NURSING_MOOSE_MP4_VIDEO = "Nursing_moose_calf.mp4"

# Test Remote Audio
TEST_REMOTE_AUDIO_MEAST_ABSALOM = 'http://165.22.38.83/archives/AbsalomMH.mp3'
TEST_REMOTE_AUDIO_MEAST_AMOS = 'http://165.22.38.83/archives/AmosGJackman.mp3'

TEST_REMOTE_VIDEO_CVIDEO_DEAD_SEA_SCROLLS = "https://www.youtube.com/watch?v=gj4Q3IvzrL8"

# well-known-name, type-of-media, renderer, location, streamed?, uri
well_known_uris = [
    ('testtext',          'TEXT',    'test',    False, TEST_TEXT),
    ('testproverbs',      'TEXT',    'test',    False, TEST_PROVERBS_TEXT),
    ('testjosephus',      'TEXT',    'test',    False, TEST_JOSEPHUS_TEXT),

    ('testaudio372',         'MPEG',    'test',    False, TEST_MP3),
    ('testcountingaudio', 'MPEG',    'test',    False, TEST_SPOKEN_NUMBERS_M4A_AUDIO),
    ('testsilentvideo',         'MPEG',    'test',    False, TEST_VIDEO),

    ('testmoosevideo',    'MPEG',    'test',    False, TEST_NURSING_MOOSE_MP4_VIDEO),
    ('trvscrolls',        'MPEG',    'remote',  True,  TEST_REMOTE_VIDEO_CVIDEO_DEAD_SEA_SCROLLS),

    ('remoteaudio1',        'MPEG',    'remote',  True,  TEST_REMOTE_AUDIO_MEAST_AMOS),
    ('remoteaudio2',        'MPEG',    'remote',  True,  TEST_REMOTE_AUDIO_MEAST_ABSALOM)

]

media_root = 'pyplay/Media'

