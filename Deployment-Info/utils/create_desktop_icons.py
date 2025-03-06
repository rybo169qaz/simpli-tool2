import errno
import hashlib
import json
import os.path
import platform
import time

import psutil
#import re
import sys
import yaml
#from pathlib import Path
##from getmac import get_mac_address as gma

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

# def get_network_physical_address(netInterfaceName):
#   nics = psutil.net_if_addrs()
#   macAddress = ([j.address for i in nics for j in nics[i] if i==netInterfaceName and j.family==psutil.AF_LINK])[0]
#   return macAddress.replace('-',':')

# def get_device_id():
#     if_name = 'enp1s0'
#     full_mac = get_network_physical_address(if_name)
#
#     dev_id = full_mac + '_' + platform.node()
#     print(f'DEV_ID = {dev_id}')
#     return dev_id

def get_dir_and_file(the_template):
    base_file = os.path.basename(the_template)
    dir_path = os.path.dirname(the_template)
    renderop(f'BASE={base_file}\t\tDIR={dir_path}\n', Optype.DEBUG)
    return (dir_path, base_file)

def remove_all_in_dir_with_prefix(base_dir, the_prefix, remove_normal_files, remove_directories):
    #print(f'CALLED remove_all_in_dir_with_prefix\n')

    # this is protection against being called with a bad base_dir
    usr1 = '/home/robert' # this is the historical user used
    usr2 = '/home/simp'   # this is the planned prefix for users
    if (not base_dir.startswith(usr1)) and (not base_dir.startswith(usr2)):
        exit_msg(99, f'Call to internal function with invalid username >>{usr1}<< , >>{usr2}<<')

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


def generate_text_from_template(template, var_struct) -> str:
    """Uses the given dictionary to substitute into the template (from jinja) and return the text output."""
    return template.render(var_struct)


def generate_file_from_template(template, var_struct, filename):
    """Uses the given structure to expand the (jinja) template and write output to the file."""
    renderop(f'Generating template_desktop_file: {filename}', Optype.DEBUG)

    #content = template.render(var_struct)
    content = generate_text_from_template(template, var_struct)
    if content is None:
        return False

    conten2 = 'abc'
    with open(filename, mode="w", encoding="utf-8") as message:
        message.write(content)
        renderop(f"... Created {filename}", Optype.DEBUG)
        os.chmod(filename, 0o755)
    return True


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
    #renderop(f'Performing action>>{the_cmd}<<', Optype.DEBUG)
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

def add_user_home_if_relative(the_user, the_path):
    if  (the_path.startswith('/')) :
        full_path = the_path
    else:
        full_path = '/home/' + the_user + '/' + the_path
    return full_path

def derive_desktop_category(global_data, category_data, icon_base_dir, template_desktop_file, populate_specials,
                            desktop_env):
    common_data = dict()
    common_data['user'] = global_data['user']
    home_dir = '/home/' + global_data['user']

    # tool command is either absolute or relative to home directory
    common_data['tool_command'] = add_user_home_if_relative(global_data['user'], category_data['tool_command'])
    # tool_cmd = category_data['tool_command']
    # if  (tool_cmd.startswith('/')) :
    #     common_data['tool_command'] = tool_cmd
    # else:
    #     common_data['tool_command'] = home_dir + '/' + tool_cmd

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
                    # leave dest_dir unchanged (i.e. as the base dir)
                    #pass
                    dest_dir = icon_base_dir
                else:
                    dest_dir = icon_base_dir + '/' + value

        # configure the specific attributes (this allows overriding)
        for key2, value2 in info_struct.items():
            if key2 == 'icon':
                #new_struct[key2] = add_user_home_if_relative(common_data['user'], value2)
                new_struct[key2] = value2
            elif key2 == 'location_for_icon':
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
            generate_file_from_template(template_desktop_file, new_struct, fname)

            if desktop_env == 'xfce':            # xfce needs checksum creating
                make_desktop_file_trusted_by_xfce(fname)

        else:
            # remove file if not enabled
            try:
                os.remove(fname)
            except:
                renderop(f'Attempting to remove non-existent file ( {fname} )')

