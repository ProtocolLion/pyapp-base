#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__main__.py

パッケージを実行可能モジュールとして動作させるためのエントリーポイント。
以下のコマンドでパッケージを実行できます：
    python -m pyapp-base

このファイルは、パッケージが `python -m package_name` として実行された時に
自動的に呼び出されます。
"""

if __name__ == "__main__":
    from .main import main

    main()
