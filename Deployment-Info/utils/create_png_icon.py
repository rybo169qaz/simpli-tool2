import os
import sys
import argparse
from PIL import Image, ImageDraw, ImageFont  # need to install Pillow
# use https://pillow.readthedocs.io/en/stable/reference/index.html for details of Pillow
# see https://www.youtube.com/watch?v=5w2QCmf2Q00

# How to Generate Images with Text Using Python
# https://codemon.medium.com/how-to-generate-images-with-text-using-python-15c73fb96bf8

# (stackoverflow) How I can load a font file with PIL.ImageFont.truetype without specifying the absolute path?
# https://stackoverflow.com/questions/24085996/how-i-can-load-a-font-file-with-pil-imagefont-truetype-without-specifying-the-ab

TOOL_TITLE = 'Create PNG from text'
DEFAULT_IMG_X_SIZE = 150
DEFAULT_IMG_Y_SIZE = 150
DEFAULT_X_POS = 10
DEFAULT_Y_POS = 50
BACKGROUND_COLOUR = "blue" #"blue" green


class CreatePng:
    """
    Creates a PNG file containing text.
    destfile        The file to be written. The file should not exist.
    text            The text to be embedded in the image
    OPTIONS
    forcewrite      If specified then wil overwrite an existing file (default False).
    Image X size    Overrides the default 987
    Image Y size    Overrides the default 887
    Text start position x coord  (0 is LHS). default is  456
    Text start position y coord  (0 is TOP). default is  441
    NOTES
        Limited validation of values is made.
        Default background colour is abc
        default font is ; default font size is 111
    """

    def __init__(self, dest_file:str, text:str,
                 imgsize_x: int=DEFAULT_IMG_X_SIZE,
                 imgsize_y: int=DEFAULT_IMG_Y_SIZE,
                 text_pos_x: int=DEFAULT_X_POS,
                 text_pos_y: int=DEFAULT_Y_POS,
                 file_overwrite: bool=False,
                 verbose: bool=False):
        self.dest_file = dest_file
        self.text = text
        self.imgsize_x = imgsize_x
        self.imgsize_y = imgsize_y
        self.text_pos_x = text_pos_x
        self.text_pos_y = text_pos_y
        self.file_overwrite = file_overwrite
        self.verbose = verbose
        self.__validate_args()
    
    def __validate_args(self):
        if self.verbose: print(f'Validating ')
        if self.dest_file == "" or self.dest_file is None:
            raise AttributeError('Null or Empty filename provided')

        if self.dest_file.endswith('/'):
            raise AttributeError('No filename after the directory part')

        filename, file_extension = os.path.splitext(self.dest_file)
        if file_extension != '.png':
            raise AttributeError('Incorrect extension (should be .png)')

    def __display_metadata(self):
        print((
            f'Filename "{self.dest_file}"'
            f', size=({self.imgsize_x},{self.imgsize_y})'
            f', txt-pos=({self.text_pos_x},{self.text_pos_y})'
            f', text="{self.text}"'
        ))

    def generate_image(self):
        if self.verbose: self.__display_metadata()
        if os.path.isfile(self.dest_file) and self.file_overwrite is False:
            raise FileExistsError("File already exists. Set file_overwrite if want to overwrite.")

        image = Image.new("RGB", (self.imgsize_x, self.imgsize_y ), BACKGROUND_COLOUR)
        draw = ImageDraw.Draw(image)
        #font = ImageFont.truetype("arial.ttf", size=20)
        #font = ImageFont.truetype(font=None, size=20)
        #font = ImageFont.load_default()
        if self.verbose: print(f'Attempt to write text within the PNG object')
        draw.text((int(self.text_pos_x), int(self.text_pos_y)), self.text, fill=(255, 255, 255))
        if self.verbose: print(f'Attempt to write the PNG file')
        image.save(self.dest_file)

        # not sure i should be doing this check
        if os.path.isfile(self.dest_file) is False:
            raise OSError(FileNotFoundError)


def describe_cli_syntax(p):
    # parser.print_usage()
    print('Syntax details')
    p.print_help()
    print('')

def report_failure(p, exit_value, exit_message):
    print(f'ERROR: {exit_message} \n')
    describe_cli_syntax(p)
    sys.exit(exit_value)

def main():
    parser = argparse.ArgumentParser(description=TOOL_TITLE)
    parser.add_argument("-v", "--verbose", help="Provide verbose output", action="store_true")
    parser.add_argument("-f", "--forcewrite", help="Will allow overwrite of existing file", action="store_true")
    parser.add_argument("destfile", help="the file to be written to")
    parser.add_argument("text", help="text to be embedded in the PNG (needs to be in quotes)")
    parser.add_argument("--xsize", type=int, help=f'image x size in pixels (default = {DEFAULT_IMG_X_SIZE})',
                        default=DEFAULT_IMG_X_SIZE)
    parser.add_argument("--ysize", type=int, help=f'image y size in pixels (default = {DEFAULT_IMG_Y_SIZE})',
                        default=DEFAULT_IMG_Y_SIZE)
    parser.add_argument("--xpos", type=int, help=f'x coord of where text starts (default = {DEFAULT_X_POS})',
                        default=DEFAULT_X_POS)
    parser.add_argument("--ypos", type=int, help=f'y coord of where text starts (default = {DEFAULT_Y_POS})',
                        default=DEFAULT_Y_POS)
    args = parser.parse_args()

    try:
        obj = CreatePng(args.destfile, args.text,
                        imgsize_x=args.xsize,
                        imgsize_y=args.ysize,
                        text_pos_x=args.xpos,
                        text_pos_y=args.ypos,
                        file_overwrite=args.forcewrite
                        )
    except AttributeError as e:
        report_failure(parser, 2, f'Filename extension must be .png : {e}')

    try:
        obj.generate_image()
    except ValueError:
        report_failure(parser, 3, f'One of the arguments is invalid e.g filename extension.')
    except FileExistsError:
        report_failure(parser, 4, f'File already exists (use force option if required).')
    except PermissionError:
        report_failure(parser, 5, f'No permission to write to file.')


if __name__ == "__main__":
    main()