#import errno
#import hashlib
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
#import yaml
#from pathlib import Path
#from getmac import get_mac_address as gma

#from jinja2 import Environment, FileSystemLoader, Template
#from enum import Enum
#import subprocess
from create_desktop_icons import DeskIcon, IconNode, IconSuite, IconSet, ExtractStructuredAttribute
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

TEST_ICON_SET = 'test_icon_set.yml'
FULL_TEST_ICON_SET = DESKTOP_CONFIG_DIR + '/' + TEST_ICON_SET

WKG_DIR = REPO_ROOT + '/' + 'Deployment-Info/wkg-misc'

disabled_dict = dict({ 'entry': 'george', 'enabled': 'false'})
noname_dict = dict({ 'enabled': 'false'})
missing_entry_dict = dict({ 'fish': 'cod', 'enabled': 'true'})
good_dict = dict({ 'entry': 'fred', 'enabled': 'true'})

@pytest.mark.skip # test_extract_struct_att
class TestExtractStructuredAttribute:

    def test_have_valid_structure(self):
        esa1 = ExtractStructuredAttribute(WKG_DIR + '/' + 'dummy-known.yaml')
        assert esa1.struct_is_valid() == True

    def test_get_root_id(self):
        esa1 = ExtractStructuredAttribute(WKG_DIR + '/' + 'dummy-known.yaml')
        assert esa1.get_root_id() == 'root_id'

    def test_root_attribute_exists(self):
        esa1 = ExtractStructuredAttribute(WKG_DIR + '/' + 'dummy-known.yaml')
        assert esa1.root_attribute_exists('env1') == True
        assert esa1.root_attribute_exists('env3') == False

    def test_root_attribute_value(self):
        esa1 = ExtractStructuredAttribute(WKG_DIR + '/' + 'dummy-known.yaml')
        assert esa1.get_root_attribute('env1') == 'env1 root value'
        assert esa1.get_root_attribute('env3') is None

    def test_get_list_of_first_level_entry_ids(self):
        esa1 = ExtractStructuredAttribute(WKG_DIR + '/' + 'dummy-known.yaml')
        assert esa1.get_list_of_first_level_entry_ids() == [ 'country_list', 'mountain_list', 'no attr', 'no entries'  ]


    def test_first_level_exists_with_name(self):
        esa1 = ExtractStructuredAttribute(WKG_DIR + '/' + 'dummy-known.yaml')
        assert esa1.first_level_exists_with_name('country_list') == True
        assert esa1.first_level_exists_with_name('gulp') == False

    def test_level2_exists(self):
        esa1 = ExtractStructuredAttribute(WKG_DIR + '/' + 'dummy-known.yaml')
        assert esa1.second_level_exists_with_name('country_list', 'france') == True
        assert esa1.second_level_exists_with_name('country_list', 'germany') == False
        assert esa1.second_level_exists_with_name('river_list', 'france') == False

    def test_get_dict_of_lev1_lev2(self):
        esa1 = ExtractStructuredAttribute(WKG_DIR + '/' + 'dummy-known.yaml')

        france_dict = {'env1': 'env1 root value',
                       'env2': 'root value for env2',
                       'command_args': 'france_tool1 a b c',
                       'description': 'France',
                       'enabled': 'true',
                       'flag': 'French Flag'
                       }
        #assert esa1.get_dict_of_lev1_lev2('country_list', 'france') == france_dict

        # everest_dict = {'env1': 'env1 root value',
        #                'env2': 'everest value for env2',
        #                'category_description': 'Well known mountains',
        #                'tool_command': 'mountain_tool',
        #                'description': 'Mount Everest',
        #                 'enabled': 'true',
        #                'icon': 'nepal_photo'
        #                }

        root_dict = {'env1': 'env1 root value', 'env2': 'root value for env2' }
        mountains_dict = {'category_description': 'Well known mountains', 'tool_command': 'mountain_tool'}
        everest_dict = {
                        'description': 'Mount Everest',
                        'enabled': 'true',
                        'env2': 'everest value for env2',
                        'icon': 'nepal_photo'
                        }

        #assert esa1.get_dict_of_lev1_lev2('mountain_list', 'everest') == root_dict
        #assert esa1.get_dict_of_lev1_lev2('mountain_list', 'everest') == mountains_dict
        #assert esa1.get_dict_of_lev1_lev2('mountain_list', 'everest') == everest_dict

        full_dict = dict({})
        full_dict |= root_dict
        full_dict = full_dict | mountains_dict
        full_dict = full_dict | everest_dict

        assert esa1.get_dict_of_lev1_lev2('mountain_list', 'everest') == full_dict



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


    def test_generate_desktop_icon_text(self):
        # with no substitution
        tmpdir1 = tempfile.TemporaryDirectory(dir="/tmp").name
        desk_ifc = DeskIcon(tmpdir1, FULL_TEST_TEMPLATE_PATH, {})
        content_text = desk_ifc.generate_desktop_icon_text()
        for entry in TEST_TEMPLATE_TEXT_NULL:
            index = content_text.find(entry)
            print(f'Find >>{entry}<<')
            assert index != -1

        # with substitution
        tmpdir2 = tempfile.TemporaryDirectory(dir="/tmp").name
        att_dict = dict({'the_river': 'Nile', 'the_country': 'Egypt'})
        desk_ifc2 = DeskIcon(tmpdir2, FULL_TEST_TEMPLATE_PATH, att_dict)
        content_text2 = desk_ifc2.generate_desktop_icon_text()
        for entry in TEST_TEMPLATE_TEXT_SUBS:
            index = content_text2.find(entry)
            print(f'Find >>{entry}<<')
            assert index != -1


    def test_generate_desktop_file(self):
        # check that all the important lines exist in the generated file
        tmpdir = tempfile.TemporaryDirectory(dir="/tmp").name
        os.mkdir(tmpdir, 0o777) # we create the dest dir
        os.path.isdir(tmpdir)

        desk_ifc = DeskIcon(tmpdir, FULL_GOOD_TEMPLATE_PATH, dict({'entry': 'test_content'}))

        report_success = desk_ifc.generate_desktop_file()
        assert report_success == True # verify that it thinks file was created ok

        expected_file = desk_ifc.get_filename()
        print(f'EXP FILE >>{expected_file}<<')

        assert os.path.isfile(expected_file) # check that expected file exists

        with open(expected_file, 'r') as file:
            file_text = file.read()
        assert file_text == desk_ifc.generate_desktop_icon_text() # check content is as the string



