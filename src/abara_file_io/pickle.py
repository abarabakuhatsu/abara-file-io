#!/usr/bin/env python
import pickle
from logging import getLogger
from pathlib import Path
from typing import Any

log = getLogger(__name__)


def read_pickle(filename: str | None = 'object_data') -> Any:  # noqa: ANN401
    """書き込んだpickleデータを読み込む、失敗時はNoneを返す

    Args:
        filename (Optional[str], optional): 保存したファイル、拡張子は不要.
        Defaults to "object_data".

    Returns:
        Any: 読み込んだpickleオブジェクト、失敗時はNoneを返すので例外処理
    """
    log.debug(f'Pickle Lord: {filename}')
    with Path(f'{filename}.pkl').open('rb') as f:
        try:
            return pickle.load(f)  # noqa: S301
        except FileNotFoundError:
            log.debug('Pickleファイルが発見出来ず、noneを返す')
            return None


def write_pickle(data: Any, filename: str | None = 'object_data') -> bool:  # noqa: ANN401
    """オブジェクトをpickleに書き込む

    Args:
        data (Any): 保存するデータ
        filename (Optional[str], optional): 保存するファイル名、拡張子は不要.
        Defaults to "object_data".

    Returns:
        bool: 書き込み成功で True 失敗で False
    """
    with Path(f'{filename}.pkl').open('wb') as f:
        try:
            log.debug(f'Pickle Save: {type(data)} - {data}')
            pickle.dump(data, f)
        except AttributeError:
            log.exception('pickleに書き込みできませんでした')
            return False
        else:
            return True


if __name__ == '__main__':
    pass
