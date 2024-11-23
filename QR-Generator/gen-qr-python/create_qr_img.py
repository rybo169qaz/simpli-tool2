from gettext import textdomain
from typing import Optional
import typer
from typer.testing import CliRunner
#from exceptiongroup import catch
from typing_extensions import Annotated
from enum import Enum
import segno
import io
import os
import sys

from fpdf import FPDF
from fpdf.enums import XPos, YPos
#from fpdf2 import FPDF
#import fpdf

#from fpdf import HTMLMixin
import lorem
from lorem.text import TextLorem

'''
    This utility creates a QR code of the specified string.
    Depending upon the ACTION command provided, it does one of 3 things:
        Action      Description
        ------      ---------------------------------
        simple      Create a QR code in a PNG file
        simpli      Create a PDF file for the simpliplay tool. This contains the QR code + the text of what is in the QR code.
        railings    Create a PDf of an A4 page which contains a Title + Prefix + QR code + Postfix text
'''

CREATE_PNG_QR_FILE = 'qr'
CREATE_RAILINGS_PDF_FILE = 'railings'
CREATE_SIMPLIPLAY_PDF_FILE = 'simpli'

class GeneratedArtifact(Enum):
    CREATE_PNG_QR_FILE = 1,
    CREATE_SIMPLIPLAY_PDF_FILE = 2,
    CREATE_RAILINGS_PDF_FILE = 3


DUMMY_QR_DATA = 'https://christadelphianvideo.org/'
#DUMMY_QR_DATA = lorem.paragraph().replace('\n', '')[0:240]   # sentence

FILLER_HEIGHT = 10

action_set =set([CREATE_PNG_QR_FILE, CREATE_RAILINGS_PDF_FILE, CREATE_SIMPLIPLAY_PDF_FILE])
action_str = (f'What to create: \n'
              + f'{CREATE_PNG_QR_FILE} (PNG format QR code);\n'
              + f'{CREATE_SIMPLIPLAY_PDF_FILE} : (PDF Document for simpliplay); \n'
              + f'{CREATE_RAILINGS_PDF_FILE} : (PDF Document for railings containing: Title, Prefix text, QR code, Postfix text); '
              )

def report_err(errno: int, msg: str):
    print(f'ERROR {errno}: {msg}')
    exit(99)

def create_qr(content: str):
    qrcode = segno.make(content)
    return qrcode

def create_png_file(content: str, filen: str, overwrite_png: bool, testurl=False):
    file_name, file_extension = os.path.splitext(filen)

    print(f'overwrite_png == {overwrite_png}')
    if not overwrite_png and os.path.isfile(filen):
        report_err(5, f'File ({filen}) exists')
    elif file_extension != '.png':
        report_err(6, 'Filename must have a .png extension')
    else:
        try:
            qrc = create_qr(content)
            qrc.save(filen, scale=5)
            print(f'Created file {filen} containing "{content}"')
        except:
            report_err(7    , 'Failed to write file')
    return True


def present_using_rectangle(pdf_obj, ypos, yheight, txt, alig='L', fnt='Times', sty='B', siz=16):
    #try:
    if txt is not None:
        this_rect = 30, ypos, 160, yheight
        pdf_obj.rect(*this_rect)
        pdf_obj.set_y(ypos)
        pdf_obj.set_left_margin(margin=40)
        pdf_obj.set_right_margin(margin=40)

        if txt is not None:
            pdf_obj.set_x(30)
            pdf_obj.set_font(fnt, sty, siz)
            pdf_obj.write(10, txt)
        return (ypos + yheight + FILLER_HEIGHT)
    else:
        return ypos
    #except:
    #    report_err(18, f'Failed to write rectangle ({txt})')

def present_using_cell(pdf_obj, ypos, yheight, txt, alig='L', fnt='Times', sty='B', siz=16):
    pdf_obj.set_y(ypos)
    #try:
    if txt is not None:
        pdf_obj.set_font(fnt, sty, siz)
        # OLD pdf.cell(0, title_h, title, align = 'C', border = 1, ln = 2)
        #pdf_obj.cell(0, yheight, txt, align=alig, border=1, new_x=XPos.LEFT, new_y=YPos.NEXT)
        pdf_obj.cell(0, yheight, txt, align=alig, border=1, new_x=XPos.LEFT, new_y=YPos.NEXT)
        # pdf.ln()
        yoff = ypos + yheight + FILLER_HEIGHT
    else:
        yoff = ypos
    return yoff
    #except:
    #    report_err(19, f'Failed to write cell ({txt})')


