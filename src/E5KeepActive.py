import asyncio
import datetime
import random
import time
from microsoftgraphrestapi import MicrosoftGraphRestAPI
from constants.constants import FROZEN, ROOT_PATH

from util.config_init import ConfigInit
from start_with_sys import start_with_sys_init


async def main():
    # 初始化配置信息
    print("ROOT_PATH: {}".format(ROOT_PATH))  # hahaha
    config = ConfigInit.config_init()
    # 设置是否开机自启
    # 如果是exe程序，则初始化开机自启注册表
    program_path = ROOT_PATH + r"\bin\E5KeepActive.exe"
    if FROZEN:
        print("FROZEN: {}".format(FROZEN))  # hahaha
        start_with_sys_init(
            program_name="E5KeepActive",
            program_path=program_path,
            program_para="-hidden",
            value=config.base_setting.start_with_sys,
        )
    # time.sleep(600)  # 开机十分钟后执行一次
    # 暂停周期
    period_min = int(config.base_setting.call_func_period[0]) * 60  # 单位：分钟
    period_max = int(config.base_setting.call_func_period[1]) * 60

    while True:
        print("*" * 100)
        # 创建 MicrosoftGraphRestAPI 实例
        mg = MicrosoftGraphRestAPI(config)

        # 创建 GraphServiceClient,drive_id 等
        await mg.init_drive_id()
        # 检查根目录是否存在 E5KeepActive ，如果不存在则创建之
        if not await mg.check_exist_item("E5KeepActive", "root"):
            await mg.create_folder("root", "E5KeepActive")
        # 获取 E5KeepActive 的item_id
        item_id = await mg.get_item_id("root:/E5KeepActive")
        # 检查是否存在 E5KeepActive.log 文件，如果不存在则创建之
        if not await mg.check_exist_item("E5KeepActive.log", item_id):
            await mg.create_file(item_id, "E5KeepActive.log")
        # 获取 E5KeepActive.log 的 item_id
        item_id = await mg.get_item_id("root:/E5KeepActive/E5KeepActive.log")
        # todo content 调用频繁报错
        # # 获取 E5KeepActive.log 文件 content
        # original_content = await mg.get_content(item_id)

        # if original_content is not None:
        #     new_content = "\n\tE5KeepActive App last run at {} {}\n".format(
        #         datetime.datetime.now().strftime("%Y:%m:%d"),
        #         datetime.datetime.now().strftime("%H:%M:%S"),
        #     ).encode("utf-8")

        #     original_str = original_content.decode("utf-8")
        #     original_str_list = original_str.split("\n")

        #     content = (
        #         (original_str_list[0]).encode("utf-8")
        #         + new_content
        #         + "\n".join(original_str_list[1:]).encode("utf-8")
        #     )
        # else:
        #     new_content = "\tE5KeepActive App last run at {} {}".format(
        #         datetime.datetime.now().strftime("%Y:%m:%d"),
        #         datetime.datetime.now().strftime("%H:%M:%S"),
        #     ).encode("utf-8")
        #     content = (
        #         "This is E5KeepActive App detailed running time:\n".encode("utf-8")
        #         + new_content
        #     )
        # # 上传 content
        # await mg.put_content(item_id, content)

        # 小数据流覆盖文件内容
        new_content = "\tE5KeepActive App last run at {} {}".format(
            datetime.datetime.now().strftime("%Y:%m:%d"),
            datetime.datetime.now().strftime("%H:%M:%S"),
        ).encode("utf-8")
        content = (
            "This is E5KeepActive App detailed running time:\n".encode("utf-8")
            + new_content
        )
        await mg.put_content(item_id, content)

        # 调用时间间隔
        del mg
        await time.sleep(random.randint(period_min, period_max))


if __name__ == "__main__":
    asyncio.run(main())
