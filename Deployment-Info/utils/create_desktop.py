import errno
import hashlib
import os.path
import platform
import time

import psutil
#import re
import sys
import yaml
from pathlib import Path
#from getmac import get_mac_address as gma

from jinja2 import Environment, FileSystemLoader
from enum import Enum


# Notes:
#   a). for desktop icons to be usable they need to be executable (not just chmod on the file).
#       The following shows how this can be achieved.
#           [SOLVED] Make *.desktop files executable : https://forum.xfce.org/viewtopic.php?id=16465
#       The above links to
#           https://forum.xfce.org/viewtopic.php?pid=70683


SIMPLI_PREFIX = 'simpli'
tool_name = 'TBD'
debug_mode = False

class Optype(Enum):
    DEBUG = 1
    INFO = 2
    ERROR = 3

def renderop(the_string, output_type=Optype.INFO):
    global debug_mode
    if debug_mode is True:
        desc = 'DEBUG-MODE-ON : '
    else:
        desc = 'DEBUG-MODE-OFF: '

    desc = ''
    msg_type = output_type.name
    desc += ' (' + str(msg_type) + ') :' + the_string
    if output_type == Optype.DEBUG and debug_mode == False:
        pass  # do not print if it i debug output and it is not in debug mode
    else:
        print(desc)

def show_syntax():
    renderop(f'Syntax : Args ==  <template_desktop_file> <config_data> <dest_dir> <desktop>\n\tWhere\tdesktop == xfce\n\n')

def show_help():
    info = """    This utility takes template file (using jinja syntax), together 
    with a yaml config file and generates a desktop file for each entry. 
    The config of each generated desktop file is based upon the values in the config file.  
    Note: It can be run on controller or client, however only the client is configured with 
    the requisite python modules.
    NOTE: This ONLY works for xfce desktop environment.
    """
    renderop(f'\nTool info:\n{info}\n')

def exit_msg(code, text):
    if code != 0:
        renderop(f'Error ({code}): {text}\n', Optype.ERROR)
        show_syntax()
    exit(code)




def silentremove(filename):
    try:
        os.remove(filename)
    except OSError as e: # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
            raise # re-raise exception if a different error occurred


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
    if_name = 'enp1s0'
    full_mac = get_network_physical_address(if_name)

    dev_id = full_mac + '_' + platform.node()
    print(f'DEV_ID = {dev_id}')
    return dev_id

def get_dir_and_file(the_template):
    base_file = os.path.basename(the_template)
    dir_path = os.path.dirname(the_template)
    renderop(f'BASE={base_file}\nDIR={dir_path}\n', Optype.DEBUG)
    return (dir_path, base_file)

def remove_all_in_dir_with_prefix(base_dir, the_prefix, remove_normal_files, remove_directories):
    #print(f'CALLED remove_all_in_dir_with_prefix\n')
    if not base_dir.startswith('/home/robert'): # this is protection against being called with a bad base_dir
        exit_msg(99, 'Call to internal function with prefix NOT  /home >>{the_dir}<<')

    for (root, dirs, files) in os.walk(base_dir, topdown=False):
        for the_file in files:
            full_path = os.path.join(root, the_file)
            #renderop(f'THE_FILE:{the_file} # >>{full_path}<<', Optype.DEBUG)
            if the_file.startswith(the_prefix) and remove_normal_files:
                renderop(f'REMOVE NORMAL FILE: {full_path}\n', Optype.DEBUG)
                try:
                    os.remove(full_path)
                except Exception as inst:
                    exit_msg(71, f'Error removing file=={full_path} RESP>>{inst}<<')

        for the_dir in dirs:
            full_path_dir = os.path.join(root, the_dir)
            #renderop(f'THE_DIR: {the_dir} # >>{full_path_dir}<<', Optype.DEBUG)
            if the_dir.startswith(the_prefix) and remove_directories:
                renderop(f'REMOVE DIR: {full_path_dir}\n', Optype.DEBUG)
                try:
                    os.rmdir(full_path_dir)
                except Exception as inst:
                    exit_msg(72, f'Error removing directory. RESP >>Exception {inst}<<')


