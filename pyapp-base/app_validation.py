#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
app_validation.py
アプリケーションのバリデーションモジュール

"""

#---------------------------------
# インポート
#---------------------------------
# standard library
import os
import re
from typing import Any, Optional, Type, Union, Sequence
from pathlib import Path

# third party library

# local library
from .app_exceptions import ValidationError, FileOperationError

#---------------------------------
# カスタムバリデーション
#---------------------------------
def validate_type(value: Any, 
                 expected_type: Union[Type, tuple], 
                 name: str = "value",
                 allow_none: bool = False) -> None:
    """型バリデーション
    
    Args:
        value: チェックする値
        expected_type: 期待する型（単一の型またはタプル）
        name: 値の名前（エラーメッセージに使用）
        allow_none: Noneを許可するかどうか
        
    Raises:
        ValidationError: 型が一致しない場合
        
    Example:
        validate_type(42, int, "age")
        validate_type("hello", (str, bytes), "message")
    """
    if allow_none and value is None:
        return
        
    if not isinstance(value, expected_type):
        if isinstance(expected_type, tuple):
            expected_type_name = " or ".join(t.__name__ for t in expected_type)
        else:
            expected_type_name = getattr(expected_type, '__name__', str(expected_type))
        actual_type_name = type(value).__name__
        raise ValidationError(
            f"{name}の型が不正です。期待: {expected_type_name}, 実際: {actual_type_name}",
            error_code="TYPE_VALIDATION_ERROR",
            context={"value": value, "expected_type": expected_type_name}
        )


def validate_not_none(value: Any, name: str = "value") -> None:
    """None でないことをバリデーション
    
    Args:
        value: チェックする値
        name: 値の名前（エラーメッセージに使用）
        
    Raises:
        ValidationError: 値がNoneの場合
        
    Example:
        validate_not_none(user_input, "user_name")
    """
    if value is None:
        raise ValidationError(
            f"{name}がNoneです",
            error_code="NULL_VALUE_ERROR",
            context={"name": name}
        )


def validate_not_empty(value: Union[str, list, dict, set], name: str = "value") -> None:
    """空でないことをバリデーション
    
    Args:
        value: チェックする値 (str, list, dict, set)
        name: 値の名前（エラーメッセージに使用）
        
    Raises:
        ValidationError: 値が空の場合
        
    Example:
        validate_not_empty("hello", "message")
        validate_not_empty([1, 2, 3], "numbers")
    """
    if not value:
        raise ValidationError(
            f"{name}が空です",
            error_code="EMPTY_VALUE_ERROR",
            context={"name": name, "type": type(value).__name__}
        )


def validate_range(value: Union[int, float], 
                  min_val: Optional[Union[int, float]] = None,
                  max_val: Optional[Union[int, float]] = None,
                  name: str = "value") -> None:
    """値の範囲をバリデーション
    
    Args:
        value: チェックする値
        min_val: 最小値（None の場合は下限なし）
        max_val: 最大値（None の場合は上限なし）
        name: 値の名前（エラーメッセージに使用）
        
    Raises:
        ValidationError: 値が範囲外の場合
        
    Example:
        validate_range(25, 0, 100, "age")
        validate_range(3.14, min_val=0, name="radius")
    """
    if min_val is not None and value < min_val:
        raise ValidationError(
            f"{name}が最小値 {min_val} 未満です: {value}",
            error_code="MIN_VALUE_ERROR",
            context={"value": value, "min_val": min_val}
        )
    
    if max_val is not None and value > max_val:
        raise ValidationError(
            f"{name}が最大値 {max_val} を超えています: {value}",
            error_code="MAX_VALUE_ERROR",
            context={"value": value, "max_val": max_val}
        )


def validate_file_exists(file_path: Union[str, Path], name: str = "file") -> None:
    """ファイルが存在することをバリデーション
    
    Args:
        file_path: ファイルパス（文字列またはPathオブジェクト）
        name: ファイルの名前（エラーメッセージに使用）
        
    Raises:
        FileOperationError: ファイルが存在しない場合またはファイルでない場合
        
    Example:
        validate_file_exists("/path/to/config.json", "設定ファイル")
        validate_file_exists(Path("data.csv"), "データファイル")
    """
    path = Path(file_path)
    if not path.exists():
        raise FileOperationError(
            f"{name}が存在しません: {file_path}",
            error_code="FILE_NOT_FOUND",
            context={"file_path": str(file_path)}
        )
    
    if not path.is_file():
        raise FileOperationError(
            f"{name}がファイルではありません: {file_path}",
            error_code="NOT_A_FILE",
            context={"file_path": str(file_path)}
        )


def validate_length(value: Union[str, list, dict, set], 
                   min_length: Optional[int] = None,
                   max_length: Optional[int] = None,
                   name: str = "value") -> None:
    """文字列や配列の長さをバリデーション
    
    Args:
        value: チェックする値 (str, list, dict, set)
        min_length: 最小長（None の場合は下限なし）
        max_length: 最大長（None の場合は上限なし）
        name: 値の名前（エラーメッセージに使用）
        
    Raises:
        ValidationError: 長さが範囲外の場合
        
    Example:
        validate_length("hello", 1, 10, "message")
        validate_length([1, 2, 3], min_length=1, name="items")
    """
    length = len(value)
    
    if min_length is not None and length < min_length:
        raise ValidationError(
            f"{name}の長さが最小値 {min_length} 未満です: {length}",
            error_code="MIN_LENGTH_ERROR",
            context={"length": length, "min_length": min_length}
        )
    
    if max_length is not None and length > max_length:
        raise ValidationError(
            f"{name}の長さが最大値 {max_length} を超えています: {length}",
            error_code="MAX_LENGTH_ERROR",
            context={"length": length, "max_length": max_length}
        )


def validate_pattern(value: str, 
                    pattern: str,
                    name: str = "value") -> None:
    """正規表現パターンでバリデーション
    
    Args:
        value: チェックする値
        pattern: 正規表現パターン
        name: 値の名前（エラーメッセージに使用）
        
    Raises:
        ValidationError: パターンにマッチしない場合
        
    Example:
        validate_pattern("user@example.com", r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$", "email")
        validate_pattern("12345", r"^\\d{5}$", "postal_code")
    """
    if not re.fullmatch(pattern, value):
        raise ValidationError(
            f"{name}が指定されたパターンにマッチしません: {value}",
            error_code="PATTERN_VALIDATION_ERROR",
            context={"pattern": pattern, "value": value}
        )


def validate_choice(value: Any, 
                   choices: Sequence,
                   name: str = "value") -> None:
    """選択肢の中から値を選択するバリデーション
    
    Args:
        value: チェックする値
        choices: 選択肢のシーケンス
        name: 値の名前（エラーメッセージに使用）
        
    Raises:
        ValidationError: 選択肢にない場合
        
    Example:
        validate_choice("red", ["red", "green", "blue"], "color")
        validate_choice(1, [1, 2, 3], "level")
    """
    if value not in choices:
        raise ValidationError(
            f"{name}が選択肢にありません: {value}. 選択肢: {choices}",
            error_code="CHOICE_VALIDATION_ERROR",
            context={"choices": list(choices), "value": value}
        )


def validate_directory_exists(dir_path: Union[str, Path], 
                             name: str = "directory") -> None:
    """ディレクトリが存在することをバリデーション
    
    Args:
        dir_path: ディレクトリパス（文字列またはPathオブジェクト）
        name: ディレクトリの名前（エラーメッセージに使用）
        
    Raises:
        FileOperationError: ディレクトリが存在しない場合またはディレクトリでない場合
        
    Example:
        validate_directory_exists("/path/to/data", "データディレクトリ")
        validate_directory_exists(Path("output"), "出力ディレクトリ")
    """
    path = Path(dir_path)
    if not path.exists():
        raise FileOperationError(
            f"{name}が存在しません: {dir_path}",
            error_code="DIRECTORY_NOT_FOUND",
            context={"dir_path": str(dir_path)}
        )
    
    if not path.is_dir():
        raise FileOperationError(
            f"{name}がディレクトリではありません: {dir_path}",
            error_code="NOT_A_DIRECTORY",
            context={"dir_path": str(dir_path)}
        )


def validate_file_extension(file_path: Union[str, Path], 
                           allowed_extensions: Sequence[str],
                           name: str = "file") -> None:
    """ファイル拡張子をバリデーション
    
    Args:
        file_path: ファイルパス（文字列またはPathオブジェクト）
        allowed_extensions: 許可される拡張子のシーケンス (.付きまたは無しで指定可能)
        name: ファイルの名前（エラーメッセージに使用）
        
    Raises:
        FileOperationError: ファイルが存在しない場合またはファイルでない場合
        ValidationError: 拡張子が許可されていない場合
        
    Example:
        validate_file_extension("data.csv", [".csv", ".txt"], "データファイル")
        validate_file_extension(Path("image.jpg"), ["jpg", "png"], "画像ファイル")
    """
    path = Path(file_path)
    if not path.exists():
        raise FileOperationError(
            f"{name}が存在しません: {file_path}",
            error_code="FILE_NOT_FOUND",
            context={"file_path": str(file_path)}
        )
    if not path.is_file():
        raise FileOperationError(
            f"{name}がファイルではありません: {file_path}",
            error_code="NOT_A_FILE",
            context={"file_path": str(file_path)}
        )
    
    # 拡張子のドットの有無を正規化
    extension = path.suffix.lower()
    allowed_exts = [ext.lower() if ext.startswith('.') else f'.{ext.lower()}' for ext in allowed_extensions]
    
    if extension not in allowed_exts:
        # 表示用に整形した拡張子リスト（ドット付き）
        display_exts = [ext if ext.startswith('.') else f'.{ext}' for ext in allowed_extensions]
        raise ValidationError(
            f"{name}の拡張子が許可されていません: {extension}. 許可される拡張子: {display_exts}",
            error_code="INVALID_FILE_EXTENSION",
            context={"allowed_extensions": display_exts, "actual_extension": extension}
        )


def validate_mutually_exclusive(*args_values: tuple, names: Optional[list] = None) -> None:
    """相互排他的な引数のバリデーション
    
    Args:
        *args_values: チェックする引数の値のタプル
        names: 引数の名前のリスト
        
    Raises:
        ValidationError: 複数の引数が同時に指定された場合
        
    Example:
        validate_mutually_exclusive(
            (args.quiet, args.verbose > 0),
            names=["--quiet", "--verbose"]
        )
    """
    if names is None:
        names = [f"引数{i+1}" for i in range(len(args_values))]
    
    specified_args = []
    for i, (value, name) in enumerate(zip(args_values, names)):
        if value:
            specified_args.append(name)
    
    if len(specified_args) > 1:
        raise ValidationError(
            f"以下の引数は同時に指定できません: {', '.join(specified_args)}",
            error_code="MUTUALLY_EXCLUSIVE_ARGS",
            context={"specified_args": specified_args}
        )


def validate_conditional_required(condition: bool, 
                                 value: Any, 
                                 condition_name: str,
                                 value_name: str) -> None:
    """条件付き必須引数のバリデーション
    
    Args:
        condition: 条件（True の場合、値が必須）
        value: チェックする値
        condition_name: 条件の名前
        value_name: 値の名前
        
    Raises:
        ValidationError: 条件が満たされているのに値が指定されていない場合
        
    Example:
        validate_conditional_required(
            args.mode == 'convert',
            args.output,
            "--mode convert",
            "--output"
        )
    """
    if condition and not value:
        raise ValidationError(
            f"{condition_name} の場合は {value_name} が必須です",
            error_code="CONDITIONAL_REQUIRED_ERROR",
            context={"condition_name": condition_name, "value_name": value_name}
        )


def validate_file_or_directory_exists(path: Union[str, Path], 
                                     name: str = "path") -> None:
    """ファイルまたはディレクトリが存在することをバリデーション
    
    Args:
        path: ファイルまたはディレクトリのパス
        name: パスの名前（エラーメッセージに使用）
        
    Raises:
        FileOperationError: パスが存在しない場合
        
    Example:
        validate_file_or_directory_exists("/path/to/input", "入力パス")
    """
    path_obj = Path(path)
    if not path_obj.exists():
        raise FileOperationError(
            f"{name}が存在しません: {path}",
            error_code="PATH_NOT_FOUND",
            context={"path": str(path)}
        )


def validate_writable_directory(dir_path: Union[str, Path], 
                               name: str = "directory",
                               create_if_missing: bool = True) -> None:
    """書き込み可能なディレクトリかどうかをバリデーション
    
    Args:
        dir_path: ディレクトリパス
        name: ディレクトリの名前（エラーメッセージに使用）
        create_if_missing: 存在しない場合に作成するかどうか
        
    Raises:
        FileOperationError: ディレクトリが書き込み不可能な場合
        
    Example:
        validate_writable_directory("/path/to/output", "出力ディレクトリ")
    """
    path = Path(dir_path)
    
    if not path.exists():
        if create_if_missing:
            try:
                path.mkdir(parents=True, exist_ok=True)
            except PermissionError:
                raise FileOperationError(
                    f"{name}を作成する権限がありません: {dir_path}",
                    error_code="PERMISSION_DENIED",
                    context={"dir_path": str(dir_path)}
                )
            except OSError as e:
                raise FileOperationError(
                    f"{name}の作成に失敗しました: {dir_path} - {e}",
                    error_code="DIRECTORY_CREATION_ERROR",
                    context={"dir_path": str(dir_path), "error": str(e)}
                )
        else:
            raise FileOperationError(
                f"{name}が存在しません: {dir_path}",
                error_code="DIRECTORY_NOT_FOUND",
                context={"dir_path": str(dir_path)}
            )
    
    if not path.is_dir():
        raise FileOperationError(
            f"{name}がディレクトリではありません: {dir_path}",
            error_code="NOT_A_DIRECTORY",
            context={"dir_path": str(dir_path)}
        )
    
    # 書き込み権限のチェック
    if not os.access(path, os.W_OK):
        raise FileOperationError(
            f"{name}に書き込み権限がありません: {dir_path}",
            error_code="PERMISSION_DENIED",
            context={"dir_path": str(dir_path)}
        )

