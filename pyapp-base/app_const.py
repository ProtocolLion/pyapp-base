#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
app_const.py

アプリケーション定数管理モジュール。

このモジュールは、アプリケーション全体で使用される定数を一元管理します。
設定値、列挙型、デフォルト値などを定義し、アプリケーションの一貫性を保ちます。

定数の種類:


使用例:


"""

# =============================================================================
# インポート
# =============================================================================
# 標準ライブラリ
import datetime
from enum import Enum

# サードパーティライブラリ


# ローカルライブラリ
from .__version__ import __version_info__


# =============================================================================
# アプリケーション基本情報
# =============================================================================
APP_NAME_FULL = "Python Application Base"
APP_NAME_SHORT = "pyapp-base"
APP_NAME = APP_NAME_SHORT
APP_VERSION = '.'.join(map(str, __version_info__))
APP_VERSION_DATE = datetime.date.today().strftime("%Y-%m-%d")
APP_DESCRIPTION = "サンプルDescription"


# =============================================================================
# ファイル・ディレクトリ関連の定数
# =============================================================================
# 設定ファイル関連
DEFAULT_CONFIG_DIR      = "config"
DEFAULT_JSON_FILENAME   = f"{APP_NAME_SHORT}_config.json"
DEFAULT_INI_FILENAME    = f"{APP_NAME_SHORT}_config.ini"
DEFAULT_YAML_FILENAME   = f"{APP_NAME_SHORT}_config.yaml"
DEFAULT_TOML_FILENAME   = f"{APP_NAME_SHORT}_config.toml"
DEFAULT_CONFIG_FILENAME = DEFAULT_JSON_FILENAME


# =============================================================================
# 列挙型定義　
# 　定数が集合的な値を持つ場合に使用します
# =============================================================================
class AppEnum(Enum):
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

