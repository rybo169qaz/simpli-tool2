import os
import sys
from PIL import Image, ImageDraw, ImageFont


def show_syntax():
    print(f'Args:   <destination_file> <text> <x-size> <y-size>\n')


def exit_msg(code, text):
    print(f'Error ({code}): {text}\n')
    show_syntax()
    exit(code)


def main():
    print(f'Create PNG\n')
    cmndline_args = sys.argv[1:]
    if len(cmndline_args) != 4:
        show_syntax()
        exit_msg(1, 'Invalid number of args')

    dest_file = cmndline_args[0]
    message = cmndline_args[1]
    xsize = int(cmndline_args[2])
    ysize = int(cmndline_args[3])

    #if os.path.isfile(dest_file):
    #    exit_msg(2, 'Destination file specified is not valid')

    image = Image.new("RGB", (xsize, ysize), "blue")
    draw = ImageDraw.Draw(image)
    #font = ImageFont.truetype("arial.ttf", size=20)
    font = ImageFont.truetype(font=None, size=20)
    #font = ImageFont.load_default()
    draw.text((10, 10), message, font=font, fill=(255, 255, 255))
    image.save(dest_file)
    print(f'Created file {dest_file}')



if __name__ == "__main__":
    main()