#!/usr/bin/bash

: '
This script starts a vlc session for a particular video
Known videos are:
  autumn          Autumn video
  earth           Earth video
  car             Jaguar video
'

tool_name='VLC'
tool_path='/usr/bin/vlc'
artifact_name='video'
media_dir="${HOME}/.simpli/media"

qual=''
extra=' --loop'

if [ "$#" -eq 0 ]
then
  describe="${tool_name} without specifying media"
elif [ "$#" -eq 1 ]
then
  ip_arg="$1"
  if [ "$ip_arg" = "autumn" ]
  then
    qual="${media_dir}/Autumn.mp4"
    describe='Autumn video'
  elif [ "$ip_arg" = "earth" ]
  then
    qual="${media_dir}/HD_Earth_Views_512kb.mp4"
    describe='Earth video'
  elif [ "$ip_arg" = "car" ]
  then
    qual="${media_dir}/RDDESjd_6M.mp4"
    describe='Car video'
  else
    describe="Invalid ${artifact_name}"
    printf "${describe}"
    exit 2
  fi
else
  printf "Invalid invocation args"
  exit 1
fi

printf "${tool_name} : connect to ${describe}\n\tQUAL: ${qual}\n\n"

tool_cmd="${tool_path} ${extra} ${qual}"
printf "Executing\t${tool_path} ${extra} ${qual}\n"

#export DISPLAY=:0

printf "STARTING ${tool_name}\n"
#the_cmd=$(export DISPLAY=:0 ; /usr/bin/zoom --url="https://zoom.us/j/92399821735?pwd=SXBJb0VsMGF3K09PRS9zUGp6YmM4Zz09")
##the_cmd=$(export DISPLAY=:0 ; ${tool_path} ${qual} )
the_cmd=$(export DISPLAY=:0 ; ${tool_path} ${qual} )

#the_cmd=$("export DISPLAY=:0 ; ${tool_path} ${qual} ")

#cmd_string="export DISPLAY=:0 ; ${tool_path} ${qual} "
#printf ">>>${cmd_string}<<<\n"
#the_cmd=$("${cmd_string}")

#source ${tool_path}
bash <(echo "${the_cmd}")

echo "END OF ${tool_name}"
