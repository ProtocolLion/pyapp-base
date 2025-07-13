#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
app_exceptions.py

アプリケーション固有の例外クラス定義モジュール。

このモジュールは、アプリケーションで使用するカスタム例外クラスを定義します。
適切な例外処理により、エラーの種類を明確にし、デバッグを容易にします。

例外の階層:
    AppBaseException (基底例外)
    ├── ConfigurationError (設定関連エラー)
    ├── ValidationError (検証エラー)
    ├── ProcessingError (処理エラー)
    ├── FileOperationError (ファイル操作エラー)

使用例:
    from app_exceptions import ValidationError
    
    def validate_data(data):
        if not data:
            raise ValidationError("データが空です", error_code="EMPTY_DATA")
"""

# =============================================================================
# インポート
# =============================================================================
# 標準ライブラリ
from typing import Any, Dict, Optional

# サードパーティライブラリ


# ローカルライブラリ


# =============================================================================
# 基底例外クラス
# =============================================================================
class AppBaseException(Exception):
    """
    アプリケーションの基底例外クラス。
    
    すべてのアプリケーション固有例外の基底となります。
    エラーコード、詳細情報、コンテキスト情報を持つことができます。
    """
    
    def __init__(
        self,
        message: str,
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        cause: Optional[Exception] = None
    ):
        """
        基底例外を初期化します。
        
        Args:
            message (str): エラーメッセージ
            error_code (Optional[str]): エラーコード
            details (Optional[Dict[str, Any]]): 詳細情報
            cause (Optional[Exception]): 原因となった例外
        """
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        self.cause = cause
    
    def __str__(self) -> str:
        """例外の文字列表現を返します。"""
        parts = [self.message]
        
        if self.error_code:
            parts.append(f"エラーコード: {self.error_code}")
        
        if self.details:
            details_str = ", ".join(f"{k}={v}" for k, v in self.details.items())
            parts.append(f"詳細: {details_str}")
        
        return " | ".join(parts)
    
    def to_dict(self) -> Dict[str, Any]:
        """例外情報を辞書形式で返します。"""
        return {
            "message": self.message,
            "error_code": self.error_code,
            "details": self.details,
            "type": self.__class__.__name__
        }


# =============================================================================
# 設定関連例外
# =============================================================================
class ConfigurationError(AppBaseException):
    """設定関連のエラー。"""
    
    def __init__(self, message: str, config_file: Optional[str] = None, **kwargs):
        super().__init__(message, **kwargs)
        if config_file:
            self.details["config_file"] = config_file


class InvalidConfigurationError(ConfigurationError):
    """無効な設定値エラー。"""
    pass


class MissingConfigurationError(ConfigurationError):
    """必須設定項目の不足エラー。"""
    pass


# =============================================================================
# 検証関連例外
# =============================================================================
class ValidationError(AppBaseException):
    """データ検証エラー。"""
    
    def __init__(self, message: str, field: Optional[str] = None, value: Any = None, **kwargs):
        super().__init__(message, **kwargs)
        if field:
            self.details["field"] = field
        if value is not None:
            self.details["value"] = str(value)


class InvalidArgumentError(ValidationError):
    """無効な引数エラー。"""
    pass


class InvalidFormatError(ValidationError):
    """無効なフォーマットエラー。"""
    pass


# =============================================================================
# 処理関連例外
# =============================================================================
class ProcessingError(AppBaseException):
    """処理実行時のエラー。"""
    pass


class TimeoutError(ProcessingError):
    """タイムアウトエラー。"""
    
    def __init__(self, message: str, timeout_seconds: Optional[float] = None, **kwargs):
        super().__init__(message, **kwargs)
        if timeout_seconds:
            self.details["timeout_seconds"] = timeout_seconds


class ResourceNotFoundError(ProcessingError):
    """リソースが見つからないエラー。"""
    
    def __init__(self, message: str, resource_type: Optional[str] = None, 
                 resource_id: Optional[str] = None, **kwargs):
        super().__init__(message, **kwargs)
        if resource_type:
            self.details["resource_type"] = resource_type
        if resource_id:
            self.details["resource_id"] = resource_id


# =============================================================================
# ファイル操作関連例外
# =============================================================================
class FileOperationError(AppBaseException):
    """ファイル操作エラー。"""
    
    def __init__(self, message: str, file_path: Optional[str] = None, 
                 operation: Optional[str] = None, **kwargs):
        super().__init__(message, **kwargs)
        if file_path:
            self.details["file_path"] = file_path
        if operation:
            self.details["operation"] = operation


class FileNotFoundError(FileOperationError):
    """ファイルが見つからないエラー。"""
    pass


class FilePermissionError(FileOperationError):
    """ファイルアクセス権限エラー。"""
    pass


class FileFormatError(FileOperationError):
    """ファイル形式エラー。"""
    pass


# =============================================================================
# 例外ハンドリングユーティリティ
# =============================================================================
def format_exception_info(exc: Exception) -> Dict[str, Any]:
    """
    例外情報をフォーマットします。
    
    Args:
        exc (Exception): 例外オブジェクト
        
    Returns:
        Dict[str, Any]: フォーマットされた例外情報
    """
    if isinstance(exc, AppBaseException):
        return exc.to_dict()
    else:
        return {
            "message": str(exc),
            "type": exc.__class__.__name__,
            "details": {}
        }


def is_app_exception(exc: Exception) -> bool:
    """
    アプリケーション固有の例外かどうかを判定します。
    
    Args:
        exc (Exception): 例外オブジェクト
        
    Returns:
        bool: アプリケーション固有例外の場合True
    """
    return isinstance(exc, AppBaseException)

