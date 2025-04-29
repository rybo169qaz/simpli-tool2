#import errno
from copy import deepcopy
from xml.dom import ValidationErr

import jinja2.exceptions
from dictdiffer import diff, patch, swap, revert
import filecmp
import hashlib
import json
import os.path
#import pathlib
#from pathlib import Path
#import platform
import pytest
import tempfile
#import time

#import psutil
#import re
#import sys
import yaml
#from pathlib import Path
#from getmac import get_mac_address as gma

#from jinja2 import Environment, FileSystemLoader, Template
#from enum import Enum
#import subprocess
from create_desktop_icons import IconText, DeskIcon, IconSet
#from create_desktop_icons import IconNode
from create_desktop_icons import IconCreationStatus
from create_desktop_icons import DeskEntryStructure, DeskEntryPositioning, DeskEntryCreator
#from create_desktop_icons import generate_text_from_template

HOME_DIR = '/home/robertryan'
REPO_ROOT = HOME_DIR + '/' + 'PROJ2/SIMPLI-TOOL/GIT-REPO/simpli-tool2'
DESKTOP_CONFIG_DIR = REPO_ROOT + '/' + 'Deployment-Info/desktop/desktop-config'

DESKTOP_FILE_PREFIX = 'Xsimpli_'
DESKTOP_FILE_POSTFIX = '.desktop'
GOOD_TEMPLATE_FILE = 'template.desktop'

TEST_TEMPLATE_FILE = 'test_template.desktop'

TEST_TEMPLATE_TEXT_ORIG = [
    'River = {{ the_river }}' ,
    'Country ={{ the_country }}' ,
    'Sentence= In {{ the_country }} there is a river {{ the_river }} flowing through it.'
    ]

TEST_TEMPLATE_TEXT_NULL = [
    'River = ' ,
    'Country =' ,
    'Sentence= In  there is a river  flowing through it.'
    ]


# TEST_TEMPLATE_TEXT_SUBS = [
#     'River = Nile' ,
#     'Country =Egypt' ,
#     'Sentence= In Egypt there is a river Nile flowing through it.'
#     ]

SIMPLE_TEST_TEMPLATE_FILE = 'simple_test_template.desktop'

FULL_GOOD_TEMPLATE_PATH = DESKTOP_CONFIG_DIR + '/' + GOOD_TEMPLATE_FILE
FULL_TEST_TEMPLATE_PATH = DESKTOP_CONFIG_DIR + '/' + TEST_TEMPLATE_FILE
FULL_SIMPLE_TEST_TEMPLATE_PATH = DESKTOP_CONFIG_DIR + '/' + SIMPLE_TEST_TEMPLATE_FILE

TEST_ICON_YAML_SET = 'test_icon_set.yml'
FULL_TEST_ICON_YAML_SET = DESKTOP_CONFIG_DIR + '/' + TEST_ICON_YAML_SET

TEST_ICON_TOML_SET = 'test_icons.toml'
FULL_TEST_ICON_TOML_SET = DESKTOP_CONFIG_DIR + '/' + TEST_ICON_TOML_SET

WKG_DIR = REPO_ROOT + '/' + 'Deployment-Info/wkg-misc'

disabled_dict = dict({ 'entry': 'george', 'enabled': 'false'})
noname_dict = dict({ 'enabled': 'false'})
missing_entry_dict = dict({ 'fish': 'cod', 'enabled': 'true'})
good_dict = dict({ 'entry': 'fred', 'enabled': 'true'})



def display_text(the_string, description):
    bar_size = 7
    start_text = 'v' * bar_size
    end_text = '^' * bar_size
    print(f'\n{start_text} START OF: {description} {start_text}')
    print(the_string)
    print(f'{end_text} END OF: {description} {end_text}\n')

def display_file(filename, desc = ''):
    with open(filename, 'r') as file:
        file_content = file.read()
    display_text(file_content, desc + ': File==' + filename)

