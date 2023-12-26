import gc
from azure.identity import ClientSecretCredential
from msgraph import GraphServiceClient
from msgraph.generated.models.drive_item import DriveItem
from msgraph.generated.models.folder import Folder
from msgraph.generated.models.file import File

from util.config_init import SETTING

# TODO move to config.ini
redirect_uri = "http://localhost:5555"


class MicrosoftGraphRestAPI:
    # 类变量
    client = None
    drive_id = None
    config = None

    # CLIENT SECRET CREDENTIALS FLOW
    def __init__(self, config: SETTING) -> None:
        # Create a credential object. Used to authenticate requests
        credential = ClientSecretCredential(
            tenant_id=config.user_setting.tenant_id,
            client_id=config.user_setting.client_id,
            client_secret=config.user_setting.client_secret,
            redirect_uri=redirect_uri,
        )
        scopes = ["https://graph.microsoft.com/.default"]

        # Create an API client with the credentials and scopes.
        MicrosoftGraphRestAPI.client = GraphServiceClient(
            credentials=credential, scopes=scopes
        )
        print("create GraphServiceClient API client successful...")

    # init onedrive drive id
    async def init_drive_id(self):
        user = await MicrosoftGraphRestAPI.client.users.get()
        MicrosoftGraphRestAPI.drive_id = (
            await MicrosoftGraphRestAPI.client.users.by_user_id(
                user.value[0].id
            ).drive.get()
        ).id
        print("init onedrive drive id successful...")

    async def check_exist_item(self, filename, drive_item_id):
        children = (
            await MicrosoftGraphRestAPI.client.drives.by_drive_id(
                MicrosoftGraphRestAPI.drive_id
            )
            .items.by_drive_item_id(drive_item_id)
            .children.get()
        )
        result = False
        for item in children.value:
            if item.name == filename:
                result = True
                break

        print("check exist item successful...")
        return result

    async def create_folder(self, father_folder, foldername):
        # 创建文件夹
        folder_request_body = DriveItem(
            name=foldername,
            folder=Folder(),
            additional_data={
                "E5KeepActive App create log folder",
            },
        )

        await MicrosoftGraphRestAPI.client.drives.by_drive_id(
            MicrosoftGraphRestAPI.drive_id
        ).items.by_drive_item_id(father_folder).children.post(folder_request_body)
        print("create folder successful...")

    async def get_item_id(self, filename):
        item = (
            await MicrosoftGraphRestAPI.client.drives.by_drive_id(
                MicrosoftGraphRestAPI.drive_id
            )
            .items.by_drive_item_id(filename)
            .get()
        )
        print("get item_id successful...")
        return item.id

    async def create_file(self, father_folder_id, filename):
        # 创建一个空文件
        file_request_body = DriveItem(
            name=filename,
            file=File(),
            additional_data={
                "E5KeepActive App create log file",
            },
        )

        await MicrosoftGraphRestAPI.client.drives.by_drive_id(
            MicrosoftGraphRestAPI.drive_id
        ).items.by_drive_item_id(father_folder_id).children.post(file_request_body)
        print("create file successful...")

    async def get_content(self, item_id):
        content = (
            await MicrosoftGraphRestAPI.client.drives.by_drive_id(
                MicrosoftGraphRestAPI.drive_id
            )
            .items.by_drive_item_id(item_id)
            .content.get()
        )
        print("get content successful...")
        return content

    async def put_content(self, item_id: str, content: bytes):
        await MicrosoftGraphRestAPI.client.drives.by_drive_id(
            MicrosoftGraphRestAPI.drive_id
        ).items.by_drive_item_id(item_id).content.put(content)
        print("put content successful...")

    def __del__(self):
        """
        执行清理操作，释放资源等。
        在不再需要使用 MicrosoftGraphRestAPI 实例时调用此方法。
        """
        # 关闭 API 客户端连接
        if MicrosoftGraphRestAPI.client:
            del MicrosoftGraphRestAPI.client
            del MicrosoftGraphRestAPI.drive_id
            gc.collect()
        print("clear MicrosoftGraphRestAPI client successful...")
