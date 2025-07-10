#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
app_exceptions.py
例外処理・カスタム例外モジュール
"""

#---------------------------------
# インポート
#---------------------------------
# standard library
import logging
import traceback
import functools
from typing import Any, Callable, Optional, Type, Union, Dict, List
from datetime import datetime
from pathlib import Path

# third party library

# local library

#---------------------------------
# カスタム例外クラス
#---------------------------------

class AppBaseException(Exception):
    """アプリケーションのベース例外クラス"""
    
    def __init__(self, 
                 message: str, 
                 error_code: Optional[str] = None,
                 context: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.context = context or {}
        self.timestamp = datetime.now()

class ConfigError(AppBaseException):
    """設定関連のエラー"""
    pass


class FileOperationError(AppBaseException):
    """ファイル操作関連のエラー"""
    pass


class ValidationError(AppBaseException):
    """バリデーション関連のエラー"""
    pass


class ProcessingError(AppBaseException):
    """処理関連のエラー"""
    pass


#---------------------------------
# エラーハンドリング機能
#---------------------------------


def validate_type(value: Any, 
                 expected_type: Union[Type, tuple], 
                 name: str = "value",
                 allow_none: bool = False) -> None:
    """型バリデーション
    
    Args:
        value: チェックする値
        expected_type: 期待する型
        name: 値の名前
        allow_none: Noneを許可するか
        
    Raises:
        ValidationError: 型が一致しない場合
    """
    if allow_none and value is None:
        return
        
    if not isinstance(value, expected_type):
        expected_type_name = getattr(expected_type, '__name__', str(expected_type))
        actual_type_name = type(value).__name__
        raise ValidationError(
            f"{name}の型が不正です。期待: {expected_type_name}, 実際: {actual_type_name}",
            error_code="TYPE_VALIDATION_ERROR"
        )


def validate_not_none(value: Any, name: str = "value") -> None:
    """None でないことをバリデーション
    
    Args:
        value: チェックする値
        name: 値の名前
        
    Raises:
        ValidationError: 値がNoneの場合
    """
    if value is None:
        raise ValidationError(
            f"{name}がNoneです",
            error_code="NULL_VALUE_ERROR"
        )


def validate_not_empty(value: Union[str, list, dict], name: str = "value") -> None:
    """空でないことをバリデーション
    
    Args:
        value: チェックする値
        name: 値の名前
        
    Raises:
        ValidationError: 値が空の場合
    """
    if not value:
        raise ValidationError(
            f"{name}が空です",
            error_code="EMPTY_VALUE_ERROR"
        )


def validate_range(value: Union[int, float], 
                  min_val: Optional[Union[int, float]] = None,
                  max_val: Optional[Union[int, float]] = None,
                  name: str = "value") -> None:
    """値の範囲をバリデーション
    
    Args:
        value: チェックする値
        min_val: 最小値
        max_val: 最大値
        name: 値の名前
        
    Raises:
        ValidationError: 値が範囲外の場合
    """
    if min_val is not None and value < min_val:
        raise ValidationError(
            f"{name}が最小値 {min_val} 未満です: {value}",
            error_code="MIN_VALUE_ERROR"
        )
    
    if max_val is not None and value > max_val:
        raise ValidationError(
            f"{name}が最大値 {max_val} を超えています: {value}",
            error_code="MAX_VALUE_ERROR"
        )


def validate_file_exists(file_path: Union[str, Path], name: str = "file") -> None:
    """ファイルが存在することをバリデーション
    
    Args:
        file_path: ファイルパス
        name: ファイルの名前
        
    Raises:
        FileOperationError: ファイルが存在しない場合
    """
    path = Path(file_path)
    if not path.exists():
        raise FileOperationError(
            f"{name}が存在しません: {file_path}",
            error_code="FILE_NOT_FOUND"
        )
    
    if not path.is_file():
        raise FileOperationError(
            f"{name}がファイルではありません: {file_path}",
            error_code="NOT_A_FILE"
        )


def create_error_response(error: Exception, 
                         include_traceback: bool = False,
                         include_context: bool = True) -> Dict[str, Any]:
    """エラーレスポンスを作成する
    
    Args:
        error: エラーオブジェクト
        include_traceback: トレースバックを含めるか
        include_context: コンテキスト情報を含めるか
        
    Returns:
        エラー情報を含む辞書
    """
    response = {
        "error": True,
        "error_type": type(error).__name__,
        "message": str(error),
        "timestamp": datetime.now().isoformat()
    }
    
    if isinstance(error, AppBaseException):
        if error.error_code:
            response["error_code"] = error.error_code
        if include_context and error.context:
            response["context"] = error.context
    
    if include_traceback:
        response["traceback"] = traceback.format_exc()
    
    return response


# グローバルエラーハンドラー
_global_error_handler: Optional[ErrorHandler] = None


def get_error_handler(logger: Optional[logging.Logger] = None,
                     enable_metrics: bool = False) -> ErrorHandler:
    """グローバルエラーハンドラーを取得する
    
    Args:
        logger: 使用するロガー
        enable_metrics: メトリクス収集を有効にするか
        
    Returns:
        ErrorHandlerインスタンス
    """
    global _global_error_handler
    
    if _global_error_handler is None:
        _global_error_handler = ErrorHandler(logger, enable_metrics)
    
    return _global_error_handler


def set_global_error_handler(handler: ErrorHandler):
    """グローバルエラーハンドラーを設定する
    
    Args:
        handler: 設定するErrorHandlerインスタンス
    """
    global _global_error_handler
    _global_error_handler = handler
