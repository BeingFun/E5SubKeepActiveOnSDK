import configparser
import chardet
from src.constants.constants import ROOT_PATH


class USER_SETTING:
    def __init__(self, tenant_id, client_id, client_secret):
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret


class BASIC_SETTING:
    def __init__(self, start_with_sys, call_func_period):
        self.start_with_sys = start_with_sys
        self.call_func_period = call_func_period


class SETTING:
    def __init__(self, base_setting: BASIC_SETTING, user_setting: USER_SETTING):
        self.base_setting = base_setting
        self.user_setting = user_setting


class ConfigInit:
    @staticmethod
    def config_init() -> SETTING:
        print("start config init...")
        # Read the configuration file information
        config = configparser.ConfigParser(allow_no_value=False)
        configfile = ROOT_PATH + "\\config\\config.ini"
        with open(configfile, "rb") as file:
            content = file.read()
            encoding = chardet.detect(content)["encoding"]

        # Reopen the file using the detected encoding format and read the content
        with open(configfile, encoding=encoding) as file:
            config.read_file(file)

        dict_config = dict(config)

        start_with_sys = dict_config["BASIC_SETTING"].getboolean("start_with_system")
        call_func_period = (
            dict_config["BASIC_SETTING"]
            .get("call_func_period")
            .strip("[]")
            .replace(" ", "")
            .split(",")
        )

        base_setting = BASIC_SETTING(
            start_with_sys=start_with_sys,
            call_func_period=call_func_period,
        )

        tenant_id = dict_config["USER_SETTING"].get("tenant_id")
        client_id = dict_config["USER_SETTING"].get("client_id")
        client_secret = dict_config["USER_SETTING"].get("client_secret")

        user_setting = USER_SETTING(
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret,
        )

        setting = SETTING(base_setting=base_setting, user_setting=user_setting)
        print("finish config init...")
        return setting
