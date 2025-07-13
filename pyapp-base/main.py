#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main.py

アプリケーションのメインエントリーポイントモジュール。

このモジュールは、アプリケーションの主要な実行フローを制御し、
各種モジュールを組み合わせてアプリケーション全体の動作を実現します。
"""

# =============================================================================
# インポート
# =============================================================================
# 標準ライブラリ


# サードパーティライブラリ


# ローカルライブラリ
from .__version__ import __version_info__
from . import app_argparser
from . import app_config
from . import app_const
from . import app_exceptions
from . import app_logger
from . import app_validation

from . import utils


# =============================================================================
# メイン処理
# =============================================================================
def main():
    """
    アプリケーションのメイン関数。
    
    アプリケーションの初期化から終了まで、全体的な処理フローを管理します。
    
    Returns:
        int: 終了コード（0: 正常終了, 1以上: エラー終了）
    """
    try:
        print(f"Application version: {__version_info__}")
        
        # サンプルユーティリティ関数の呼び出し
        utils.util0_test()
        
        print("Application started successfully.")
        return 0
        
    except Exception as e:
        print(f"Application error: {e}")
        return 1


# =============================================================================
# スクリプト実行時の処理
# =============================================================================
if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
