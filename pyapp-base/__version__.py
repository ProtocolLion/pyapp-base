#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
__version__.py
バージョン情報モジュール
"""

# このモジュールは、アプリケーションのバージョン情報を定義します。

# 変更履歴
# 20xx-xx-xx : 初期バージョン作成

__version_info__ = (0, 1, 0)
__version__ = '.'.join(map(str, __version_info__))

def get_version():
    return __version__

if __name__ == "__main__":
    print("Version:", get_version())
