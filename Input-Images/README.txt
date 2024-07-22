#
# https://www.omgubuntu.co.uk/2011/03/how-to-create-qr-codes-in-ubuntu#:~:text=You%20will%20need%20to%20install,see%20this%20post%20for%20that).

# Syntax
qrencode -o [filename.png] ‘[text/url/information to encode]’

example

qrencode -o google.png 'http://google.com'

#######

======================================================
select -u testproverbs
qrencode -o testproverbs.png -s 6 'select -u testproverbs'

======================================================
select -p vlc -u testcountingaudio
qrencode -o testcountingaudio-vlc.png -s 6 'select -p vlc -u testcountingaudio'

======================================================
select media -w testsilentvideo
qrencode -o testsilentvideo.png -s 6 'select media -w testsilentvideo'


======================================================
select -p vlc -u testvideo
qrencode -o testvideo-vlc.png -s 6 'select -p vlc -u testvideo'

======================================================
select -p ffmpeg   -u testvideo
qrencode -o testvideo-ffmpeg.png -s 6 'select -p ffmpeg -u testvideo'
