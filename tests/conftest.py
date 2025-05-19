#!/usr/bin/env python3
from logging import getLogger
from pathlib import Path
from textwrap import dedent

import pytest

log = getLogger()


@pytest.fixture(scope='session')
def sample_str() -> str:
    text = """\
    これがサンプルテキストです。
    果たしてファイルはきちんと認識できるのでしょうか？
    よろしくお願いします！
    """
    return dedent(text)


@pytest.fixture(scope='session')
def sample_text_file(tmp_path_factory: pytest.TempPathFactory, sample_str: str) -> Path:
    dir_path = tmp_path_factory.mktemp('pytest')
    file_path = dir_path / 'sample_text.txt'
    file_path.touch()
    file_path.write_text(sample_str)
    return file_path


@pytest.fixture
def sample_text_file_shift_jis(
    tmp_path_factory: pytest.TempPathFactory, sample_str: str, request: pytest.FixtureRequest
) -> Path:
    log.info(f'{request.param}')
    dir_path: Path = tmp_path_factory.mktemp('pytest')
    file_path: Path = dir_path / f'sample_text_{request.param}.txt'
    file_path.touch()
    file_path.write_text(sample_str, encoding=str(request.param))
    return file_path
