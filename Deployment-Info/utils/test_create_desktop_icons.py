#import errno
from dictdiffer import diff, patch, swap, revert
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


TEST_TEMPLATE_TEXT_SUBS = [
    'River = Nile' ,
    'Country =Egypt' ,
    'Sentence= In Egypt there is a river Nile flowing through it.'
    ]

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

    def test_no_args_to_sub(self):
        simple_template_text = "BEFORE {{ field1 }} MID {{ field2 }} AFTER"
        expected_icon_text = "BEFORE  MID  AFTER"
        icontext1 = IconText(simple_template_text, dict({}))
        assert icontext1.gen_icon_text() == expected_icon_text


    def test_empty_template_text(self):
        args_dict = dict({'first': 'xxfirstxxx', 'second': 'xxsecondxx'})
        icontext2 = IconText("", args_dict)
        assert icontext2.gen_icon_text() == ""
        assert IconText("", args_dict).gen_icon_text() == ""


    def test_template_bad_syntax(self):
        args_dict = dict({'first': 'xxfirstxxx', 'second': 'xxsecondxx'})
        template_missing_brace1 = "Other={ field1 }} PACK"
        assert IconText(template_missing_brace1, args_dict).gen_icon_text() == template_missing_brace1

        template_missing_brace2 = "Other={{ field1 } PACK"
        assert IconText(template_missing_brace2, args_dict).gen_icon_text() == None


    def test_bad_arg_name_starts_wth_numeric(self):
        # jinja does not allow args which start with non-alpha
        bad_first_char_dict_numeric = dict({'9abcdefghijklmnopqrstuvwxyz': 'xyz'})
        template_text1 = "BEFORE {{ 9abcdefghijklmnopqrstuvwxyz }} MID {{ field2 }} AFTER"
        assert IconText(template_text1, bad_first_char_dict_numeric).gen_icon_text() == None

        bad_first_char_dict_other = dict({'+abcdefghijklmnopqrstuvwxyz': 'xyz'})
        template_text1 = "BEFORE {{ +abcdefghijklmnopqrstuvwxyz }} MID {{ field2 }} AFTER"
        assert IconText(template_text1, bad_first_char_dict_other).gen_icon_text() == None


    def test_template_not_found_args(self):
        args_dict = dict({'field2': 'pqr'})
        simple_template_text = "BEFORE {{ field1 }} MID {{ field2 }} AFTER"
        expected_icon_text = "BEFORE  MID pqr AFTER"
        assert IconText(simple_template_text, args_dict).gen_icon_text() == expected_icon_text


    def test_template_multiple_on_same_line(self):
        args_dict = dict({'field1': 'xyz'})
        template_text = "Other={{ field1 }} PACK {{ field1 }}"
        expected_icon_text = "Other=xyz PACK xyz"
        assert IconText(template_text, args_dict).gen_icon_text() == expected_icon_text


    def test_template_extra_space_in_braces(self):
        # jinja allows extra spaces in the braces - it appears
        args_dict = dict({'first': 'abc', 'second': 'rst'})
        expected_text = "BEFOREabcAFTER"

        template_extra_space_before = "BEFORE{{  first }}AFTER"
        assert IconText(template_extra_space_before, args_dict).gen_icon_text() == expected_text

        # mismatch in spacing fails to match
        template_extra_space_after = "BEFORE{{ first  }}AFTER"
        assert IconText(template_extra_space_after, args_dict).gen_icon_text() == expected_text

        template_extra_space_before_and_after = "BEFORE{{  first  }}AFTER"
        assert IconText(template_extra_space_before_and_after, args_dict).gen_icon_text() == expected_text

    def test_complex_template_and_args(self):
        args_dict = dict({'field1': 'abc', 'field3': 'xyz'})
        template_text = "INITIAL={{ field1  }} FIRST {{ fields2 }} SECOND{{  field1 }}NOSPACE{{  field1  }}"
        expected_icon_text = "INITIAL=abc FIRST  SECONDabcNOSPACEabc"
        assert IconText(template_text, args_dict).gen_icon_text() == expected_icon_text


    def test_long_arg_name(self):
        args_dict = dict({'a2bcdefghijklmnopqrstuvwxyz': 'xyz'})
        temp_text = "BEFORE {{ a2bcdefghijklmnopqrstuvwxyz }} MID {{ field2 }} AFTER"
        expected_icon_text = "BEFORE xyz MID  AFTER"
        assert IconText(temp_text, args_dict).gen_icon_text() == expected_icon_text


    def test_template_spaces_preserved(self):
        args_dict = dict({'first': 'abc', 'second': 'rst', 'third': 'xyz'})
        template_text = "ALPHA{{  first }}BETA {{  second }}  GAMMA  {{ third  }}OMEGA"
        expected_text = "ALPHAabcBETA rst  GAMMA  xyzOMEGA"
        assert IconText(template_text, args_dict).gen_icon_text() == expected_text