@pytest.mark.icontext
class TestIconText:

    def test_missing_one_param(self):
        args_dict = dict({'field1': 'abc', 'field3': 'xyz'})
        template_text = "INITIAL={{ field1  }} FIRST {{ fields2 }} SECOND{{  field1 }}NOSPACE{{  field1  }}"
        assert IconText(template_text, args_dict).gen_icon_text() is None

    def test_missing_all_params(self):
        icontext1 = IconText("BEFORE {{ field1 }} MID {{ field2 }} AFTER", dict({}))
        assert icontext1.gen_icon_text() is None

    def test_empty_template_text(self):
        assert IconText("", dict({'first': 'xxfirstxxx', 'second': 'xxsecondxx'})).gen_icon_text() == ""

    def test_template_single_brace_not_expanded(self):
        template_single_open_brace = "Other={ field1 }} PACK"
        assert IconText(template_single_open_brace, dict({'first': 1, 'second': 2})).gen_icon_text() == template_single_open_brace

    def test_template_bad_syntax(self):
        assert IconText("Other={{ field1 } PACK", dict({'first': 1, 'second': 2})).gen_icon_text() == None

    def test_bad_arg_name_starts_wth_numeric(self):
        # jinja does not allow args which start with non-alpha : parameter name starts with numeric
        assert IconText("BEFORE {{ 9abcde }} AFTER", dict({'9abcde': 'xyz'})).gen_icon_text() == None

        # jinja does not allow args which start with non-alpha : use non-alpha
        assert IconText("BEFORE {{ +abcde }} AFTER", dict({'+abcde': 'xyz'})).gen_icon_text() == None

    def test_template_multiple_on_same_line(self):
        assert IconText("Other={{ field1 }} PACK {{ field1 }}", dict({'field1': 'xyz'})).gen_icon_text() == "Other=xyz PACK xyz"

    def test_template_extra_space_after_open_brace(self):
        # jinja allows extra spaces in the braces - it appears
        assert IconText("BEFORE{{  first }}AFTER", dict({'first': 'abc', 'second': 'rst'})).gen_icon_text() == "BEFOREabcAFTER"

    def test_template_extra_space_before_closing_brace(self):
        # It appears trailing spaces before closing do not get checked for
        assert IconText("BEFORE{{ first  }}AFTER", dict({'first': 1, 'second': 2})).gen_icon_text() == "BEFORE1AFTER"

        template_extra_space_before_and_after = "BEFORE{{  first  }}AFTER"
        assert IconText(template_extra_space_before_and_after, dict({'first': 1, 'second': 2})).gen_icon_text() == "BEFORE1AFTER"

    def test_long_arg_name(self):
        assert ((IconText("A {{ a2bcdefghijklmnopqrstuvwxyz }} B {{ field2 }} C",
                        dict({'a2bcdefghijklmnopqrstuvwxyz': 'xyz', 'field2': 'FISH'})).gen_icon_text()) == "A xyz B FISH C")

    def test_template_spaces_preserved_around_body_text(self):
        assert IconText("X{{  first }}Y {{  second }}  Z  {{ third  }}T",
                        dict({'first': 'abc', 'second': 'rst', 'third': 'xyz'})).gen_icon_text() == "XabcY rst  Z  xyzT"

def create_test_folder():
    # create a temporary directory
    tmpdir = tempfile.TemporaryDirectory(dir="/tmp", prefix="simpli_").name
    os.mkdir(tmpdir, 0o777)  # we create the dest dir
    # print(f'XYZ Tempdir = {tmpdir}')
    if os.path.isdir(tmpdir) == False:
        raise ValueError('Failed to create temp directory')
    return tmpdir

PYT_PRE = 'Pytest Pre-condition test failed. Test framework has an error'

