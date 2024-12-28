#!/usr/bin/bash

GSET='/usr/bin/gsettings'

LIGHTDM_CONF='etc/lightdm/lightdm.conf'
LIGHTDM_DIR='/etc/lightdm/lightdm.conf.d'
LIGHTDM_CONF_01='/etc/lightdm/lightdm.conf.d/01_my.conf'

COMMANDS_SYNTAX='<command> <desktop>\n\where\n\t<command> == show | check \n\t<desktop> == cinnamon | xfce\n'
COMMANDS_LIST='show | check '
COMMANDS_DESC="show == Show all variables\n\tcheck == check the important settings and report discrepencies\n"

DIVIDER_SECTION='============'
START_SECTION='vvvvvvvvvvvv'
END_SECTION='^^^^^^^^^^^^^'


xfcedesk='xfce4-desktop'

BACKDROP_IMAGE_KEY='/backdrop/screen0/monitorDisplayPort-0/workspace0/last-image'
BACKDROP_PALM_IMAGE='/usr/share/xfce4/backdrops/wilma_mpiwnicki_palm.jpg'
BACKDROP_MOUNTAIN_IMAGE='/usr/share/xfce4/backdrops/wilma_mpiwnicki_torres_del_paine.jpg'

ICON_FONT_SIZE_KEY='/desktop-icons/font-size'
ICON_FONT_SIZE_9='9.000000'
ICON_FONT_SIZE_BIG='14.000000'

ICON_SIZE_KEY='/desktop-icons/icon-size'
ICON_SIZE_VALUE_BIG='82'

SINGLE_CLICK='/desktop-icons/single-click'

old_back='/usr/share/xfce4/backdrops/linuxmint.jpg'
new_back='/usr/share/xfce4/backdrops/sele_ring_green.jpg'
new2_back='/usr/share/xfce4/backdrops/edesigner_linuxmint.png'

sc0mon0_imgpath="/backdrop/screen0/monitor0/image-path"
sc0mon0_lastimg="/backdrop/screen0/monitor0/last-image"
sc0mon0_lastsingimg="/backdrop/screen0/monitor0/last-single-image"

sc0mon1_imgpath="/backdrop/screen0/monitor1/image-path"
sc0mon1_lastimg="/backdrop/screen0/monitor1/last-image"
sc0mon1_lastsingimg="/backdrop/screen0/monitor1/last-single-image"

MON_DP0='/backdrop/screen0/monitorDisplayPort-0/workspace0/last-image'




NOW=$( date '+%F_T_%H-%M-%S' )

dest_dir='/home/robert/.simpli/logs'
node=$(/usr/bin/uname -n)
#op="${dest_dir}/${node}_${NOW}.txt"
PERMA_NAME="${dest_dir}/${node}_report"

screen_info() {
  printf "\n=== screenfetch ===\n"
  screenfetch -N -n

  printf "\n=== neofetch ===\n"
  neofetch --off --color_blocks off
}


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

show_xfconf_schema() {
  the_schema="$1"
  XCONFQ="/usr/bin/xfconf-query"
  printf "\n\n+++ START LIST SCHEMA KEYS: schema==${the_schema}\n"
  /usr/bin/xfconf-query -c ${the_schema} -l -v | paste /dev/null -
  printf "\n++ END LIST OF SCHEMA KEYS\n"
}

get_xfconf_property() {
  the_sch="$1"
  the_prop="$2"

  printf "\nGET SCHEMA PROPERTY: schema= ${the_sch} , property= ${the_prop}\n"
  /usr/bin/xfconf-query -c ${the_sch} -p ${the_prop} -l -v | paste /dev/null -
  printf "=\n"
}

reset_xfconf_property() {
  the_sch="$1"
  the_prop="$2"

  printf "\nRESET SCHEMA PROPERTY: schema= ${the_sch} , property= ${the_prop}\n"
  /usr/bin/xfconf-query -c ${the_sch} -p ${the_prop} -r | paste /dev/null -
  printf "=\n"
}

set_xfconf_property() {
  the_sch="$1"
  the_prop="$2"
  the_value="$3"

  printf "\nSET SCHEMA PROPERTY: schema= ${the_sch} , property= ${the_prop} , value=>>${the_value}<<\n"
  /usr/bin/xfconf-query -c ${the_sch} -p ${the_prop} -s "$the_value"  | paste /dev/null -
  printf "==\n"
}

