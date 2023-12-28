# E5_Subscription_AutoActive

基于Microsoft Graph REST API 自动调用OneDrive 相关 api 请求，模拟开发者活动
以续订微软E5开发者账号

官方SDK在请求文件内容时存在重定向BUG[GitHub ISSUES](https://github.com/microsoftgraph/msgraph-sdk-python/issues/504),推荐使用E5_Subscription_AutoActive_ByPython


## 使用说明

在配置文件 config/config.ini 中指定相关程序参数后，点击/bin/E5KeepActive.exe 文件运行程序。

首次运行会弹出登录对话框，按步骤登录即可。
程序运行正常会在 相应账号的 OneDrive 网盘上生成 E5KeepActive/E5KeepActive.log 文件(记录了上次调用api的时间)。

### 参数说明

    1.基础配置
        # 是否随系统一起启动，[True or False]
        start_with_system = True

        # API调用时间间隔范围(两端包含), 单位：分钟
        call_func_period = [20,60]

    2.用户信息(包含的信息来自于你在Microsoft Entra 管理中心上注册的应用，如若不清楚可自行百度/Google)
        # 租户ID (Directory (tenant) ID)  
        tenant_id = xxxxxx

        # 客户端ID (Application (client) ID)
        client_id = xxxxxx

        # 客户端密码 (client_value)
        client_secret = xxxxxx

### 应用权限说明

    todo

### 应用详细调用API列表

    todo
