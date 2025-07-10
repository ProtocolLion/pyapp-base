#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
system_info.py
システム情報関連ユーティリティ
"""

import os
import platform
from typing import Dict, Any


def get_system_info() -> Dict[str, Any]:
    """システム情報を取得する
    
    Returns:
        システム情報の辞書
    """
    return {
        "platform": platform.platform(),
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation(),
    }


def get_memory_usage() -> Dict[str, Any]:
    """メモリ使用量を取得する（MB単位）
    
    Returns:
        メモリ使用量の辞書
    """
    try:
        import psutil
        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()
        
        return {
            "rss": memory_info.rss / 1024 / 1024,  # MB
            "vms": memory_info.vms / 1024 / 1024,  # MB
        }
    except ImportError:
        return {"error": "psutil not available"}
