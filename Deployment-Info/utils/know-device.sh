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

NOW=$( date '+%F_T_%H-%M-%S' )

dest_dir='/home/robert/.simpli/logs'
node=$(/usr/bin/uname -n)
#op="${dest_dir}/${node}_${NOW}.txt"
PERMA_NAME="${dest_dir}/${node}_report"



show_schema() {
  schema_name=$1
  schema_keys=$(/usr/bin/gsettings list-keys ${schema_name})
  printf "\nSCHEMA - ${schema_name}\n"
  for i in ${schema_keys}; do
    desc=$(/usr/bin/gsettings describe ${schema_name} ${i})

    the_val1=$(/usr/bin/gsettings get ${schema_name} ${i})
    the_val2=$(${DISP} ; /usr/bin/gsettings get ${schema_name} ${i})

    #printf "\n\t : key=${i} : val=${the_val1} : desc=${desc}\n"
    printf "  key= %-30s : val=%-12s : desc=%s\n" "$i" "$the_val1" "$desc"

    if [ "$the_val1" != "$the_val2" ]
    then
      printf "  OLD differs NEW: key= %-30s : oldval=%-12s : newval=%-12s \n" "$i" "$the_val1"  "$the_val2"
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

show_all_schema_keys() {
  schemas=$(/usr/bin/gsettings list-schemas)
  printf "\n\nSCHEMAS\n${schemas}\n\n"

  schema_keys=$(/usr/bin/gsettings list-recursively)
  printf "\n\nSCHEMA-KEYS\n${schema_keys}\n\n"
}

show_gsettings() {
  printf "\nDESKTOP - gsettings\n"

  DISP='export DISPLAY=:0 '
  show_schema 'org.cinnamon.desktop.screensaver'
  show_schema 'org.cinnamon.desktop.session'

  show_schema 'org.gtk.Settings.FileChooser'
  show_schema 'org.cinnamon.org.gtk.gtk4.Settings.FileChooser'

  show_schema 'com.linuxmint.mintmenu.plugins.places'
  show_schema 'com.linuxmint.mintmenu.plugins.system_management'
  show_schema 'org.cinnamon.desktop.interface'

  show_schema 'org.nemo.preferences'

  # Now sound related
  show_schema 'org.cinnamon.desktop.sound'
  show_schema 'org.cinnamon.sounds'
  show_schema 'org.gnome.desktop.sound'


}

show_nemo() {
  nemo_data=$(/usr/bin/cat ~/.config/nemo/desktop-metadata)
  printf "\n\nNEMO - ${nemo_data}\n"
}

check_gkey() {
  schema_name=$1
  key_name=$2
  req_val=$3

  DISP='export DISPLAY=:0 '

  #initial_get=$(${DISP} ; ${GSET} get ${schema_name} ${key_name} )
  initial_get=$(${GSET} get ${schema_name} ${key_name} )

  if [ "$initial_get" == "$req_val" ]
  then
    prefix='OK  :'
    desc="ACTUAL=WANTED=${initial_get} "
  else
    prefix='BAD :'
    desc="\n\t\t\tACTUAL=${initial_get} ; \n\t\t\tWANTED=${req_val} "
  fi
  #printf "${prefix} Schema:${schema_name}  key:${key_name} : ACTUAL=${initial_get} ; WANTED=${req_val} \n\n"
  printf "${prefix} Schema:${schema_name}  key:${key_name} : ${desc}\n\n"
}

check_gsettings() {
  # graphical control is via dconf-editor
  printf "\n\n${DIVIDER_SECTION}\nGSETTINGS\n"
  check_gkey 'org.cinnamon.desktop.session' 'idle-delay' 'uint32 0'
  check_gkey 'org.cinnamon.desktop.screensaver' 'idle-activation-enabled' 'false'
  check_gkey 'org.cinnamon.desktop.screensaver' 'lock-enabled' 'false'

  #
  check_gkey 'org.cinnamon.desktop.background' 'picture-uri' "'file:///usr/share/backgrounds/linuxmint/sele_ring_center_green.jpg'" # orig 'file:///usr/share/backgrounds/linuxmint/default_background.jpg'

  check_gkey 'com.linuxmint.mintmenu.plugins.places' 'allow-scrollbar' 'false'
  check_gkey 'com.linuxmint.mintmenu.plugins.system_management' 'allow-scrollbar' 'false'
  check_gkey 'org.cinnamon.desktop.interface' 'gtk-overlay-scrollbars' 'false'

  check_gkey 'org.nemo.preferences' 'click-policy' "'single'"

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
  usertimeout='3'

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

if [ $cmd == "show" -o $cmd == "check" ]; then
  #op="${dest_dir}/${node}_${cmd}_${NOW}.txt"
  op="${dest_dir}/${node}_${NOW}_${cmd}.txt"
  printf "COMMAND = ${cmd}\n${NOW}\n" 2>&1 | tee -a $op
else
  printf "Invalid command argument\n"
  op="${dest_dir}/${node}_${NOW}.txt"
fi

#this_perm="${PERMA_NAME}_${cmd}.txt"
this_perm="${dest_dir}/${cmd}.txt"

if [ -L "${this_perm}" ]
then
  printf "Info: Removing perma link ${this_perm}\n"
  rm -f "${this_perm}"
fi


#printf "COMMAND2 = ${cmd}\n${NOW}\n" 2>&1 | tee -a $op

running_as=$(/usr/bin/whoami)
printf "USER = ${running_as}\n" 2>&1 | tee -a $op

if [ "$cmd" == 'show' ]
then
  main_settings  2>&1 | tee -a $op

  show_all_schema_keys 2>&1 | tee -a $op

  show_gsettings 2>&1 | tee -a $op
  show_lightdm_settings 2>&1 | tee -a $op
  show_xset 2>&1 | tee -a $op
  show_nemo 2>&1 | tee -a $op
  printf "\n\nSOUND\n" 2>&1 | tee -a $op
  /home/robert/.simpli/utils/sound_control.sh list 2>&1 | tee -a $op


elif [ "$cmd" == 'check' ]
then
  check_gsettings 2>&1 | tee -a $op
  check_lightdm_settings 2>&1 | tee -a $op
  check_xset 2>&1 | tee -a $op

else
  printf "Valid commands are:${COMMANDS_DESC}\n"
  exit 2
fi

printf "\n\nOutput destination = ${op}\n"
/usr/bin/chmod 444 "${op}"
#rm -f "${this_perm}"
/usr/bin/ln -s "${op}" "${this_perm}"
printf "\nUpdated perma-link  ${this_perm}  to point to ${op}\n"

printf "\nEND \n\n"