@pytest.mark.deskicon
class TestDeskIcon:

    def test_not_a_dict(self):
        with pytest.raises(ValueError) as excinfo:
            DeskIcon(create_test_folder(), FULL_GOOD_TEMPLATE_PATH, 123)
        assert str(excinfo.value) == 'Args is not a dictionary'

    def test_entry_is_missing(self):
        with pytest.raises(ValueError) as excinfo:
            sam = {'fruit': 'orange'}
            if type(missing_entry_dict) is dict:
                print('IS DICT')
            else:
                print('IS NOT DICT')
            DeskIcon(create_test_folder(), FULL_GOOD_TEMPLATE_PATH, missing_entry_dict)
        assert str(excinfo.value) == 'Missing entry key'

    def test_entry_is_not_a_string(self):
        with pytest.raises(ValueError) as excinfo:
            empty_entry = deepcopy(missing_entry_dict)
            empty_entry['entry'] = 123
            DeskIcon(create_test_folder(), FULL_GOOD_TEMPLATE_PATH, empty_entry)
        assert str(excinfo.value) == 'Entry field is not a string'

    def test_entry_is_zero_length(self):
        with pytest.raises(ValueError) as excinfo:
            entry_is_zero_length = deepcopy(missing_entry_dict)
            entry_is_zero_length['entry'] = ''
            DeskIcon(create_test_folder(), FULL_GOOD_TEMPLATE_PATH, entry_is_zero_length)
        assert str(excinfo.value) == 'Entry name is zero length'

    def test_bad_destdir(self):
        dest1 = DeskIcon(create_test_folder(), FULL_GOOD_TEMPLATE_PATH, good_dict)
        assert dest1.dest_dir_is_valid() == True

        non_existant_dir = os.path.join(create_test_folder(), 'abc')
        dest2 = DeskIcon(non_existant_dir, FULL_GOOD_TEMPLATE_PATH, good_dict)
        assert dest2.dest_dir_is_valid() == False

    def test_template_file(self):
        template1 = DeskIcon(create_test_folder(), FULL_GOOD_TEMPLATE_PATH, dict({'entry': 'dummy'}))
        assert template1.template_file_exists() == True

        non_existant_file = os.path.join(create_test_folder(), 'not-a-file')
        template2 = DeskIcon(create_test_folder(), non_existant_file, good_dict)
        assert template2.template_file_exists() == False

    def test_get_filename(self):
        ent_name = 'felix'
        attribs_dict = dict({'entry': ent_name})
        desk1_fname = DeskIcon(create_test_folder(), FULL_GOOD_TEMPLATE_PATH, attribs_dict).get_filename()
        assert os.path.basename(desk1_fname) == DESKTOP_FILE_PREFIX + ent_name + DESKTOP_FILE_POSTFIX

    def test_created_icon_file_path(self):
        tempdir = create_test_folder()
        desk3_fname = DeskIcon(tempdir, FULL_GOOD_TEMPLATE_PATH, good_dict).get_filename()
        assert os.path.dirname(desk3_fname) == tempdir

    def test_generate_desktop_file_enabled_false(self):
        # check that if not enabled then no file is to be created
        desk_not_enabled = DeskIcon(create_test_folder(), FULL_GOOD_TEMPLATE_PATH, dict({'entry': 'test_not_enabled', 'enabled': 'false'}))
        assert desk_not_enabled.generate_desktop_file() == IconCreationStatus.ICONNOTENABLED
        assert os.path.isfile(desk_not_enabled.get_filename()) is False # check that expected file does not exist

        # if enabled field not specified then it will be disabled
        desk_not_specify_enabled = DeskIcon(create_test_folder(), FULL_GOOD_TEMPLATE_PATH, dict({'entry': 'test_not_specify_enabled'}))
        assert desk_not_specify_enabled.generate_desktop_file() == IconCreationStatus.ICONNOTENABLED
        assert os.path.isfile(desk_not_specify_enabled.get_filename()) is False

    def test_generate_desktop_enabled_is_true(self):
        tmpdir = create_test_folder()

        expected_path = tmpdir + '/' + 'X' + 'simpli_' + 'test_content' + '.desktop'
        if os.path.isfile(expected_path): raise RuntimeError(f'{PYT_PRE} File already exists')

        the_dict = dict({'entry': 'test_content', 'enabled': 'true'})
        the_dict['the_river'] = 'abc'
        the_dict['the_country'] = 'pqr'
        desk_enabled = DeskIcon(tmpdir, FULL_TEST_TEMPLATE_PATH, the_dict)
        resp = desk_enabled.generate_desktop_file()
        assert resp == IconCreationStatus.ICONFILECREATED
        assert os.path.isfile(expected_path)  # check that expected file really exists

    def test_generate_desktop_missing_param_expansion(self):
        tmpdir = create_test_folder()

        expected_path = tmpdir + '/' + 'X' + 'simpli_' + 'test_content' + '.desktop'
        if os.path.isfile(expected_path): raise RuntimeError(f'{PYT_PRE} File already exists')

        the_dict = dict({'entry': 'test_content', 'enabled': 'true'})
        the_dict['the_river'] = 'abc'
        #the_dict['the_country'] = 'pqr'
        desk_enabled = DeskIcon(tmpdir, FULL_TEST_TEMPLATE_PATH, the_dict)
        resp = desk_enabled.generate_desktop_file()
        assert resp == IconCreationStatus.FAILURETOPROCESSTEMPLATE
        assert os.path.isfile(expected_path) == False # check that file has not been created


def write_text_to_file(dest_dir, filename, text_to_use):
    full_path_filename = os.path.join(dest_dir, filename)
    if os.path.isfile(full_path_filename): raise RuntimeError(f'{PYT_PRE} File already exists')

    with open(full_path_filename, mode="w", encoding="utf-8") as message:
        message.write(text_to_use)
    if os.path.isfile(full_path_filename) is False:
        raise ValueError('write_text_to_file: failed to create file')
    return full_path_filename

