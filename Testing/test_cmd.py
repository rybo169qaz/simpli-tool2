import os
import subprocess
import test_data

BASH_TOOL_CMD = "play.sh"
TOOL_CMD = './' + BASH_TOOL_CMD

print(f'Testing commandline invocation')

os.chdir("../MySimpleApp")

for entry in test_data.full_test_known:
    (wellknown, type_info, describe) = entry
    print(f'\nCommandline test of {wellknown:30} which is : {type_info:12} Expected o/p: {describe}')

    comlist = ["select", "-f", "cmdstr", "-k", wellknown]
    com_data = [TOOL_CMD] + comlist
    print(f'Attempt to subproceess.run: {com_data}')

    comstring = " ".join(comlist)
    print(f'String to use when manually invoking: {comstring}')
    capture_info = False if type_info == 'text' else True
    result = subprocess.run(com_data, capture_output=capture_info, text=True)
