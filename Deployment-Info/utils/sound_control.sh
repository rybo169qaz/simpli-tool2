#!/usr/bin/bash

# Sets desktop config
TOOL_FUNC='sound_control'
USER='robert'
PACTL='/usr/bin/pactl'
LINUX_PULSE_PACKAGE='pulseaudio'
LINUX_PAVU_PACKAGE='pavucontrol'

dest_dir="/home/${USER}/.simpli/logs"
node=$(/usr/bin/uname -n)
NOW=$( date '+%F_%H-%M-%S' )

op="${dest_dir}/${node}_${TOOL_FUNC}.txt"


show_help() {
  printf "Use  sound_control \n"
  printf "\t list                 To report/show all the existing sound settings/config\n"
  printf "\t findsinks            Find the numbers of the sinks. \n"
  printf "\t details  <port_num>  Lists details info of specified port\n"
  printf "\t type <port_num>      Show Lists details info of specified port\n"
  printf "\t get      <port_num>  Get the volume of port specified.\n"
  printf "\t set      <port_num>  <volume> Set the volume of port specified.\n"
  printf "\t\t\t\tThe number is a PERCENTAGE\n"
  #printf "\t\t\t\tThe number is a VALUE NOT a percentage\n"

  printf "\t set                  NOT IMPL To configure the system to the required values\n"
  printf "\t check                NOT IMPL To identify discrepancies in the config from the desired settings\n"
}

list_pactl() {
  cmd_all='/usr/bin/pactl list sinks'
  all_op=$( ${cmd_all} )
  printf "\n\nALL PACTL SINKS\nCommand: ${cmd_all}\n\nOutput\n"
  /usr/bin/pactl list sinks
  printf "\n\nEND\n\n"

  cmd_sinks="pactl list | grep -oP 'Sink #\K([0-9]+)' | while read -r i ; do pactl -- get-sink-volume $i ; done"
  printf "\n\nSINKS PACTL INFO\nCommand: ${cmd_sinks}\n\nOutput\n\n"
  /usr/bin/pactl list | grep -oP 'Sink #\K([0-9]+)' | while read -r i ; do pactl -- get-sink-volume $i ; done
  printf "\n\nEND\n\n"

  #pactl list | grep -oP 'Sink #\K([0-9]+)' | while read -r i ; do pactl -- get-sink-volume $i ; done
}

find_sinks() {
  printf "Print the sink numbers\n"
  #find_sink_cmd="/usr/bin/pactl list | grep -oP 'Sink #\K([0-9]+)' "
  /usr/bin/pactl list | grep -oP 'Sink #\K([0-9]+)'
}

sink_details() {
  arg1="$1"
  printf "Showing details of port ${arg1}\n"
  /usr/bin/pactl info "${arg1}"
}

show_port_type() {
  arg1="$1"
  printf "Showing the type of port of port ${arg1}. (Return True if it contains teh word HDMI)\n"
  type_op=$( /usr/bin/pactl info ${arg1} | grep 'Default Sink' )
  #printf "SINK LINE >>${type_op}<<\n"
  found=$( echo "${type_op}" | grep -i hdmi )
  #printf "FOUND=  >>${found}<<\n"
  if [ "${found}" == '' ]
  then
    desc='NOT HDMI'
  else
    desc='HDMI'
  fi
  printf "Port ${arg1} is ${desc} \n"
}

get_port_volume() {
  portno="$1"
  printf "Volume of port ${portno} is \n"
  ${PACTL}  "--" "get-sink-volume" "${portno}"
  printf "\n===\n"
}

set_port_volume() {
  portno="$1"
  vol="$2"
  # (stack exchange) Changing audio output from terminal
  # https://unix.stackexchange.com/questions/459240/changing-audio-output-from-terminal
  #printf "SETTING SINK VOLUME OF PRT ${portno} to ${percentvol}%% \n"
  printf "Setting volume of port ${portno} to ${vol}%% \n"
  ${PACTL} "--" "set-sink-volume" "${portno}" "${vol}%"
  printf "\n\n"

  printf "Reading back volume for port ${portno} \n"
  get_port_volume "${portno}"
  #printf "\nN.B. Still to work out how to specify percentage in the set command.\n"
}


if [ "$#" = "0" ]
then
  show_help
  exit 1
fi

cmd="$1"
param1="$2"
param2="$3"

if [ "$cmd" == "-h" ]
then
  show_help

elif [ "$cmd" == 'list' ]
then
  list_pactl

elif [ "$cmd" == 'findsinks' ]
then
  find_sinks

elif [ "$cmd" == 'details' ]
then
  sink_details "${param1}"

elif [ "$cmd" == 'type' ]
then
  show_port_type "${param1}"

elif [ "$cmd" == 'get' ]
then
  get_port_volume "${param1}"

elif [ "$cmd" == 'set' ]
then
  set_port_volume "${param1}" "${param2}"

else
  show_help
fi

#printf "Output destination = ${op}\n"

exit 0

}