@pytest.mark.skip # @pytest.mark.iconnode
class TestIconNode:

    def test_get_node_name(self):
        node1 = IconNode('first', 'fruit', {})
        assert node1.get_node_name() == 'first'

    def test_get_get_child_type(self):
        node2 = IconNode('first', 'fish', {})
        assert node2.get_child_type() == 'fish'

    def test_get_list_attribute_names(self):
        node3 =IconNode('animals', 'fish', {'eggs': 'brown', 'dogs': '0', 'cats': 42})
        assert node3.get_list_attribute_names() == ['cats', 'dogs', 'eggs']

    def test_get_attribute_value(self):
        node4 = IconNode('animals', 'fish', {'eggs': 'brown', 'dogs': '0', 'cats': 42})
        assert node4.get_attribute_value('cats') == 42
        assert node4.get_attribute_value('eggs') == 'brown'
        assert node4.get_attribute_value('trees') == None

    def test_get_count_of_children(self):
        node5 = IconNode('first', 'fruit', {})
        assert node5.get_count_of_children() == 0
        node5 = IconNode('animals', 'fish', {'eggs': 'brown', 'dogs': '0', 'cats': 42})
        assert node5.get_count_of_children() == 0

    def test_add_child(self):
        nodeA = IconNode('first', 'fruit', {})
        assert nodeA.add_child('notfruit', 'key_pqr', 'value_pqr') == False
        assert nodeA.add_child('fruit', 'key_pqr', 'value_pqr') == True


    def test_get_list_of_children_names(self):
        node7 = node5 = IconNode('root', 'category', {})
        assert node7.get_list_of_children_names() == []
        node7.add_child('category', 'key_pqr', 'value_pqr')
        assert node7.get_list_of_children_names() == ['key_pqr']

        node7.add_child('category', 'key_new', 'value_new')
        assert node7.get_list_of_children_names() == ['key_new', 'key_pqr']

        node7.add_child('category', 'key_alpha', 'value_alpha')
        assert node7.get_list_of_children_names() == ['key_alpha', 'key_new', 'key_pqr']

    def test_get_child_of_given_name(self):
        node8 = IconNode('animals', 'fish', {'eggs': 'brown', 'dogs': '0', 'cats': 42})
        assert node8.get_child_of_given_name('fred') == None
        node8.add_child('fish', 'key_alpha', 'value_alpha')
        node8.add_child('fish', 'key_new', 'value_new')
        assert node8.get_child_of_given_name('key_new') == 'value_new'
        #node8.print()

    def test_integration(self):
        nodeC = IconNode('root', 'categories', {'cat_att1': 'at1_val', 'cat_att2': 'att2val', 'catatt3': 42})
        #nodeC.print()

        mountain_everest = IconNode('everest', None, {'height': 9999, 'conquered_by': 'Mallory', 'country': 'Tibet'})
        mountain_mtblanc = IconNode('Mt Blanc', None, {'height': 123, 'conquered_by': 'Unknown', 'country': 'France'})

        mountains = IconNode('mountain_info', 'mountain', {'madeOf': 'rock', 'activity': 'climbable'})
        assert mountains.add_child('mountain', 'everest', mountain_everest) == True
        assert mountains.add_child('mountain', 'Mt Blanc', mountain_mtblanc) == True

        root_node = IconNode('root_info', 'mountains', {'vlcPath': '/abc/def', 'description': 'Media playing tool'})
        assert root_node.add_child('mountains', 'mountaininfo', mountains) == True
        root_node.print_node()
        root_node.print_full_node()