def create_pdf_file(content: str, filen: str, layout, title=None, prefix: str = None, postfix: str = None,
                    overwrite_pdf: bool = False, testmode=False):
    #layout='simpli'

    print(f'\tTitle == {title}')
    print(f'\tPrefix text == {prefix}')
    print(f'\tPostfix text == {postfix}')

    if layout == GeneratedArtifact.CREATE_SIMPLIPLAY_PDF_FILE:
        print(f'CREATE_PDF: layout == simpli == {layout.name}')
    elif layout == GeneratedArtifact.CREATE_RAILINGS_PDF_FILE:
        print(f'CREATE_PDF: layout == rail == {layout.name}')

    file_name, file_extension = os.path.splitext(filen)
    if not overwrite_pdf and os.path.isfile(filen):
        report_err(9, 'File exists')
    elif file_extension != '.pdf':
        report_err(10, 'Filename must have a .pdf extension')
    else:
        #try:
        pngname = file_name + '.png'
        create_png_file(content, pngname, overwrite_png=overwrite_pdf)

        pdf = FPDF() # see https://pyfpdf.readthedocs.io/en/latest/index.html
        # https://py-pdf.github.io/fpdf2/index.html

        pdf.add_page(orientation='P', format='A4')
        pdf.set_left_margin(margin=20)
        # pdf.set_right_margin(margin=20)

        if layout == GeneratedArtifact.CREATE_RAILINGS_PDF_FILE:
            if testmode:
                text_string = lorem.paragraph()
                prefix = text_string[0:200]
                postfix = text_string[201:400] # sentence  [0:60]
                # prefix = TextLorem(wsep='-', srange=(2, 3), words="A B C D".split())

        yoff = 0

        TITLE_HEIGHT = 40
        #yoff = present_using_rectangle(pdf, yoff, TITLE_HEIGHT, title, alig='C', fnt='Times', sty='B', siz=32)
        yoff = present_using_cell(pdf, yoff, TITLE_HEIGHT, title, alig='C', fnt='Times', sty='B', siz=32)

        PREFIX_HEIGHT = 50
        #yoff = present_using_rectangle(pdf, yoff, PREFIX_HEIGHT, prefix, alig='L', fnt='Helvetica', sty='B', siz=16)
        yoff = present_using_cell(pdf, yoff, PREFIX_HEIGHT, prefix, fnt='Helvetica', sty='B', siz=16)

        # xoffset, yoffset, x-size, y-size
        IMAGE_HEIGHT = 50
        rect1 = 90, yoff, IMAGE_HEIGHT, IMAGE_HEIGHT
        pdf.rect(*rect1)
        pdf.image(
            pngname,
            *rect1,
            keep_aspect_ratio=True
        )
        yoff += IMAGE_HEIGHT
        yoff += FILLER_HEIGHT

        POST_HEIGHT = 60
        present_using_rectangle(pdf, yoff, POST_HEIGHT, postfix, alig='L', fnt='Times', sty='B', siz=16)

        pdf.output(filen)
        print(f'Created file {filen} containing')
        print(f'\tTitle == {title}')
        print(f'\tPrefix text == {prefix}')
        print(f'\tPostfix text == {postfix}')
        #except:
        #    report_err(11    , 'Failed to write file')

    pass


def main(action: Annotated[str, typer.Argument(help=action_str)],
         filename: Annotated[str, typer.Argument(help="The file to be written to (must have appropriate extension)")],
         content: Annotated[str, typer.Argument(help="The string that is to be used to embed in the QR code")],
         title: Annotated[
            str,
            typer.Option(help=f'Title to be used (only applicable to the action={CREATE_RAILINGS_PDF_FILE}).'),
            ] = None,
          prefix: Annotated[
            str,
            typer.Option(help=f'Text to prefix the QR code. (only applicable to the action={CREATE_RAILINGS_PDF_FILE}).'),
            ] = None,
          postfix: Annotated[
            str,
            typer.Option(help=f'Text to postfix the QR code. (only applicable to the action={CREATE_RAILINGS_PDF_FILE}).'),
            ] = None,
          testdata: Annotated[
            bool,
            typer.Option(help=f'Run in test mode using dummy text.'),
            ] = False,
          forcewrite: Annotated[
            bool,
            typer.Option(help="Option to force overwrite of existing file."),
            ] = False,
         ):
    if testdata:
        content = DUMMY_QR_DATA
        print(f'Running in testdata mode')

    if action == CREATE_PNG_QR_FILE:
        genart = GeneratedArtifact.CREATE_PNG_QR_FILE
        create_png_file(content, filename, overwrite_png=forcewrite)

    elif action == CREATE_SIMPLIPLAY_PDF_FILE:
        genart = GeneratedArtifact.CREATE_SIMPLIPLAY_PDF_FILE
        create_pdf_file(content, filename, layout=genart, title="SIMPLI-PLAY MEDIA LINK", prefix=None,
                        postfix=content, overwrite_pdf=forcewrite, testmode=testdata)
        # layout = 'simple'

    elif action == CREATE_RAILINGS_PDF_FILE:
        genart = GeneratedArtifact.CREATE_RAILINGS_PDF_FILE
        create_pdf_file(content, filename, layout=genart, title=title, prefix=prefix, postfix=postfix,
                        overwrite_pdf=forcewrite, testmode=testdata)
        # layout='rail'

    else:
        report_err(2, f'Invalid action. Valid actions are: {action_str}')
        return None

def perform_unit_test():
    print(f'START unit tests')
    runner = CliRunner()
    test_args = [CREATE_PNG_QR_FILE, 'sam.png', '"this is the text"', ]
    result = runner.invoke(main, test_args)
    cmd = ''
    fname = 'test.png'
    freqd = False
    regex = 'abc'
    listarg = [CREATE_PNG_QR_FILE, 'sam.png', '"this is the text"', ]
    #main(listarg)
    typer.run(main, listarg)
    print(f'END unit tests')


def selector():
    first_arg = sys.argv[1]
    print(f'First arg =={first_arg}')
    if first_arg == 'ut':
        perform_unit_test()
    else:
        typer.run(main)

if __name__ == "__main__":
    selector()
    #typer.run(main)