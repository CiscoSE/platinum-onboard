import utilities
import pytest

def test_validate_byte():
    ret = utilities.validate_byte_as_printable(chr(30))
    assert ret=='.'

    ret = utilities.validate_byte_as_printable(chr(32))
    assert ret==' '

    ret = utilities.validate_byte_as_printable(chr(128))
    assert ret=='.'

    ret = utilities.validate_byte_as_printable(chr(76))
    assert ret==chr(76)
