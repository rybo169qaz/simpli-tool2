import errno
import hashlib
import json
import os.path
import platform
import pytest
import time

import psutil
#import re
import sys
import yaml
from pathlib import Path
#from getmac import get_mac_address as gma

from jinja2 import Environment, FileSystemLoader
from enum import Enum
import subprocess
from create_desktop_icons import DeskIcon, IconNode, IconSuite, CreateDummyKnown, ExtractStructuredAttribute

HOME_DIR = '/home/robertryan'
REPO_ROOT = HOME_DIR + '/' + 'PROJ2/SIMPLI-TOOL/GIT-REPO/simpli-tool2'
DESKTOP_CONFIG_DIR = REPO_ROOT + '/' + 'Deployment-Info/desktop/desktop-config'
GOOD_TEMPLATE_FILE = 'template.desktop'
TEST_TEMPLATE_FILE = 'test_template.desktop'

FULL_GOOD_TEMPLATE_PATH = DESKTOP_CONFIG_DIR + '/' + GOOD_TEMPLATE_FILE
FULL_TEST_TEMPLATE_PATH = DESKTOP_CONFIG_DIR + '/' + TEST_TEMPLATE_FILE
WKG_DIR = REPO_ROOT + '/' + 'Deployment-Info/wkg-misc'

disabled_dict = dict({ 'entry': 'george', 'enabled': 'false'})
noname_dict = dict({ 'enabled': 'false'})
good_dict = dict({ 'entry': 'fred', 'enabled': 'true'})

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
        full_dict = full_dict | root_dict
        full_dict = full_dict | mountains_dict
        full_dict = full_dict | everest_dict

        assert esa1.get_dict_of_lev1_lev2('mountain_list', 'everest') == full_dict

@pytest.mark.deskicon
class TestDeskIcon:

    def test_create_known(self):
        dumdata = CreateDummyKnown(WKG_DIR, 'dummy-known.yaml')
        #dumdata.create_test_data()
        dumdata.new_create_testd_file()

    def test_is_valid_data(self):
        dsk = DeskIcon(WKG_DIR, FULL_GOOD_TEMPLATE_PATH, good_dict)
        assert dsk.valid() == True

    def test_bad_destdir(self):
        dsk1 = DeskIcon('unknowndir', FULL_GOOD_TEMPLATE_PATH, good_dict)
        assert dsk1.valid() == False

    def test_bad_template(self):
        dsk1 = DeskIcon(WKG_DIR, 'noname-template', noname_dict)
        assert dsk1.valid() == False

        dsk2 = DeskIcon(WKG_DIR, 'disabled-template', disabled_dict)
        assert dsk2.valid() == False


    def test_bad_structure(self):
        assert DeskIcon(WKG_DIR, FULL_GOOD_TEMPLATE_PATH, ()).valid() == False
        assert DeskIcon(WKG_DIR, FULL_GOOD_TEMPLATE_PATH, []).valid() == False
        assert DeskIcon(WKG_DIR, FULL_GOOD_TEMPLATE_PATH, 'abc').valid() == False

    def test_created_filename(self):
        desk1_fname= DeskIcon(WKG_DIR, FULL_GOOD_TEMPLATE_PATH, good_dict).get_filename()
        assert desk1_fname.endswith('.desktop')

        basefilename = os.path.basename(desk1_fname)
        assert basefilename.startswith('simpli_')
        assert basefilename.find('fred')

    def test_existing_icon_removed(self):
        test_icon_file = WKG_DIR + '/' + 'simpli_test123.desktop'
        if os.path.isfile(test_icon_file):
            os.remove(test_icon_file)

        desk1_obj = DeskIcon(WKG_DIR, FULL_GOOD_TEMPLATE_PATH, dict({'entry': 'test123'}))

        # check that it works when file does not exist
        assert desk1_obj.icon_file_to_be_non_existant() == True

        # check that it works when file DOES exist
        with open(test_icon_file, "w") as f:
            f.write("blurb")
        f.close()
        assert desk1_obj.icon_file_to_be_non_existant() == True

    def _strings_found_in_file(self, wanted_strings, file_to_test):
        fnd_dict = dict({})
        for i in wanted_strings:
            fnd_dict[i] = False

        with open(file_to_test, 'r+') as file:
            for line in file:
                for wanted in wanted_strings:
                    if wanted in line:
                        fnd_dict[wanted] = True
        file.close()
        found = True
        for key in fnd_dict:
            if fnd_dict[key] == False:
                found = False
                print(f'Failed to find match for >>{key}<<\n')
                break
        return found

    def test_internal_string_finder(self):
        expected_temp_str = [ '[Desktop Entry]', 'Version=1.0', 'Comment[en_GB]=',
        'Exec={{ tool_command }} {{ command_args }}', 'Icon={{ icon }}.png' ]
        assert self._strings_found_in_file(expected_temp_str, FULL_GOOD_TEMPLATE_PATH) == True

    def test_icon_file_created(self):
        desk_ifc = DeskIcon(WKG_DIR, FULL_GOOD_TEMPLATE_PATH, dict({'entry': 'test123'}))
        desk_ifc.icon_file_to_be_non_existant()
        assert os.path.exists(WKG_DIR + '/simpli_test123.desktop') == False
        desk_ifc.write_content_of_desktop_file('abc')
        assert os.path.exists(WKG_DIR + '/simpli_test123.desktop') == True

    def test_desktop_file_contents(self):
        # check that all the important lines exist in the generated file
        desk_ifc = DeskIcon(WKG_DIR, FULL_GOOD_TEMPLATE_PATH, dict({'entry': 'test_content'}))
        gen_filename = desk_ifc.get_filename()
        desk_ifc.generate_desktop_file()

        expected_str2 = [ '[Desktop Entry]', 'Version=1.0', 'Name=', 'GenericName=', 'Comment=',
        'Name[en_GB]=', 'GenericName[en_GB]=',
        'Comment[en_GB]=', 'Exec=', 'Icon=',
        'Terminal=', 'Type=', 'Categories=', 'Keywords=' ]

        assert self._strings_found_in_file(expected_str2, gen_filename) == True

    def test_substitution_engine(self):
        # check that the jinja engine substitutes correctly
        vars_to_sub = dict({'entry': 'test_sub', 'the_country': 'Egypt', 'the_river': 'Nile', 'the_location': 'by the med'})
        desk_se = DeskIcon(WKG_DIR, FULL_TEST_TEMPLATE_PATH, vars_to_sub)
        gen_filename = desk_se.get_filename()
        desk_se.generate_desktop_file()

        expected_sub = ['River = Nile', 'Country =Egypt', 'Sentence= In Egypt there is a river Nile flowing through it.']

        assert self._strings_found_in_file(expected_sub, gen_filename) == True

@pytest.mark.iconnode
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




@pytest.mark.iconsuite
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




