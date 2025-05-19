#!/usr/bin/env python3
from logging import getLogger
from pathlib import Path

import pytest

from abara_file_io import read_str_file, write_str_file

log = getLogger(__name__)


def test_read_str_file_fixture(sample_text_file: Path, sample_str: str) -> None:
    read_data = read_str_file(sample_text_file)
    assert isinstance(read_data, str)
    assert read_data == sample_str


def test_write_str_file(tmp_path: Path, sample_str: str) -> None:
    file_path = tmp_path / 'pytest' / 'pytest_str.txt'
    write_str_file(sample_str, file_path)
    read_data = file_path.read_text(encoding='utf-8')
    assert read_data == sample_str


@pytest.mark.parametrize(
    'sample_text_file_shift_jis',
    [('utf-8'), ('shift_jis')],
    indirect=['sample_text_file_shift_jis'],
)
def test_read_str_file_shiftjis(sample_text_file_shift_jis: Path, sample_str: str) -> None:
    read_data = read_str_file(sample_text_file_shift_jis)
    assert read_data == sample_str
