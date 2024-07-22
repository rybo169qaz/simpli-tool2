import os
import const_data
import report


def print_well_known_fixed(wellk, mtyp, mlocation, mstr, mident):
    streamed = 'True' if mstr == 1 else 'False'
    if mstr == 0:
        streamed = 'False (file)'
    elif mstr == 1:
        streamed = 'True  (streamed)'
    else:
        streamed = mstr
    print(f"{wellk:25}, {mtyp:12}, {mlocation:15}, {streamed:16}, {mident:50}")

def list_well_known():
    print(f'List of well-known media\n')
    print_well_known_fixed('Well-known Name', 'Media-Type', 'Media-Location', 'Stream', 'ID')
    #print(f'Well-known Name,\tMedia-Type,\tMedia-Location,\tStream,\tID\n')
    for entry in const_data.well_known_uris:
        (wellknown, mtype, mloc, mstream, mid) = entry
        print_well_known_fixed(wellknown,mtype,mloc,mstream,mid)
    print(f'\n')
    known_name_desc =     'Well-known Name : Use this wellKnown name to shotthand specify the folowing attributes.'
    media_type_desc =     'Media Type      : If TEXT then it will be printed out. If MPEG then it will be played thru a media player.'
    media_location_desc = 'Media Location  : If test then it is in the local Media folder (pyplay/Media). If remote then it is on the network.'
    streamed_desc =       'Streamed        : Indicates whether the identity is a file that could be copied or only a stream. True==Streamed'
    identity_desc =       'Identity        : This is used in conjunction with the location field'
    print(f'Key:\n\t{known_name_desc}\n\t{media_type_desc}\n\t{media_location_desc}\n\t{streamed_desc}\n\t{identity_desc}')


def list_all_media():
    start = const_data.media_root
    msg = f'\nContents of Media directory: ({start})\n\n'

    for root, dirs, files in os.walk(start, topdown=True):
        for name in files:
            comb = os.path.join(root, name)
            comb = root + ' : ' + name
            msg += f'ENTRY {comb} \n'
    msg += '\n'
    return msg


def print_all_media():
    report.mod_mess(__name__, list_all_media())