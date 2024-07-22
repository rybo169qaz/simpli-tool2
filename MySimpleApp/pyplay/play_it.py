from report import *
from media_identity import *
import process_qr


def play_material(playobj, is_streamed, media_type, path_to_use):
    if media_type not in MEDIA_TYPE_SET:
        exit_with_message(f'Unknown media type ({media_type})', 11)

    #print(f'\nplay_media: \n\tmediaType={media_type} \n\tfile={path_to_use}', flush=True)

    #print(f'\nMedia found', flush=True)
    try:
        resp = True
        if media_type == 'TEXT':
            step_details = 0.01
            start = 5
            numline = 7
            #play_text(path_to_use, step_details, line_start=start, line_total=numline)
            playobj.play_text(path_to_use, step_details, line_start=start, line_total=numline)

        elif media_type == 'MPEG':
            # mpeg
            starttime = 5
            dur = 20
            vol = 30
            playobj.play_media(is_streamed, path_to_use, start_time=starttime, duration=dur, volume=vol)

        else:
            print(f'ERROR: Unknown media type')
            resp = False
    except Exception as e:
        print(f'Error ({e}): Media path is invalid {path_to_use}')
        resp = False

    return resp


def play_wellknown(playobj, well_known, verbose=True):
    print(f'(play_wellknown): use {well_known}')
    media_id = MediaIdentity(well_known)
    media_type = media_id.med_type()
    media_location = media_id.med_location()
    media_streamed = media_id.med_streamed()
    media_identity = media_id.med_identity()

    if media_type == 'UNKNOWN':
        unknown_media_err_msg = 'Specified name (' + well_known + ') is NOT known.'
        exit_with_message(unknown_media_err_msg, 15)

    is_abs = utils.is_absolute_path(media_identity)
    if verbose:
        print(f'wellknown={well_known} , id={media_id}, IsAbs={is_abs}, Loc={media_location}')

    # sanity check on some of the identified meta-data
    if media_location != 'remote':
        if not file_is_readable(media_identity):
            exit_with_message(f'File is not readable: {media_identity}', 21)
    else:
        print(f'SHOULD (but not doing) a remote media test for {media_identity}')

    play_material(playobj, media_streamed, media_type, media_identity)


def play_qr(playobj, qr_file, verbose=True):
    qrobj = process_qr.ProcessQR(qr_file, False)
    extracted_data = qrobj.get_known()
    # we will ASSUME  that the xtracted data is in teh wellknown format
    wellknown_name = extracted_data
    play_wellknown(playobj, wellknown_name)


def map_qr_image_to_content(the_image_file):
    print(f'(map_qr_image_to_content) image file=={the_image_file}')
    qr_obj = process_qr.ProcessQR(the_image_file)
    content = qr_obj.get_raw()
    return content