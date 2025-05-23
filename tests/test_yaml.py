#!/usr/bin/env python3
from logging import DEBUG, getLogger
from pathlib import Path

import pytest

from abara_file_io import read_yaml, write_yaml

log = getLogger(__name__)


@pytest.mark.parametrize(
    ('sample_ini_dicts', 'file_name'),
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
            'nest_dict',
            id='nest_dict',
        ),
        pytest.param(
            5,
            'empty_dict',
            id='empty_dict',
        ),
    ],
    indirect=['sample_ini_dicts'],
)
def test_write_yaml(
    sample_ini_dicts: tuple[dict, str],
    file_name: str,
    tmp_path: Path,
    caplog: pytest.LogCaptureFixture,
) -> None:
    caplog.set_level(DEBUG)

    file_path = tmp_path / 'tmp' / f'test_yaml_file_{file_name}.yml'
    write_yaml(sample_ini_dicts[0], file_path)

    assert Path(file_path).exists()
    assert read_yaml(file_path) == sample_ini_dicts[0]
