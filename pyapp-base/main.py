#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
body.py
メインエントリポイントモジュール
"""

#---------------------------------
# インポート
#---------------------------------
# standard library


# third party library


# local library
from .__version__ import __version_info__
from . import app_argparser
from . import app_config
from . import app_const
from . import app_exceptions
from . import app_logger
from . import app_validation

from . import utils

#---------------------------------
# main
#---------------------------------
def main():
    """Main function for the body module."""
    print(f"Application version: {__version_info__}")
    utils.util0_test()  # Call a sample utility function
    print("Application started successfully.")


#---------------------------------
# if __name__ == "__main__":
#---------------------------------
if __name__ == "__main__":
    main()
