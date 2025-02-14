#!/usr/bin/bash

# Runs the
# args
# tool {{ simpli_utils_dir }}/create_desktop_icons.py
#1 {{ simpli_config_dir }}/template.desktop
#2 {{ simpli_config_dir }}/desktop_known.yml
#3 {{ desktop_dir }}
#4 {{ clients[inventory_hostname].desktop }}

USERNAME='simp'
myscript='create_desktop_icons.py'
my_home="/home/${USERNAME}"
simpli_utils_dir="${my_home}/.simpli/utils"
simpli_config_dir="${my_home}/.simpli/config"


#desktop_dir="${my_home}/Desktop"
desktop_dir="${my_home}/xDesktop"


hostname='wyse-9'

py='python3' # /usr/bin/python3
tool="${simpli_utils_dir}/${myscript}"
desktop_type='xfce'

fullcmd="$py $tool ${simpli_config_dir}/template.desktop ${simpli_config_dir}/desktop_known.yml $desktop_dir $desktop_type"

# ORIG /usr/bin/python3 {{ simpli_utils_dir }}/create_desktop_icons.py {{ simpli_config_dir }}/template.desktop {{ simpli_config_dir }}/desktop_known.yml {{ desktop_dir }} {{ clients[inventory_hostname].desktop }}

printf "About to execute: \n${fullcmd}\n"

bash <(echo "${fullcmd}")

printf "\nEND desktest\n"