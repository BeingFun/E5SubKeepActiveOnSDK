import os
import shutil
import time
import uuid
import datetime
from constants.constants import CustomConfig, ROOT_PATH
from src.start_with_sys import start_with_sys


def generate_file(CustomConfig):
    os.chdir(CustomConfig.BASIC_SETTING.FILE_PATH)
    text = CustomConfig.BASIC_SETTING.FILE_CONTENT
    text_size_bytes = len(CustomConfig.BASIC_SETTING.FILE_CONTENT.encode('utf-8'))  # 每个重复的文本的大小（以字节为单位)

    # 需要分割为多少个文件
    file_num = CustomConfig.BASIC_SETTING.FILE_SIZE // 100  # 每个文件 100 MB
    file_remainder = CustomConfig.BASIC_SETTING.FILE_SIZE % 100  # 剩余文件的大小

    # 日志
    with open("log.log", 'w') as file:
        file.write("# file time: {} {}\n".format(datetime.datetime.now().strftime("%Y:%m:%d"), datetime.datetime.now().strftime("%H:%M:%S")))
        file.write("# file size: {} MB\n".format(CustomConfig.BASIC_SETTING.FILE_SIZE))

    for _ in range(file_num):
        repetitions = 1024 * 1024 * 100 // text_size_bytes  # 需要重复的次数
        remainder = 1024 * 1024 * 100 % text_size_bytes  # 剩余的字节数
        with open("tmp-{}.txt".format(uuid.uuid1()), "w") as file:
            for _ in range(repetitions):
                file.write(text)

            if remainder > 0:
                file.write(text[:remainder])

    if file_remainder > 0:
        repetitions = file_remainder * 1024 * 1024 // text_size_bytes  # 需要重复的次数
        remainder = file_remainder * 1024 * 1024 % text_size_bytes  # 剩余的字节数
        with open("tmp-{}.txt".format(uuid.uuid1()), "w") as file:
            for _ in range(repetitions):
                file.write(text)

            if remainder > 0:
                file.write(text[:remainder])
    os.chdir(ROOT_PATH)


def delete_file(CustomConfig):
    if os.path.exists(CustomConfig.BASIC_SETTING.FILE_PATH):
        if not os.listdir(CustomConfig.BASIC_SETTING.FILE_PATH):
            os.rmdir(CustomConfig.BASIC_SETTING.FILE_PATH)
        else:
            shutil.rmtree(CustomConfig.BASIC_SETTING.FILE_PATH)
    os.mkdir(CustomConfig.BASIC_SETTING.FILE_PATH)


def start_init():
    print("Start with sys init...")
    if CustomConfig.BASIC_SETTING.START_WITH_SYSTEM:
        try:
            start_with_sys()
        except BaseException as e:
            print("获取管理员权限失败，随系统开机自启设置失败")
            print(e)
    print("Start with sys finish...")


if __name__ == '__main__':
    start_init()
    period = CustomConfig.BASIC_SETTING.GENERATE_PERIOD * 60 * 60
    time.sleep(600)  # 开机十分钟后执行一次
    while True:
        delete_file(CustomConfig)  # 删除临时文件
        generate_file(CustomConfig)  # 生成临时文件
        time.sleep(period)  # 暂停周期
