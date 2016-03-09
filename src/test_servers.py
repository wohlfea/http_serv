
# -*- coding: UTF-8 -*-
import pytest


def test_client():
    """Test message shorter than 1 buffer in length"""
    from client import client
    assert client("message 1") == "message 1"


def test_client_long_msg():
    """Test message longer than several buffers in length"""
    from client import client
    msg = u''
    for i in range(1024):
        msg += 'abc'
    msg += 'abc'
    assert client(msg) == msg


def test_client_buffer_divisible_msg():
    """Test message with length as multiple of buffer length"""
    from client import client
    msg = u''
    for i in range(1024):
        msg += 'abc'
    assert client(msg) == msg


def test_client_non_ascii_msg():
    """Test message with non-ascii characters"""
    from client import client
    # try explicitly creating str
    msg = u'aeieno\'é\', \'ö\' or \'ĉ\','
    assert client(msg) == msg