@pytest.mark.iconset
class TestIconSet:

    def test_basic_yaml_test(self):
        good_set_and_template = IconSet(FULL_SIMPLE_TEST_TEMPLATE_PATH, FULL_TEST_ICON_YAML_SET, create_test_folder())
        assert good_set_and_template.is_valid_set() == True

    def test_invalid_yaml_template_file_identified(self):
        bad_template = IconSet('abc', FULL_TEST_ICON_YAML_SET, create_test_folder())
        assert bad_template.is_valid_set() == False

    def test_invalid_yaml_set_file_identified(self):
        bad_set = IconSet(FULL_SIMPLE_TEST_TEMPLATE_PATH, 'abc', create_test_folder())
        assert bad_set.is_valid_set() == False

    def test_get_title(self):
        # This is only available in the TOML format
        good_yaml_set_and_template = IconSet(FULL_SIMPLE_TEST_TEMPLATE_PATH, FULL_TEST_ICON_YAML_SET, create_test_folder())
        assert good_yaml_set_and_template.get_title() is None

        good_toml_set_and_template = IconSet(FULL_SIMPLE_TEST_TEMPLATE_PATH, FULL_TEST_ICON_TOML_SET, create_test_folder())
        assert good_toml_set_and_template.get_title() == "Config data for desktop icons"


    def test_get_common_attributes(self):
        expected_common = {'vlc': '/etc/bin/vlc',
                           'com2': 222,
                           'the_river': 'Amazon'
                           }
        good_yaml_set_and_template = IconSet(FULL_SIMPLE_TEST_TEMPLATE_PATH, FULL_TEST_ICON_YAML_SET, WKG_DIR)
        assert good_yaml_set_and_template.get_common_attributes() == expected_common

        good_toml_set_and_template = IconSet(FULL_SIMPLE_TEST_TEMPLATE_PATH, FULL_TEST_ICON_TOML_SET, WKG_DIR)
        assert good_toml_set_and_template.get_common_attributes() == expected_common

    def test_entry_exists(self):
        toml_entry_exists = IconSet(FULL_SIMPLE_TEST_TEMPLATE_PATH, FULL_TEST_ICON_TOML_SET, create_test_folder())
        assert toml_entry_exists.entry_exists('mountain_everest') == True
        assert toml_entry_exists.entry_exists('nonexistantentry') == False

    def test_list_and_num_of_all_entries(self):
        iconset = IconSet(FULL_SIMPLE_TEST_TEMPLATE_PATH, FULL_TEST_ICON_TOML_SET, create_test_folder())
        expected_entries = ['country_france', 'country_the_netherlands', 'mountain_everest', 'mountain_mount-blanc']
        assert iconset.list_of_all_entries() == expected_entries
        assert iconset.num_all_icons() == 4

    def test_num_all_icons(self):
        good_yaml_set_and_template = IconSet(FULL_SIMPLE_TEST_TEMPLATE_PATH, FULL_TEST_ICON_YAML_SET, create_test_folder())
        assert good_yaml_set_and_template.num_all_icons() == 4

        good_toml_set_and_template = IconSet(FULL_SIMPLE_TEST_TEMPLATE_PATH, FULL_TEST_ICON_TOML_SET, create_test_folder())
        assert good_toml_set_and_template.num_all_icons() == 4


    def test_num_enabled_icons(self):
        good_yaml_set_and_template = IconSet(FULL_SIMPLE_TEST_TEMPLATE_PATH, FULL_TEST_ICON_YAML_SET, create_test_folder())
        assert good_yaml_set_and_template.num_enabled_icons() == 3

        good_toml_set_and_template = IconSet(FULL_SIMPLE_TEST_TEMPLATE_PATH, FULL_TEST_ICON_TOML_SET, create_test_folder())
        assert good_toml_set_and_template.num_enabled_icons() == 3


    def test_enabled_disabled_icons(self):
        enabled_entries = ['country_france', 'mountain_everest', 'mountain_mount-blanc']

        good_yaml_set_and_template = IconSet(FULL_SIMPLE_TEST_TEMPLATE_PATH, FULL_TEST_ICON_YAML_SET, create_test_folder())
        good_toml_set_and_template = IconSet(FULL_SIMPLE_TEST_TEMPLATE_PATH, FULL_TEST_ICON_TOML_SET, create_test_folder())
        assert good_yaml_set_and_template.list_enabled_icons() == enabled_entries
        assert good_toml_set_and_template.list_enabled_icons() == enabled_entries

        disabled_entries = ['country_the_netherlands']  # netherlands is disabled
        #assert good_yaml_set_and_template.list_disabled_icons() == disabled_entries
        #assert good_toml_set_and_template.list_disabled_icons() == disabled_entries


    def test_list_enabled_icon_filenames(self):
        enabled_entries = ['simpli_country_france.desktop',  'simpli_mountain_everest.desktop', 'simpli_mountain_mount-blanc.desktop']
        good_yaml_set_and_template = IconSet(FULL_SIMPLE_TEST_TEMPLATE_PATH, FULL_TEST_ICON_YAML_SET, create_test_folder())
        good_toml_set_and_template = IconSet(FULL_SIMPLE_TEST_TEMPLATE_PATH, FULL_TEST_ICON_TOML_SET, create_test_folder())
        assert good_yaml_set_and_template.list_enabled_icon_filenames() == enabled_entries
        assert good_toml_set_and_template.list_enabled_icon_filenames() == enabled_entries


    def test_icons_generated_in_correct_dir(self):
        tmpdir = create_test_folder()

        good_yaml_set_and_template = IconSet(FULL_SIMPLE_TEST_TEMPLATE_PATH, FULL_TEST_ICON_YAML_SET, tmpdir)
        assert good_yaml_set_and_template.get_target_dir() == tmpdir

        good_toml_set_and_template = IconSet(FULL_SIMPLE_TEST_TEMPLATE_PATH, FULL_TEST_ICON_TOML_SET, tmpdir)
        assert good_toml_set_and_template.get_target_dir() == tmpdir

    def test_get_raw_attribs_of_entry(self):
        expected_raw_mtblanc = {
            'enabled': 'true',
            'icon': "photo_of_mt_blanc",
            'description': "Mt Blanc",
            'tool_command': '/pqr/display_height',
            'command_args': '3210 metres'
        }
        iset = IconSet(FULL_SIMPLE_TEST_TEMPLATE_PATH, FULL_TEST_ICON_TOML_SET, create_test_folder())
        assert iset.get_raw_attribs_of_entry('mountain_mount-blanc') == expected_raw_mtblanc
        assert iset.get_raw_attribs_of_entry('unknown-entry') == None


    def test_attributes_of_entry(self):
        good_yaml_set_and_template = IconSet(FULL_SIMPLE_TEST_TEMPLATE_PATH, FULL_TEST_ICON_YAML_SET, create_test_folder())
        good_toml_set_and_template = IconSet(FULL_SIMPLE_TEST_TEMPLATE_PATH, FULL_TEST_ICON_TOML_SET, create_test_folder())

        expected_everest = {
            'enabled': 'true',
            'the_river': 'Amazon',
            'vlc': '/etc/bin/vlc',
            'com2': 'newcom2',
            'icon': "nepal_photo",
            'description': "Everest",
            'tool_command': '/pqr/display_height',
            'command_args': '5678 metres'
        }
        assert good_yaml_set_and_template.get_attribs_of_entry('mountain_everest') == expected_everest
        assert good_toml_set_and_template.get_attribs_of_entry('mountain_everest') == expected_everest

        expected_netherlands = {
            'enabled': 'false',
            'the_river': 'Amazon',
            'vlc': '/etc/bin/vlc',
            'com2': 222,
            'icon': "dutch_flag",
            'description': "Holland",
            'tool_command': '/abc/show-flag',
            'command_args': 'dutch_flag'
        }
        assert good_yaml_set_and_template.get_attribs_of_entry('country_the_netherlands') == expected_netherlands
        assert good_toml_set_and_template.get_attribs_of_entry('country_the_netherlands') == expected_netherlands

        assert good_yaml_set_and_template.get_attribs_of_entry('unknown_entry') == None
        assert good_toml_set_and_template.get_attribs_of_entry('unknown_entry') == None


    def test_only_enabled_files_created(self):
        # This should be mocked

        destdir_yaml = create_test_folder()
        destdir_toml = create_test_folder()

        # FULL_TEST_ICON_TOML_SET
        # FULL_TEST_TEMPLATE_PATH
        good_yaml_set_and_template = IconSet(FULL_TEST_TEMPLATE_PATH, FULL_TEST_ICON_YAML_SET, destdir_yaml)
        good_toml_set_and_template = IconSet(FULL_TEST_TEMPLATE_PATH, FULL_TEST_ICON_TOML_SET, destdir_toml)
        print(f'test_only_enabled_files_created : {str(good_yaml_set_and_template)} \n')
        print(f'test_only_enabled_files_created : {str(good_toml_set_and_template)} \n')

        good_yaml_set_and_template.generate_all_icons(False)
        good_toml_set_and_template.generate_all_icons(False)

        enabled_entries = ['Xsimpli_country_france.desktop', 'Xsimpli_mountain_everest.desktop',
                           'Xsimpli_mountain_mount-blanc.desktop']

        list_of_wanted_yaml_files = list(map(lambda x: os.path.join(destdir_yaml, x), enabled_entries))
        for i in list_of_wanted_yaml_files:
            assert os.path.isfile(i) is True

        list_of_wanted_toml_files = list(map(lambda x: os.path.join(destdir_toml, x), enabled_entries))
        for i in list_of_wanted_toml_files:
            assert os.path.isfile(i) is True

        # check that files in yaml and toml dest folders are the same
        for file in enabled_entries:
            #(matching, mismatching, errs) = filecmp.cmpfiles(destdir_yaml, destdir_toml, file) is True
            yaml_file = os.path.join(destdir_yaml, file)
            toml_file = os.path.join(destdir_toml, file)
            assert filecmp.cmp(yaml_file, toml_file) is True


        disabled_entries = ['simpli_country_the_netherlands.desktop']

        list_of_unwanted_yaml_files = list(map(lambda x: os.path.join(destdir_yaml, x), disabled_entries))
        for i in list_of_unwanted_yaml_files:
            assert os.path.isfile(i) is False

        list_of_unwanted_toml_files = list(map(lambda x: os.path.join(destdir_toml, x), disabled_entries))
        for i in list_of_unwanted_toml_files:
            assert os.path.isfile(i) is False

        #assert False

    def test_dump_config_to_file(self):
        '''
        Checks whether the dumped data file representing the icon-set matches what
        is used when loading.
        Note: because there are multiple representations of the same data, and the
        input file is not necessarily canonical, then rather than check the text in
        the file, it is better to check the dictionary/structure that is obtained when loaded.
        If at some point we may be able to specify the layout of data (say using pydantic)
        then we may be able revert to file comparision.
        '''

        def calculate_md5(file_path):
            hasher = hashlib.md5()
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    hasher.update(chunk)
            return hasher.hexdigest()

        def compare_struct_from_yaml_file(fileA, fileB):
            # see https://miguendes.me/the-best-way-to-compare-two-dictionaries-in-python
            # use dictdiffer (as deepdiff encountered error)
            # https://dictdiffer.readthedocs.io/en/latest/
            resp = True
            print(f'Comparing \n\t"{fileA}" and \n\t"{fileB}"\n')
            with open(fileA, 'r') as f:
                dataA = yaml.load(f, Loader=yaml.SafeLoader)
            with open(fileB, 'r') as f:
                dataB = yaml.load(f, Loader=yaml.SafeLoader)

            # bodge dataB for testing purposes
            if False:
                dataB['common']['extra_common_value'] = 'unwanted_common_value'
                # entries = dataB['entries']['extra_common_value'] = 'unwanted_common_value'
                # entries.append({'unwanted_entry_key': 'unwanted_entry_value'})

            result = diff(dataA, dataB)
            list_info = list(result)
            print(f'Comparison >>{list_info}<<')
            assert list_info == []
            return resp

        tmpdir = create_test_folder()

        wkg_set = IconSet(FULL_GOOD_TEMPLATE_PATH, FULL_TEST_ICON_YAML_SET, tmpdir)
        dump_file = tmpdir + '/' + 'dumped.txt'
        assert os.path.isfile(FULL_TEST_ICON_YAML_SET) == True
        assert os.path.isfile(dump_file) == False # ensure file doe snot exist

        dump_success = wkg_set.dump_config_to_yaml_file(dump_file)
        assert dump_success == True

        #compare two files
        assert os.path.isfile(dump_file) == True # ensure file now exists
        #assert calculate_md5(FULL_TEST_ICON_YAML_SET) == calculate_md5(dump_file)

        # compare structures obtained when loading the files
        assert compare_struct_from_yaml_file(FULL_TEST_ICON_YAML_SET, dump_file) == True

        #assert False



