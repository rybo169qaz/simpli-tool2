from enum import Enum
import errno
import hashlib
from fileinput import close

import jinja2
import json
import os.path
import platform
import pprint
from pydantic import BaseModel
import time
import tomli as tomllib

#import psutil
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


class InvocationMode(Enum):
    ORIGINAL = 1
    LEGACYSIM = 2
    NEW = 3


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


class IconText:
    """
    Given the template text and the args to be substituted,
    return the text to be used in icon file.
    """

    def __init__(self, template_text, args_to_replace):
        self.template_text = template_text
        self.args_to_replace = args_to_replace

        self.common_dict = dict()
        self.common_dict.update({"user": "robert"})
        self.common_dict.update({"client_hostname": platform.node()})
        self.args_to_replace.update(self.common_dict)
        self._expand_paths()

    def _expand_paths(self):
        keys_to_modify = ['tool_command', 'icon']
        for item_key in keys_to_modify:
            if item_key in self.args_to_replace:
                self.args_to_replace[item_key] = add_user_home_if_relative(self.common_dict['user'],
                                                                                 self.args_to_replace[item_key])

    def __str__(self):
        print(f'vvvv Template text vvvv\n{self.template_text}\n^^^^\n')
        pp = pprint.PrettyPrinter(indent=4)
        print('vvvv Params vvvv')
        pp.pprint(self.args_to_replace)
        print('^^^^')


    def gen_icon_text(self):
        """
        If the template text is invalid, then return None
        Else return the substituted
        :return:
        """
        #environment = Environment()
        environment = Environment(undefined=jinja2.StrictUndefined)

        try:
            template_obj = environment.from_string(self.template_text)
            cont = template_obj.render(self.args_to_replace)
        except (jinja2.exceptions.UndefinedError, jinja2.exceptions.TemplateSyntaxError) as exception:
            #print('JINJA UndefinedError')
            print(f"Exception Name: {type(exception).__name__}")
            print(f"Exception Desc: {exception}")
            self.__str__()
            #raise ValueError('Missing parameter substitutions')
            cont = None
        except(Exception):
            print('JINJA other')
            cont = None

        return cont

class DeskEntryStructure(BaseModel):
    """
    This holds the data required for a Desktop Entry file.
    """
    description: str
    client_hostname: str = 'UNK-CLIENT'
    comment: str = 'NO COMMENT'
    tool_command: str
    command_args: str
    icon: str
    desktop_categories: str = ''
    kde_protocols: str = ''
    keywords: str = ''

class DeskEntryPositioning(BaseModel):
    """
    This holds the data required for fixing the desk entry
    structure file in position.
    If the base dir is not specified it implicitly means that the
    users home directory should be used as the base dir.
    """
    dep_base_dir: str
    #dep_relative_dir: str = None
    dep_entry_name: str
    dep_make_trusted: bool = False