check_xfconf_property() {
  the_sch="$1"
  the_prop="$2"
  the_value="$3"

  /usr/bin/xfconf-query -c "${the_sch}" -p "${the_prop}"
  printf "ZYZ\n"
  resp=$(/usr/bin/xfconf-query -c "${the_sch}" -p "${the_prop}"  )
  printf "RAW ANALYSIS : >>${resp}<<\n"

  resparray=($resp)
  prop=$( echo ${resparray[0]} )
  val=$( echo ${resparray[1]} )
  other=$( echo ${resparray[2]} )


  printf "ARRAY ANALYSIS : PROPERTY=${prop} , VALUE=${val} , OTHER=${other}\n"

  if [ "$the_value" != "$val" ]
  then
    desc='BAD'
    printf "\tValues differ\n"
  else
    desc='OK '
  #  printf "\tThey match\n"
  fi
  printf "\n${desc} : CHECK schema=${the_sch} , property=${the_prop} , req=${the_value}, actual=${val}\n"
}

list_xfconf_schemas() {
  # Xfce Commands and Other Useful Stuff
  # https://mxlinux.org/wiki/xfce/xfce-commands-and-other-useful-stuff/#listconfig
  declare -a schemaArray1=("displays" "keyboard-layout" "keyboards" "thunar" "thunar-volman" "xfce4-appfinder" )
  declare -a schemaArray2=("xfce4-desktop" "xfce4-keyboard-shortcuts" "xfce4-mime-settings" )
  declare -a schemaArray3=("xfce4-mixer" "xfce4-notifyd" "xfce4-panel" "xfce4-power-manager" )
  declare -a schemaArray4=("xfce4-session" "xfce4-settings-editor" "xfce4-settings-manager" "xfce4-xfwm4" "xfce4-xsettings" )

  for key in "${!schemaArray1[@]}"
  do
    schema=${schemaArray1[$key]}   #printf "Key for schemaArray1 array is: $key \n"
    show_xfconf_schema "$schema"
  done

  for key in "${!schemaArray2[@]}"
  do
    schema=${schemaArray2[$key]}
    show_xfconf_schema "$schema"
  done

  for key in "${!schemaArray3[@]}"
  do
    schema=${schemaArray3[$key]}
    show_xfconf_schema "$schema"
  done

  for key in "${!schemaArray4[@]}"
  do
    schema=${schemaArray4[$key]}
    show_xfconf_schema "$schema"
  done

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



mod_backdrop() {
  screen_no="$1"
  monitor_no="$2"
  the_args="$3"

}

main_settings() {
  printf "=== HOST NAME CTL ===\n"
  hostnamectl

  printf "\n=== screenfetch + neofetch ===\n"
  screen_info


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

  printf "\nXCONF - SCHEMAS\n"
  list_xfconf_schemas



  get_xfconf_property "xfce4-desktop" "/backdrop/screen0/monitor0/brightness" # was 0

  get_xfconf_property "$xfcedesk" "$MON_DP0"
  #set_xfconf_property "$xfcedesk" "$MON_DP0" "$new_back"
  #get_xfconf_property "$xfcedesk" "$MON_DP0"


  #reset_xfconf_property "$xfcedesk" "$sc0mon0_imgpath"
  #reset_xfconf_property "$xfcedesk" "$sc0mon0_lastimg"
  #reset_xfconf_property "$xfcedesk" "$sc0mon0_lastsingimg"

  #reset_xfconf_property "$xfcedesk" "$sc0mon1_imgpath"
  #reset_xfconf_property "$xfcedesk" "$sc0mon1_lastimg"
  #reset_xfconf_property "$xfcedesk" "$sc0mon1_lastsingimg"



  get_xfconf='xfconf-query -c SCHEMA -p PROPERTY '
  set_xfconf='xfconf-query -c SCHEMA -p PROPERTY -s VALUE '
  printf "GET XFCONF\t${get_xfconf}\n"
  printf "SET XFCONF\t${set_xfconf}\n"

}

show_all_schema_keys() {
  #schemas=$(/usr/bin/gsettings list-schemas)
  #printf "\nSCHEMAS\n${schemas}\n\n"
  printf "\nSCHEMAS\n"
  /usr/bin/gsettings list-schemas

  #schema_keys=$(/usr/bin/gsettings list-recursively)
  #printf "\n\nSCHEMA-KEYS\n${schema_keys}\n"
  printf "\n\nSCHEMA-KEYS\n"
  /usr/bin/gsettings list-recursively
}

show_gsettings() {
  deskt="$1"
  printf "\nDESKTOP - gsettings\n"
  show_gsettings_syntax
  #dtop='cinnamon'
  if [ "$deskt" == 'cinnamon' ]
  then
    dtop="$1"
  else
    dtop='gnome'
  fi
  printf "Desktop=${deskt} ; URIComponent=${dtop}\n"
  DISP='export DISPLAY=:0 '
  show_schema "org.${dtop}.desktop.screensaver"
  show_schema "org.${dtop}.desktop.session""

  show_schema "org.gtk.Settings.FileChooser"
  show_schema "org.${dtop}.org.gtk.gtk4.Settings.FileChooser"

  show_schema "com.linuxmint.mintmenu.plugins.places"
  show_schema "com.linuxmint.mintmenu.plugins.system_management"
  show_schema "org.${dtop}.desktop.interface""

  show_schema "org.nemo.preferences"

  # Now sound related
  show_schema "org.${dtop}.desktop.sound"
  show_schema "org.${dtop}.sounds"
  show_schema "org.gnome.desktop.sound"

}

show_nemo() {
  nemo_data=$(/usr/bin/cat ~/.config/nemo/desktop-metadata)
  printf "\n\nNEMO - ${nemo_data}\n"
}

show_gsettings_syntax() {
  get_syntax='gsettings get <schema> <keyName> '
  set_syntax='gsettings set <schema> <keyName> <value>'
  printf "Syntax:\n\t${get_syntax}\n\t${set_syntax}\n\n"
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
  #dtop='cinnamon'
  deskt="$1"
  if [ "$deskt" == 'cinnamon' ]
  then
    dtop="$1"
  else
    dtop='gnome'
  fi
  printf "\n${DIVIDER_SECTION}\nGSETTINGS\n"

  # desktop backdrop image

  # single click

  # =======
  printf "Desktop=${deskt} ; URIComponent=${dtop}\n"
  show_gsettings_syntax

  check_gkey "org.${dtop}.desktop.session" 'idle-delay' 'uint32 0'
  check_gkey "org.${dtop}.desktop.screensaver" 'idle-activation-enabled' 'false'
  check_gkey "org.${dtop}.desktop.screensaver" 'lock-enabled' 'false'

  # cinnamon only
  check_gkey "org.cinnamon.desktop.interface" 'gtk-overlay-scrollbars' 'false'

  # valid - but ineffective
  check_gkey "org.${dtop}.desktop.background" 'picture-uri' "'file:///usr/share/backgrounds/linuxmint/sele_ring_center_green.jpg'" # orig 'file:///usr/share/backgrounds/linuxmint/default_background.jpg'

  # The following has wrong value
  check_gkey "com.linuxmint.mintmenu.plugins.system_management" 'allow-scrollbar' 'false'
  check_gkey "org.nemo.preferences" 'click-policy' "'single'"

  # The following fail on xfce
  check_gkey "com.linuxmint.mintmenu.plugins.places" 'allow-scrollbar' 'false'

}

show_lightdm_settings() {
  printf "\n${DIVIDER_SECTION}\nLIGHTDM CONFIG - ${LIGHTDM_CONF} ${LIGHTDM_DIR}\n"

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
  printf "\n${DIVIDER_SECTION}\nLIGHTDM SETTINGS\n"
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
  printf "\n${DIVIDER_SECTION}\nXSET SETTINGS\n${xset_config}\n\n"
}

check_xset() {
  xset_config=$(export DISPLAY=:0 ; /usr/bin/xset q)
  printf "\n${DIVIDER_SECTION}\nXSET SETTINGS\n${xset_config}\n\n"
}

do_show() {
  dsk="$1"
  main_settings 2>&1 | tee -a $op
  show_all_schema_keys 2>&1 | tee -a $op

  show_gsettings ${dsk} 2>&1 | tee -a $op
  show_lightdm_settings 2>&1 | tee -a $op
  show_xset 2>&1 | tee -a $op
  show_nemo 2>&1 | tee -a $op
  printf "\n\nSOUND\n" 2>&1 | tee -a $op
  /home/robert/.simpli/utils/sound_control.sh list 2>&1 | tee -a $op
  get_xfconf_property "$xfcedesk" "$MON_DP0"  2>&1 | tee -a $op
}

do_check() {
  dsk="$1"
  check_gsettings ${desktop} 2>&1 | tee -a $op
  check_lightdm_settings 2>&1 | tee -a $op
  check_xset 2>&1 | tee -a $op

  check_xfconf_property "$xfcedesk" "$MON_DP0" "$new_back" 2>&1 | tee -a $op
}

do_set() {
  # change the screen backdrop


  set_xfconf_property   "$xfcedesk" "$BACKDROP_IMAGE_KEY" "$BACKDROP_MOUNTAIN_IMAGE"
  check_xfconf_property   "$xfcedesk" "$BACKDROP_IMAGE_KEY" "$BACKDROP_MOUNTAIN_IMAGE"

  #set_xfconf_property   "$xfcedesk" "$MON_DP0" "$new_back"
  #check_xfconf_property "$xfcedesk" "$MON_DP0" "$new_back"

  set_xfconf_property   "$xfcedesk" "$SINGLE_CLICK" "true"
  check_xfconf_property "$xfcedesk" "$SINGLE_CLICK" "true"

  set_xfconf_property   "$xfcedesk" "$ICON_FONT_SIZE_KEY" "$ICON_FONT_SIZE_BIG"
  check_xfconf_property   "$xfcedesk" "$ICON_FONT_SIZE_KEY" "$ICON_FONT_SIZE_BIG"

  set_xfconf_property   "$xfcedesk" "$ICON_SIZE_KEY" "$ICON_SIZE_VALUE_BIG"
  check_xfconf_property "$xfcedesk" "$ICON_SIZE_KEY" "$ICON_SIZE_VALUE_BIG"


  # make scroll bar permanently visible
  # see Disable scrollbar overlay in XFCE? (past posted solutions do not work)
  # https://forum.xfce.org/viewtopic.php?id=16062
  #get_gkey 'org.gnome.desktop.interface' 'overlay-scrolling'
  #mod_gkey 'org.gnome.desktop.interface' 'overlay-scrolling' false # only impacts terminal



}

do_reset() {
  reset_xfconf_property "$xfcedesk" "$MON_DP0"
  get_xfconf_property "$xfcedesk" "$MON_DP0"
}

if [ "$#" = "0" ]
then
  printf "Syntax is \n\tenv_config   ${COMMANDS_SYNTAX} \nwhere\t${COMMANDS_DESC}\n"
  exit 1
fi

cmd="$1"
desktop="xfce"

avail_verbs=("show" "check" "set" "reset")

#if [ $cmd == "show" -o $cmd == "check" -o $cmd == "set" ]
if [[ ${avail_verbs[@]} =~ $cmd ]]
then
  op="${dest_dir}/${node}_${NOW}_${cmd}.txt"
  printf "COMMAND = ${cmd}\n${NOW}\n" 2>&1 | tee -a $op
else
  printf "Invalid command argument\n"
  #op="${dest_dir}/${node}_${NOW}.txt"
  exit 88
fi

#if [ "$desktop" == "xfce" ]; then
#  printf "DESKTOP = ${desktop}\n" 2>&1 | tee -a $op
#else
#  printf "Invalid (non-existant or unknown) desktop argument\n"
#fi

this_perm="${dest_dir}/${cmd}.txt"

if [ -L "${this_perm}" ]
then
  printf "Info: Removing perma link ${this_perm}\n"
  rm -f "${this_perm}"
fi

running_as=$(/usr/bin/whoami)
printf "USER = ${running_as}\n" 2>&1 | tee -a $op
printf "DESKTOP = ${desktop}\n" 2>&1 | tee -a $op

if [ "$cmd" == 'show' ]
then
  do_show "${desktop}"

elif [ "$cmd" == 'check' ]
then
  do_check "${desktop}"

elif [ "$cmd" == 'set' ]
then
  do_set

elif [ "$cmd" == 'reset' ]
then
  do_reset

else
  printf "Invalid command argument\n"
  printf "Valid commands are:${COMMANDS_DESC}\n"
  exit 2
fi

printf "\n\nOutput destination = ${op}\n"
/usr/bin/chmod 444 "${op}"
#rm -f "${this_perm}"
/usr/bin/ln -s "${op}" "${this_perm}"
printf "\nUpdated perma-link  ${this_perm}  to point to ${op}\n"

printf "\nEND \n\n"