# @pytest.mark.skip # @pytest.mark.iconnode
# class TestIconNode:
#
#     def test_get_node_name(self):
#         node1 = IconNode('first', 'fruit', {})
#         assert node1.get_node_name() == 'first'
#
#     def test_get_get_child_type(self):
#         node2 = IconNode('first', 'fish', {})
#         assert node2.get_child_type() == 'fish'
#
#     def test_get_list_attribute_names(self):
#         node3 =IconNode('animals', 'fish', {'eggs': 'brown', 'dogs': '0', 'cats': 42})
#         assert node3.get_list_attribute_names() == ['cats', 'dogs', 'eggs']
#
#     def test_get_attribute_value(self):
#         node4 = IconNode('animals', 'fish', {'eggs': 'brown', 'dogs': '0', 'cats': 42})
#         assert node4.get_attribute_value('cats') == 42
#         assert node4.get_attribute_value('eggs') == 'brown'
#         assert node4.get_attribute_value('trees') == None
#
#     def test_get_count_of_children(self):
#         node5 = IconNode('first', 'fruit', {})
#         assert node5.get_count_of_children() == 0
#         node5 = IconNode('animals', 'fish', {'eggs': 'brown', 'dogs': '0', 'cats': 42})
#         assert node5.get_count_of_children() == 0
#
#     def test_add_child(self):
#         nodeA = IconNode('first', 'fruit', {})
#         assert nodeA.add_child('notfruit', 'key_pqr', 'value_pqr') == False
#         assert nodeA.add_child('fruit', 'key_pqr', 'value_pqr') == True
#
#
#     def test_get_list_of_children_names(self):
#         node7 = node5 = IconNode('root', 'category', {})
#         assert node7.get_list_of_children_names() == []
#         node7.add_child('category', 'key_pqr', 'value_pqr')
#         assert node7.get_list_of_children_names() == ['key_pqr']
#
#         node7.add_child('category', 'key_new', 'value_new')
#         assert node7.get_list_of_children_names() == ['key_new', 'key_pqr']
#
#         node7.add_child('category', 'key_alpha', 'value_alpha')
#         assert node7.get_list_of_children_names() == ['key_alpha', 'key_new', 'key_pqr']
#
#     def test_get_child_of_given_name(self):
#         node8 = IconNode('animals', 'fish', {'eggs': 'brown', 'dogs': '0', 'cats': 42})
#         assert node8.get_child_of_given_name('fred') == None
#         node8.add_child('fish', 'key_alpha', 'value_alpha')
#         node8.add_child('fish', 'key_new', 'value_new')
#         assert node8.get_child_of_given_name('key_new') == 'value_new'
#         #node8.print()
#
#     def test_integration(self):
#         nodeC = IconNode('root', 'categories', {'cat_att1': 'at1_val', 'cat_att2': 'att2val', 'catatt3': 42})
#         #nodeC.print()
#
#         mountain_everest = IconNode('everest', None, {'height': 9999, 'conquered_by': 'Mallory', 'country': 'Tibet'})
#         mountain_mtblanc = IconNode('Mt Blanc', None, {'height': 123, 'conquered_by': 'Unknown', 'country': 'France'})
#
#         mountains = IconNode('mountain_info', 'mountain', {'madeOf': 'rock', 'activity': 'climbable'})
#         assert mountains.add_child('mountain', 'everest', mountain_everest) == True
#         assert mountains.add_child('mountain', 'Mt Blanc', mountain_mtblanc) == True
#
#         root_node = IconNode('root_info', 'mountains', {'vlcPath': '/abc/def', 'description': 'Media playing tool'})
#         assert root_node.add_child('mountains', 'mountaininfo', mountains) == True
#         root_node.print_node()
#         root_node.print_full_node()