class DeskEntryCreator:
    """
    The class for creating a Desk Entry file using a DeskEntry object.
    """
    default_template_text = """
    [Desktop Entry]
    Version=1.0 xyz
    Name={{ description }}
    GenericName=Generic {{ description }}
    Comment=Comment {{ description }}
    Name[en_GB]={{ description }} {{ client_hostname }}
    GenericName[en_GB]=GB Generic {{ description }} {{ client_hostname }}
    Comment[en_GB]=Details: {{ comment }}
    Exec={{ tool_command }} {{ command_args }}
    Icon={{ icon }}
    Terminal=false
    Type=Application
    Categories={{ desktop_categories }}
    X-KDE-Protocols={{ desktop_kde_protocols }}
    Keywords={{ desktop_keywords }}
    """
    def __init__(self, des: DeskEntryStructure, dep: DeskEntryPositioning, template_text: str = default_template_text):
        self.des = des
        self.dep = dep
        self.template_text = template_text # The template on which to apply the DeskEntryStructure
        self._validate_data()

    def _validate_data(self):
        DeskEntryPositioning.model_validate(self.dep)
        DeskEntryStructure.model_validate(self.des)
        # try:
        #     DeskEntryPositioning.model_validate(self.dep)
        #     DeskEntryStructure.model_validate(self.dep)
        # except Exception as ex:
        #     exit_msg(72, f'Invoking data is invalid.\nvvv\n{ex}\n^^^\n')

    def get_generated_text(self):
        """
        Returns the content of the desktop icon file.
        Will return None if structure information is invalid"""
        environment = Environment()
        try:
            template_obj = environment.from_string(self.template_text)
            cont = template_obj.render(self.des)
        except:
            # if the jinja engine throws an error then return None
            print(f'Exception - jinja')
            cont = None
        return cont

    def get_path_of_desktop_file(self):
        """
        Derived from the base_dir and the entry_name.
        Will return None if the file al
        """
        base_dir = self.dep['dep_base_dir']
        entry = 'simpli-' + self.dep['dep_entry_name'] + '.desktop'
        if base_dir == '':
            path_name = os.path.join(os.path.expanduser("~"), os.path.join('Desktop', entry))
        else:
            path_name = os.path.join(base_dir, entry)
        return path_name

    def get_path_of_con_file(self):
        return self.des.icon

    def generate_file(self):
        """
        Writes the generated text to the required file.
        The destination file MUST NOT exist.
        The icon file must exist.
        """
        # if os.path.isfile(self.get_path_of_con_file()) == False : # icon file must exist
        #     return False

        filename = self.get_path_of_desktop_file()
        if os.path.isfile(filename): # desktop file must NOT exist
            return False
        text_content = self.get_generated_text()
        with open(filename, mode="w", encoding="utf-8") as message:
            message.write(text_content)
            os.chmod(filename, 0o755)
        if os.path.isfile(filename): # ensure that file exists
            return True

        if self.dep.dep_make_trusted:
            make_desktop_file_trusted_by_xfce(filename)

class IconCreationStatus(Enum):
    ICONFILECREATED = 1
    ICONNOTENABLED = 2
    COULDNOTWRITEFILE = 3
    FAILURETOPROCESSTEMPLATE = 4
    ASSERTERROR = 5
    TYPEERROR = 6
    OTHERERROR = 7

