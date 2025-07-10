#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
body.py
メインエントリポイントモジュール
"""

#---------------------------------
# インポート
#---------------------------------
# standard library
import os
import subprocess

# third party library

# local library
from .__version__ import __version_info__
from . import app_argparser
from . import app_config
from . import app_const
from . import app_exceptions
from . import app_logger

#---------------------------------
# 定数
#---------------------------------

#---------------------------------
# main
#---------------------------------
def main():
    """Main function for the body module."""

    ############################################################
    # argparser
    ############################################################
    parser = app_argparser.create_parser()
    args = parser.parse_args()

    ############################################################
    # logger
    ############################################################
    if args.log_level:
        app_logger.set_log_level(args.log_level)
    LOGGER.info("Start vtool.")

    ############################################################
    # config
    ############################################################
    config = app_config.load_config(args.config)
    slang_path = config.get('slang_path', 'slang')
    # 相対パスの場合は絶対パスに変換
    if not os.path.isabs(slang_path):
        # スクリプトからの相対パスを計算
        script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        slang_path = os.path.join(script_dir, slang_path)
    
    # JSON出力ディレクトリ
    json_output_dir = config.get('json_output_dir', '.')
    if not os.path.isabs(json_output_dir):
        json_output_dir = os.path.abspath(json_output_dir)
    # ディレクトリが存在することを確認
    os.makedirs(json_output_dir, exist_ok=True)
    
    LOGGER.info(f"Using slang binary: {slang_path}")
    LOGGER.info(f"JSON output directory: {json_output_dir}")

    ############################################################
    # main process
    ############################################################