@pytest.mark.deskentrystruct
class TestDeskEntryStructure:

    def test_good_des(self):
        minimal_pop = {
            "description": "desc",
            "tool_command": "toolcmd",
            "command_args": "cmdargs",
            "icon": "iconfile"
        }

        de_min = DeskEntryStructure.model_validate(minimal_pop)
        assert de_min.description == 'desc'
        assert de_min.client_hostname == 'UNK-CLIENT'
        assert de_min.comment == 'NO COMMENT'
        assert de_min.tool_command == 'toolcmd'
        assert de_min.command_args == 'cmdargs'
        assert de_min.icon == 'iconfile'

        partial_pop = dict(minimal_pop)
        partial_pop["desktop_categories"] = ""
        partial_pop["kde_protocols"] = "kdeprot"
        partial_pop["keywords"] = ""

        de_partial = DeskEntryStructure.model_validate(partial_pop)
        assert de_partial.description == 'desc'
        assert de_partial.desktop_categories == ''
        assert de_partial.kde_protocols == 'kdeprot'
        assert de_partial.keywords == ''

        fully_pop = dict(partial_pop)
        fully_pop["desktop_categories"] = "deskcat"
        fully_pop["keywords"] = "keyw"

        de_full = DeskEntryStructure.model_validate(fully_pop)
        assert de_full.description == 'desc'
        assert de_full.desktop_categories == 'deskcat'
        assert de_full.keywords == 'keyw'


    def test_bad_des(self):
        missing_description = {
            "tool_command": "toolcmd",
            "command_args": "cmdargs",
            "icon": "iconfile"
        }
        with pytest.raises(Exception) as e_info:
            de_no_desc = DeskEntryStructure.model_validate(missing_description)

        missing_command_args = {
            "tool_command": "toolcmd",
            "description": "mydesc",
            "icon": "iconfile"
        }
        with pytest.raises(Exception) as e_info:
            de_no_cmd_args = DeskEntryStructure.model_validate(missing_command_args)


