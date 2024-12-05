import os.path
import platform
import psutil
#import re
import sys
import yaml
#from pathlib import Path
#from getmac import get_mac_address as gma

from jinja2 import Environment, FileSystemLoader

SIMPLI_PREFIX = 'simpli'

def show_syntax():
    print(f'Syntax : Args ==  <template_desktop_file> <config_data> <dest_dir> <displayName>\n')

def show_help():
    info = """    This utility takea template file (using jinja syntax), together 
    with a yaml config file and generates a desktop file for each entry. 
    The config of each generated desktop file is based upon the values in the config file.  
    Note: It can be run on controller or client, however only the client is configured with 
    the requisite python modules.
    """
    print(f'\nTool info:\n{info}\n')

def exit_msg(code, text):
    if code != 0:
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
    print(f'Generating template_desktop_file: {filename}')
    content = temp.render(
        var_struct
    )
    with open(filename, mode="w", encoding="utf-8") as message:
        message.write(content)
        print(f"... Created {filename}")
        os.chmod(filename, 0o755)

def derive_desktop_category(category_data, dest_dir, template_desktop_file):
    common_data = dict()
    common_data['tool_command'] = category_data['tool_command']
    common_data['desktop_categories'] = category_data['desktop_categories']
    common_data['desktop_kde_protocols'] = category_data['desktop_kde_protocols']
    common_data['desktop_keywords'] = category_data['desktop_keywords']

    zoom_entries = category_data['entries']
    for info_struct in zoom_entries:
        if info_struct['enabled'] == 'true':
            new_struct = dict()

            # inherit the common attributes
            for key, value in common_data.items():
                new_struct[key] = value

            # configure the specific attributes (this allows overriding)
            for key2, value2 in info_struct.items():
                new_struct[key2] = value2

            fname = f"{dest_dir}/{SIMPLI_PREFIX}_{new_struct['entry']}.desktop"
            generate_from_template(template_desktop_file, new_struct, fname)


def derive_all_desktops(template_file, yaml_source_data, dest_dir, display_name):
    device_id = get_device_id()

    with open(yaml_source_data) as stream:
        try:
            data_struct = yaml.safe_load(stream)
            # print(yaml.safe_load(stream))
            # print(data_struct['zoom'])

        except yaml.YAMLError as exc:
            print(exc)

    # Obtain the overall template
    (dirpath, basefile) = get_dir_and_file(template_file)
    environment = Environment(loader=FileSystemLoader(dirpath))
    template = environment.get_template(basefile)

    derive_desktop_category(data_struct['zoom'], dest_dir, template)
    derive_desktop_category(data_struct['browser'], dest_dir, template)
    derive_desktop_category(data_struct['video'], dest_dir, template)
    derive_desktop_category(data_struct['platform'], dest_dir, template)


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
    cmndline_args = sys.argv[1:]

    if cmndline_args[0] == '-h' or cmndline_args[0] == '--help':
        show_help()
        show_syntax()
        exit_msg(0, '')

    if len(cmndline_args) != 4:
        show_syntax()
        exit_msg(1, 'Invalid number of args')

    template_file = cmndline_args[0]
    yaml_source_data = cmndline_args[1]
    dest_dir = cmndline_args[2]
    display_name = cmndline_args[3]

    print(f'DISPLAYNAME == {display_name}\n')

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

    # derive desktop files
    derive_all_desktops(template_file, yaml_source_data, dest_dir, display_name)


if __name__ == "__main__":
    main()