class ExtractStructuredAttribute:
    def __init__(self, input_file):
        self.input_file = input_file
        self.the_struct = None
        self.is_valid = False
        self._validate_args()
        self.attribs = None
        self.entries = None

    def _validate_args(self):
        if not os.path.isfile(self.input_file):
            return False
        with open(self.input_file) as stream:
            try:
                self.the_struct = yaml.safe_load(stream)
                # print(yaml.safe_load(stream))
            except yaml.YAMLError as exc:
                print(f'Bad YAML\n')
                exit(99)

        if 'attributes' not in self.the_struct:
            print(f'Missing root attributes')
            return False
        self.attribs = self.the_struct['attributes']

        if 'entries' not in self.the_struct:
            print(f'Missing root entries')
            return False
        self.entries = self.the_struct['entries']
        self.is_valid = True

    def struct_is_valid(self):
        return self.is_valid

    def get_root_id(self):
        return self.the_struct.get('a_id')



    def root_attribute_exists(self, attrib_name):
        if self.is_valid is False: return False
        if self.the_struct.get('attributes') is None: return False
        if self.the_struct['attributes'].get(attrib_name) is None:
            return False
        else:
            return True

    def _get_list_of_entries(self, root):
        the_entry_list = root['entries']
        list_of_ids = []
        for entry in the_entry_list:
            list_of_ids.append(entry['a_id'])
        return list_of_ids

    def _get_attributes(self, root):
        return root['attributes']

    def _get_specified_attribute(self, root, attribute_name):
        atts = root.get('attributes')
        return atts.get(attribute_name)

    def _get_specified_entry(self, root, entry_name):
        the_entry_list = root['entries']
        entry_obj = None
        for entry in the_entry_list:
            if entry['a_id'] == entry_name:
                entry_obj = entry
                break
        return entry_obj

    def get_root_attribute(self, attrib_name):
        return self._get_specified_attribute(self.the_struct, attrib_name)

    def get_list_of_first_level_entry_ids(self):
        return self._get_list_of_entries(self.the_struct)

    def first_level_exists_with_name(self, level1_name ):
        obj = self._get_specified_entry(self.the_struct, level1_name)
        if obj is None:
            return False
        else:
            return True

    def second_level_exists_with_name(self, level1_name, level2_name ):
        obj1 = self._get_specified_entry(self.the_struct, level1_name)
        if obj1 is None: return False

        obj2 = self._get_specified_entry(obj1, level2_name)
        if obj2 is None: return False
        return True

    def get_dict_of_lev1_lev2(self, level1_name, level2_name):
        if self.second_level_exists_with_name(level1_name, level2_name) is False: return None
        cumulative = dict({})

        cumulative = cumulative | self._get_attributes(self.the_struct)

        lev1 = self._get_specified_entry(self.the_struct, level1_name)
        cumulative = cumulative | self._get_attributes(lev1)

        lev2 = self._get_specified_entry(lev1, level2_name)
        cumulative = cumulative | self._get_attributes(lev2)

        return cumulative







