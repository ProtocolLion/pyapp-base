#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
app_const.py
プロジェクト定数モジュール
"""

#---------------------------------
# インポート
#---------------------------------
# standard library
import datetime
from enum import Enum

# third party library

# local library
from .__version__ import __version_info__

#---------------------------------
# 定数
#---------------------------------
APP_NAME_FULL    = "Python Application Base"
APP_NAME_SHORT   = "APP"
APP_NAME         = APP_NAME_SHORT
APP_VERSION      = '.'.join(map(str, __version_info__))
APP_VERSION_DATE = datetime.date.today().strftime("%Y-%m-%d")
APP_DESCRIPTION  = "A base template for Python applications"

#---------------------------------
# config
#---------------------------------
DEFAULT_CONFIG_DIR = 'config'
DEFAULT_CONFIG_FILENAME = f'{APP_NAME_SHORT.lower()}_config.json'
DEFAULT_INI_FILENAME = f'{APP_NAME_SHORT.lower()}_config.ini'

#---------------------------------
# logger
#---------------------------------
DEFAULT_LOG_LEVEL = 'DEBUG'
DEFAULT_LOG_FORMAT = '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
DEFAULT_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
DEFAULT_LOG_FILE = f'{APP_NAME_SHORT.lower()}.log'

#---------------------------------
# app
#---------------------------------
# 処理関連
class AppProcessMode(Enum):
    BATCH = 'batch'
    INTERACTIVE = 'interactive'
    DAEMON = 'daemon'

class AppOutputFormat(Enum):
    JSON = 'json'
    CSV = 'csv'
    YAML = 'yaml'
