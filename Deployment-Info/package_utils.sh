#!/bin/bash

printf "%0.s\n" {1..3}
printf "%0.sv" {1..40}

THIS_SCRIPT=$(basename "$0")
printf "\nThis script\t: ${THIS_SCRIPT}\n"

the_cwd=$(pwd)
printf "Invoked from dir\t: ${the_cwd}\n"

# the directory this script is in
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )


show_help() {
  cat << BLOCK
  syntax
     <NULL>               : This help info
     CREATE_UTILS_PKGFILE : shortcut to package the create_desktop_icons utility as a file
     CREATE_UTILS_PKGDIR  : shortcut to package the create_desktop_icons utility as a directory
BLOCK
  }


cd ${SCRIPT_DIR}

new_cwd=$(pwd)
printf "Now running in dir\t: ${new_cwd}\n"

tool="python3 create_desktop_icons.py"

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
  show_help
  exit 0
else
  if [ $1 == 'CREATE_UTILS_PKGFILE' ]
  then
    printf "DOING NOTHING"
    exit 0
    generated_artifact='dist/pkgfile'
    rm ${generated_artifact}
    source make_file_pkg
    printf "Finished packaging into a file: ${generated_artifact} \nExecute ${generated_artifact}\n"
    exit 0

  elif [ $1 == 'CREATE_UTILS_PKGDIR' ]
  then
    # Note that this tool ONLY calls the create_desktop_icons tool
    source package_create_desktop_icons
    printf "BASH: Finished packaging into a dir: dist/dir-package \n"
    printf "BASH: Execute dist/dir-package/dir-package\n"
    exit 0

  else
    printf "Unknown option."
    show_help
    exit 1
  fi
fi

exit 0



}