class CreateDummyKnown:
    def __init__(self, dest_dir, dest_gen_file):
        self.dest_dir = dest_dir
        self.dest_gen_file = dest_gen_file
        self.test_data = None

    def _create_node_struct(self, node_id, list_of_entries, dict_of_atts):
        create_empty_structures = True

        attrib_dict = dict({})
        for key in dict_of_atts:
            attrib_dict[key] = dict_of_atts[key]

        entry_list = []
        for entry in list_of_entries:
            entry_list.append(entry)

        my_dict = dict({'a_id': node_id, 'attributes': attrib_dict})
        # create_empty_structures
        if create_empty_structures or len(entry_list) != 0:
            my_dict['entries'] = entry_list
        return my_dict

    def _write_yaml_to_file(self, filename, the_struct):
        file_handle = open(filename, "w")
        file_handle.write("---\n")
        yaml.dump(the_struct, file_handle)
        file_handle.write("...\n")
        file_handle.close()
        print(f'YAML file saved to file {filename}.')

    def new_create_testd_file(self):

        france_struct = self._create_node_struct('france', [],
                                                 {'command_args': 'france_tool1 a b c',
                                                  'enabled': 'true',
                                                  'description': 'France',
                                                  'flag': 'French Flag'})
        self._write_yaml_to_file(f'{self.dest_dir}/dummy-france.yml', france_struct)

        neth_struct = self._create_node_struct('netherlands', [],
                                                 {
                                                  'enabled': 'false',
                                                  'description': 'Holland',
                                                  'flag': 'Dutch Flag'})
        self._write_yaml_to_file(f'{self.dest_dir}/dummy-netherlands.yml', neth_struct)

        #countries_entries_list = [ 'france-placeholder', 'netherlands-placeholder']
        countries_entries_list = [france_struct, neth_struct]
        countries_struct = self._create_node_struct('country_list', countries_entries_list,
                                               {'command_args': 'country_tool1 A B C',
                                                'description': 'European countries'})
        self._write_yaml_to_file(f'{self.dest_dir}/dummy-countries.yml', countries_struct)

        # mountains
        everest_struct = self._create_node_struct('everest', [],
                                                 {
                                                    'enabled': 'true',
                                                  'description': 'Mount Everest',
                                                     'env2': 'everest value for env2',
                                                  'icon': 'nepal_photo'})
        #self._write_yaml_to_file(f'{self.dest_dir}/dummy-everest.yml', everest_struct)

        mtblanc_struct = self._create_node_struct('mt blanc', [],
                                                  {
                                                      'enabled': 'false',
                                                      'description': 'Mt Blanc',
                                                      'icon': 'photo_of_my_blanc'})

        mountains_entries_list = [everest_struct, mtblanc_struct]
        mountains_struct = self._create_node_struct('mountain_list', mountains_entries_list,
                                                    {'category_description': 'Well known mountains',
                                                     'tool_command': 'mountain_tool'})
        self._write_yaml_to_file(f'{self.dest_dir}/dummy-mountains.yml', mountains_struct)

        # CATEGORY with no attributes
        no_attr_struct1 = self._create_node_struct('no_attr1', [], { 'abc': 'cba', 'def': 'fed'})
        no_attr_struct2 = self._create_node_struct('no_attr2', [], {'pqr': 'rqp', 'xyz': 'zyx'})
        no_attr_struct = self._create_node_struct('no attr', [no_attr_struct1, no_attr_struct2],{})

        #category with no entries
        no_entr_struct = self._create_node_struct('no entries', [], {'attribute_of_no_entry': 'myatt'})

        #root_entries_list = ['a', 'b']
        root_entries_list = [countries_struct, mountains_struct, no_attr_struct, no_entr_struct]

        root_struct = {
            'env1': 'env1 root value',
            'env2': 'root value for env2'}
        root_struct = self._create_node_struct('root_id', root_entries_list, root_struct)

        #root_filename = f'{self.dest_dir}/dummy-rooty.yml'
        root_filename = f"{self.dest_dir}/{self.dest_gen_file}"
        self._write_yaml_to_file(root_filename, root_struct)



    def create_test_data(self):
        attrib_france = dict({'identity': 'france', 'enabled': 'true', 'flag': 'france_flag', 'description': 'France',
                              'command_args': '/home/robert/.simpli/config/dev-info.txt'})
        entry_france = dict({'attributes': attrib_france })

        attrib_netherlands = dict({'identity': 'the_netherlands', 'enabled': 'false', 'flag': 'dutch_flag', 'description': 'Holland',
                              'command_args': '/home/robert/.simpli/config/dev-info.txt'})
        entry_netherlands = dict({'attributes': attrib_netherlands })

        attrib_countries = dict({'category_description': 'Lots of countries', 'tool_command': 'country_tools', 'location_for_icon': 'simpli-admin'})
        entry_countries = list([entry_france, entry_netherlands])
        obj_countries = dict({'attributes': attrib_countries, 'entries': entry_countries})


        attrib_everest = dict({'identity': 'everest', 'enabled': 'true', 'photo': 'nepal_photo', 'description': 'Everest' })
        entry_everest = dict({'attributes': attrib_everest})

        attrib_mtblanc = dict(
            {'identity': 'mount blanc', 'enabled': 'true', 'photo': 'photo_of_mt_blanc', 'description': 'Mt Blanc',
             'tool_command': 'special_mountain_tool'})
        entry_mtblanc = dict({'attributes': attrib_mtblanc})

        attrib_mountains = dict({'category_description': 'Well known mountains', 'tool_command': 'mountain_tool'})
        entry_mountains = list([entry_everest, entry_mtblanc])
        obj_mountains = dict({'attributes': attrib_mountains, 'entries': entry_mountains})

        attrib_global = dict({'com1': '111', 'com2': '222'})

        self.test_data = dict({
            'attributes': attrib_global,
            'entries': [obj_countries, obj_mountains]
        })

        #yaml_string = yaml.dump(self.test_data)
        #print("The YAML string is:")
        #print(yaml_string)

        dummy_fname = f"{self.dest_dir}/{self.dest_gen_file}"
        self._write_yaml_to_file(dummy_fname, self.test_data)