@pytest.mark.iconset
class TestIconSet:

    def test_basic_test(self):
        good_set_and_template = IconSet(FULL_SIMPLE_TEST_TEMPLATE_PATH, FULL_TEST_ICON_SET, WKG_DIR)
        assert good_set_and_template.is_valid_set() == True


    def test_invalid_template_file_identified(self):
        bad_template = IconSet('abc', FULL_TEST_ICON_SET, WKG_DIR)
        assert bad_template.is_valid_set() == False


    def test_invalid_set_file_identified(self):
        bad_set = IconSet(FULL_SIMPLE_TEST_TEMPLATE_PATH, 'abc', WKG_DIR)
        assert bad_set.is_valid_set() == False


    def test_get_common_attributes(self):
        good_set_and_template = IconSet(FULL_SIMPLE_TEST_TEMPLATE_PATH, FULL_TEST_ICON_SET, WKG_DIR)
        expected_common = {'vlc': '/etc/bin/vlc',
                           'com2': 222,
                           'the_river': 'Amazon'
                           }
        assert good_set_and_template.get_common_attributes() == expected_common


    def test_num_all_icons(self):
        good_set_and_template = IconSet(FULL_SIMPLE_TEST_TEMPLATE_PATH, FULL_TEST_ICON_SET, WKG_DIR)
        assert good_set_and_template.num_all_icons() == 4


    def test_num_enabled_icons(self):
        good_set_and_template = IconSet(FULL_SIMPLE_TEST_TEMPLATE_PATH, FULL_TEST_ICON_SET, WKG_DIR)
        assert good_set_and_template.num_enabled_icons() == 3


    def test_enabled_disabled_icons(self):
        good_set_and_template = IconSet(FULL_SIMPLE_TEST_TEMPLATE_PATH, FULL_TEST_ICON_SET, WKG_DIR)
        enabled_entries = ['country_france',  'mountain_everest', 'mountain_mount-blanc']
        assert good_set_and_template.list_enabled_icons() == enabled_entries

        disabled_entries = ['country_the_netherlands']  # netherlands is disabled
        assert good_set_and_template.list_disabled_icons() == disabled_entries


    def test_list_enabled_icon_filenames(self):
        good_set_and_template = IconSet(FULL_SIMPLE_TEST_TEMPLATE_PATH, FULL_TEST_ICON_SET, WKG_DIR)
        enabled_entries = ['simpli_country_france.desktop',  'simpli_mountain_everest.desktop', 'simpli_mountain_mount-blanc.desktop']
        assert good_set_and_template.list_enabled_icon_filenames() == enabled_entries


    def test_icons_generated_in_correct_dir(self):
        # create a temporary diectory
        tmpdir = tempfile.TemporaryDirectory(dir="/tmp").name
        os.mkdir(tmpdir, 0o777)  # we create the dest dir
        os.path.isdir(tmpdir)

        good_set_and_template = IconSet(FULL_SIMPLE_TEST_TEMPLATE_PATH, FULL_TEST_ICON_SET, tmpdir)
        assert good_set_and_template.get_target_dir() == tmpdir

    def test_attributes_of_entry(self):
        good_set_and_template = IconSet(FULL_SIMPLE_TEST_TEMPLATE_PATH, FULL_TEST_ICON_SET, WKG_DIR)
        #actual = good_set_and_template.get_attribs_of_entry('mountain_everest')
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
        assert good_set_and_template.get_attribs_of_entry('mountain_everest') == expected_everest

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
        assert good_set_and_template.get_attribs_of_entry('country_the_netherlands') == expected_netherlands

        assert good_set_and_template.get_attribs_of_entry('unknown_entry') == None


    def test_only_enabled_files_created(self):
        # This should be mocked

        # create a temporary directory
        tmpdir = tempfile.TemporaryDirectory(dir="/tmp", prefix="simpli_").name
        os.mkdir(tmpdir, 0o777)  # we create the dest dir
        os.path.isdir(tmpdir)

        #good_set_and_template = IconSet(FULL_SIMPLE_TEST_TEMPLATE_PATH, FULL_TEST_ICON_SET, tmpdir)
        good_set_and_template = IconSet(FULL_GOOD_TEMPLATE_PATH, FULL_TEST_ICON_SET, tmpdir)
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

        assert False





