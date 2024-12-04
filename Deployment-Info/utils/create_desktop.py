import os.path
import platform
import psutil
#import re
import sys
import yaml
#from pathlib import Path
#from getmac import get_mac_address as gma

from jinja2 import Environment, FileSystemLoader


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

def get_dir_and_file(the_template):
    base_file = os.path.basename(the_template)
    dir_path = os.path.dirname(the_template)
    print(f'BASE={base_file}\nDIR={dir_path}\n')
    return (dir_path, base_file)

def generate_from_template(temp, var_struct, filename):
    print(f'Generating template: {filename}')
    content = temp.render(
        var_struct
    )
    with open(filename, mode="w", encoding="utf-8") as message:
        message.write(content)
        print(f"... Created {filename}")
        os.chmod(filename, 0o755)


def derive_zoom_desktops(template_file, yaml_source_data, dest_dir, display_name):
    device_id = get_device_id()

    with open(yaml_source_data) as stream:
        try:
            data_struct = yaml.safe_load(stream)
            # print(yaml.safe_load(stream))
            # print(data_struct['zoom'])

        except yaml.YAMLError as exc:
            print(exc)

    # Generate dynamic desktop icons
    (dirpath, basefile) = get_dir_and_file(template_file)
    environment = Environment(loader=FileSystemLoader(dirpath))
    template = environment.get_template(basefile)

    zoom_data = data_struct['zoom']

    for info_struct in zoom_data:

        item = info_struct
        fname = f"{dest_dir}/{item['entry']}.desktop"
        generate_from_template(template, info_struct, fname )


def derive_info_desktop(info_template_file, dest_dir):
    (dirpath2, basefile2) = get_dir_and_file(info_template_file)
    environment = Environment(loader=FileSystemLoader(dirpath2))
    template2 = environment.get_template(basefile2)
    src_info_file = f"{dirpath2}/dev-info.txt"
    info_struct = { 'description': 'Simpli Information',
                    'icon': 'zoom',
                    'comment': 'This contains info useful for diagnostics',
                    'info_file': src_info_file}
    op_desktop_filename = f"{dest_dir}/info.desktop"
    generate_from_template(template2, info_struct, op_desktop_filename)



def main():
    print('IN MAIN\n')
    cmndline_args = sys.argv[1:]
    if len(cmndline_args) != 4:
        show_syntax()
        exit_msg(1, 'Invalid number of args')

    template_file = cmndline_args[0]
    yaml_source_data = cmndline_args[1]
    dest_dir = cmndline_args[2]
    display_name = cmndline_args[3]

    os.path.isfile(template_file)
    if not os.path.isfile(template_file):
        exit_msg(2, 'Template file specified is not valid')
    elif not os.path.isfile(yaml_source_data):
        exit_msg(3, 'Data file specified is not valid')
    elif not os.path.isdir(dest_dir):
        exit_msg(4, 'Destination dir does not exist')

    #display_is_valid = bool(re.match('[a-zA-Z\s]+$', display_name))
    display_is_valid = display_name != '' and all(chr.isalpha() or chr.isspace() for chr in display_name)
    if not display_is_valid:
        exit_msg(5, 'Display name contains non valid characters')

    # derive desktop files for all zoom entries
    derive_zoom_desktops(template_file, yaml_source_data, dest_dir, display_name)

    # now derive the desktop for the info
    (dirpath, basefile) = get_dir_and_file(template_file) # assume the info template is in the same dir as the zoom
    INFO_TEMPLATE = 'template_info.desktop'
    info_template_file = dirpath + '/' + INFO_TEMPLATE
    derive_info_desktop(info_template_file, dest_dir)



if __name__ == "__main__":
    main()