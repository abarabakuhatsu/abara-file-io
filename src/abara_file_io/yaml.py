#!/usr/bin/env python3
from logging import getLogger
from os import PathLike
from pathlib import Path

from ruamel.yaml import YAML
from ruamel.yaml.parser import ParserError

from .util import check_encoding_open_file

log = getLogger(__name__)


def read_yaml_file(file_path: str | PathLike) -> dict:
    """YAMLファイルの読み込み

        リスト、もしくは辞書型の変数として読み込む
        読み込みに失敗した場合は空の辞書を返す

    Args:
        file_path (Union[Path, str]): 書き込むファイル名

    Returns:
        Union[dict, None]:
            正確にはdictのインスタンスのruamel.yaml.comments.CommentedMap
    """
    try:
        yaml = YAML()

        path_obj = Path(file_path)

        with path_obj.open(mode='r', encoding='utf-8') as yaml_file:
            return yaml.load(yaml_file)
    except UnicodeDecodeError:
        log.exception('読み込みファイルのエンコードがutf-8ではありません]')
        file_encode = check_encoding_open_file(file_path)
        yaml = YAML()
        path_obj = Path(str(file_path))
        with path_obj.open(mode='r', encoding=file_encode) as yaml_file:
            yaml_dict = yaml.load(yaml_file)
        log.warning(f'不正なエンコード（{file_encode}）なので強制的にutf-8に変換を試みます')
        with path_obj.open(mode='w', encoding='utf-8') as yaml_file:
            yaml.dump(yaml_dict, yaml_file)
        return yaml_dict
    except FileNotFoundError:
        log.exception('読み込もうとしたファイルが存在しません')
        return {}
    except PermissionError:
        log.exception(f'YAML読み込みファイル名が正しく指定されていません: {file_path}')
        return {}
    except ParserError:
        log.exception('YAMLファイルの記述が不正です')
        return {}


def write_yaml_file(
    data: list | dict, file_path: str | PathLike, *, crlf_flag: bool = False
) -> None:
    """YAMLファイルとして出力する

        第一引数で受け取ったパスに、第二引数で受け取った内容をYAMLとして書き込む。

    Args:
        data (list | dict): _description_
        file_path (str | PathLike): _description_
        crlf_flag (bool, optional): _description_. Defaults to False.
    """
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    try:
        yaml = YAML()
        yaml.indent(mapping=2, sequence=4, offset=2)

        path_obj = Path(file_path)

        if crlf_flag is False:
            with path_obj.open(mode='w', encoding='utf-8', newline='\n') as yaml_file:
                yaml.dump(data, yaml_file)
        else:
            with path_obj.open(mode='w', encoding='utf-8') as yaml_file:
                yaml.dump(data, yaml_file)
    except PermissionError:
        log.exception(f'書き込みファイル名が正しく指定されていません: {file_path}')


if __name__ == '__main__':
    pass
