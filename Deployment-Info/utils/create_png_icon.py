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

tool_title = 'Create PNG from text'
default_img_x_size = 150
default_img_y_siize = 150
default_xpos = 10
default_ypos = 50

def show_syntax():
    print(f'Args:   <destination_file> <text> <x-size> <y-size>')
    print(f'where\n\t <destination_file> : relative to invocation directory.')
    print(f'\t text : quoted.')
    print(f'\t x-size, y-size : in pixels.\n')

def describe_icon(the_args):
    print(f'Created file "{the_args.destfile}" size=({the_args.xsize},{the_args.ysize}), txt-pos=({the_args.xpos},{the_args.ypos}), text="{the_args.text}"')

def main():
    #print(f'{tool_title}: Starting')

    parser = argparse.ArgumentParser(description=tool_title)
    parser.add_argument("-f", "--forcewrite", help="Will allow overwrite of existing file", action="store_true")
    parser.add_argument("destfile", help="the file to be written to")
    parser.add_argument("text", help="text to be embedded in the PNG (needs to be in quotes)")
    parser.add_argument("--xsize", type=int, help=f'image x size in pixels (default = {default_img_x_size})',
                        default=default_img_x_size)
    parser.add_argument("--ysize", type=int, help=f'image y size in pixels (default = {default_img_y_siize})',
                        default=default_img_y_siize)
    parser.add_argument("--xpos", type=int, help=f'x coord of where text starts (default = {default_xpos})',
                        default=default_xpos)
    parser.add_argument("--ypos", type=int, help=f'y coord of where text starts (default = {default_ypos})',
                        default=default_ypos)
    args = parser.parse_args()

    if os.path.isfile(args.destfile) and args.forcewrite is False:
        print(f'ERROR: File already exists\n')
        #parser.print_usage()
        parser.print_help()
        print('')
        sys.exit(2)

    background_colour = "blue" #"blue" green

    image = Image.new("RGB", (args.xsize, args.ysize ), background_colour)
    draw = ImageDraw.Draw(image)
    #font = ImageFont.truetype("arial.ttf", size=20)
    #font = ImageFont.truetype(font=None, size=20)
    #font = ImageFont.load_default()
    draw.text((int(args.xpos), int(args.ypos)), args.text, fill=(255, 255, 255))
    try:
        image.save(args.destfile)
        describe_icon(args)
        # print(f'{tool_title}: Finished')
    except (PermissionError):
        print(f'Permissions prevent writing to file.\n')
    finally:
        print('')




if __name__ == "__main__":
    main()