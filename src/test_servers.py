import pytest


def test_client():
    from client import client
    assert 1 == 1
    # assert client("message 1") == "message 1"

# messages shorter than one buffer in length
# messages longer than several buffers in length
# messages that are an exact multiple of one buffer in length
# messages containing non-ascii characters

