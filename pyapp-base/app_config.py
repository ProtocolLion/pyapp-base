#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
app_config.py
アプリケーション設定管理モジュール

使用モジュール
    INI形式: configparser (標準ライブラリ)
    JSON形式: json (標準ライブラリ)
    YAML形式: PyYAML (外部ライブラリ)
    TOML形式: tomli (外部ライブラリ/Python 3.11以降はtomllibとして標準ライブラリ入り)
"""

#---------------------------------
# インポート
#---------------------------------
# standard library
import json
import os
import configparser
from pathlib import Path
from typing import Any, Dict, Optional, Union
import logging

# third party library

# local library
from . import app_const


#---------------------------------
# 関数
#---------------------------------
def load_config(config_file: Optional[str] = None) -> Dict[str, Any]:
    """設定ファイルを読み込む
    
    Args:
        config_file: 設定ファイルのパス（Noneの場合はデフォルト設定ファイルを使用）
    
    Returns:
        設定辞書
    """
    config = AppConfig(config_file=config_file)
    return config.config


#---------------------------------
# class
#---------------------------------
class AppConfig:
    """設定管理クラス"""
    
    def __init__(self, 
                 config_file: Optional[str] = None,
                 config_dir: Optional[str] = None,
                 create_if_not_exists: bool = True):
        """
        Args:
            config_file: 設定ファイルのパス
            config_dir: 設定ディレクトリ
            create_if_not_exists: 設定ファイルが存在しない場合に作成するか
        """
        self.config_dir = Path(config_dir or app_const.DEFAULT_CONFIG_DIR)
        self.config_file = Path(config_file or (self.config_dir / app_const.DEFAULT_CONFIG_FILENAME))
        self.create_if_not_exists = create_if_not_exists
        self.logger = logging.getLogger(__name__)
        
        # デフォルト設定
        self.default_config = {
            "app": {
                "name": app_const.APP_NAME,
                "version": app_const.APP_VERSION,
                "debug_mode": False
            },
            "logging": {
                "level": "INFO",
                "log_dir": "logs",
                "enable_console": True,
                "enable_file": True
            },
            "gui": {
                "window_width": 800,
                "window_height": 600,
                "theme": "default"
            },
            "processing": {
                "max_file_size": "100MB",
                "supported_formats": ["jpg", "png", "gif", "bmp", "tiff"],
                "output_format": "json"
            }
        }
        
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """設定ファイルを読み込む"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                self.logger.info(f"設定ファイルを読み込みました: {self.config_file}")
                
                # デフォルト設定とマージ
                merged_config = self._merge_configs(self.default_config, config)
                return merged_config
            else:
                if self.create_if_not_exists:
                    self.logger.info("設定ファイルが存在しないため、デフォルト設定で作成します")
                    self.save_config(self.default_config)
                    return self.default_config.copy()
                else:
                    self.logger.warning("設定ファイルが存在しません。デフォルト設定を使用します")
                    return self.default_config.copy()
        except Exception as e:
            self.logger.error(f"設定ファイルの読み込みに失敗しました: {e}")
            return self.default_config.copy()
    
    def save_config(self, config: Optional[Dict[str, Any]] = None):
        """設定をファイルに保存する"""
        config_to_save = config or self.config
        
        try:
            # ディレクトリの作成
            self.config_dir.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_to_save, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"設定ファイルを保存しました: {self.config_file}")
        except Exception as e:
            self.logger.error(f"設定ファイルの保存に失敗しました: {e}")
            raise
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """設定値を取得する
        
        Args:
            key_path: "app.name" のようなドット区切りのキーパス
            default: デフォルト値
            
        Returns:
            設定値
        """
        keys = key_path.split('.')
        value = self.config
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key_path: str, value: Any):
        """設定値を設定する
        
        Args:
            key_path: "app.name" のようなドット区切りのキーパス
            value: 設定する値
        """
        keys = key_path.split('.')
        config = self.config
        
        # 最後のキー以外をたどって辞書を作成
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        # 最後のキーに値を設定
        config[keys[-1]] = value
    
    def update(self, updates: Dict[str, Any]):
        """設定を一括更新する"""
        self.config = self._merge_configs(self.config, updates)
    
    def _merge_configs(self, base: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
        """設定辞書をマージする"""
        result = base.copy()
        
        for key, value in updates.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def reset_to_default(self):
        """設定をデフォルトにリセットする"""
        self.config = self.default_config.copy()
        self.save_config()
        self.logger.info("設定をデフォルトにリセットしました")
    
    def get_config_dict(self) -> Dict[str, Any]:
        """設定辞書のコピーを取得する"""
        return self.config.copy()


# グローバル設定管理インスタンス
_config_manager: Optional[AppConfig] = None


def get_config_manager(config_file: Optional[str] = None) -> AppConfig:
    """設定管理インスタンスを取得する"""
    global _config_manager
    
    if _config_manager is None:
        _config_manager = AppConfig(config_file=config_file)
    
    return _config_manager


def get_config(key_path: str, default: Any = None) -> Any:
    """設定値を取得する便利関数"""
    return get_config_manager().get(key_path, default)


def set_config(key_path: str, value: Any):
    """設定値を設定する便利関数"""
    get_config_manager().set(key_path, value)


def save_config():
    """設定を保存する便利関数"""
    get_config_manager().save_config()
