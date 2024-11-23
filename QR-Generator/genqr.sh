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

PY_TOOL_DIR='gen-qr-python'
PYTOOL='create_qr_img.py'
tool="python3 ${PY_TOOL_DIR}/${PYTOOL}"

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

     everything else       : passed through to the tool

BLOCK
  exit 0

else
  if [ $# != 3 ]
  then
    printf "\nError - arguments missing.\nsyntax is: genpng -f <dest-filename> '<string>''\n"
    exit 99
  fi
  dest_file="$2"
  the_string="$3"
  required_action="genpng -f ${dest_file}} ${the_string}"

  thecmd="$tool ${required_action} "
  printf "${desc} \n"
  printf "Will invoke with\t: ${thecmd}\n"
  printf "Passing over to python\n"
  printf "%0.s#" {1..40}
  printf "\n"
  bash <(echo "$thecmd")
fi


exit 0