class DeskIcon:
    """
    Given the specified jinja template in the template file, it uses the provided_args
    to populate the necessary text in the file at the specified base_dir
    """
    def __init__(self, base_dir, template_file, provided_args):
        self.dest_dir = base_dir
        self.template_file = template_file
        self.provided_args = provided_args # dictionary
        self.extra_prefix = '' # 'X'
        self.FILE_PREFIX = self.extra_prefix + SIMPLI_PREFIX
        self.is_valid = False
        self._validate_args()

    def __str__(self):
        return f'DeskIcon\n\tTemplate file={self.template_file}\n\tBase dir={self.dest_dir}\n\tProvided args={self.provided_args}\n'

    def _validate_args(self):
        """Necessary validation checks for the object to be valid."""
        if not isinstance(self.provided_args, dict):
            print("is NOT dictionary")
            raise ValueError('Args is not a dictionary')

        entryname = self.provided_args.get('entry')
        if entryname is None:
            raise ValueError('Missing entry key')

        if not isinstance(entryname, str):
            print("is NOT string")
            raise ValueError('Entry field is not a string')

        if len(entryname) == 0:
            raise ValueError('Entry name is zero length')


    def dest_dir_is_valid(self):
        if os.path.isdir(self.dest_dir):
            return True
        else:
            return False

    def template_file_exists(self):
        if os.path.isfile(self.template_file):
            return True
        else:
            return False

    def paths_are_valid(self):
        if self.dest_dir_is_valid() and self.template_file_exists():
            return True
        else:
            return False


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


    # def generate_desktop_icon_text(self):
    #     #dict_of_vars_to_replace = self.provided_args  # dict({}
    #     # this loads the template file and then processes the string
    #     with open(self.template_file, 'r') as file:
    #         template_string = file.read()
    #     cont = IconText(template_string, self.provided_args).gen_icon_text()
    #     return cont


    def generate_desktop_file(self, make_trusted=False):
        # pp = pprint.PrettyPrinter(indent=4)
        # print('vvvvv')
        # pp.pprint(self.provided_args)
        # print('^^^^')
        if self.provided_args.get('enabled') != 'true':
            resp = IconCreationStatus.ICONNOTENABLED
        else:
            # attempt to create file as it is enabled
            #print(f'Template={self.template_file}')
            with open(self.template_file, 'r') as file:
                template_string = file.read()
            text_content = IconText(template_string, self.provided_args).gen_icon_text()
            if text_content is None:
                print(f'TemplateFile=={self.template_file}')
                resp = IconCreationStatus.FAILURETOPROCESSTEMPLATE
            else:
                filename = self.get_filename()
                #print(f'generate_desktop_file filename={filename}')
                try:
                    with open(filename, mode="w", encoding="utf-8") as message:
                        message.write(text_content)
                    renderop(f"... Created {filename}", Optype.DEBUG)
                    os.chmod(filename, 0o755)
                    resp = IconCreationStatus.ICONFILECREATED
                    if make_trusted:
                        make_desktop_file_trusted_by_xfce(filename)
                except TypeError as exception:
                    resp = IconCreationStatus.TYPEERROR
                except AssertionError as exception:
                    resp = IconCreationStatus.ASSERTERROR
                except BaseException as exception:
                    # print(f"Exception Name: {type(exception).__name__}")
                    # print(f"Exception Desc: {exception}")
                    resp = IconCreationStatus.OTHERERROR
        return resp

    def generate_trusted_desktop_file(self):
        resp = self.generate_desktop_file(make_trusted=True)
        return resp



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
        self.set_format_is_toml = None
        self.common = None
        self.entries = None
        self.toml_entries = None
        self.is_valid = False
        self._validate()

    def __str__(self):
        return f'IconSet\n\tTemplate file={self.template_file}\n\tIcon set file={self.icons_set_file}\n\tTarget dir={self.target_dir}\n'

    def _validate(self):
        if not os.path.isfile(self.template_file):
            return False
        if not os.path.isfile(self.icons_set_file):
            return False

        if self.icons_set_file.endswith('.yml'):
            self.set_format_is_toml = False
            self._validate_yaml(self.icons_set_file)
        elif self.icons_set_file.endswith('.toml'):
            self.set_format_is_toml = True
            self._validate_toml(self.icons_set_file)
        else:
            return False

        self.common = self.the_dict.get('common')
        if self.common is None:
            self._dump_structure()
            sys.exit('Structure is missing the "common" section in the icon file.')

        self._dump_structure()
        self.is_valid = True

    def _validate_toml(self, toml_set_file):
        with (open(toml_set_file, 'r') as file):
            catch_flag = True
            try:
                file_content = file.read()
                self.the_dict =tomllib.loads(file_content)
                # print(yaml.safe_load(stream))
            except tomllib.TOMLDecodeError as exc:
                sys.exit('Structure has malformed TOML in the icon file.')

            self.toml_entries = self.the_dict.get('entries')
            if self.toml_entries is None:
                self._dump_structure()
                sys.exit(f'Structure is missing the "toml_entries" section in the icon file ({toml_set_file}).')
            # we should check that for each there are the two entries : "entry" and "enabled"

    def _validate_yaml(self, yaml_set_file):
        with open(yaml_set_file) as stream:
            try:
                self.the_dict = yaml.safe_load(stream)
                # print(yaml.safe_load(stream))
            except yaml.YAMLError as exc:
                sys.exit('Structure has malformed YAML in the icon file.')

            self.entries = self.the_dict.get('entries')
            if self.entries is None:
                self._dump_structure()
                sys.exit(f'Structure is missing the "entries" section in the icon file ({yaml_set_file}).')
            # we should check that for each there are the two entries : "entry" and "enabled"

    def _dump_specific_struct(self, my_struct, header):
        json_object = json.dumps(my_struct, indent=4)
        print(f'STRUCT {header}\n{json_object}\nEND-STRUCT\n\n')

    def _dump_structure(self):
        if self.set_format_is_toml is True:
            desc = 'TOML'
        else:
            desc = 'YAML'
        self._dump_specific_struct(self.the_dict, desc)

    def is_valid_set(self):
        return self.is_valid

    def get_title(self):
        if self.set_format_is_toml:
            return self.the_dict.get('title')
        else:
            return None

    def get_common_attributes(self):
        return self.common

    def entry_exists(self, entry_name):
        if self.set_format_is_toml:
            found_it = self.toml_entries.get(entry_name)
            if found_it is None:
                resp = False
            else:
                resp = True
        else:
            resp = False
        return resp

    def list_of_all_entries(self):
        return list(self.toml_entries.keys())

    def num_all_icons(self):
        if self.set_format_is_toml:
            return len(self.list_of_all_entries())
        else:
            return len(self.entries)

    def get_full_filename_of_entry(self, the_entry):
        return self.FILE_PREFIX + the_entry + self.FILE_POSTFIX

    def list_icon_entries(self):
        enabled_icons = []
        disabled_icons = []
        if self.set_format_is_toml:
            app_entries = self.toml_entries
            for key in app_entries:
                print(f'Processing key {key}\n')
                #self._dump_specific_struct(app_entries[key], 'LISTENTRY' + key)
                if app_entries[key].get('enabled') == 'true':
                    enabled_icons.append(key)
                else:
                    disabled_icons.append(key)
        else:
            app_entries = self.entries
            for the_entry in app_entries:
                nam = the_entry['entry']
                if the_entry['enabled'] == 'true':
                    enabled_icons.append(nam)  # fullname
                else:
                    disabled_icons.append(nam)  # fullname
        return enabled_icons, disabled_icons

    def list_enabled_icons(self):
        enab, disab = self.list_icon_entries()
        return enab

    def num_enabled_icons(self):
        return len(self.list_enabled_icons())

    def list_enabled_icon_filenames(self):
        enab, disab = self.list_icon_entries()
        return list(map(lambda x: self.get_full_filename_of_entry(x) , enab))

    def get_target_dir(self):
        return self.target_dir

    def list_fullpath_icons_to_create(self):
        enab, disab = self.list_icon_entries()
        list_of_all_entries = list(map(lambda x: self.get_target_dir() + '/' + x, enab))
        return list_of_all_entries

    def get_raw_attribs_of_entry(self, entry_name):
        return self.toml_entries.get(entry_name)

    def get_attribs_of_entry(self, entry_name):
        """Will return None if the entry does not exist"""
        if self.set_format_is_toml:
            specific_dict = self.common.copy()
            raw_att = self.get_raw_attribs_of_entry(entry_name)
            if raw_att is None:
                specific_dict = None
            else:
                specific_dict.update(raw_att)
        else:
            specific_dict = self.common.copy()
            found_entry = False
            for ent in self.entries:
                if ent['entry'] == entry_name:
                    found_entry = True
                    specific_dict.update(ent)
                    del specific_dict['entry']
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
        invalid_entries = []
        for ent in self.list_enabled_icons():
            renderop(f'\nENTRY= {ent}', Optype.INFO)
            atts = self.get_attribs_of_entry(ent)
            atts['entry'] = ent
            try:
                iconobj = DeskIcon(self.target_dir, self.template_file, atts)
                #print(f'IconSet::generate_all_icons : {str(iconobj)} \n')
                if not fake_it:
                    iconobj.generate_desktop_file()
                    print(f'TRYING TO GNERATE DESKTOP FILE')
            except ValueError as exception:
                desc = str(exception)
                inval_entry = (desc, atts)
                invalid_entries.append(inval_entry)
                #print(f'Failed to create deskicon1 >>{desc}\nvvv\n{atts}\n^^^')

        bad_entries = len(invalid_entries)
        renderop(f'IconSet::generate_all_icons:', Optype.INFO)
        renderop(f'\tNumber of entries that failed={bad_entries}', Optype.INFO)
        if bad_entries > 0:
            for item in invalid_entries:
                descrip, the_struct = item
                #renderop(f'ENTRY= {ent}', Optype.INFO)
                renderop(f'\tError={descrip}', Optype.INFO)
                print(f'vvv{the_struct}\n^^^\n')

            # pp = pprint.PrettyPrinter(indent=4)
            # print('vvvvv')
            # pp.pprint(atts)
            # print('^^^^')

            # except BaseException as exception:
            #     print(f'Failed to create deskicon2')
            #     print(f"Exception Name: {type(exception).__name__}")
            #     print(f"Exception Desc: {exception}")

    # def dump_config_to_yaml_file(self, dump_name):
    #     is_successful = False
    #     thedict = dict({})
    #     thedict['common'] = self.common
    #     thedict['entries'] = self.entries
    #     yaml_string = yaml.dump(thedict)
    #
    #     if os.path.isfile(dump_name):
    #         return False # file must NOT exist
    #     file = open(dump_name, "w")
    #     yaml.dump(thedict, file)
    #     file.close()
    #
    #     if os.path.isfile(dump_name):
    #         return True # file must exist
    #     else:
    #         return False
    #
    # def dump_config_to_toml_file(self, dump_toml_name):
    #     pass




