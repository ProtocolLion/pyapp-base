#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
app_logger.py
アプリケーション用ロギングモジュール
"""

#---------------------------------
# インポート
#---------------------------------
# standard library
import functools
import logging
import logging.handlers
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Callable, Any

# third party library

# local library
from . import app_const


class AppLogger:
    """アプリケーション用のロガークラス"""
    
    def __init__(self, 
                 name: str = app_const.APP_NAME,
                 level: str = 'INFO',
                 log_dir: Optional[str] = None,
                 log_filename: Optional[str] = None,
                 enable_console: bool = True,
                 enable_file: bool = True):
        """
        Args:
            name: ロガー名
            level: ログレベル（DEBUG, INFO, WARNING, ERROR, CRITICAL）
            log_dir: ログディレクトリ（デフォルト: logs）
            log_filename: ログファイル名（デフォルト: app.log）
            enable_console: コンソール出力を有効にするか
            enable_file: ファイル出力を有効にするか
            
        Raises:
            ValueError: 無効なログレベルが指定された場合
        """
        self.name = name
        
        # ログレベルの検証
        level_upper = level.upper()
        if not hasattr(logging, level_upper):
            raise ValueError(f"Invalid log level: {level}. Must be one of: DEBUG, INFO, WARNING, ERROR, CRITICAL")
        
        self.level = getattr(logging, level_upper)
        self.log_dir = Path(log_dir or app_const.DEFAULT_LOG_DIR)
        self.log_filename = log_filename or app_const.DEFAULT_LOG_FILENAME
        self.enable_console = enable_console
        self.enable_file = enable_file
        
        self.logger = self._setup_logger()
    
    def _setup_logger(self) -> logging.Logger:
        """ロガーの設定を行う
        
        Returns:
            設定されたロガーインスタンス
            
        Raises:
            OSError: ログディレクトリまたはファイルの作成に失敗した場合
        """
        logger = logging.getLogger(self.name)
        logger.setLevel(self.level)
        
        # 既存のハンドラーをクリア
        logger.handlers.clear()
        
        # フォーマッターの設定
        formatter = logging.Formatter(app_const.DEFAULT_LOG_FORMAT, app_const.DEFAULT_DATE_FORMAT)
        
        # コンソールハンドラー
        if self.enable_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(self.level)
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
        
        # ファイルハンドラー
        if self.enable_file:
            try:
                # ログディレクトリの作成
                self.log_dir.mkdir(parents=True, exist_ok=True)
                
                log_file_path = self.log_dir / self.log_filename
                
                # ローテーションファイルハンドラー（10MB、5世代）
                file_handler = logging.handlers.RotatingFileHandler(
                    log_file_path,
                    maxBytes=10*1024*1024,  # 10MB
                    backupCount=5,
                    encoding='utf-8'
                )
                file_handler.setLevel(self.level)
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)
            except OSError as e:
                # ファイルハンドラーの作成に失敗した場合は警告を出力してコンソールハンドラーのみで続行
                if self.enable_console:
                    logger.warning(f"Failed to create file handler: {e}. Continuing with console logging only.")
                else:
                    raise OSError(f"Failed to create log file handler and console logging is disabled: {e}")
        
        return logger
    
    def get_logger(self) -> logging.Logger:
        """ロガーインスタンスを取得する"""
        return self.logger
    
    def set_level(self, level: str):
        """ログレベルを設定する
        
        Args:
            level: 設定するログレベル（DEBUG, INFO, WARNING, ERROR, CRITICAL）
            
        Raises:
            ValueError: 無効なログレベルが指定された場合
        """
        level_upper = level.upper()
        if not hasattr(logging, level_upper):
            raise ValueError(f"Invalid log level: {level}. Must be one of: DEBUG, INFO, WARNING, ERROR, CRITICAL")
        
        log_level = getattr(logging, level_upper)
        self.level = log_level
        self.logger.setLevel(log_level)
        for handler in self.logger.handlers:
            handler.setLevel(log_level)
    
    def debug(self, message: str, *args, **kwargs):
        """DEBUGレベルでログを出力
        
        Args:
            message: ログメッセージ
            *args: メッセージのフォーマット引数
            **kwargs: 追加のキーワード引数
        """
        self.logger.debug(message, *args, **kwargs)
    
    def info(self, message: str, *args, **kwargs):
        """INFOレベルでログを出力
        
        Args:
            message: ログメッセージ
            *args: メッセージのフォーマット引数
            **kwargs: 追加のキーワード引数
        """
        self.logger.info(message, *args, **kwargs)
    
    def warning(self, message: str, *args, **kwargs):
        """WARNINGレベルでログを出力
        
        Args:
            message: ログメッセージ
            *args: メッセージのフォーマット引数
            **kwargs: 追加のキーワード引数
        """
        self.logger.warning(message, *args, **kwargs)
    
    def error(self, message: str, *args, **kwargs):
        """ERRORレベルでログを出力
        
        Args:
            message: ログメッセージ
            *args: メッセージのフォーマット引数
            **kwargs: 追加のキーワード引数
        """
        self.logger.error(message, *args, **kwargs)
    
    def critical(self, message: str, *args, **kwargs):
        """CRITICALレベルでログを出力
        
        Args:
            message: ログメッセージ
            *args: メッセージのフォーマット引数
            **kwargs: 追加のキーワード引数
        """
        self.logger.critical(message, *args, **kwargs)
    
    def exception(self, message: str, *args, **kwargs):
        """例外情報付きでERRORレベルでログを出力
        
        Args:
            message: ログメッセージ
            *args: メッセージのフォーマット引数
            **kwargs: 追加のキーワード引数
        """
        self.logger.exception(message, *args, **kwargs)
    
    def get_log_file_path(self) -> Optional[Path]:
        """ログファイルのパスを取得する
        
        Returns:
            ログファイルのパス（ファイル出力が無効の場合はNone）
        """
        if self.enable_file:
            return self.log_dir / self.log_filename
        return None
    
    def is_enabled_for(self, level: str) -> bool:
        """指定されたログレベルが有効かどうかを確認する
        
        Args:
            level: 確認するログレベル
            
        Returns:
            指定されたレベルが有効かどうか
        """
        level_upper = level.upper()
        if hasattr(logging, level_upper):
            return self.logger.isEnabledFor(getattr(logging, level_upper))
        return False


class LogContext:
    """ログのコンテキストマネージャー"""
    
    def __init__(self, logger: AppLogger, context_name: str, level: str = 'DEBUG'):
        """
        Args:
            logger: AppLoggerインスタンス
            context_name: コンテキスト名
            level: ログレベル
        """
        self.logger = logger
        self.context_name = context_name
        self.level = level.upper()
        self.start_time = None
    
    def __enter__(self):
        self.start_time = datetime.now()
        if hasattr(self.logger, self.level.lower()):
            getattr(self.logger, self.level.lower())(f"Entering context: {self.context_name}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        end_time = datetime.now()
        duration = end_time - self.start_time if self.start_time else None
        
        if exc_type is None:
            if hasattr(self.logger, self.level.lower()):
                getattr(self.logger, self.level.lower())(
                    f"Exiting context: {self.context_name} (duration: {duration})"
                )
        else:
            self.logger.error(
                f"Exiting context: {self.context_name} with exception: {exc_type.__name__}: {exc_val} (duration: {duration})"
            )


# グローバルロガーインスタンス
_app_logger: Optional[AppLogger] = None


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """ロガーを取得する
    
    Args:
        name: ロガー名（Noneの場合はアプリケーションロガーを返す）
        
    Returns:
        ロガーインスタンス
    """
    global _app_logger
    
    if name:
        return logging.getLogger(name)
    
    if _app_logger is None:
        _app_logger = AppLogger()
    
    return _app_logger.get_logger()


def set_log_level(level: str):
    """ロガーのログレベルを設定する
    
    Args:
        level: 設定するログレベル（DEBUG, INFO, WARNING, ERROR, CRITICAL）
    """
    global _app_logger
    if _app_logger is None:
        _app_logger = AppLogger()
    _app_logger.set_level(level)


def setup_logger(level: str = 'INFO',
                log_dir: Optional[str] = None,
                log_filename: Optional[str] = None,
                enable_console: bool = True,
                enable_file: bool = True) -> AppLogger:
    """アプリケーションロガーを設定する
    
    Args:
        level: ログレベル（DEBUG, INFO, WARNING, ERROR, CRITICAL）
        log_dir: ログディレクトリ（デフォルト: logs）
        log_filename: ログファイル名（デフォルト: app.log）
        enable_console: コンソール出力を有効にするか
        enable_file: ファイル出力を有効にするか
        
    Returns:
        設定されたAppLoggerインスタンス
        
    Raises:
        ValueError: 無効なログレベルが指定された場合
    """
    global _app_logger
    _app_logger = AppLogger(
        level=level,
        log_dir=log_dir,
        log_filename=log_filename,
        enable_console=enable_console,
        enable_file=enable_file
    )
    return _app_logger


def log_function_call(func: Callable[..., Any]) -> Callable[..., Any]:
    """関数呼び出しをログに記録するデコレータ
    
    Args:
        func: デコレータを適用する関数
        
    Returns:
        ログ機能が追加された関数
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = get_logger()
        func_name = func.__name__
        logger.debug(f"Calling function: {func_name}")
        
        try:
            result = func(*args, **kwargs)
            logger.debug(f"Function {func_name} completed successfully")
            return result
        except Exception as e:
            logger.error(f"Function {func_name} failed with error: {type(e).__name__}: {e}")
            raise
    
    return wrapper


def create_log_context(context_name: str, level: str = 'DEBUG') -> LogContext:
    """ログコンテキストを作成する
    
    Args:
        context_name: コンテキスト名
        level: ログレベル
        
    Returns:
        LogContextインスタンス
    """
    global _app_logger
    if _app_logger is None:
        _app_logger = AppLogger()
    return LogContext(_app_logger, context_name, level)


def log_execution_time(level: str = 'INFO') -> Callable:
    """関数の実行時間をログに記録するデコレータ
    
    Args:
        level: ログレベル
        
    Returns:
        デコレータ関数
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger = get_logger()
            func_name = func.__name__
            start_time = datetime.now()
            
            try:
                result = func(*args, **kwargs)
                end_time = datetime.now()
                duration = end_time - start_time
                
                if hasattr(logger, level.lower()):
                    getattr(logger, level.lower())(
                        f"Function {func_name} executed successfully in {duration}"
                    )
                return result
            except Exception as e:
                end_time = datetime.now()
                duration = end_time - start_time
                logger.error(
                    f"Function {func_name} failed after {duration} with error: {type(e).__name__}: {e}"
                )
                raise
        
        return wrapper
    return decorator
