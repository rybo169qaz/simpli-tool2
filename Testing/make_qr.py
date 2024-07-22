import os
import sys
import qrcode
from qrcode.image.pure import PyPNGImage

def generate_qr(content):
    imginfo = qrcode.make(content)
    type(imginfo)  # qrcode.image.pil.PilImage

    if False:
        # for ideas see https://pypi.org/project/qrcode/
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_Q,
            box_size=10,
            border=5,
        )

    #qr.add_data('Some data')
    #qr.make(fit=True)
    #img = qr.make_image(fill_color="black", back_color="white")
    return imginfo

def make_qr_file(content, op_file):
    if os.path.isfile(op_file):
        print(f'\tDest file exists. Removing')
        os.remove(op_file)
        if os.path.isfile(op_file):
            print(f'Failed to remove exiting file before generation ({op_file})')
            exit(3)

    qrimg = generate_qr(content)
    qrimg.save(op_file)
    if not os.path.isfile(op_file):
        print(f'Failed to generate file ({op_file}')
        exit(5)
    else:
        print(f'Generated file "{op_file}" containing the QR info in png format')

def main():
    print('Argument list: ', sys.argv, '\n')
    argcount = len(sys.argv)
    tool_name = sys.argv[0]
    if argcount != 3:
        print(f'Syntax is: {tool_name} <filename> "<content>" \n\tNote that content should be in quotes to protect from shell')
        exit(1)

    destination_filename = sys.argv[1]
    required_content = sys.argv[2]

    print(f'Destination filename = {destination_filename}')
    print(f'Content = >>{required_content}<<')
    make_qr_file(required_content, destination_filename)

if __name__ == "__main__":
    main()