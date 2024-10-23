#!/bin/bash

printf "%0.s\n" {1..3}
printf "%0.sv" {1..40}

THIS_SCRIPT=$(basename "$0")
printf "\nThis script\t: ${THIS_SCRIPT}\n"

the_cwd=$(pwd)
printf "Invoked from dir\t: ${the_cwd}\n"

# the directory this script is in
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cd ${SCRIPT_DIR}

new_cwd=$(pwd)
printf "Now running in dir\t: ${new_cwd}\n"

tool="python3 pyplay/startplay.py"

printf "ARG COUNT = $# \n"
printf "ARGS: "
#printf "ARGS = $@ \n"
for i in $*; do
  printf "%s " "$i"
done
printf "\n"
desc="Process given args"
if [ $# == 0 ]
then
  cat << BLOCK
  syntax
     <NULL>                : This help info
     PKGFILE               : shortcut to package the python project as a file
     PKGDIR                : shortcut to package the python project as a directory
     CREATEQR              : Creates QR code. Syntax is
                             CREATEQR <op-filename> <data-string>                    (data-string being in quotes)
     repl                  : Reads and processes commands using a REPL

     ----------------------- TEST MEDIA SHORTCUTS -------------------------------------------------
     TT                    : shortcut to play some TEST TEXT                 (select             -u testproverbs )

     TAC                   : shortcut to play some TEST AUDIO using CHROMIUM (select -p chromium -u testcountingaudio )
     TAF                   : shortcut to play some TEST AUDIO using FFMPEG   (select -p ffmpeg   -u testcountingaudio )
     TAV                   : shortcut to play some TEST AUDIO using VLC      (select -p vlc      -u testcountingaudio )

     TVC                   : shortcut to play some TEST VIDEO using CHROMIUM (select -p chromium -u testvideo )
     TVF                   : shortcut to play some TEST VIDEO using FFMPEG   (select -p ffmpeg   -u testvideo )
     TVV                   : shortcut to play some TEST VIDEO using VLC      (select -p vlc      -u testvideo )
     TVS                   : shortcut to play some TEST VIDEO using default player  (select media -w testsilentvideo )

     everything else       : passed through to the play tool
                             (use  'help'   argument to get help of syntax )

BLOCK
  exit 0
else
  if [ $1 == 'PKGFILE' ]
  then
    generated_artifact='dist/pkgfile'
    rm ${generated_artifact}
    source make_file_pkg
    printf "Finished packaging into a file: ${generated_artifact} \nExecute ${generated_artifact}\n"
    exit 0

  elif [ $1 == 'PKGDIR' ]
  then
    source make_dir_pkg
    printf "Finished packaging into a dir: dist/dir-package \nExecute dist/dir-package/dir-package\n"
    exit 0

  elif [ $1 == 'CREATEQR' ]
  then
    if [ $# != 3 ]
    then
      printf "\nError - arguments missing.\nsyntax is: <op-filename> <data-string>\n"
      exit 1
    fi

    qr_file="${2}.png"
    qr_info="$3"

    source ../create_qr "$qr_file" "$qr_info"
    printf "\nFinished creating QR code in file '${qr_file}' containing info >>${qr_info}<<\n"
    exit 0



  elif [ $1 == 'TT' ]
  then
    required_action="select -k testproverbs "

  elif [ $1 == 'TAC' ]
  then
    required_action="select -p chromium -k testcountingaudio "
  elif [ $1 == 'TAF' ]
  then
    required_action="select -p ffmpeg -k testcountingaudio "
  elif [ $1 == 'TAV' ]
  then
    required_action="select -p vlc -k testcountingaudio "


  elif [ $1 == 'TVC' ]
  then
    required_action="select -p chromium -k testvideo "
  elif [ $1 == 'TVF' ]
  then
    required_action="select -p ffmpeg -k testvideo "
  elif [ $1 == 'TVV' ]
  then
    required_action="select -p vlc -k testvideo "
  elif [ $1 == 'TVS' ]
  then
    required_action="select media -w testsilentvideo  "

  else
    required_action="$@ "
  fi

  thecmd="$tool ${required_action} "
  printf "${desc} \n"
  printf "Will invoke with\t: ${thecmd}\n"
  printf "Passing over to python\n"
  printf "%0.s#" {1..40}
  printf "\n"
  bash <(echo "$thecmd")
fi


exit 0


