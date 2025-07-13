#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__license__.py

ライセンス情報管理モジュール。

このモジュールは、パッケージのライセンス情報を管理し、
MIT ライセンスの全文を提供します。

機能:
    - ライセンステキストの提供
    - 著作権情報の動的生成
    - ライセンス情報の表示

使用例:
    # コンソール出力
    from __license__ import print_license, print_copyright
    print_license()
    print_copyright()
    # string取得
    from __license__ import get_license, get_copyright_info
    str_license      = get_license()
    str_license_info = get_copyright_info()
"""

# =============================================================================
# インポート
# =============================================================================
from datetime import datetime


# =============================================================================
# ライセンス情報
# =============================================================================
COPYRIGHT_START_YEAR = 2025
COPYRIGHT_END_YEAR = datetime.now().year
COPYRIGHT_YEARS = (
    f'{COPYRIGHT_START_YEAR}-{COPYRIGHT_END_YEAR}' 
    if COPYRIGHT_START_YEAR != COPYRIGHT_END_YEAR 
    else str(COPYRIGHT_START_YEAR)
)

# 著作権者情報
COPYRIGHT_HOLDER = 'ProtocolLion'

# ライセンス全文
__license__ = (
    'MIT License\n'
    '\n'
    f'Copyright (c) {COPYRIGHT_YEARS} {COPYRIGHT_HOLDER}\n'
    '\n'
    'Permission is hereby granted, free of charge, to any person obtaining a copy\n'
    'of this software and associated documentation files (the "Software"), to deal\n'
    'in the Software without restriction, including without limitation the rights\n'
    'to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n'
    'copies of the Software, and to permit persons to whom the Software is\n'
    'furnished to do so, subject to the following conditions:\n'
    '\n'
    'The above copyright notice and this permission notice shall be included in all\n'
    'copies or substantial portions of the Software.\n'
    '\n'
    'THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n'
    'IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n'
    'FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n'
    'AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n'
    'LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n'
    'OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n'
    'SOFTWARE.\n'
)


# =============================================================================
# ライセンス生成関数
# =============================================================================
def get_license() -> str:
    """
    パッケージのライセンステキストを取得します。
    
    Returns:
        str: MITライセンスの全文
    """
    return __license__


def get_copyright_info() -> str:
    """
    著作権情報を取得します。
    
    Returns:
        str: 著作権情報
    """
    return f"Copyright (c) {COPYRIGHT_YEARS} {COPYRIGHT_HOLDER}"


def print_license() -> None:
    """ライセンス情報をコンソールに出力します。"""
    print(get_license(), end='')


def print_copyright() -> None:
    """著作権情報をコンソールに出力します。"""
    print(get_copyright_info())


# =============================================================================
# スクリプト実行時の処理
# =============================================================================
if __name__ == "__main__":
    print_license()
