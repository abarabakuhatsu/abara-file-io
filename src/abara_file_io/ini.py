#!/usr/bin/env python3
import configparser
from logging import getLogger
from pathlib import Path

log = getLogger(__name__)


def get_regex_setting(file_path: Path | str) -> list[str]:
    # 正規表現をテキストから所得
    p = Path(file_path)
    with p.open(encoding='utf-8') as lines:
        return [i.rstrip('\r\n') for i in lines]


def read_config_file(file_path: Path | str) -> dict[str, str] | list[dict[str, str]] | None:
    """受け取ったパスのiniを読み込み辞書として返す。

    Args:
        file_path (Union[Path, str]): 読み込むファイルのパス

    Returns:
        Union[Dict[str], List[Dict[str]], None]:
            複数セクションの場合はlistへの入れ子辞書になるので注意
    """
    file_path = Path(file_path)
    try:
        config = configparser.ConfigParser()
        config.read(filenames=file_path, encoding='utf-8')
        log.debug(file_path)
        config_sections: list = config.sections()
        log.debug(config_sections)
        config_result: dict = {}
        if len(config_sections) > 1:
            for i in config_sections:
                config_result[i] = dict(config.items(i))
        else:
            config_result = dict(config.items(config_sections[0]))
    except IndexError:
        log.exception(f'読み込もうとしたファイルが存在しません [{file_path}]')
        return None
    else:
        return config_result


if __name__ == '__main__':
    pass