@pytest.mark.deskicon
class TestDeskIcon:

    def test_bad_destdir(self):
        dsk1 = DeskIcon('unknowndir', FULL_GOOD_TEMPLATE_PATH, good_dict)
        assert dsk1.valid() == False


    def test_bad_template_file(self):
        dsk1 = DeskIcon(WKG_DIR, 'non-existant-template', good_dict)
        assert dsk1.valid() == False


    def test_bad_structure(self):
        assert DeskIcon(WKG_DIR, FULL_GOOD_TEMPLATE_PATH, ()).valid() == False
        assert DeskIcon(WKG_DIR, FULL_GOOD_TEMPLATE_PATH, []).valid() == False
        assert DeskIcon(WKG_DIR, FULL_GOOD_TEMPLATE_PATH, 'abc').valid() == False
        assert DeskIcon(WKG_DIR, FULL_GOOD_TEMPLATE_PATH, noname_dict).valid() == False


    def test_get_filename(self):
        ent_name = 'felix'
        attribs_dict = dict({'entry': ent_name})
        tempdir = tempfile.TemporaryDirectory(dir="/tmp").name
        desk1_fname = DeskIcon(tempdir, FULL_GOOD_TEMPLATE_PATH, attribs_dict).get_filename()
        basefilename = os.path.basename(desk1_fname)
        expected_name = DESKTOP_FILE_PREFIX + ent_name + DESKTOP_FILE_POSTFIX
        assert basefilename == expected_name
        # the following are redundant
        # the following are redundant
        assert basefilename.endswith('.desktop')
        assert basefilename.startswith('X' + 'simpli_')


    def test_created_icon_file_path(self):
        tempdir = tempfile.TemporaryDirectory(dir="/tmp").name
        desk3_fname = DeskIcon(tempdir, FULL_GOOD_TEMPLATE_PATH, good_dict).get_filename()
        assert os.path.dirname(desk3_fname) == tempdir


    # def test_generate_desktop_icon_text(self):
    #     # with no substitution
    #     tmpdir1 = tempfile.TemporaryDirectory(dir="/tmp").name
    #     desk_ifc = DeskIcon(tmpdir1, FULL_TEST_TEMPLATE_PATH, {})
    #     content_text = desk_ifc.generate_desktop_icon_text()
    #     for entry in TEST_TEMPLATE_TEXT_NULL:
    #         index = content_text.find(entry)
    #         print(f'Find >>{entry}<<')
    #         assert index != -1
    #
    #     # with substitution
    #     tmpdir2 = tempfile.TemporaryDirectory(dir="/tmp").name
    #     att_dict = dict({'the_river': 'Nile', 'the_country': 'Egypt'})
    #     desk_ifc2 = DeskIcon(tmpdir2, FULL_TEST_TEMPLATE_PATH, att_dict)
    #     content_text2 = desk_ifc2.generate_desktop_icon_text()
    #     for entry in TEST_TEMPLATE_TEXT_SUBS:
    #         index = content_text2.find(entry)
    #         print(f'Find >>{entry}<<')
    #         assert index != -1


    def test_generate_desktop_file(self):
        # check that all the important lines exist in the generated file
        tmpdir = tempfile.TemporaryDirectory(dir="/tmp").name
        os.mkdir(tmpdir, 0o777) # we create the dest dir
        os.path.isdir(tmpdir)

        # check that if not enabled then no file is to be created
        desk_not_enabled = DeskIcon(tmpdir, FULL_GOOD_TEMPLATE_PATH, dict({'entry': 'test_not_enabled', 'enabled': 'false'}))
        report_success = desk_not_enabled.generate_desktop_file()
        assert report_success == False  # verify that it thinks the file was NOT created
        assert os.path.isfile(desk_not_enabled.get_filename())  == False # check that expected file does not exist

        # if enabled field not specified then it will be disabled
        desk_not_specify_enabled = DeskIcon(tmpdir, FULL_GOOD_TEMPLATE_PATH, dict({'entry': 'test_not_specify_enabled'}))
        report_success = desk_not_specify_enabled.generate_desktop_file()
        assert report_success == False  # verify that it thinks the file was NOT created
        assert os.path.isfile(desk_not_specify_enabled.get_filename()) == False  # check that expected file does not exist

        #  desktop icon is enabled
        desk_enabled = DeskIcon(tmpdir, FULL_GOOD_TEMPLATE_PATH, dict({'entry': 'test_content', 'enabled': 'true'}))

        expected_path = tmpdir + '/' + 'X' + 'simpli_' + 'test_content' + '.desktop'

        assert os.path.isfile(expected_path) == False # file does not exist beforehand
        assert desk_enabled.generate_desktop_file() == True # verify that it thinks file was created ok
        assert os.path.isfile(expected_path) # check that expected file exists
        #display_text('SOME TEXT\nON TWO LINES\n', 'ExpERIMENTAL')
        #display_file(expected_path, '(test_generate_desktop_file)')
        #assert False