@pytest.mark.deskentrypositioning
class TestDeskEntryPositioning:
    """
    Is there any point in testing the Pydantic structures?
    """

    def test_good_dep(self):
        minimal_dep = {
            "dep_base_dir": "",
            "dep_entry_name": "fish",
            "dep_make_trusted": True
        }
        dep_minimal = DeskEntryPositioning.model_validate(minimal_dep)
        assert dep_minimal.dep_base_dir == ''
        assert dep_minimal.dep_entry_name == 'fish'

        # partial_dep = dict(minimal_dep)
        # partial_dep["dep_relative_dir"] = "fgh"
        # dep_partial = DeskEntryPositioning.model_validate(partial_dep)
        # assert dep_partial.dep_relative_dir == 'fgh'


    def test_bad_dep(self):
        missing_entry = {
            "dep_make_trusted": True
        }
        with pytest.raises(Exception) as e_info:
            dep_no_entry = DeskEntryPositioning.model_validate(missing_entry)

        # missing_trusted = {
        #     "dep_entry_name": "abc"
        # }
        # with pytest.raises(Exception) as e_info:
        #     dep_no_trusted = DeskEntryPositioning.model_validate(missing_trusted)


@pytest.mark.deskentrycreator
class TestDeskEntryCreator:

    whoami = "robertryan"

    # negative tests
    def test_bad_structural_data(self):
        struct_missing_tool_cmd = {
            "de_description": "mydesc",
            "de_command_args": "cmdargs",
            "de_icon_file": "iconfile"
        }
        struct_good_struct = {
            "de_description": "mydesc",
            "de_tool_command": "toolcmd",
            "de_command_args": "cmdargs",
            "de_icon_file": "iconfile"
        }

        position_missing_entry = {
        }
        position_good_abs_base = {
            "dep_base_dir": '/tmp/simpli',
            "dep_entry_name": "apple"
        }
        position_good_no_base = {
            "dep_base_dir": '',
            "dep_entry_name": "berry"
        }

        with pytest.raises(Exception) as e_info:
            DeskEntryCreator(struct_missing_tool_cmd,
                                position_good_no_base, None)

        with pytest.raises(Exception) as e_info:
            DeskEntryCreator(struct_good_struct,
                                position_missing_entry, None)

    def test_path(self):
        struct_good_struct = {
            "description": "mydesc",
            "tool_command": "toolcmd",
            "command_args": "cmdargs",
            "icon": "iconfile"
        }
        pos_good_abs_base = {
            "dep_base_dir": '/tmp/simpli',
            "dep_entry_name": "pathCheckApple"
        }
        position_good_no_base = {
            "dep_base_dir": '',
            "dep_entry_name": "pathCheckBerry"
        }

        dec_abs_base = DeskEntryCreator(struct_good_struct, pos_good_abs_base, None)
        assert dec_abs_base.get_path_of_desktop_file() == '/tmp/simpli/simpli-pathCheckApple.desktop'

        dec_no_base = DeskEntryCreator(struct_good_struct, position_good_no_base, None)
        who_i_am = 'robertryan'
        assert dec_no_base.get_path_of_desktop_file() == '/home/' + who_i_am + '/Desktop/simpli-pathCheckBerry.desktop'

    def test_content(self):
        tmpdir = tempfile.TemporaryDirectory(dir="/tmp", prefix="SIMPLI_").name
        os.mkdir(tmpdir, 0o777)  # we create the dest dir

        pos_good_abs_base = {
            "dep_base_dir": tmpdir,
            "dep_entry_name": "content-apple"
        }
        struct_good_struct = {
            "description": "mydesc",
            "tool_command": "toolcmd",
            "command_args": "cmdargs",
            "icon": "iconfile"
        }
        template_text = "A {{ description }} B {{ tool_command }} C {{ command_args }} D {{ icon }} E"
        expected_text = "A mydesc B toolcmd C cmdargs D iconfile E"
        dec = DeskEntryCreator(struct_good_struct, pos_good_abs_base, template_text)
        assert dec.get_generated_text() == expected_text

    def test_file_generation(self):


        tmpdir = tempfile.TemporaryDirectory(dir="/tmp", prefix="SIMPLI_").name
        os.mkdir(tmpdir, 0o777)  # we create the dest dir

        # create a dummy icon file
        icon_file_path = os.path.join(tmpdir, 'dumicon')
        open(icon_file_path, 'w')
        # the following line should not be an assert as it is part of the setting up of the test
        #assert os.path.isfile(icon_file_path) # ensure that the dummy icon file exists

        struct_good_struct = {
            "description": "mydesc",
            "tool_command": "toolcmd",
            "command_args": "cmdargs",
            "icon": icon_file_path
        }
        template_text = "A {{ description }} B {{ tool_command }} C {{ command_args }} D {{ icon }} E"
        expected_text = "A mydesc B toolcmd C cmdargs D " + icon_file_path + " E"

        pos_good_abs_base_no_checksum = {
            "dep_base_dir": tmpdir,
            "dep_entry_name": "fileGenFig"
        }
        dec_no_cs = DeskEntryCreator(struct_good_struct, pos_good_abs_base_no_checksum, template_text)
        expected_file = os.path.join(tmpdir, 'simpli-fileGenFig.desktop')
        assert os.path.isfile(expected_file) == False
        assert dec_no_cs.generate_file() == True
        assert os.path.isfile(expected_file) == True

        pos_good_abs_base_with_checksum = {
            "dep_base_dir": tmpdir,
            "dep_entry_name": "fileGenPear",
            "dep_make_trusted": False
        }
        dec_cs = DeskEntryCreator(struct_good_struct, pos_good_abs_base_with_checksum, template_text)
        expected_file = os.path.join(tmpdir, 'simpli-fileGenPear.desktop')
        assert os.path.isfile(expected_file) == False
        assert dec_cs.generate_file() == True
        assert os.path.isfile(expected_file) == True

        # read back contents
        with open(expected_file, 'r') as file:
            file_content = file.read()
        assert file_content == expected_text