def derive_all_desktops(template_file, yaml_source_data, base_dir_for_icons, type_of_desktop):

    fname = 'derive_all_desktops'
    def show_invocation_args(tfile, srcy, dest_base_dir, tdesk):
        print(f'{fname}: ')
        print(f'\tTemplate= {tfile}')
        print(f'\tSourceData= {srcy}')
        print(f'\tDestBaseDir= {dest_base_dir}')
        print(f'\tDesktopType= {tdesk}')
        print('')

    show_invocation_args(template_file, yaml_source_data, base_dir_for_icons, type_of_desktop)
    #return None

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


def new_create_icons(template_file, config_file, desktop_dir):
    print(f'USING IconSet')
    iconset = IconSet(template_file, config_file, desktop_dir)
    print('IconSet details:\n{0}\n'.format(str(iconset)))
    print('Current Working Dir:\n{0}\n'.format(os.getcwd()))


    # Check files are present
    if iconset.is_valid_set():
        print(f'Valid files given')
    else:
        print(f'Invalid files specified')
        exit_msg(25, 'Invalid fies pecified')


    list_files_to_create = iconset.list_fullpath_icons_to_create()
    string_of_files = '\n\t'.join(list_files_to_create)
    print(f'List of files to create: \n{string_of_files}\n')


def legacy_invoke(template_file, config_file, desktop_dir):

    host_name = 'dev'
    if host_name != 'dev':
        myhome = '/home/simpli'
        simpli_config_dir = os.path.join(myhome, '.simpli/config')
        template_file =  os.path.join(simpli_config_dir, 'template.desktop')
        config_file = os.path.join(simpli_config_dir, 'desktop_known.yml')
        desktop_dir = os.path.join(myhome, 'xDesktop')

    derive_all_desktops(template_file, config_file, desktop_dir, 'xfce')


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
    newmode = True
    #the_mode = InvocationMode.ORIGINAL
    #the_mode = InvocationMode.LEGACYSIM
    the_mode = InvocationMode.NEW

    template = 'template.desktop'
    config = 'desktop_known.yml'
    dest = '/home/robertryan/zDesktop'

    print(f'DEST dir is : {dest}')
    exit_msg(0, 'ending while in testing phase')

    if the_mode == InvocationMode.LEGACYSIM:
        legacy_invoke(template, config, dest)
    elif the_mode == InvocationMode.ORIGINAL:
        create_desktop_icon_main()
    elif the_mode == InvocationMode.NEW:
        new_create_icons(template, config, dest)
    else:
        exit_msg(23, 'invalid invocation mode')


