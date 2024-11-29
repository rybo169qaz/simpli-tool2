#!/usr/bin/bash

GSET='/usr/bin/gsettings'

LIGHTDM_CONF='etc/lightdm/lightdm.conf'
LIGHTDM_DIR='/etc/lightdm/lightdm.conf.d'
LIGHTDM_CONF_01='/etc/lightdm/lightdm.conf.d/01_my.conf'

COMMANDS_LIST='show | check '
COMMANDS_DESC="show == Show all variables\n\tcheck == check the important settings and report discrepencies\n"

DIVIDER_SECTION='============'
START_SECTION='vvvvvvvvvvvv'
END_SECTION='^^^^^^^^^^^^^'

NOW=$( date '+%F_%H-%M-%S' )

dest_dir='/home/robert/.simpli/logs'
node=$(/usr/bin/uname -n)
op="${dest_dir}/${node}_${NOW}.txt"
PERMA_NAME="${dest_dir}/${node}_report.txt"

if [ -L "${PERMA_NAME}" ]
then
  printf "Info: Removing perma link ${PERMA_NAME}\n"
  rm "$PERMA_NAME"
  #ln -s "${dest_dir}/${op}" "${dest_dir}/$PERMA_NAME"
  #ln -s "${dest_dir}/${op}" "${dest_dir}/$PERMA_NAME"
fi


show_schema() {
  schema_name=$1
  schema_keys=$(/usr/bin/gsettings list-keys ${schema_name})
  printf "\nSCHEMA - ${schema_name}\n" | tee -a $op
  for i in ${schema_keys}; do
    desc=$(/usr/bin/gsettings describe ${schema_name} ${i})

    the_val1=$(/usr/bin/gsettings get ${schema_name} ${i})
    the_val2=$(${DISP} ; /usr/bin/gsettings get ${schema_name} ${i})

    #printf "\n\t : key=${i} : val=${the_val1} : desc=${desc}\n"
    printf "  key= %-30s : val=%-12s : desc=%s\n" "$i" "$the_val1" "$desc" | tee -a $op

    if [ "$the_val1" != "$the_val2" ]
    then
      printf "  OLD differs NEW: key= %-30s : oldval=%-12s : newval=%-12s \n" "$i" "$the_val1"  "$the_val2"  | tee -a $op
    fi
  done
}

main_settings() {
  printf "=== HOST NAME CTL ===\n"
  hostnamectl

  printf "\n=== screenfetch ===\n"
  screenfetch

  printf "\nDesktop: $XDG_CURRENT_DESKTOP"
  if [[ "$XDG_CURRENT_DESKTOP" == 'X-Cinnamon' ]]
  then
    config_details=$(lightdm --show-config)
    printf "\nCONFIG DETAILS:\n${config_details}\n\n"
  fi

  printf "\nDisplay server: $XDG_SESSION_TYPE"

  printf "\nDISK SPACE\n"
  /usr/bin/df -kh

  printf "\nSOUND - PACTL\n"
  pactl list sinks | grep "Sink #"

}

show_gsettings() {
  printf "\nDESKTOP - gsettings\n"
  schemas=$(/usr/bin/gsettings list-schemas)
  printf "SCHEMAS\n${schemas}\n\n"
  DISP='export DISPLAY=:0 '
  show_schema 'org.cinnamon.desktop.screensaver'
  show_schema 'org.cinnamon.desktop.session'
}

check_gkey() {
  schema_name=$1
  key_name=$2
  req_val=$3

  DISP='export DISPLAY=:0 '
  initial_get=$(${DISP} ; ${GSET} get ${schema_name} ${key_name} )
  if [ "$initial_get" == "$req_val" ]
  then
    prefix='OK        :'
  else
    prefix='MISMATCH  :'
  fi
  printf "${prefix} Schema:${schema_name}  key:${key_name} : ACTUAL=${initial_get} ; WANTED=${req_val} \n\n"
}

check_gsettings() {
  printf "\n\n${DIVIDER_SECTION}\nGSETTINGS\n"
  check_gkey 'org.cinnamon.desktop.session' 'idle-delay' 'uint32 0'
  check_gkey 'org.cinnamon.desktop.screensaver' 'idle-activation-enabled' 'false'
  check_gkey 'org.cinnamon.desktop.screensaver' 'lock-enabled' 'false'
}

show_lightdm_settings() {
  printf "\n\n${DIVIDER_SECTION}\nLIGHTDM CONFIG - ${LIGHTDM_CONF} ${LIGHTDM_DIR}\n"

  printf "LIGHTDM CONF : ${LIGHTDM_CONF}\n"
  conf=$(cat ${LIGHTDM_CONF})
  printf "\n${conf}"

  lightdm_files=$(ls ${LIGHTDM_DIR})
  printf "${lightdm_files}\n"
  for i in ${lightdm_files}; do
    full_filename="${LIGHTDM_DIR}/${i}"
    printf "\n\n${full_filename}"
    desc=$(cat ${full_filename})

    printf "\n${START_SECTION}\n${desc}\n${END_SECTION}"
  done
}

check_lightdm_settings() {
  printf "\n\n${DIVIDER_SECTION}\nLIGHTDM SETTINGS\n"
  greeterhide='false'
  username='robert'
  usertimeout='7'

  checkgreeter="greeter-hide-users=${greeterhide}"
  checkname="autologin-user=${username}"
  checktimeout="autologin-user-timeout=${usertimeout}"

  printf "Checking for: \n\t${checkgreeter}\n\t${checkname}\n\t${checktimeout}\n\n"

  grep -E -q "${checkgreeter}|${checkname}|${checktimeout}" ${LIGHTDM_CONF_01}
  checkresp=$?

  if [ "$checkresp" == '0' ]
  then
    printf "Matched all"
  else
    printf "Failed to match all. The following is the contents of ${LIGHTDM_CONF_01}\n"
    conf01=$(cat ${LIGHTDM_CONF_01})
    printf "${START_SECTION}\n${conf01}\n${END_SECTION}\n"
  fi
}


show_xset() {
  xset_config=$(export DISPLAY=:0 ; /usr/bin/xset q)
  printf "\n\n${DIVIDER_SECTION}\nXSET SETTINGS\n${xset_config}\n\n"
}

check_xset() {
  xset_config=$(export DISPLAY=:0 ; /usr/bin/xset q)
  printf "\n\n${DIVIDER_SECTION}\nXSET SETTINGS\n${xset_config}\n\n"
}


if [ "$#" = "0" ]
then
  printf "Syntax is \n\tenv_config   ${COMMANDS_LIST} \nwhere\t${COMMANDS_DESC}\n"
  exit 1
fi

cmd="$1"


printf "COMMAND = ${cmd}\n"
if [ "$cmd" == 'show' ]
then
  main_settings  | tee -a $op
  show_gsettings | tee -a $op
  show_lightdm_settings | tee -a $op
  show_xset | tee -a $op

elif [ "$cmd" == 'check' ]
then
  check_gsettings | tee -a $op
  check_lightdm_settings | tee -a $op
  check_xset | tee -a $op

else
  printf "Valid commands are:${COMMANDS_DESC}\n"
  exit 2
fi

ln -s "${op}" "${PERMA_NAME}"
printf "\n\nOutput destination = ${op}\n"
printf "\nUpdated perma-link  ${PERMA_NAME}  to  ${op}\n"

#printf "\nEND \t${NOW}\n\n" | tee -a $op
printf "\nEND \n\n"