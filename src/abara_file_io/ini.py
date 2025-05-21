#!/usr/bin/env python3
from configparser import ConfigParser
from logging import getLogger
from os import PathLike
from pathlib import Path
from typing import cast

from abara_file_io.util import create_file

log = getLogger(__name__)


def get_regex_setting(file_path: Path | str) -> list[str]:
    # 正規表現をテキストから所得
    p = Path(file_path)
    with p.open(encoding='utf-8') as lines:
        return [i.rstrip('\r\n') for i in lines]


type IniConfigValue = str | int | float | bool


def _restore_ini_config(input_str: str) -> IniConfigValue:
    """iniファイル化でstrに変換された値を元に戻す

    Args:
        input_str (str): iniから読み込んだ値

    Returns:
        IniConfigValue: 修正された値
    """
    try:
        return int(input_str)
    except ValueError:
        pass

    try:
        return float(input_str)
    except ValueError:
        pass

    if input_str == 'True':
        return True
    if input_str == 'False':
        return False

    return input_str


def _restore_ini_configs(input_dict: dict[str, str]) -> dict[str, IniConfigValue]:
    """辞書内のvalueをini化する前の元の型に復元する

    Args:
        input_dict (dict[str, str]): iniファイルから読み込んだ辞書

    Returns:
        dict[str, IniConfigValue]: 型を修正された辞書
    """
    return {key: _restore_ini_config(value) for key, value in input_dict.items()}


def read_ini_file(
    file_path: str | PathLike[str],
) -> dict[str, IniConfigValue] | dict[str, dict[str, IniConfigValue]]:
    """iniをファイルを読み込み、辞書に変換して出力する

    iniはstr以外を扱えないので、辞書に変換する時に自動的にint,float,boolをpythonの型に変換する
    ソースとなる辞書に文字列で'True'や'12.34'などを保存していた場合も、strやfloatに変換される

    Args:
        file_path (str | PathLike[str]): _description_

    Returns:
        dict[str, IniConfigValue] | dict[str, dict[str, IniConfigValue]]:
            IniConfigValueはiniに保存できるstr,int,float,boolの4種類のどれか
    """
    file_path = Path(file_path)

    if not file_path.exists():
        return {}

    try:
        config = ConfigParser()
        with file_path.open(encoding='utf-8') as f:
            config.read_file(f)
        config_sections: list = config.sections()
        config_result: dict = {}
        if len(config_sections) > 1:
            for i in config_sections:
                config_result[i] = _restore_ini_configs(dict(config.items(i)))
        else:
            config_result = _restore_ini_configs(dict(config.items(config_sections[0])))
    except IndexError:
        log.exception(f'読み込もうとしたファイルが存在しません [{file_path}]')
        return {}
    else:
        return config_result


def _correct_all_input_values(input_dict: dict) -> bool:
    """入力された辞書のvalueが全てIniConfig = str | int | float | bool であればTrueを返す

    Args:
        input_dict (dict): 判定する辞書

    Returns:
        bool: 全てが str | int | float | bool であればTrue
    """
    return all(isinstance(i, (str, int, float, bool)) for i in input_dict.values())


def _data_ini_convertible_is_decision(
    data: dict[str, IniConfigValue] | dict[str, dict[str, IniConfigValue]],
    config: ConfigParser,
) -> ConfigParser:
    """入力されたデータがiniに変換できるか判定してconfigparserに書き込む

    Args:
        data (dict[str, IniConfigValue] | dict[str, dict[str, IniConfigValue]]):
            iniに書き込む辞書データ
        config (ConfigParser): 入力されたconfigparser

    Returns:
        ConfigParser: 辞書の内容を格納したconfigparser
    """
    data_values_all_dict_type: bool = all(isinstance(i, dict) for i in data.values())
    data_values_all_ini_config_type = all(
        _correct_all_input_values(i) for i in data.values() if isinstance(i, dict)
    )
    if data_values_all_dict_type and data_values_all_ini_config_type:
        log.debug('multi section')
        log.debug('Success')
        multi_section_data = cast('dict[str, dict[str, IniConfigValue]]', data)
        for i in multi_section_data:
            config.add_section(i)
            for key, value in multi_section_data[i].items():
                config.set(i, key, str(value))

    elif _correct_all_input_values(data):
        log.debug('single section')
        log.debug('Success')
        config.add_section('configs')
        for key, value in data.items():
            config.set('configs', key, str(value))
    else:
        log.warning('入力された内容がini化できない形式です')
        log.debug('Error')

    return config


def write_ini_file(
    data: dict[str, IniConfigValue] | dict[str, dict[str, IniConfigValue]],
    file_path: str | PathLike[str],
) -> None:
    file_path = Path(file_path)

    config = _data_ini_convertible_is_decision(data, ConfigParser())

    if len(config.sections()) == 0:
        return

    create_file(file_path)
    with Path(file_path).open(mode='w', encoding='utf-8') as config_data:
        config.write(config_data)
