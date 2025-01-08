#!/usr/bin/bash

# Pulls down the anydesk binaries (approx 8MB each)
# We do this because we are trying to avoid putting the binaries into GIT

TOOL_NAME='anydesk'
ROOT_URL='https://download.anydesk.com'

VERSION='6.4.0-1'

OS_X64='linux'
ARCH_X64='amd64'

OS_ARM='rpi'
ARCH_ARM='arm64'

FORMAT='deb'

# RASPBERRY PI DOWNLOAD LINK : https://download.anydesk.com/rpi/anydesk_6.4.0-1_arm64.deb
# X64 DOWNLOAD LINK : https://download.anydesk.com/linux/anydesk_6.4.0-1_amd64.deb.sum

get_binary() {
	vers="$1"
	my_os="$2"
	archy="$3"
	formy="$4"

	printf "Obtaining binary of anydesk for OS=${my_os} , ARCH=${archy} , with EXTENSION=${formy}\n\n"
fname="${TOOL_NAME}_${vers}_${archy}.${formy}"
sumfname="${fname}.sum"


rm ${sumfname} 
sum_cmd="curl -o ${sumfname} ${ROOT_URL}/${my_os}/${sumfname}" 
#printf "Obtaining sumfile using: ${sum_cmd}\n"

printf "========================================\n"
sum_op=$( ${sum_cmd} )

printf "........................................\n"

rm ${fname} 
bin_cmd="curl -o ${fname} ${ROOT_URL}/${my_os}/${fname}"
printf "Obtaining bin file using: ${bin_cmd}\n\n"
bin_op=$( ${bin_cmd} )

printf "========================================\n"
the_sum_line=$(/usr/bin/md5sum ${fname} )
#printf "CALCULATED SUM LINE >>${the_sum_line}<< \n"
the_sum=$(echo ${the_sum_line} | cut -d " " -f 1 )
#printf "CALC ${the_sum} \n"


given_md5_line=$(grep md5 ${sumfname} )
#printf "MD5LINE == ${given_md5_line}\n"

given_md5=$(echo ${given_md5_line} | cut -d " " -f 3 )
#printf "GIVEN MD5 == ${given_md5}\n"

the_size=$(ls -lh ${fname} | cut -d " " -f 5 )
if [ "${the_sum}" != "${given_md5}" ]
then
	printf "Incorrect checksum on downloaded of  '${archy}'  binary as file    ${fname} of size ${the_size}\n"
	printf "MD5 CHECKSUM: CALCULATED == ${the_sum}  , GIVEN == ${given_md5}\n"
	printf "\n\n"
	return 22
else
	printf "Successfully downloaded the  '${archy}'  binary as file    ${fname} of size ${the_size}\n\n\n"
	return 0
fi
}

get_binary "$VERSION" "$OS_X64" "$ARCH_X64" "$FORMAT"
get_binary "$VERSION" "$OS_ARM" "$ARCH_ARM" "$FORMAT"

# https://anydesk.com/en-gb/downloads/thank-you?dv=raspberrypi


printf "\nEND\n"
exit 0