class DeskIcon:
    """
    Given the specified jinja template in the template file, it uses the provided_args
    to populate the necessary text in the file at the specified base_dir
    """
    def __init__(self, base_dir, template_file, provided_args):
        self.dest_dir = base_dir
        self.template_file = template_file
        self.provided_args = provided_args # dictionary
        self.FILE_PREFIX = 'X' + SIMPLI_PREFIX
        self.is_valid = False
        self._validate_args()


    def _validate_args(self):
        """Necessary validation checks for the object to be valid."""
        if not os.path.isdir(self.dest_dir):
            return False
        if not os.path.isfile(self.template_file):
            return False
        if not isinstance(self.provided_args, dict):
            return False
        if not 'entry' in self.provided_args:
            return False
        self.is_valid = True


    def valid(self):
        return self.is_valid


    def get_filename(self):
        """The full filename of the desktop file that would be created."""

        renderop(f"DEST_DIR = {self.dest_dir}", Optype.INFO)
        renderop(f"FILE_PREFIX = {self.FILE_PREFIX}", Optype.INFO)
        str_args = str(self.provided_args)
        renderop(f"Provided args:  {str_args}", Optype.INFO)

        #the_entry = self.provided_args['entry']
        the_entry = self.provided_args.get('entry')
        if the_entry is None:
            print(f'self.provided_args[entry] = NON-EXISTANT')
            fname = None
        else:
            print(f'self.provided_args[entry] = {the_entry}')
            fname = f"{self.dest_dir}/{self.FILE_PREFIX}_{self.provided_args['entry']}.desktop"
        return fname


    def generate_desktop_icon_text(self):
        dict_of_vars_to_replace = self.provided_args  # dict({}
        # this loads the template file and then processes the string
        with open(self.template_file, 'r') as file:
            template_string = file.read()
        environment = Environment()
        template_obj = environment.from_string(template_string)

        cont = template_obj.render(dict_of_vars_to_replace)
        return cont


    def generate_desktop_file(self, make_trusted=False):
        text_content = self.generate_desktop_icon_text()
        filename = self.get_filename()
        with open(filename, mode="w", encoding="utf-8") as message:
            message.write(text_content)
            renderop(f"... Created {filename}", Optype.DEBUG)
            os.chmod(filename, 0o755)
            if make_trusted:
                make_desktop_file_trusted_by_xfce(filename)
        return True

    def generate_trusted_desktop_file(self):
        self.generate_desktop_file(make_trusted=True)



class IconNode:
    def __init__(self, node_name, child_type, attrib_struct):
        self.node_name = node_name
        self.child_type_name = child_type
        self.attrib_struct = attrib_struct
        self.child_struct = dict({})

    def get_node_name(self):
        return self.node_name

    def get_child_type(self):
        return self.child_type_name

    def get_list_attribute_names(self):
        the_list = list(self.attrib_struct.keys())
        the_list.sort()
        return the_list

    def get_attribute_value(self, attr_name):
        return self.attrib_struct.get(attr_name)

    def get_count_of_children(self):
        return len(self.child_struct)

    def get_list_of_children_names(self):
        the_list = list(self.child_struct)
        the_list.sort() # we return a sorted list
        return the_list

    def add_child(self, new_child_type, child_key, child_value):
        if new_child_type != self.child_type_name:
            return False
        self.child_struct[child_key] = child_value
        return True

    def get_child_of_given_name(self, wanted_child_name):
        child = self.child_struct.get(wanted_child_name) # this is None if it is non-existant
        return child

    def get_node_struct(self):
        mystruct = dict({})
        mystruct['attributes'] = self.attrib_struct
        child_names = self.get_list_of_children_names()
        mystruct['children'] = child_names

    def get_full_node_struct(self):
        mystruct = dict({})
        mystruct['attributes'] = self.attrib_struct
        mystruct['children'] = None
        child_names = self.get_list_of_children_names()

        children_handle = mystruct['children']
        child_struct = dict({})
        for child_name in child_names:
            children_handle[child_name] = self.get_child_of_given_name(child_name)
        return mystruct

    def print_node(self):
        mystruct = self.get_node_struct()
        print(json.dumps(mystruct, sort_keys=True, indent=4))

    def print_full_node(self):
        mystruct = self.get_full_node_struct()
        print(json.dumps(mystruct, sort_keys=True, indent=4))




