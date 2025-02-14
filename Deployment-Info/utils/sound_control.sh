#!/usr/bin/bash

# Sets desktop config
TOOL_FUNC='sound_control'
USER='simp' # #robert'
PACTL='/usr/bin/pactl'
LINUX_PULSE_PACKAGE='pulseaudio'
LINUX_PAVU_PACKAGE='pavucontrol'

dest_dir="/home/${USER}/.simpli/logs"
node=$(/usr/bin/uname -n)
NOW=$( date '+%F_%H-%M-%S' )

op="${dest_dir}/${node}_${TOOL_FUNC}.txt"

# Changing audio output from terminal
# https://unix.stackexchange.com/questions/459240/changing-audio-output-from-terminal

show_help() {
  printf "Use  sound_control \n"
  printf "\t list                              To report/show all the existing sound settings/config\n"
  printf "\t findsinks                         Find the numbers of the sinks. \n"
  printf "\t details      <port_num>           Lists details info of specified port\n"
  printf "\t hdmi                              Lists details of hdmi sinks\n"
  printf "\t gethdmiport                       Lists hdmi port no \n"
  printf "\t setvolume                         Set volume of hdmi at 80 percent \n"

  printf "\t gethdminame                       Lists hdmi port name\n"

  printf "\t get          <port_num>           Get the volume of port specified.\n"
  printf "\t set          <port_num>  <volume> Set the volume of port specified. (units in %%)\n"
  printf "\t getdefault                        Gets the default sink\n"
  printf "\t hdminame                          Get the name of the hdmi port\n"
  printf "\t sethdmi                           Set the default to be the hdmi port\n"

  printf "\t\t\t\tThe number is a PERCENTAGE\n"
  #printf "\t\t\t\tThe number is a VALUE NOT a percentage\n"

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

remove_temp_dir() {
  dir_to_remove="$1"
  if [[ "$dir_to_remove" != /tmp/* ]]
  then
    printf "ERROR: Being asked to delete dir not under /tmp >>${dir_to_remove}<<\n"
    exit 1
  fi

  find "${dir_to_remove}" -type f  -exec rm {} \;
  rmdir "${dir_to_remove}"

  # check that directory has been removed
  if [ -d "$dir_to_remove" ]; then
    printf "ERROR: directory '${dir_to_remove}' still exists\n"
    exit 2
  fi
}

get_sink_numbers() {
  #printf "Print the sink numbers\n"
  #find_sink_cmd="/usr/bin/pactl list | grep -oP 'Sink #\K([0-9]+)' "
  all_sink_num=$( ${PACTL} list sinks | grep -oP 'Sink #\K([0-9]+)' )
  printf "${all_sink_num}"
}

process_sinks_info() {
  work_dir="$1"
  #printf "Created templatefile directory ${wkg}\n"
  the_tmp="$(dirname "${work_dir}")" ; temp_dir="$(basename "${work_dir}")"
  #printf "DIR part==${the_tmp} \t LASTpart==${temp_dir}\n"

  all_sinks="${work_dir}/all.txt"
  ${PACTL} list sinks > ${all_sinks}
  printf "\nSink #999\n" >> ${all_sinks}

  mod_sinks="${work_dir}/mod.txt"
  cat ${all_sinks} | awk '{gsub(/Sink #/,"Sink #\nPort: ");print}' > ${mod_sinks}

  # Now splitting file based upon 'Sink #'
  # (stackoverflow) How to split a file by using keyword boundaries
  # https://unix.stackexchange.com/questions/76929/how-to-split-a-file-by-using-keyword-boundaries
  csplit -f "${work_dir}/sink_" -b %02d.txt ${mod_sinks} -z '/Sink #/+1' '{*}' > /dev/null
  list_of_files=$(ls ${work_dir} )
  #printf "\nList of sinks: ${list_of_files}\n++\n"
}



find_hdmi_details() {
  wkg=$(mktemp -d)
  process_sinks_info "${wkg}"

  shopt -s globstar
  find ${wkg} -name "sink*.txt"|while read file
  do
    cond="${file/sink_/condensed_}"
    grep -Ei 'Port:|State:|Name:|Description:|Volume:|Monitor Source:|hdmi-output-0:|Active Port:|alsa.card_name' ${file} > ${cond}

    # alsa_output.pci-0000_00_14.2.3.analog-stereo
    #fulltext=$(cat ${cond} )

    if grep -i --quiet hdmi ${cond}; then
      #printf "XXX\n${fulltext}\n"
      printf "\nMATCHED HDMI\n"
      cat ${cond}
    fi
  done

  remove_temp_dir "${wkg}"
}

get_name_of_hdmi_port() {
  wkg=$(mktemp -d)
  process_sinks_info "${wkg}"

  shopt -s globstar
  find ${wkg} -name "sink*.txt"|while read file
  do
    #printf "Processing sink file: ${file}\n"
    cond="${file/sink_/condensed_}"
    #grep -Ei 'Monitor Source:' ${file} | sed "s@\s*Monitor Source: @@" > ${cond} # wrong field
    grep -Ei 'Name:' ${file} | sed "s@\s*Name: @@" > ${cond}

    # alsa_output.pci-0000_00_14.2.3.analog-stereo
    fulltext=$(cat ${cond} )

    if grep -i --quiet hdmi ${cond}; then
      printf "${fulltext}"
    fi
  done

  remove_temp_dir "${wkg}"
}

show_hdmi_name() {
  port_name=$(get_name_of_hdmi_port)
  printf "Name of HDMI port: >>${port_name}<<\n"

}

get_hdmi_portno() {
  port_info=$(find_hdmi_details)
  portno=$(echo "${port_info}" | grep -oP 'Port: \K([0-9]+)' )
  printf "${portno}"
}

get_hdmi_name() {
  port_info=$(find_hdmi_details)
  portname=$(echo "${port_info}" | grep -oP 'Name: \K([.]+)' )
  #portname=$(echo "${port_info}" | sed -n 's/(.*)(Name:\s...)(.*Desc)/\2/' )
  printf "${portname}"
}

find_hdmi_port() {
  #port_info=$(find_hdmi_details)
  #portno=$(echo "${port_info}" | grep -oP 'Port: \K([0-9]+)' )
  portnum=$(get_hdmi_portno)
  printf "HDMI port is ${portnum}\n\n"
}

set_hdmi_vol() {
  # set the default to the name
  set_hdmi_as_default

  # now set the volume of this port to hdmi
  portnum=$(get_hdmi_portno)

  wanted_vol='80'
  printf "Setting (HDMI) port ${portnum} to ${wanted_vol}\n"
  set_port_volume "${portnum}" "${wanted_vol}"

}


find_hdmi_name() {
  portnum=$(get_hdmi_name)
  printf "HDMI name is ${portnum}\n\n"
}


get_default() {
  current_default=$( /usr/bin/pactl get-default-sink)
  printf "Current default port is: ${current_default}\n"
}

set_hdmi_as_default() {
  get_default

  port_name=$(get_name_of_hdmi_port)
  printf "Will set default sink as >>${port_name}<<\n"
  /usr/bin/pactl set-default-sink "${port_name}"
  #printf "Sett comand resp= >>${resp}<<"

  get_default
}

find_sinks() {
  sink_num_list=$( get_sink_numbers )
  printf "Sink numbers: ( $sink_num_list )\n"
}


sink_details() {
  arg1="$1"
  printf "Showing details of port ${arg1}\n"
  info=$( ${PACTL} info "${arg1}" )
  printf "Port ${arg1} details:\n${info}\n\n"

  # Try to determine if its an HDMI port
  #type_op=$( echo "$info}" | grep 'Default Sink' )
  type_op=$( echo "$info}" | grep 'Active Port:' )
  found=$( echo "${type_op}" | grep -i hdmi )
  if [ "${found}" == '' ]
  then
    desc='NOT HDMI'
  else
    desc='HDMI'
  fi
  printf "Assessment: Port Type is ${desc} \n"

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

elif [ "$cmd" == 'hdmi' ]
then
  find_hdmi_details

elif [ "$cmd" == 'gethdmiport' ]
then
  find_hdmi_port

elif [ "$cmd" == 'setvolume' ]
then
  set_hdmi_vol

elif [ "$cmd" == 'gethdminame' ]
then
  # this does not work
  find_hdmi_name



elif [ "$cmd" == 'get' ]
then
  get_port_volume "${param1}"

elif [ "$cmd" == 'set' ]
then
  set_port_volume "${param1}" "${param2}"

elif [ "$cmd" == 'getdefault' ]
then
  get_default

elif [ "$cmd" == 'hdminame' ]
then
  show_hdmi_name

elif [ "$cmd" == 'sethdmi' ]
then
  set_hdmi_as_default

else
  show_help
fi

#printf "Output destination = ${op}\n"

exit 0

}