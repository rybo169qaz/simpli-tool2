#!/usr/bin/bash

dest_dir='/home/robert/.simpli/logs'
node=$(/usr/bin/uname -n)

NOW=$( date '+%F_%H-%M-%S' )

op="${dest_dir}/${node}_${NOW}.txt"

printf "Output destination = ${op}\n"
#
printf "=== HOST NAME CTL ===\n"
hostnamectl | tee -a $op

printf "\n=== screenfetch ===\n"
screenfetch | tee -a $op

printf "\nDesktop: $XDG_CURRENT_DESKTOP"
if [[ "$XDG_CURRENT_DESKTOP" == 'X-Cinnamon' ]]
then
  config_details=$(lightdm --show-config)
  printf "\nCONFIG DETAILS:\n${config_details}\n\n"  | tee -a $op
fi

printf "\nDisplay server: $XDG_SESSION_TYPE" | tee -a $op

printf "\nDISK SPACE\n"
/usr/bin/df -kh | tee -a $op

printf "\nSOUND - PACTL\n"
pactl list sinks | grep "Sink #" | tee -a $op

printf "\nDESKTOP - gsettings\n"
schemas=$(/usr/bin/gsettings list-schemas)
printf "SCHEMAS\n${schemas}\n\n" | tee -a $op

DISP='export DISPLAY=:0 '

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

show_schema 'org.cinnamon.desktop.screensaver'
show_schema 'org.cinnamon.desktop.session'



printf "\nEND \t${NOW}\n\n" | tee -a $op