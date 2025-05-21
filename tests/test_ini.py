#!/usr/bin/env python3
from logging import DEBUG, getLogger
from pathlib import Path

import pytest

from abara_file_io import read_ini_file, write_ini_file

log = getLogger(__name__)


@pytest.mark.parametrize(
    ('ini_dict', 'file_name'),
    [
        pytest.param(1, 'flat_dict1', id='flat_dict1'),
        pytest.param(2, 'flat_dict2', id='flat_dict2'),
        pytest.param(
            3,
            'section_dict',
            id='section_dict',
        ),
        pytest.param(
            4,
            'error_dict',
            id='error_dict',
        ),
        pytest.param(
            5,
            'empty_dict',
            id='empty_dict',
        ),
    ],
    indirect=['ini_dict'],
)
def test_write_ini_file(
    ini_dict: tuple[dict, str],
    file_name: str,
    tmp_path: Path,
    caplog: pytest.LogCaptureFixture,
) -> None:
    caplog.set_level(DEBUG)

    file_path = tmp_path / 'tmp' / f'test_ini_file_{file_name}.ini'
    write_ini_file(ini_dict[0], file_path)

    assert ('abara_file_io.ini', DEBUG, ini_dict[1]) in caplog.record_tuples


@pytest.mark.parametrize(
    ('ini_dict', 'file_name'),
    [
        pytest.param(1, 'flat_dict1', id='flat_dict1'),
        pytest.param(2, 'flat_dict2', id='flat_dict2'),
        pytest.param(
            3,
            'section_dict',
            id='section_dict',
        ),
        pytest.param(
            4,
            'error_dict',
            id='error_dict',
        ),
        pytest.param(
            5,
            'empty_dict',
            id='empty_dict',
        ),
    ],
    indirect=['ini_dict'],
)
def test_read_ini_file(
    ini_dict: tuple[dict, str],
    file_name: str,
    tmp_path: Path,
    caplog: pytest.LogCaptureFixture,
) -> None:
    caplog.set_level(DEBUG)
    file_path = tmp_path / 'tmp' / f'test_ini_file_{file_name}.ini'
    write_ini_file(ini_dict[0], file_path)
    read_file = read_ini_file(file_path)
    if ini_dict[1] == 'Success':
        assert ini_dict[0] == read_file
    else:
        assert read_file == {}
