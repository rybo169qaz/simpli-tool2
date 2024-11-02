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
#from fpdf2 import FPDF
#import fpdf

#from fpdf import HTMLMixin
import lorem


CREATE_PNG_QR_FILE = 'qr'
CREATE_RAILINGS_PDF_FILE = 'railings'
CREATE_SIMPLIPLAY_PDF_FILE = 'simpli'

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

def create_png_file(content: str, filen: str, forcew: bool):
    file_name, file_extension = os.path.splitext(filen)

    if not forcew and os.path.isfile(filen):
        report_err(5, 'File exists')
    elif file_extension != '.png':
        report_err(6, 'Filename must have a .png extension')
    else:
        try:
            qrc = create_qr(content)
            qrc.save(filen, scale=5)
            print(f'Created file {filen} containing >>{content}<<')
        except:
            report_err(7    , 'Failed to write file')
    return True


def create_pdf_file(content: str, filen: str, layout='simpli', title=None, prefix: str = None, postfix: str = None,
                    forcew: bool = False):
    file_name, file_extension = os.path.splitext(filen)
    if not forcew and os.path.isfile(filen):
        report_err(9, 'File exists')
    elif file_extension != '.pdf':
        report_err(10, 'Filename must have a .pdf extension')
    else:
        try:
            pngname = file_name + '.png'
            create_png_file(content, pngname, forcew)

            pdf = FPDF() # see https://pyfpdf.readthedocs.io/en/latest/index.html
            # https://py-pdf.github.io/fpdf2/index.html
            #pdf.add_page()

            #pdf.add_page(format='A4')
            #pdf.add_page(orientation='L')
            if layout == 'simple':
                #pdf.add_page(orientation = 'L', format = 'A5')
                pdf.add_page(orientation='P', format='A4')
                pdf.set_left_margin(margin=20)
            else:
                pdf.add_page(orientation='P', format='A4')
                pdf.set_left_margin(margin=20)
                #pdf.set_right_margin(margin=20)

            yoff = 0
            title_h = 20
            if title is not None:
                pdf.set_font('Times', 'B', 32)
                pdf.cell(0, title_h, title, align = 'C', border = 1, ln = 2)
                pdf.ln()
                yoff += title_h

            prefix_h = 40
            if prefix is not None:
                pdf.set_font('Arial', 'B', 16)
                pdf.cell(0, prefix_h, prefix, border = 1, ln = 2)
                yoff += prefix_h

            # xoffset, yoffset, x-size, y-size
            img_y_off = 35
            yoff += img_y_off
            rect1 = 80, yoff, 50, 50
            pdf.rect(*rect1)
            pdf.image(
                pngname,
                *rect1,
                keep_aspect_ratio=True
            )

            lorum_test = lorem.paragraph()
            test_text = lorum_test[0:256]
            # test_text = lorum_test
            #lorum_test = lorem.sentence()

            post_h = 60
            yoff += post_h
            pdf.set_y(yoff)
            pdf.set_left_margin(margin=30)
            pdf.set_right_margin(margin=30)
            if postfix is not None:
                pdf.set_font('Times', 'B', 16)
                #pdf.cell(0, 80, lorum_test, border = 1, ln = 2)
                pdf.write(10, test_text)

            pdf.output(filen, 'F')
            print(f'Created file {filen} containing')
            print(f'\tTitle == {title}')
            print(f'\tPrefix text == {prefix}')
            print(f'\tPostfix text == {postfix}')
        except:
            report_err(11    , 'Failed to write file')

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
          forcewrite: Annotated[
            bool,
            typer.Option(help="Option to force overwrite of existing file."),
            ] = False,
         ):

    if action == CREATE_PNG_QR_FILE:
        create_png_file(content, filename, forcewrite)
    elif action == CREATE_RAILINGS_PDF_FILE:
        create_pdf_file(content, filename, layout='rail', title=title, prefix=prefix, postfix=postfix, forcew=forcewrite)
    elif action == CREATE_SIMPLIPLAY_PDF_FILE:
        create_pdf_file(content, filename, layout='simple', title="SIMPLI-PLAY MEDIA LINK", prefix=None, postfix=content,
                        forcew=forcewrite)
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
    #selector()
    typer.run(main)