#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__init__.py
プロジェクトの初期化モジュール
"""

# utilsパッケージで公開する関数をインポート
from .util0 import util0_test

# パッケージレベルで公開するオブジェクトを定義
__all__ = [
    "util0_test",
]

# パッケージの初期化処理（必要に応じて）
def _initialize_package():
    """パッケージの初期化処理"""
    pass

# パッケージロード時の初期化実行
_initialize_package()
