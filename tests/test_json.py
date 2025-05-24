#!/usr/bin/env python3
from logging import DEBUG, getLogger
from pathlib import Path

import pytest

from abara_file_io import read_json, write_json

from .common_test_data import common_params

log = getLogger(__name__)


@pytest.mark.parametrize(*common_params())
def test_json_read_write(
    description: str,
    data: dict,
    file_name: str,
    expected: dict,
    options: dict,
    tmp_path: Path,
    caplog: pytest.LogCaptureFixture,
) -> None:
    caplog.set_level(DEBUG)
    file_path = tmp_path / 'tmp' / f'{file_name}.json'

    write_json(data=data, path=file_path)
    response = read_json(path=file_path)

    assert file_path.exists()
    assert response == data
