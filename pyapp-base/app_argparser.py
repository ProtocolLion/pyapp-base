#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
app_argparser.py
コマンドライン引数パーサーモジュール
"""

#---------------------------------
# インポート
#---------------------------------
# standard library
import argparse
import sys
import os
from pathlib import Path
from typing import Optional, List, Dict, Any, Union

# third party library

# local library
from . import app_const
from .app_exceptions import ValidationError, FileOperationError, ConfigError
from .app_validation import (
    validate_file_exists, 
    validate_directory_exists, 
    validate_range,
    validate_mutually_exclusive,
    validate_conditional_required,
    validate_file_or_directory_exists,
    validate_writable_directory
)

#---------------------------------
# カスタムアクション
#---------------------------------
class ValidateFileAction(argparse.Action):
    """ファイル存在チェックを行うカスタムアクション"""
    
    def __call__(self, parser, namespace, values, option_string=None):
        try:
            if isinstance(values, list):
                # 複数ファイルの場合
                for file_path in values:
                    validate_file_exists(file_path, f"ファイル({file_path})")
            elif values:
                validate_file_exists(str(values), f"ファイル({values})")
            setattr(namespace, self.dest, values)
        except FileOperationError as e:
            parser.error(str(e))


class ValidateDirectoryAction(argparse.Action):
    """ディレクトリ存在チェックを行うカスタムアクション"""
    
    def __call__(self, parser, namespace, values, option_string=None):
        if values:
            try:
                validate_directory_exists(str(values), f"ディレクトリ({values})")
            except FileOperationError as e:
                parser.error(str(e))
        setattr(namespace, self.dest, values)


class RangeAction(argparse.Action):
    """数値の範囲チェックを行うカスタムアクション"""
    
    def __init__(self, option_strings, dest, min_val=None, max_val=None, **kwargs):
        self.min_val = min_val
        self.max_val = max_val
        super().__init__(option_strings, dest, **kwargs)
    
    def __call__(self, parser, namespace, values, option_string=None):
        try:
            # 値が数値型であることを確認
            if not isinstance(values, (int, float)):
                parser.error(f"{option_string} の値は数値である必要があります: {values}")
            
            validate_range(values, self.min_val, self.max_val, f"オプション{option_string}")
            setattr(namespace, self.dest, values)
        except ValidationError as e:
            parser.error(str(e))


#---------------------------------
# main
#---------------------------------
class AppArgParser:
    """アプリケーション用の引数パーサークラス"""

    def __init__(self):
        """引数パーサーを初期化する"""
        self.parser = argparse.ArgumentParser(
            prog=app_const.APP_NAME,
            description=app_const.APP_DESCRIPTION,
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        
        self._setup_argument_groups()
        self._setup_arguments_common()
        self._setup_arguments()
    
    def _setup_argument_groups(self):
        """引数グループを設定する"""
        self.basic_group = self.parser.add_argument_group(
            'basic options',
            '基本的なオプション'
        )
        
        self.logging_group = self.parser.add_argument_group(
            'logging options',
            'ログ関連のオプション'
        )
        
        self.advanced_group = self.parser.add_argument_group(
            'advanced options',
            '高度なオプション'
        )
    
    def _setup_arguments_common(self):
        """共通引数の設定を行う"""
        # バージョン情報
        self.basic_group.add_argument(
            '-v', '--version',
            action='version',
            version=f'{app_const.APP_NAME} {app_const.APP_VERSION}',
            help='バージョン情報を表示して終了'
        )

        # 設定ファイル
        self.basic_group.add_argument(
            '-c', '--config',
            type=str,
            action=ValidateFileAction,
            default=app_const.DEFAULT_CONFIG_FILENAME,
            metavar='FILE',
            help=f'設定ファイルのパス (default: {app_const.DEFAULT_CONFIG_FILENAME})'
        )

        # ログレベル
        self.logging_group.add_argument(
            '--log-level',
            choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
            default=app_const.DEFAULT_LOG_LEVEL,
            metavar='LEVEL',
            help=f'ログレベルの設定 (default: {app_const.DEFAULT_LOG_LEVEL})'
        )

        # ログファイルのパス
        self.logging_group.add_argument(
            '--log-file',
            type=str,
            default=app_const.DEFAULT_LOG_FILE,
            metavar='FILE',
            help=f'ログ出力先ファイルのパス (default: {app_const.DEFAULT_LOG_FILE})'
        )

        # デバッグモード
        self.advanced_group.add_argument(
            '--debug',
            action='store_true',
            help='デバッグモードで実行（ログレベルがDEBUGに設定されます）'
        )

    def _setup_arguments(self):
        """アプリケーション固有の引数の設定を行う"""
        # 実行モード
        self.basic_group.add_argument(
            '--mode',
            choices=['analyze', 'convert', 'validate', 'batch'],
            default='analyze',
            metavar='MODE',
            help='実行モード: analyze(ファイル分析), convert(変換), validate(検証), batch(バッチ処理)'
        )

        # 入力ファイル/ディレクトリ
        self.basic_group.add_argument(
            'input',
            nargs='*',
            help='処理対象のファイルまたはディレクトリ'
        )

        # 出力ディレクトリ
        self.basic_group.add_argument(
            '-o', '--output',
            type=str,
            metavar='DIR',
            help='出力ディレクトリのパス'
        )

        # 出力フォーマット
        self.basic_group.add_argument(
            '--format',
            choices=['json', 'xml', 'csv', 'txt'],
            default='json',
            metavar='FORMAT',
            help='出力フォーマット (default: json)'
        )

    def parse_args(self, args: Optional[List[str]] = None) -> argparse.Namespace:
        """引数を解析する

        Args:
            args: 解析する引数のリスト（None の場合は sys.argv を使用）

        Returns:
            解析された引数のNamespace
            
        Raises:
            ValidationError: 引数の解析に失敗した場合
        """
        try:
            parsed_args = self.parser.parse_args(args)
            return self._post_process_args(parsed_args)
        except SystemExit as e:
            if e.code != 0:
                raise ValidationError(f"引数の解析に失敗しました: {e}")
            raise
    
    def _post_process_args(self, args: argparse.Namespace) -> argparse.Namespace:
        """引数の後処理を行う"""
        # デバッグモードの場合、ログレベルを自動調整
        if args.debug:
            args.log_level = 'DEBUG'
        
        # verboseレベルに応じてログレベルを調整
        elif args.verbose >= 2:
            args.log_level = 'DEBUG'
        elif args.verbose == 1:
            args.log_level = 'INFO'
        
        # quietモードの場合、ログレベルを調整
        if args.quiet:
            args.log_level = 'ERROR'
            args.no_console = True
        
        # パスを絶対パスに変換
        if hasattr(args, 'config') and args.config:
            args.config = str(Path(args.config).resolve())
        
        if hasattr(args, 'output') and args.output:
            args.output = str(Path(args.output).resolve())
        
        if hasattr(args, 'log_file') and args.log_file:
            args.log_file = str(Path(args.log_file).resolve())
        
        return args

    def validate_args(self, args: Optional[List[str]] = None) -> argparse.Namespace:
        """引数の検証と依存関係の解決を行う

        Args:
            args: 解析する引数のリスト（None の場合は sys.argv を使用）

        Returns:
            解析された引数のNamespace

        Raises:
            ValidationError: 引数の依存関係に問題がある場合
        """
        try:
            parsed_args = self.parse_args(args)
            self._validate_dependencies(parsed_args)
            self._validate_file_paths(parsed_args)
            return parsed_args
        except SystemExit as e:
            if e.code != 0:
                raise ValidationError(f"引数の検証に失敗しました")
            raise
    
    def _validate_dependencies(self, args: argparse.Namespace):
        """引数の依存関係を検証する"""
        # convertモードの場合は出力ディレクトリが必須
        validate_conditional_required(
            args.mode == 'convert',
            args.output,
            "--mode convert",
            "--output"
        )
        
        # batchモードの場合は入力が必須
        validate_conditional_required(
            args.mode == 'batch',
            args.input,
            "--mode batch",
            "入力ファイルまたはディレクトリ"
        )
        
        # 入力ファイルが指定されている場合の存在チェック
        if args.input:
            for input_path in args.input:
                validate_file_or_directory_exists(input_path, f"入力パス({input_path})")
        
        # quietとverboseは同時指定不可
        validate_mutually_exclusive(
            (args.quiet, args.verbose > 0),
            names=["--quiet", "--verbose"]
        )
        
        # dry-runとforceは同時指定不可
        validate_mutually_exclusive(
            (args.dry_run, args.force),
            names=["--dry-run", "--force"]
        )
    
    def _validate_file_paths(self, args: argparse.Namespace):
        """ファイルパスの検証を行う"""
        # 設定ファイルの存在チェック（デフォルトファイルは除く）
        if hasattr(args, 'config') and args.config != app_const.DEFAULT_CONFIG_FILENAME:
            validate_file_exists(args.config, "設定ファイル")
        
        # 出力ディレクトリの検証
        if hasattr(args, 'output') and args.output:
            validate_writable_directory(args.output, "出力ディレクトリ", create_if_missing=False)
        
        # ログディレクトリの検証
        if hasattr(args, 'log_dir') and args.log_dir:
            validate_writable_directory(args.log_dir, "ログディレクトリ", create_if_missing=True)

    def print_help(self):
        """ヘルプメッセージを表示する"""
        self.parser.print_help()
    
    def get_config_dict(self, args: argparse.Namespace) -> Dict[str, Any]:
        """引数を設定用の辞書に変換する
        
        Args:
            args: 解析された引数
            
        Returns:
            設定辞書
        """
        config = {}
        
        # 各引数を設定辞書に変換
        for key, value in vars(args).items():
            if value is not None:
                # キー名を設定ファイル形式に変換（ハイフンをアンダースコアに）
                config_key = key.replace('-', '_')
                config[config_key] = value
        
        return config
    
    def print_parsed_args(self, args: argparse.Namespace):
        """解析された引数を表示する（デバッグ用）"""
        print("=== 解析された引数 ===")
        for key, value in sorted(vars(args).items()):
            print(f"{key:20}: {value}")
        print("=====================")

