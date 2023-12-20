import os
import sys
from collections import namedtuple

from src.config_init import ConfigInit

FROZEN = getattr(sys, 'frozen', False)

# 获取当前文件所在目录的路径
if FROZEN:
    # 如果是可执行文件，则用 compass 获取可执行文件的目录
    _CUR_PATH = os.path.dirname(os.path.abspath(sys.executable))
else:
    # 否则，从 __file__ 中获取当前文件的路径，并取其所在目录作为当前目录
    _CUR_PATH = os.path.dirname(os.path.abspath(__file__))

# 根目录
ROOT_PATH = os.path.dirname(_CUR_PATH)


class Constants:
    # 工程根目录
    ROOT_PATH = ROOT_PATH
    # 是否是 release 版本
    VERSION = "release"
    # 是否为可执行文件
    FROZEN = FROZEN


class CustomConfig:
    # __ 私有变量
    _custom_config = ConfigInit.config_init()

    _BASIC_SETTING = namedtuple('BASIC_SETTING', ['START_WITH_SYSTEM', 'FILE_PATH', 'FILE_SIZE', 'FILE_CONTENT', 'GENERATE_PERIOD'])

    # BASIC_SETTING
    _start_with_sys = _custom_config["BASIC_SETTING"].getboolean('START_WITH_SYSTEM')
    _file_path = _custom_config["BASIC_SETTING"].get('FILE_PATH')
    _file_size = _custom_config["BASIC_SETTING"].getint('FILE_SIZE')
    _file_content = _custom_config["BASIC_SETTING"].get('FILE_CONTENT')[1:-1]
    _generate_period = _custom_config["BASIC_SETTING"].getint('GENERATE_PERIOD')

    BASIC_SETTING = _BASIC_SETTING(_start_with_sys, _file_path, _file_size, _file_content, _generate_period)
