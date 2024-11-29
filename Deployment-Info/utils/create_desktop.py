import os.path
import platform
import psutil
import re
import sys
import yaml
#from pathlib import Path
#from getmac import get_mac_address as gma

from jinja2 import Environment, FileSystemLoader

TOOL_CMD = 'simpli-zoom grosv'
TEMPLATE_DIR = '/home/robert/utils'
TEMPLATE_FILE = 'template_zoom.desktop'

def show_syntax():
    print(f'Args:   <template> <config_data> <dest_dir> <displayName>\n')

def exit_msg(code, text):
    print(f'Error ({code}): {text}\n')
    show_syntax()
    exit(code)

def get_mac():
    my_mac = None
    for interface in psutil.net_if_addrs():
        # Check if the interface has a valid MAC address
        if psutil.net_if_addrs()[interface][0].address:
            # Print the MAC address for the interface
            my_mac = psutil.net_if_addrs()[interface][0].address
            print(f'MAC {my_mac}')
            break
    return my_mac

def get_network_physical_address(netInterfaceName):
  nics = psutil.net_if_addrs()
  macAddress = ([j.address for i in nics for j in nics[i] if i==netInterfaceName and j.family==psutil.AF_LINK])[0]
  return macAddress.replace('-',':')

def get_device_id():
    #full_mac = gma()
    #mac_comp = full_mac.split(':')
    #dev_id = mac_comp[4] + mac_comp[5] + '_' + platform.node()

    #full_mac = get_mac()

    if_name = 'enp1s0'
    full_mac = get_network_physical_address(if_name)

    dev_id = full_mac + '_' + platform.node()
    print(f'DEV_ID = {dev_id}')
    return dev_id


def main():
    print('IN MAIN\n')
    cmndline_args = sys.argv[1:]
    if len(cmndline_args) != 4:
        exit_msg(1, 'Invalid number of args')
    # for i in cmndline_args:
    #     print(f'X {i}\n')



    template_file = cmndline_args[0]
    source_data = cmndline_args[1]
    dest_dir = cmndline_args[2]
    display_name = cmndline_args[3]

    os.path.isfile(template_file)
    if not os.path.isfile(template_file):
        exit_msg(2, 'Template file specified is not valid')
    elif not os.path.isfile(source_data):
        exit_msg(3, 'Data file specified is not valid')
    elif not os.path.isdir(dest_dir):
        exit_msg(4, 'Destination dir does not exist')

    #display_is_valid = bool(re.match('[a-zA-Z\s]+$', display_name))
    display_is_valid = display_name != '' and all(chr.isalpha() or chr.isspace() for chr in display_name)

    basefile = os.path.basename(template_file)
    dirpath = os.path.dirname(template_file)
    print(f'BASE={basefile}\nDIR={dirpath}\n')

    if not display_is_valid:
        exit_msg(5, 'Display name contains non valid characters')

    device_id = get_device_id()

    students = [
        {"name": "Sandrine", "score": 100},
        {"name": "Gergeley", "score": 87},
        {"name": "Frieda", "score": 92},
    ]

    with open(source_data) as stream:
        try:
            data_struct = yaml.safe_load(stream)
            #print(yaml.safe_load(stream))
            #print(data_struct['zoom'])

        except yaml.YAMLError as exc:
            print(exc)

    environment = Environment(loader=FileSystemLoader(dirpath))
    template = environment.get_template(basefile)

    name_packer = '_' + device_id
    for item in data_struct['zoom']:
        #print(str(entry))
        #my_ent = str(entry['entry'])
        #my_desc = str(entry['description'])
        item['devid'] = name_packer

        #print(f'ENTRY={my_ent}, DESC={my_desc}\n')
        filename = f"{dest_dir}/{item['entry']}.desktop"
        content = template.render(
            item
        )
        with open(filename, mode="w", encoding="utf-8") as message:
            message.write(content)
            print(f"... Created {filename}")
            os.chmod(filename, 0o755)



if __name__ == "__main__":
    main()