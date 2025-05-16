#!/usr/bin/env python
import logging
from collections.abc import Iterable
from types import ModuleType
from typing import Final

from rich.logging import RichHandler


def setup_logging(
    set_level: int | str = logging.DEBUG,
    *,
    output_log_file: bool = False,
    log_file_name: str = 'app.log',
    tracebacks_suppress: Iterable[str | ModuleType] = (),
) -> None:
    """richを使って色付きのログを表示する設定

    Args:
        set_level (int | str, optional): 表示されるログレベルの設定 Defaults to logging.DEBUG.
        output_log_file (bool, optional): ログをファイルに書き出す Defaults to False.
        log_file_name (str, optional): 書き出されるログのファイル名 Defaults to 'app.log'.
        tracebacks_suppress (Iterable[str  |  ModuleType], optional):
            他のライブラリから出力されたログの除外リスト Defaults to ().
    """
    # ルートロガー（全体）を取得
    root_logger = logging.getLogger()
    root_logger.setLevel(set_level)

    if not root_logger.hasHandlers():
        # RichHandlerを作成
        rich_handler = RichHandler(
            rich_tracebacks=True, markup=True, tracebacks_suppress=tracebacks_suppress
        )

        # ルートロガーにハンドラーを追加
        root_logger.addHandler(rich_handler)

        if output_log_file:
            # FileHandler（ログファイル用）
            file_formatter: Final = logging.Formatter(
                '%(asctime)s %(levelname)-8s - %(filename)s - '
                '%(funcName)s %(lineno)d - %(message)s'
            )
            file_handler = logging.FileHandler(log_file_name, encoding='utf-8')
            file_handler.setFormatter(file_formatter)
            root_logger.addHandler(file_handler)