class IconSet:

    """
    This takes the specified icon_set file and for each entry it
    invokes the DeskIcon class to create the relevant desktop
    icon file.
    """
    FILE_PREFIX = 'simpli_'
    FILE_POSTFIX = '.desktop'

    def __init__(self, template_file, icons_set_file, target_dir):
        self.template_file = template_file
        self.icons_set_file = icons_set_file
        self.target_dir = target_dir
        self.the_dict = None
        self.common = None
        self.entries = None
        self.is_valid = False
        self._validate()

    def _validate(self):
        if not os.path.isfile(self.template_file):
            return False
        if not os.path.isfile(self.icons_set_file):
            return False
        with open(self.icons_set_file) as stream:
            try:
                self.the_dict = yaml.safe_load(stream)
                # print(yaml.safe_load(stream))
            except yaml.YAMLError as exc:
                sys.exit('Structure has malformed YAML in the icon file.')
            self.common = self.the_dict.get('common')
            if self.common is None:
                sys.exit('Structure is missing the "common" section in the icon file.')

            self.entries = self.the_dict.get('entries')
            if self.entries is None:
                sys.exit('Structure is missing the "entries" section in the icon file.')
            # we should check that for each there are the two entries : "entry" and "enabled"
        self.is_valid = True

    def is_valid_set(self):
        return self.is_valid

    def get_common_attributes(self):
        return self.common

    def num_all_icons(self):
        return len(self.entries)

    def get_full_filename_of_entry(self, the_entry):
        return self.FILE_PREFIX + the_entry + self.FILE_POSTFIX

    def list_icon_files(self):
        enabled_icons = []
        disabled_icons = []
        for the_entry in self.entries:
            nam = the_entry['entry']
            if the_entry['enabled'] == 'true':
                enabled_icons.append(nam) # fullname
            else:
                disabled_icons.append(nam) # fullname
        return enabled_icons, disabled_icons


    def list_disabled_icons(self):
        enab, disab = self.list_icon_files()
        return disab


    def list_enabled_icons(self):
        enab, disab = self.list_icon_files()
        return enab

    def num_enabled_icons(self):
        enab, disab = self.list_icon_files()
        return len(enab)

    def list_enabled_icon_filenames(self):
        enab, disab = self.list_icon_files()
        return list(map(lambda x: self.get_full_filename_of_entry(x) , enab))

    def get_target_dir(self):
        return self.target_dir

    def list_fullpath_icons_to_create(self):
        enab, disab = self.list_icon_files()
        list_of_all_entries = list(map(lambda x: self.get_target_dir() + '/' + x, enab))
        return list_of_all_entries

    def get_attribs_of_entry(self, entry_name):
        specific_dict = self.common.copy()
        found_entry = False
        for ent in self.entries:
            if ent['entry'] == entry_name:
                found_entry = True
                specific_dict.update(ent)
                break
        if found_entry is False:
            specific_dict = None
        return specific_dict

    def generate_all_icons(self,fake_it):
        """
        This has been written for readablity not performance
        :param fake_it:
        :return:
        """
        files_to_be_created = []
        invalid_entry_found = False
        for ent in self.list_enabled_icons():
            atts = self.get_attribs_of_entry(ent)
            #fname = self.get_full_filename_of_entry(ent)
            iconobj = DeskIcon(self.target_dir, self.template_file, atts)

            if not fake_it:
                iconobj.generate_desktop_file()

            # exp_fname = iconobj.get_filename()
            # if exp_fname is None:
            #     invalid_entry_found = True
            # else:
            #     files_to_be_created.append(exp_fname)

        # if fake_it:
        #     # dummy_list_of_files = []  # [ 'aa.txt', 'b.txt']
        #     # ret_list = dummy_list_of_files
        # else:
        #     ret_list = files_to_be_created

        #return ret_list


