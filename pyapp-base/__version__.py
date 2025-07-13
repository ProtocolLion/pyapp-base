#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__version__.py

アプリケーションのバージョン情報管理モジュール。

このモジュールは、アプリケーションのバージョン情報を一元管理し、
セマンティック バージョニング（https://semver.org/）に従った
バージョン表記を提供します。

バージョン形式: MAJOR.MINOR.PATCH
- MAJOR: 互換性のない API の変更
- MINOR: 後方互換性のある機能の追加
- PATCH: 後方互換性のあるバグ修正

変更履歴:
    2025-xx-xx: 初期バージョン作成 (v0.1.0)
"""

# バージョン情報（タプル形式）
__version_info__ = (0, 1, 0)

# バージョン文字列（ドット区切り形式）
__version__ = '.'.join(map(str, __version_info__))


def get_version():
    """
    バージョン文字列を取得します。
    
    Returns:
        str: バージョン文字列（例: "0.1.0"）
    """
    return __version__


def get_version_info():
    """
    バージョン情報をタプル形式で取得します。
    
    Returns:
        tuple: バージョン情報タプル（例: (0, 1, 0)）
    """
    return __version_info__


if __name__ == "__main__":
    print(f"Version: {get_version()}")
    print(f"Version info: {get_version_info()}")
