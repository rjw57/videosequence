import pytest
from videosequence import VideoSequence

def test_no_such_file():
    with pytest.raises(IOError):
        VideoSequence("does-not-exist")

def test_invalid_file():
    with pytest.raises(IOError):
        VideoSequence(__file__)