class IconSuite:
    def __init__(self, icon_spec_file):
        self.icon_spec_file = icon_spec_file
        self.the_dict = None
        self.is_valid = False
        self._validate_icon_args()

    def _validate_icon_args(self):
        if not os.path.isfile(self.icon_spec_file):
            return False
        with open(self.icon_spec_file) as stream:
            try:
                self.the_dict = yaml.safe_load(stream)
                # print(yaml.safe_load(stream))
            except yaml.YAMLError as exc:
                print(f'Bad YAML\n')
                exit(99)
        self.is_valid = True

    def validsuite(self):
        return self.is_valid

    def get_categories(self):
        category_dict = self.the_dict.get('categories')
        if not category_dict:
            return None
        category_set = set(())
        for entry in category_dict:
            category_set.add(entry)
            print(f'Category: {entry}\n')
        return category_set

    def get_entries_in_category(self, cat):
        the_cat_info = self.the_dict.get('categories').get(cat)
        if not the_cat_info:
            return None
        entries_dict = the_cat_info['entries']
        entry_set = set(())
        for entry in entries_dict:
            entry_name = entry['entry']
            entry_set.add(entry_name)
            #print(f'Entry: {entry_name}\n')
        return entry_set

    def entries_in_all_categories(self):
        gen_list = []
        gen_dict = dict({})
        list_of_cat = self.get_categories()
        print(f'All categories= {list_of_cat}')
        for cat in list_of_cat:
            gen_dict[cat] = []
            list_of_entries = self.get_entries_in_category(cat)
            for entry in list_of_entries:
                print(f'Category={cat}   , Entry={entry}')
                gen_dict[cat].append(entry)
                gen_list.append((cat, entry))
        print(json.dumps(gen_dict))
        return gen_dict



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

    common_dict = dict()
    common_dict.update({"user": "robert"})

    category_data = data_struct['categories']
    derive_desktop_category(common_dict, category_data['zoom'], base_dir_for_icons, template, False, type_of_desktop)
    derive_desktop_category(common_dict, category_data['browser'], base_dir_for_icons, template, False, type_of_desktop)
    derive_desktop_category(common_dict, category_data['video'], base_dir_for_icons, template, False, type_of_desktop)
    derive_desktop_category(common_dict, category_data['platform'], base_dir_for_icons, template, True, type_of_desktop)
    derive_desktop_category(common_dict, category_data['genrep'], base_dir_for_icons, template, True, type_of_desktop)
    derive_desktop_category(common_dict, category_data['terminal'], base_dir_for_icons, template, True, type_of_desktop)


def new_create_icons():
    print(f'')

def create_desktop_icon_main():
    tool_name = os.path.basename(sys.argv[0])
    renderop(f'TOOL_NAME == {tool_name}\n', Optype.DEBUG)

    if len(sys.argv) <= 1:
        show_help()
        show_syntax()
        exit_msg(1, 'Invalid number of args')

    cmndline_args = sys.argv[1:]
    args_string = 'Invocation args== ' + '   '.join(cmndline_args)

    if cmndline_args[0] == 'x':
        print(f'Enhanced mode\n')
        exit_msg(0, 'COMPLETED OK')
    else:
        print(f'Standard mode\n')

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


    print(f'STARTING ACTIONS')
    print(f'TEMPLATE_FILE={template_file}')
    print(f'DATA_FILE={yaml_source_data}')
    print(f'DEST_DIR={dest_dir_root}')
    print(f'DESKTOP_TYPE={desktop_type_name}')
    print('')

    remove_all_simpli_files_in_desktop_dir(dest_dir_root)
    # derive desktop files
    derive_all_desktops(template_file, yaml_source_data, dest_dir_root, desktop_type_name)


if __name__ == "__main__":
    create_desktop_icon_main()