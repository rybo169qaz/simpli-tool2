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
import subprocess
from create_desktop_icons import DeskIcon, IconSuite

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

class TestDeskIcon:

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



