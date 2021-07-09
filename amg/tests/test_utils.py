import pytest
import os
import pathlib

from amg import utils

@pytest.mark.parametrize("n_images, expected", 
                        [(1, '/home/user/metadata/Image0.cub'),
                         (2, None)
                         ])
def test_find_file(fs, n_images, expected):
    basepath = "/home/user/metadata"
    for i in range(n_images):
        fs.create_file(os.path.join(basepath, f'Image{i}.cub'))
    found = utils.find_file('/home/user/metadata', '*.cub')
    # pathlib homogenizes over OSes (win vs. unix style paths)
    assert pathlib.Path(found) == pathlib.Path(expected)

def test_find_files(fs):
    basepath = '/home/user/metadata'
    fs.create_file(os.path.join(basepath, 'Image1.cub'))
    fs.create_file(os.path.join(basepath, 'Image2.cub'))
    found = utils.find_files('home/user/metadata', '*.cub')
    assert len(found) == 2

def test_write_fgdc():
    #assert False
    pass
  
def test_write_stac():
    #assert False
    pass