def remove_all_simpli_files_in_desktop_dir(my_dir):
    #remove_all_in_dir_with_prefix(my_dir, 'simpli_', False, False)
    remove_all_in_dir_with_prefix(my_dir, 'simpli_', True, False)
    remove_all_in_dir_with_prefix(my_dir, 'simpli-', False, True)
    time.sleep(3)


def generate_from_template(temp, var_struct, filename):
    renderop(f'Generating template_desktop_file: {filename}', Optype.DEBUG)
    content = temp.render(var_struct)
    with open(filename, mode="w", encoding="utf-8") as message:
        message.write(content)
        renderop(f"... Created {filename}", Optype.DEBUG)
        os.chmod(filename, 0o755)


def make_desktop_file_trusted_by_xfce(desktop_file):
    # The following for python implementation
    # https://stackoverflow.com/questions/64730177/how-to-hash-a-big-file-without-having-to-manually-process-chunks-of-data
    sha256 = hashlib.sha256()
    with open(desktop_file, 'rb') as handle_desktop_file:
        sha256.update(handle_desktop_file.read())
    sha256_of_desktop_file = sha256.hexdigest()
    full_msg = f'File: {desktop_file} has hash of: {sha256_of_desktop_file}\n'
    renderop(f'{full_msg}', Optype.DEBUG)

    # perform the gio action
    # How to mass-trust .desktop files via shell?  https://forum.xfce.org/viewtopic.php?pid=70683
    the_cmd = f'gio set -t string {desktop_file} metadata::xfce-exe-checksum {sha256_of_desktop_file}'
    returned_value = os.system(the_cmd)  # returns the exit code in unix

    ret_val = f'Command: {the_cmd}\nReturned value: {returned_value}\n'
    renderop(f'{ret_val}', Optype.DEBUG)

    # for debugging purposes we will write the hash we are using (+ other info) to a file (based on the filename)
    my_debug = False
    if my_debug:
        hash_info_file = desktop_file + '-sha256.txt'
        f1 = open(hash_info_file, 'w')
        f1.write(full_msg)
        f1.write(ret_val)
        f1.close()


def derive_desktop_category(category_data, icon_base_dir, template_desktop_file, populate_specials, desktop_env):
    common_data = dict()
    common_data['tool_command'] = category_data['tool_command']
    common_data['desktop_categories'] = category_data['desktop_categories']
    common_data['desktop_kde_protocols'] = category_data['desktop_kde_protocols']
    common_data['desktop_keywords'] = category_data['desktop_keywords']
    common_data['location_for_icon'] = category_data['location_for_icon']

    # set data for desktop_info
    common_data['desktop_info'] = '( DE=' + desktop_env + ') '

    if populate_specials:
        hostname = platform.node()
        common_data['client_hostname'] = hostname
    else:
        common_data['client_hostname'] = ''

    this_category_entries = category_data['entries']

    for info_struct in this_category_entries:

        dest_dir = icon_base_dir
        new_struct = dict()

        # copy attributes common to the category to the structure
        # in teh case of attribute relating to the desktop file location we use this to determine where we create the file
        for key, value in common_data.items():
            new_struct[key] = value
            if key == 'location_for_icon':
                if value == '.':
                    # leave dest_dir unchanged (i.e. as teh base dir)
                    pass
                else:
                    dest_dir = icon_base_dir + '/' + value

        # configure the specific attributes (this allows overriding)
        for key2, value2 in info_struct.items():
            if key2 == 'location_for_icon':
                if value2 == '.':
                    # leave dest_dir unchanged (as may have been overridden by base stuff)
                    pass
                else:
                    dest_dir = icon_base_dir + '/' + value2
            else:
                new_struct[key2] = value2

        # check if the dest dir exists
        #print(f'DEBUG: Destination dir == {dest_dir}')
        renderop(f'Destination dir == {dest_dir}')
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
            renderop(f'Creating folder {dest_dir}\n')

        fname = f"{dest_dir}/{SIMPLI_PREFIX}_{new_struct['entry']}.desktop"
        silentremove(fname) # remove file if it exists

        if info_struct['enabled'] == 'true':
            generate_from_template(template_desktop_file, new_struct, fname)

            if desktop_env == 'xfce':            # xfce needs checksum creating
                make_desktop_file_trusted_by_xfce(fname)

        else:
            # remove file if not enabled
            try:
                os.remove(fname)
            except:
                renderop(f'Attempting to remove non-existent file ( {fname} )')


