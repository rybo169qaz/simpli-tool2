import os
import subprocess
import shutil
import test_data
import prepare_qr

BASH_TOOL_CMD = "play.sh"
DEST_DIR = "../Input-Images"
SRC_DIR = "GenQR"

TOOL_CMD = './' + BASH_TOOL_CMD

print(f'Testing QR invocation')


def do_test():
    for entry in test_data.full_test_known:
        (wellknown, type_info, describe) = entry

        print(f'')
        qr_file = wellknown + ".qr"
        srcfile = SRC_DIR + "/" + qr_file
        destfile = DEST_DIR + "/" + qr_file

        print(f'Checking src {srcfile}')
        if os.path.isfile(srcfile):
            print(f'\tSource file exists')
        else:
            print(f'\tSource file does NOT exist ({srcfile})')
            exit(7)

        print(f'Checking dest {destfile}')
        if os.path.isfile(destfile):
            print(f'\tDest file exists')
            print(f'Removing {destfile}')
            os.remove(destfile)
        else:
            print(f'\tDest file does NOT exist ')

        print(f'Copy file {srcfile:60} to : {destfile:60}')
        shutil.copy2(srcfile, destfile)

        if not os.path.isfile(destfile):
            print(f'\tDest file does not exist must haved to copy')
            exit(8)

    os.chdir("../MySimpleApp")

    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for f in files:
        print(f'File: {f}')

    for entry in test_data.full_test_known:
        (wellknown, type_info, describe) = entry
        print(f'\nQR test of {wellknown:30} which is : {type_info:12} Expected o/p: {describe}')

        qr_file = wellknown + ".qr"
        comlist = ["select", "-f", "qr", "-q", qr_file]
        com_data = [TOOL_CMD] + comlist
        print(f'Attempt to subproceess.run: {com_data}')

        comstring = " ".join(comlist)
        print(f'String to use when manually invoking: {comstring}')

        capture_info = False if type_info == 'text' else True
        result = subprocess.run(com_data, capture_output=capture_info, text=True)


def test_qr():
    prepare_qr.prepare_qr_set()
    do_test()


if __name__ == "__main__":
    test_qr()
