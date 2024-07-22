#!/bin/sh

printf "STARTING SCRIPT\n"
guvtool='/usr/bin/guvcview'

printf "STARTING guvcview\n"
#${guvtool} --verbosity=2 --gui=none  &
#${guvtool} --verbosity=2  &
${guvtool} --verbosity=2 --image=snap --photo_timer=5 &

printf "ENDING SCRIPT\n"

