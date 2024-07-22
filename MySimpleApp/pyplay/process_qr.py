import os

from my_argparse import *
import qr_decode


class ProcessQR:
    def __init__(self, qr_image_file, verbose=True, dummy=False):
        self.qr_image_file = qr_image_file
        self.cwd = os.getcwd()
        self.verbose = verbose
        self.dummy = dummy
        self.raw = None
        self.parser = None
        self.known = None
        print(f'(ProcessQR:file={self.qr_image_file}')

    def get_image_file(self):
        return self.qr_image_file

    def image_file_exists(self):
        if os.path.isfile(self.qr_image_file):
            resp = True
        else:
            resp = False
        return resp

    def get_raw(self):
        if self.raw is None:
            self.raw = qr_decode.decode_qr(self.qr_image_file, False)
        if self.verbose:
            print(f'(ProcessQR:get_raw): >>{self.raw}<<')
        return self.raw

    def parse_args(self):
        self.get_raw()
        if self.verbose:
            print(f'(ProcessQR:parse_args): starting')
        self.parser = argparse.ArgumentParser(description='Parses the qr args')

        self.parser.add_argument('-f', '--format', required=False, type=str,
                                default='cmdstr',
                                choices=['cmdstr', 'qr', 'camera'],
                                help='The media player')

        self.parser.add_argument('-k', "--known", required=False, type=str,
                        default='unspecified',
                        help='A wellknown file is being specified.\n ')

        self.parser.add_argument("verb", type=str, choices=['select'], help='The verb')

        the_string = self.raw
        if self.verbose:
            print(f'ProcessQR:parse_args) raw == {the_string}')
        new_string = the_string.strip()
        if self.verbose:
            print(f': new_string == >>{new_string}<<')
        arg_list = new_string.split(" ")
        #arg_list = new_string.split(self.raw)
        #arg_list = new_string.split('--keep fred')
        #arg_list = new_string.split('--keep', 'fred')
        qr_args = self.parser.parse_args(arg_list, None)
        self.known = qr_args.known
        #print(f'(ProcessQR:parse_args): KNOWN=>>{self.known}<<')

    def get_known(self):
        if self.parser is None:
            self.parse_args()
        if self.verbose:
            print(f'(ProcessQR:get_known): known == >>{self.known}<<')
        return self.known
