#!/usr/bin/bash

: '
This script starts a zoom meeting to the specified meeting.
Known meetings are:
  grosv          Coventry Grosvenor Rd
  west           Coventry West
  rev            Coventry Grosv Revelation class
'
tool_name='ZOOM'
tool_path='/usr/bin/zoom'
artifact_name='meeting'

qual=''

if [ "$#" -eq 0 ]
then
  describe="${tool_name} without joining"
elif [ "$#" -eq 1 ]
then
  ip_arg="$1"
  if [ "$ip_arg" = "grosv" ]
  then
    #qual=' --url="https://zoom.us/j/92399821735?pwd=SXBJb0VsMGF3K09PRS9zUGp6YmM4Zz09"'
    qual='https://zoom.us/j/92399821735?pwd=SXBJb0VsMGF3K09PRS9zUGp6YmM4Zz09'
    describe='Coventry Grosvenor Rd'
  elif [ "$ip_arg" = "west" ]
  then
    qual=' --url="https://us02web.zoom.us/j/9170212859?pwd=U1FNQWJ5ZEVxMlZ5U1FVek8xajFXZz09"'
    describe='Coventry West'
  elif [ "$ip_arg" = "rev" ]
  then
    #zoommtg://zoom.us/join?action=join&confno=<your_conference_number>
    base='zoommtg://zoom.us/join?action=join&'
    rev_mtng='83090303325'
    fulluri="'${base}confno=${rev_mtng}'"
    qual=" --url=${fulluri}"
    describe='Coventry Grosv Revelation'
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

tool_cmd="${tool_path} ${qual}"
printf "Executing\t${tool_path} ${qual}\n"

#export DISPLAY=:0

printf "STARTING ${tool_name}\n"
#the_cmd=$(export DISPLAY=:0 ; /usr/bin/zoom --url="https://zoom.us/j/92399821735?pwd=SXBJb0VsMGF3K09PRS9zUGp6YmM4Zz09")
##the_cmd=$(export DISPLAY=:0 ; ${tool_path} ${qual} )
the_cmd=$(export DISPLAY=:0 ; ${tool_path} --url="${qual}" )

#the_cmd=$("export DISPLAY=:0 ; ${tool_path} ${qual} ")

#cmd_string="export DISPLAY=:0 ; ${tool_path} ${qual} "
#printf ">>>${cmd_string}<<<\n"
#the_cmd=$("${cmd_string}")

#source ${tool_path}
bash <(echo "${the_cmd}")

echo "END OF ${tool_name}"