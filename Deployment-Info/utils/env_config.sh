#!/usr/bin/bash

# (xfce) Change background to all monitors by one xfconf command
# https://forum.xfce.org/viewtopic.php?id=17028

# How to Change Desktop Wallpaper from the Terminal
# https://www.baeldung.com/linux/change-desktop-wallpaper-from-terminal#:~:text=For%20Xfce&text=As%20seen%20above%2C%20the%20command,to%20change%20(desktop%20background).


# Sets desktop config
TOOL_FUNC='env_conf'
USER='robert'

LIGHTDM_CONF_01='/etc/lightdm/lightdm.conf.d/01_my.conf'

GSET='/usr/bin/gsettings'
XSET='/usr/bin/xset'

SHOW_COMMAND='SHOW'
DUMMY_ACTION='FALSE'

dest_dir="/home/${USER}/.simpli/logs"
node=$(/usr/bin/uname -n)

NOW=$( date '+%F_%H-%M-%S' )
HOMEDIR='/home/robert'
SIMPLI_ROOT="${HOMEDIR}/.simpli"
SIMPLI_LOGS="${SIMPLI_ROOT}/logs"

op="${dest_dir}/${node}_${TOOL_FUNC}.txt"
LOG="${SIMPLI_LOGS}/latest_log.txt"


mod_gkey() {
  schema_name=$1
  key_name=$2
  new_val=$3

  #printf "Setting schema:${schema_name}  key:${key_name} to value:${new_val}\n"
  DISP='export DISPLAY=:0 '

  initial_get=$(${DISP} ; ${GSET} get ${schema_name} ${key_name} )

  if [ "$SHOW_COMMAND" == "SHOW" ]; then
    printf "ORIGINAL VALUE: >>${initial_get}<<\n"
    printf "COMMAND: ${DISP} ; ${GSET} set ${schema_name} ${key_name} ${new_val} \n"
  fi

  if [ "$DUMMY_ACTION" == "DUMMY" ]; then
    printf "DUMMY ACTION\n"
    printf "Setting schema:${schema_name}  key:${key_name} : WAS=${initial_get} ; WANTED=${new_val} POST=${new_get}\n\n"
  else
    the_set=$(${DISP} ; ${GSET} set ${schema_name} ${key_name} ${new_val} )
    new_get=$(${DISP} ; ${GSET} get ${schema_name} ${key_name} )
    printf "Setting schema:${schema_name}  key:${key_name} : WAS=${initial_get} ; WANTED=${new_val} POST=${new_get}\n\n"
  fi

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
  if [ "$SHOW_COMMAND" == "SHOW" ]; then
    printf "File to be written to: ${LIGHTDM_CONF_01}\n"
  fi

  if [ "$DUMMY_ACTION" == "DUMMY" ]; then
    printf "DUMMY ACTION\n"
  else
    sudo cat << EOF > ${LIGHTDM_CONF_01}
[Seat:*]
greeter-hide-users=false
autologin-user=robert
autologin-user-timeout=5

EOF
  fi

}

restart_lightdm() {
  printf "Restarting lightdm\n"
  sleep 1
  service lightdm restart
}

show_help() {
  printf "Use  env_config \n"
  printf "\t set1     \t Configure using the best known settings\n"
  printf "\t setg     \t To configure the gsettings aspects of the system\n"
  printf "\t setlight \t To configure the lightdm aspects of the system\n"
  printf "\t xset     \t To configure the xset aspects of the system\n"

  description="""
  The requirements for the platform are:
    a) Screen image is ALWAYS available while unit is switched on.
    b) That it requires a single click on desktop icons.
    c) The text is big enough to see at a distance.
    d) It is possible to join Cov West & Grosv zoom meetings.
    e) It is possible to ...
    f) It is possible to determine the software version from GUI w/o keyboard.
    g) It is possible to determine the desktop settings from the GUI w/o keyboard.
"""
  printf "Requirements:\n${description}\n"

  printf "\nTo   show  or chech the desktop settings use: simpli-report\n"
}

do_gsettings() {
  # DOES NOT WORK - DO NOT USE
  given_desk="$1"
  if [ "$given_desk" == "cinnamon" ]
  then
    deskt='cinnamon'
  elif [ "$given_desk" == "xfce" ]
  then
    # no xfce entries exist. I understand xfce is based on gnome
    deskt='gnome'
  else
    printf "Error: desktop is not cinnamon or xfce\n"
    exit 7
  fi

  # did not work
  #mod_gkey "org.gnome.desktop.background" 'picture-uri' "'file:///usr/share/backgrounds/xfce/xfce-teal.jpg'"
  #mod_gkey "org.gnome.desktop.background" 'picture-uri' "'file:///usr/share/backgrounds/linuxmint/default_background.jpg'"
  #mod_gkey "org.${deskt}.desktop.background" 'picture-uri' "'file:///usr/share/backgrounds/linuxmint/sele_ring_center_green.jpg'"

  #mod_gkey "org.${deskt}.desktop.session" 'idle-delay' "0"
  #mod_gkey "org.${deskt}.desktop.screensaver" 'idle-activation-enabled' 'false'
  #mod_gkey "org.${deskt}.desktop.screensaver" 'lock-enabled' 'false'


  #mod_gkey "org.${deskt}.desktop.background" 'picture-uri' "'file:///usr/share/backgrounds/linuxmint/default_background.jpg'"
  #mod_gkey "org.${deskt}.desktop.background" 'picture-uri' "'file:///usr/share/backgrounds/linuxmint/sele_ring_center_green.jpg'"

  #mod_gkey "org.nemo.preferences" 'click-policy' 'single'
  #mod_gkey "org.${deskt}.desktop.interface" 'gtk-overlay-scrollbars' 'false'
}

do_set1() {
  giv_desk="$1"
  printf "Doing set1 (given-desktop=${giv_desk})\n"
  printf "SIMPLI_LOGS ${NOW}\n" >> $LOG

  mod_xset " -display :0 dpms 0 0 0 "

  #mod_gkey "org.${deskt}.desktop.session" 'idle-delay' "0"
  #do_gsettings "$giv_desk" # use xconf instead to change desktop

  mod_lightdm
  restart_lightdm

  #do_gsettings "$giv_desk"
  # Change background image
  # Change so that single click
  # Change scrollbar to be wide
  # Ensure that hdmi signal remains

  printf "Finished doing set1\n"
}

if [ "$#" = "0" ]
then
  show_help
  exit 1
fi

cmd="$1"
arg1="$2"

printf "LOGGING\n" > ${LOG}

if [ "$cmd" == "-h" ]
then
  show_help

elif [ "$cmd" == 'set1' ]
then
  do_set1 "${arg1}"

elif [ "$cmd" == 'setg' ]
then
  do_gsettings "$arg1"

elif [ "$cmd" == 'xset' ]
then
  # Arch Linux : Display Power Management Signaling
  # https://wiki.archlinux.org/title/Display_Power_Management_Signaling
  #mod_xset " -display :0 s off -dpms "
  mod_xset " -display :0 dpms 0 0 0 "
  #mod_xset " -display :0 -dpms "
  #mod_xset " dpms force on "
  #mod_xset " s off "
  #mod_xset " s noblank "

elif [ "$cmd" == 'setlight' ]
then
  mod_lightdm
  restart_lightdm

else
  show_help
fi

printf "Output destination = ${op}\n"

exit 0

#}