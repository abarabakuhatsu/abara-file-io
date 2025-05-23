#!/usr/bin/env python3
from collections.abc import Sequence
from logging import WARNING, getLogger
from pathlib import Path
from textwrap import dedent

import pytest

log = getLogger()


@pytest.fixture(autouse=True)
def log_level_set() -> None:
    getLogger('chardet').setLevel(WARNING)


# test_str


@pytest.fixture(scope='session')
def sample_str() -> str:
    text = """\
    瑣　事

    　人生を幸福にするためには、日常の瑣事を愛さなければならぬ。雲の光、竹の戦ぎ、群雀の声、行人の顔、――あらゆる日常の瑣事のうちに無上の甘露味を感じなければならぬ。
    　人生を幸福にするためには？　しかし瑣事を愛するものは瑣事のために苦しまなければならぬ。庭前の古池に飛びこんだ蛙は百年の愁いを破ったであろう。が、古池を飛び出した蛙は百年の愁いを与えたかもしれない。いや、芭蕉の一生は享楽の一生であるとともに、誰の目にも受苦の一生である。我々も微妙に楽しむためには、やはりまた微妙に苦しまなければならぬ。
    　人生を幸福にするためには、日常の瑣事に苦しまなければならぬ。雲の光、竹の戦ぎ、群雀の声、行人の顔、――あらゆる日常の瑣事のうちに堕地獄の苦痛を感じなければならぬ。
    """  # noqa: E501
    return dedent(text)


@pytest.fixture(scope='session')
def create_sample_text_file(tmp_path_factory: pytest.TempPathFactory, sample_str: str) -> Path:
    dir_path = tmp_path_factory.mktemp('pytest')
    file_path = dir_path / 'sample_text.txt'
    file_path.touch()
    file_path.write_text(sample_str)
    return file_path


@pytest.fixture
def create_sample_text_files_multiple_encodings(
    tmp_path_factory: pytest.TempPathFactory, sample_str: str, request: pytest.FixtureRequest
) -> Path:
    log.info(f'{request.param}')
    dir_path: Path = tmp_path_factory.mktemp('pytest')
    file_path: Path = dir_path / f'sample_text_{request.param}.txt'
    file_path.touch()
    file_path.write_text(sample_str, encoding=str(request.param), newline='\n')
    return file_path


# test_ini


@pytest.fixture
def sample_ini_dicts(request: pytest.FixtureRequest) -> tuple[dict, str]:
    match request.param:
        case 1:
            return ({'foo': 'a', 'bar': 'b', 'baz': 'c', 'qux': 'd'}, 'Success')
        case 2:
            return ({'foo': 1, 'bar': 2, 'baz': 'three', 'qux': True}, 'Success')
        case 3:
            return (
                {
                    'section1': {'foo': 'one', 'bar': 2, 'baz': 'three', 'qux': True},
                    'section2': {'foo': 1, 'bar': 'two', 'baz': 3.5, 'qux': False},
                },
                'Success',
            )
        case 4:
            return (
                {
                    'section1': {'foo': {'qux': 4}, 'bar': 'two', 'baz': 'three'},
                    'section2': {
                        'foo': 'one',
                        'bar': [1, 2, 3],
                        'baz': {'qux': 130, 'quux': 256},
                    },
                },
                'Error',
            )
        case _:
            return ({}, 'Error')


# test_json_yaml_toml


@pytest.fixture
def base_dicts() -> list[dict]:
    return [
        {'foo': 'a', 'bar': 'b', 'baz': 'c', 'qux': 'd'},
        {'foo': 1, 'bar': 2, 'baz': 'three', 'qux': True},
        {
            'section1': {'foo': 'one', 'bar': 2, 'baz': 'three', 'qux': True},
            'section2': {'foo': 1, 'bar': 'two', 'baz': 3.5, 'qux': False},
        },
        {
            'section1': {'foo': {'qux': 4}, 'bar': 'two', 'baz': 'three'},
            'section2': {
                'foo': 'one',
                'bar': [1, 2, 3],
                'baz': {'qux': 130, 'quux': 256},
            },
        },
        {
            'section1': {'foo': {'qux': 4}, 'bar': 'two', 'baz': 'three'},
            'section2': {
                'foo': 'one',
                'bar': [1, 2, 3],
                'baz': {'qux': 130, 'quux': 256},
            },
        },
        {},
    ]


@pytest.fixture
def base_dicts_title() -> list[str]:
    return [
        'flat_dict1',
        'flat_dict2',
        'section_dict1',
        'section_dict2',
        'section_dict3',
        'empty_dict',
    ]


@pytest.fixture
def sample_common_dicts(
    request: pytest.FixtureRequest, base_dicts: list[dict], base_dicts_title: list[str]
) -> tuple[dict, str]:
    suffix = ''

    if isinstance(request.param, int):
        if request.param > len(base_dicts) - 1:
            return {}, 'End'
        result_dict = base_dicts[request.param]
        result_title = 'no_titile'

    elif isinstance(request.param, Sequence) and isinstance(request.param[0], int):
        request_dict_no = request.param[0]
        if request_dict_no > len(base_dicts) - 1:
            return {}, 'End'
        result_dict = base_dicts[request_dict_no]
        result_title = base_dicts_title[request_dict_no]
        if len(request.param) > 1 and isinstance(request.param[1], str):
            suffix = request.param[1]

    else:
        return {}, 'Error'

    return result_dict, result_title + suffix
