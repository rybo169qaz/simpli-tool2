#!/usr/bin/bash

# Sets desktop config
TOOL_FUNC='dsk_conf'



dest_dir='/home/robert/.simpli/logs'
node=$(/usr/bin/uname -n)

NOW=$( date '+%F_%H-%M-%S' )

op="${dest_dir}/${node}_${TOOL_FUNC}.txt"
printf "Output destination = ${op}\n"

GSET='/usr/bin/gsettings'


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

mod_gkey 'org.cinnamon.desktop.session' 'idle-delay' "0"
mod_gkey 'org.cinnamon.desktop.screensaver' 'idle-activation-enabled' 'false'
mod_gkey 'org.cinnamon.desktop.screensaver' 'lock-enabled' 'false'

service lightdm restart

exit 0