@pytest.mark.skip # @pytest.mark.iconsuite
class TestIconSuite:

    def test_invalid_suite(self):
        suite1 = IconSuite('unknownfile')
        assert suite1.validsuite() == False

    def test_valid_suite(self):
        suite2 = IconSuite(DESKTOP_CONFIG_DIR + '/' + 'test_desktop_known.yml')
        assert suite2.validsuite() == True

    def test_categories(self):
        suite3 = IconSuite(DESKTOP_CONFIG_DIR + '/' + 'test_desktop_known.yml')
        expected_categories = set(('countries', 'mountains'))
        assert suite3.get_categories() == expected_categories

    def test_entries_in_category(self):
        suite4 = IconSuite(DESKTOP_CONFIG_DIR + '/' + 'test_desktop_known.yml')
        expected_entries = set(('france', 'the_netherlands'))
        assert suite4.get_entries_in_category('countries') == expected_entries

    def test_entries_in_all_categories(self):
        suite5 = IconSuite(DESKTOP_CONFIG_DIR + '/' + 'test_desktop_known.yml')
        expected_list_of_cat_ent = [
            ('countries', 'france'),
            ('countries', 'the_netherlands'),
            ('mountains', 'everest'),
            ('mountains', 'mount blanc')
        ]

        expected_dict_of_cat_ent = {
            'countries' : [ 'france', 'the_netherlands'],
            'mountains': ['everest', 'mount blanc'],
        }
        # The following were excluded because they are NOT enabled
        # ('countries', 'the_netherlands'),
        ret_struct = suite5.entries_in_all_categories()
        #assert len(ret_struct) == 4
        print(f'returned structure')
        print(json.dumps(ret_struct))
        print(f'\nexpected structure')
        print(json.dumps(expected_dict_of_cat_ent))

        assert suite5.entries_in_all_categories() == expected_dict_of_cat_ent




