import pytest

from amg import plaintextmetadata as ptm

@pytest.fixture
def pcalign_metadata(datadir):
    return ptm.PcAlignMetadata(datadir.join('pc_align.txt'))

def test_data(pcalign_metadata):
    data = pcalign_metadata.data
    assert len(data) == 9

def test_vertical_accuracy_test_name(pcalign_metadata):
    name = pcalign_metadata.vertical_accuracy_test_name
    assert 'Median vertical offset' in  name

def test_median_error(pcalign_metadata):
    median_error = pcalign_metadata.median_error
    assert median_error == -1.56749

def test_vertical_accuracy_value(pcalign_metadata):
    assert pcalign_metadata.vertical_accuracy_value == -1.56749