import os
import subprocess
import test_data
import make_qr

DEST_DIR = 'GenQR'


def format_info(wellknown, embedded, qr_invoke):
    resp = "{:<30.30} : {:<45.45} : {:<55.55}\n".format(wellknown, embedded, qr_invoke)
    return resp


def prepare_qr_set():
    print(f'Preparing QR codes for Testing QR control')
    info_file = DEST_DIR + '/' + 'info.txt'
    if os.path.isfile(info_file):
        print(f'\tDest file exists. Removing')
        os.remove(info_file)
        if os.path.isfile(info_file):
            print(f'Failed to remove info file - exiting ({info_file})')
            exit(1)

    # create the header for the info file
    info_file_handle = open(info_file, 'a')
    the_line = format_info('Well-known name ', 'Text embedded in the QR code', 'How to invoke with the QR file')
    info_file_handle.write(the_line)
    packer = '=' * 50
    info_file_handle.write(format_info(packer, packer, packer))

    for entry in test_data.full_test_known:
        (wellknown, type_info, describe) = entry
        print(f'\nCommandline test of {wellknown:30} which is : {type_info:12} Expected o/p: {describe}')
        qr_file = wellknown + ".qr"
        qr_filename = DEST_DIR + '/' + qr_file

        embedded_command = 'select --known ' + wellknown
        embedded_command = 'select -w ' + wellknown

        #qr_command = "select --format qr -q " + qr_file
        qr_command = "NONE"


        print(f'using the python module')
        make_qr.make_qr_file(embedded_command, qr_filename)

        print(f'File written == {qr_filename}')
        print(f'File contains >>{embedded_command}<<')

        the_line = format_info(wellknown, embedded_command, qr_command)
        info_file_handle.write(the_line)

    info_file_handle.close()


if __name__ == "__main__":
    prepare_qr_set()