def derive_all_desktops(template_file, yaml_source_data, base_dir_for_icons, type_of_desktop):

    with open(yaml_source_data) as stream:
        try:
            data_struct = yaml.safe_load(stream)
            # print(yaml.safe_load(stream))
            # print(data_struct['zoom'])

        except yaml.YAMLError as exc:
            renderop(exc)

    # Obtain the overall template
    (dirpath, basefile) = get_dir_and_file(template_file)
    environment = Environment(loader=FileSystemLoader(dirpath))
    template = environment.get_template(basefile)

    derive_desktop_category(data_struct['zoom'], base_dir_for_icons, template, False, type_of_desktop)
    derive_desktop_category(data_struct['browser'], base_dir_for_icons, template, False, type_of_desktop)
    derive_desktop_category(data_struct['video'], base_dir_for_icons, template, False, type_of_desktop)
    derive_desktop_category(data_struct['platform'], base_dir_for_icons, template, True, type_of_desktop)
    derive_desktop_category(data_struct['genrep'], base_dir_for_icons, template, True, type_of_desktop)


def main():
    tool_name == os.path.basename(sys.argv[0])
    renderop(f'TOOL_NAME == {tool_name}\n', Optype.DEBUG)

    if len(sys.argv) <= 1:
        show_help()
        show_syntax()
        exit_msg(1, 'Invalid number of args')

    cmndline_args = sys.argv[1:]
    args_string = 'Invocation args== ' + '   '.join(cmndline_args)

    if cmndline_args[0] == '-h' or cmndline_args[0] == '--help':
        show_help()
        show_syntax()
        exit_msg(0, '')

    if cmndline_args[0] == '-d':
        #print('discovered -d flag\n')
        global debug_mode
        debug_mode = True
        cmndline_args.pop(0)

    if len(cmndline_args) != 4:
        show_syntax()
        exit_msg(1, 'Invalid number of args')

    renderop(args_string, Optype.DEBUG)
    template_file = cmndline_args[0]
    yaml_source_data = cmndline_args[1]
    dest_dir_root = cmndline_args[2]

    desktop_type_name = cmndline_args[3]
    renderop(f'DESKTOP SPECIFIED == {desktop_type_name}\n', Optype.DEBUG)

    os.path.isfile(template_file)
    if not os.path.isfile(template_file):
        exit_msg(2, 'Template file specified is not valid')
    elif not os.path.isfile(yaml_source_data):
        exit_msg(3, 'Data file specified is not valid')
    elif not os.path.isdir(dest_dir_root):
        exit_msg(4, 'Destination dir does not exist')

    #display_is_valid = bool(re.match('[a-zA-Z\s]+$', display_name))
    desktop_is_valid = desktop_type_name != '' and all(chr.isalpha() or chr.isspace() for chr in desktop_type_name)
    if desktop_type_name != 'xfce': # only cinnamon now supported
        exit_msg(5, 'Desktop is not a valid known ( only xfce)')

    remove_all_simpli_files_in_desktop_dir(dest_dir_root)
    # derive desktop files
    derive_all_desktops(template_file, yaml_source_data, dest_dir_root, desktop_type_name)


if __name__ == "__main__":
    main()