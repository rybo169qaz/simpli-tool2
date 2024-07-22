#from qrtools import QR
#import qrtools

import segno
#import opencv-contrib-python as cv2
import cv2
#from PIL import Image
#import Image

#import Pillow
from pyzbar.pyzbar import decode, ZBarSymbol


def doit():
    print("DOIT start\n")
    #my_QR = QR(data=u"Example")
    #my_QR.encode()
    ip_text = "Hellllo World"
    qr_filename = "hello.png"
    qrcode = segno.make_qr(ip_text)
    qrcode.save(qr_filename)
    print(f'Image created at {qr_filename}\n')

    print(cv2.__version__)
    #img = Image.open(qr_filename)
    #decoded_list = decode(img, symbols=[ZBarSymbol.QRCODE])
    #print('decode info')
    #print(len(decoded_list))



    #filen = my_QR.filename
    #print(f'Image created at {filen}\n')


if __name__ == '__main__':
    #fred = qrtools.QR()
    doit()

#



