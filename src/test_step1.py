import pytest


def test_response_ok():
    from server import response_ok
    response = response_ok()
    lines = response.split('\n')
    init_line = lines[0].split(' ')
    second_line = lines[1].split(' ')
    assert len(lines) >= 1
    assert '200' in init_line[1]
    assert init_line[0][:4] == 'HTTP'
    assert 'OK' in init_line[2]
    assert 'Content-Type:' in second_line[0]
    assert 'text/plain' in second_line[1]
    assert '\r\n' in response


def test_response_error():
    from server import response_error
    response = response_error()
    lines = response.split('\n')
    init_line = lines[0].split(' ')
    assert len(lines) >= 1
    assert '500' in init_line[1]
    assert init_line[0][:4] == 'HTTP'
    assert 'Internal' in init_line[2]
    assert 'Server' in init_line[3]
    assert 'Error' in init_line[4]
    assert '\r\n' in response