@pytest.mark.iconset
class TestIconSet:

    def test_basic_yaml_test(self):
        good_set_and_template = IconSet(FULL_SIMPLE_TEST_TEMPLATE_PATH, FULL_TEST_ICON_YAML_SET, WKG_DIR)
        assert good_set_and_template.is_valid_set() == True


    def test_invalid_yaml_template_file_identified(self):
        bad_template = IconSet('abc', FULL_TEST_ICON_YAML_SET, WKG_DIR)
        assert bad_template.is_valid_set() == False


    def test_invalid_yaml_set_file_identified(self):
        bad_set = IconSet(FULL_SIMPLE_TEST_TEMPLATE_PATH, 'abc', WKG_DIR)
        assert bad_set.is_valid_set() == False


    def test_get_title(self):
        good_yaml_set_and_template = IconSet(FULL_SIMPLE_TEST_TEMPLATE_PATH, FULL_TEST_ICON_YAML_SET, WKG_DIR)
        assert good_yaml_set_and_template.get_title() is None

        good_toml_set_and_template = IconSet(FULL_SIMPLE_TEST_TEMPLATE_PATH, FULL_TEST_ICON_TOML_SET, WKG_DIR)
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


    def test_num_all_icons(self):
        good_yaml_set_and_template = IconSet(FULL_SIMPLE_TEST_TEMPLATE_PATH, FULL_TEST_ICON_YAML_SET, WKG_DIR)
        assert good_yaml_set_and_template.num_all_icons() == 4

        good_toml_set_and_template = IconSet(FULL_SIMPLE_TEST_TEMPLATE_PATH, FULL_TEST_ICON_TOML_SET, WKG_DIR)
        assert good_toml_set_and_template.num_all_icons() == 4


    def test_num_enabled_icons(self):
        good_yaml_set_and_template = IconSet(FULL_SIMPLE_TEST_TEMPLATE_PATH, FULL_TEST_ICON_YAML_SET, WKG_DIR)
        assert good_yaml_set_and_template.num_enabled_icons() == 3

        good_toml_set_and_template = IconSet(FULL_SIMPLE_TEST_TEMPLATE_PATH, FULL_TEST_ICON_TOML_SET, WKG_DIR)
        assert good_toml_set_and_template.num_enabled_icons() == 3


    def test_enabled_disabled_icons(self):
        enabled_entries = ['country_france', 'mountain_everest', 'mountain_mount-blanc']
        disabled_entries = ['country_the_netherlands']  # netherlands is disabled

        good_yaml_set_and_template = IconSet(FULL_SIMPLE_TEST_TEMPLATE_PATH, FULL_TEST_ICON_YAML_SET, WKG_DIR)
        good_toml_set_and_template = IconSet(FULL_SIMPLE_TEST_TEMPLATE_PATH, FULL_TEST_ICON_TOML_SET, WKG_DIR)
        assert good_yaml_set_and_template.list_enabled_icons() == enabled_entries
        assert good_toml_set_and_template.list_enabled_icons() == enabled_entries

        assert good_yaml_set_and_template.list_disabled_icons() == disabled_entries
        assert good_toml_set_and_template.list_disabled_icons() == disabled_entries


    def test_list_enabled_icon_filenames(self):
        enabled_entries = ['simpli_country_france.desktop',  'simpli_mountain_everest.desktop', 'simpli_mountain_mount-blanc.desktop']
        good_yaml_set_and_template = IconSet(FULL_SIMPLE_TEST_TEMPLATE_PATH, FULL_TEST_ICON_YAML_SET, WKG_DIR)
        good_toml_set_and_template = IconSet(FULL_SIMPLE_TEST_TEMPLATE_PATH, FULL_TEST_ICON_TOML_SET, WKG_DIR)
        assert good_yaml_set_and_template.list_enabled_icon_filenames() == enabled_entries
        assert good_toml_set_and_template.list_enabled_icon_filenames() == enabled_entries


    def test_icons_generated_in_correct_dir(self):
        # create a temporary diectory
        tmpdir = tempfile.TemporaryDirectory(dir="/tmp").name
        os.mkdir(tmpdir, 0o777)  # we create the dest dir
        os.path.isdir(tmpdir)

        good_yaml_set_and_template = IconSet(FULL_SIMPLE_TEST_TEMPLATE_PATH, FULL_TEST_ICON_YAML_SET, tmpdir)
        assert good_yaml_set_and_template.get_target_dir() == tmpdir

        good_toml_set_and_template = IconSet(FULL_SIMPLE_TEST_TEMPLATE_PATH, FULL_TEST_ICON_TOML_SET, WKG_DIR)
        assert good_toml_set_and_template.get_target_dir() == tmpdir



    def test_attributes_of_entry(self):
        good_yaml_set_and_template = IconSet(FULL_SIMPLE_TEST_TEMPLATE_PATH, FULL_TEST_ICON_YAML_SET, WKG_DIR)
        good_toml_set_and_template = IconSet(FULL_SIMPLE_TEST_TEMPLATE_PATH, FULL_TEST_ICON_TOML_SET, WKG_DIR)

        expected_everest = {
            'entry': 'mountain_everest',
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
            'entry': 'country_the_netherlands',
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

        # create a temporary directory
        tmpdir = tempfile.TemporaryDirectory(dir="/tmp", prefix="simpli_").name
        os.mkdir(tmpdir, 0o777)  # we create the dest dir
        print(f'XYZ Tempdir = {tmpdir}')
        os.path.isdir(tmpdir)

        #good_set_and_template = IconSet(FULL_SIMPLE_TEST_TEMPLATE_PATH, FULL_TEST_ICON_YAML_SET, tmpdir)
        good_set_and_template = IconSet(FULL_GOOD_TEMPLATE_PATH, FULL_TEST_ICON_YAML_SET, tmpdir)
        good_set_and_template.generate_all_icons(False)

        def full_path(rootdir, x):
            return rootdir + '/' + x

        enabled_entries = ['Xsimpli_country_france.desktop', 'Xsimpli_mountain_everest.desktop',
                           'Xsimpli_mountain_mount-blanc.desktop']
        list_of_wanted_files = list(map(lambda x: full_path(tmpdir, x), enabled_entries))
        for i in list_of_wanted_files:
            print(f'Check exist: {i}')
            assert os.path.isfile(i) == True

        disabled_entries = ['simpli_country_the_netherlands.desktop']
        list_of_unwanted_files = list(map(lambda x: full_path(tmpdir, x), disabled_entries))
        for i in list_of_unwanted_files:
            print(f'Check not exist: {i}')
            assert os.path.isfile(i) == False



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

        tmpdir = tempfile.TemporaryDirectory(dir="/tmp", prefix="simpli_").name
        os.mkdir(tmpdir, 0o777)  # we create the dest dir
        print(f'XYZ Tempdir = {tmpdir}')
        os.path.isdir(tmpdir)

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



