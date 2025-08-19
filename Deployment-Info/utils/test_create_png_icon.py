import os.path
import pytest
import tempfile
from pathlib import Path
from create_png_icon import CreatePng

# To invoke:
# cd THIS FOLDER
# clear ; pytest -v -x -m createpng


def create_test_folder():
    # create a temporary directory
    tmpdir = tempfile.TemporaryDirectory(dir="/tmp", prefix="simpli_").name
    os.mkdir(tmpdir, 0o777)  # we create the dest dir
    if os.path.isdir(tmpdir) == False:
        raise ValueError('Failed to create temp directory')
    return tmpdir


PYT_PRE = 'Pytest Pre-condition test failed. Test framework has an error'

@pytest.mark.createpng
class TestCreatePng:
    """
    Tests the functionality of the CreatePng class.
    It does not test the wrapper code for CLI invocation of the script.
    """

    def test_empty_string(self):
        with pytest.raises(AttributeError) as excinfo:
            CreatePng('', 'ABC')
        assert str(excinfo.value) == 'Null or Empty filename provided'


    def test_filename_part_is_empty(self):
        with pytest.raises(AttributeError) as excinfo:
            tmpdir = create_test_folder()
            CreatePng(tmpdir + '/', 'ABC')
        assert str(excinfo.value) == 'No filename after the directory part'
        assert len(os.listdir(tmpdir)) == 0


    def test_filename_extension_is_not_png(self):
        with pytest.raises(AttributeError) as excinfo:
            tmpdir = create_test_folder()
            fname1 = tmpdir + '/zzzz'
            CreatePng(fname1, 'ABC')
        assert str(excinfo.value) == 'Incorrect extension (should be .png)'
        assert os.path.isfile(fname1) is False
        assert len(os.listdir(tmpdir)) == 0

        with pytest.raises(AttributeError) as excinfo:
            tmpdir = create_test_folder()
            fname2 = tmpdir + '/abc.doc'
            CreatePng(fname2, 'ABC')
        assert str(excinfo.value) == 'Incorrect extension (should be .png)'
        assert os.path.isfile(fname2) is False
        assert len(os.listdir(tmpdir)) == 0

    def test_file_already_exists(self):
        with pytest.raises(FileExistsError) as excinfo:
            filename = create_test_folder() + '/abc.png'
            Path(filename).touch()
            obj = CreatePng(filename, 'ABC')
            obj.generate_image()
        assert str(excinfo.value) == 'File already exists. Set file_overwrite if want to overwrite.'

    def test_good_simple_with_defaults(self):
        tmpdir = create_test_folder()
        fname = tmpdir + '/pqr.png'
        obj = CreatePng(fname, 'ABC')
        obj.generate_image()
        assert os.path.isfile(fname) is True
        assert len(os.listdir(tmpdir)) == 1

    def test_overwrite_existing_file(self):
        tmpdir = create_test_folder()
        fname = tmpdir + '/pqr.png'
        Path(fname).touch()
        touched_file_size = os.path.getsize(fname)
        print(f"The file size is: {touched_file_size} bytes")
        assert touched_file_size == 0 # this is just testing the pre-conditions

        obj = CreatePng(fname, 'ABC', file_overwrite=True)
        obj.generate_image()
        assert os.path.isfile(fname) is True
        assert len(os.listdir(tmpdir)) == 1
        post_method_file_size = os.path.getsize(fname)
        print(f"The file size is: {post_method_file_size} bytes")
        assert post_method_file_size != 0

