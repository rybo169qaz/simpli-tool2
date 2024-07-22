#!/bin/bash

#iport='127.0.0.1:8087'
iport='localhost:8087'
vlc=$(type -p vlc)

printf 'VLC is located at: %s \n' "$vlc"

mediafile="$1"

if [ "${mediafile}" == '' ]
then
	printf 'No media file specified'
	exit 2
fi
printf 'Specified media file: %s \n' "${mediafile}"

fullmedia=$(realpath $mediafile)
printf 'Specified full media file: >>%s<< \n' "${fullmedia}"

if [ ! -r "${fullmedia}" ]
then
	printf 'Specified file is not readable (%s)\n' "${fullmedia}"
fi

serv1=$(printf "%s -vvv input_stream --sout '#standard{access=http,mux=ogg,dst=%s}'" "$vlc" "$iport")
serv2=$(printf "%s -vvv %s --loop --intf dummy --sout udp://%s" "$vlc" "$fullmedia" "$iport")
serv3=$(printf "%s -vvv %s --loop --sout '#standard{access=http,mux=ogg,dst=%s}'" "$vlc" "$fullmedia" "$iport")


printf '\n\n'
#====================
width='960'   # 1920 960
height='540'  # 1080  540
printf 'Dimension text: width:%s , height:%s \n' "$width" "$height"

recv2=$(printf "%s -vv --meta-title="RECV2" --width="%s" --height="%s" udp://@%s " "$vlc" "$width" "$height" "$iport" )
recv3=$(printf "%s -vv --meta-title="RECV3" --width="%s" --height="%s" http://@%s " "$vlc" "$width" "$height" "$iport" )

printf 'Server 1 command: %s \n' "$serv1"

printf '\n--- p2 ---\n'
printf 'Server 2 command: %s \n' "$serv2"
printf 'Player 2 command: %s \n' "$recv2"

printf '\n--- p3 ---\n'
printf 'Server 3 command: %s \n' "$serv3"
printf 'Player 3 command: %s \n' "$recv3"

printf 'FINISHED\n'

