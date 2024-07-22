# https://thecleverprogrammer.com/2022/01/18/decode-a-qr-code-using-python/
from pyzbar.pyzbar import decode
from PIL import Image

# also see https://pypi.org/project/qreader/


def decode_qr(filename, include_verb, verbose=False):
    folder = '../Input-Images'
    fullpath = folder + '/' + filename
    if verbose:
        print(f'DECODE_QR: Filename == {fullpath}')

    decocdeQR = decode(Image.open(fullpath))
    content = decocdeQR[0].data.decode('ascii')
    if verbose:
        print(f'DECODED >>{content}<<')

    full_content = content
    if include_verb:
        full_content = 'select ' + full_content

    return full_content
