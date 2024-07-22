import argparse
import sys
import my_docs

# (Stackoverflow) Display help message with Python argparse when script is called without any arguments
# https://stackoverflow.com/questions/4042452/display-help-message-with-python-argparse-when-script-is-called-without-any-argu
class MyArgParse(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        #sys.exit(2)

    def print_help(self):
        print(f'START additional help')
        my_docs.help_info('verb')
        print(f'END additional help\n')
