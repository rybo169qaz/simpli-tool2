#!/usr/bin/bash

# Sets desktop config
TOOL_FUNC='env_conf'
USER='robert'

LIGHTDM_CONF_01='/etc/lightdm/lightdm.conf.d/01_my.conf'

GSET='/usr/bin/gsettings'
XSET='/usr/bin/xset'

dest_dir="/home/${USER}/.simpli/logs"
node=$(/usr/bin/uname -n)

NOW=$( date '+%F_%H-%M-%S' )

op="${dest_dir}/${node}_${TOOL_FUNC}.txt"


mod_gkey() {
  schema_name=$1
  key_name=$2
  new_val=$3

  #printf "Setting schema:${schema_name}  key:${key_name} to value:${new_val}\n"
  DISP='export DISPLAY=:0 '
  printf "${GSET} set ${schema_name} ${key_name} ${new_val}\n"

  initial_get=$(${DISP} ; ${GSET} get ${schema_name} ${key_name} )
  the_set=$(${DISP} ; ${GSET} set ${schema_name} ${key_name} ${new_val} )
  new_get=$(${DISP} ; ${GSET} get ${schema_name} ${key_name} )
  printf "Setting schema:${schema_name}  key:${key_name} : WAS=${initial_get} ; WANTED=${new_val} POST=${new_get}\n\n"
}


get_gkey() {
  schema_name=$1
  key_name=$2

  #printf "Setting schema:${schema_name}  key:${key_name} to value:${new_val}\n"
  DISP='export DISPLAY=:0 '
  printf "${GSET} set ${schema_name} ${key_name} \n"

  initial_get=$(${DISP} ; ${GSET} get ${schema_name} ${key_name} )
  printf "Getting schema:${schema_name}  key:${key_name} : ${initial_get} \n"
}

mod_xset() {
  the_command=$1
  fullcmd="${XSET} ${the_command}"
  printf "Setting XSET   ${fullcmd}\n"
  resp=$(${fullcmd} )
}

mod_lightdm() {
  # add auto logon
  sudo cat << EOF > ${LIGHTDM_CONF_01}
[Seat:*]
greeter-hide-users=false
autologin-user=robert
autologin-user-timeout=5

EOF

}

restart_lightdm() {
  printf "Restarting lightdm\n"
  sleep 3
  service lightdm restart
}

show_help() {
  printf "Use  env_config \n"
  printf "\t setg     \t To configure the gsettings aspects of the system\n"
  printf "\t setlight \t To configure the lightdm aspects of the system\n"
  printf "\t xset     \t To configure the xset aspects of the system\n"

  printf "\nTo   show  or chechk the desktop settings use: simpli-report\n"
}



if [ "$#" = "0" ]
then
  show_help
  exit 1
fi

cmd="$1"

if [ "$cmd" == "-h" ]
then
  show_help

elif [ "$cmd" == 'setg' ]
then
  mod_gkey 'org.cinnamon.desktop.session' 'idle-delay' "0"
  mod_gkey 'org.cinnamon.desktop.screensaver' 'idle-activation-enabled' 'false'
  mod_gkey 'org.cinnamon.desktop.screensaver' 'lock-enabled' 'false'

  #mod_gkey 'org.cinnamon.desktop.background' 'picture-uri' "'file:///usr/share/backgrounds/linuxmint/default_background.jpg'"
  mod_gkey 'org.cinnamon.desktop.background' 'picture-uri' "'file:///usr/share/backgrounds/linuxmint/sele_ring_center_green.jpg'"

  mod_gkey 'org.nemo.preferences' 'click-policy' 'single'
  mod_gkey 'org.cinnamon.desktop.interface' 'gtk-overlay-scrollbars' 'false'
  #restart_lightdm

elif [ "$cmd" == 'xset' ]
then
  mod_xset " -dpms "
  mod_xset " dpms force on "
  mod_xset " s off "
  mod_xset " s noblank "

elif [ "$cmd" == 'setlight' ]
then
  mod_lightdm
  restart_lightdm

else
  show_help
fi

printf "Output destination = ${op}\n"

exit 0

}