#!/usr/bin/env python3
from logging import DEBUG, getLogger
from pathlib import Path

import pytest

from abara_file_io import read_ini, write_ini

log = getLogger(__name__)


@pytest.mark.parametrize(
    ('sample_dicts', 'file_name'),
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
    indirect=['sample_dicts'],
)
def test_write_ini(
    sample_dicts: tuple[dict, str],
    file_name: str,
    tmp_path: Path,
    caplog: pytest.LogCaptureFixture,
) -> None:
    caplog.set_level(DEBUG)

    file_path = tmp_path / 'tmp' / f'test_ini_file_{file_name}.ini'
    write_ini(sample_dicts[0], file_path)

    assert ('abara_file_io.ini', DEBUG, sample_dicts[1]) in caplog.record_tuples


@pytest.mark.parametrize(
    ('sample_dicts', 'file_name'),
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
    indirect=['sample_dicts'],
)
def test_read_ini(
    sample_dicts: tuple[dict, str],
    file_name: str,
    tmp_path: Path,
    caplog: pytest.LogCaptureFixture,
) -> None:
    caplog.set_level(DEBUG)
    file_path = tmp_path / 'tmp' / f'test_ini_file_{file_name}.ini'
    write_ini(sample_dicts[0], file_path)
    read_file = read_ini(file_path)
    if sample_dicts[1] == 'Success':
        assert sample_dicts[0] == read_file
    else:
        assert read_file == {}
