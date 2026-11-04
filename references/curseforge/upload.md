# CurseForge 版本发布

## 范围

- 用户要求发布或创建时直接完成相应流程，不重复询问同一个授权；缺登录、凭据或无法确定目标项目时说明缺项。
- 项目 ID 来自项目发布记录、作者后台或确定的项目页，不从第三方依赖来源表里取自己的项目。

## API

参考：<https://support.curseforge.com/support/solutions/articles/9000197321-curseforge-api>

- 上传端点：`POST https://minecraft.curseforge.com/api/projects/{projectId}/upload-file`，multipart 包含 metadata 与 file。
- metadata 含 changelog、changelogType、displayName、releaseType，以及实际支持的版本/加载器/环境；关联项目按需提供 relations。
- 版本数字 ID 来自 Game Versions API，不凭记忆填写；用名称时取接口支持的完整名称。Client/Server 标签按实际支持情况选。
- `X-Api-Token` 从 `CURSEFORGE_API_TOKEN` 注入，不写入文件、命令文本或输出。
- 请求复用系统现有代理（本机需要代理才能访问 CF 时），不把 Cloudflare HTML 当成字段错误。

## Cloudflare 挑战页

**现象**：`curl`、PowerShell 或 Python `urllib` 请求 `minecraft.curseforge.com/api/...` 返回 `<title>Just a moment...</title>` 的 HTML，JSON 解析失败；换代理返回 000。原因是 Cloudflare 按 TLS/HTTP2 指纹识别出非浏览器客户端，不是令牌或字段错误。

**解决**：所有 CF 请求统一走 [scripts/cf-http](../../scripts/cf-http/browser_http.py)，用 `curl_cffi` 的 `impersonate='chrome'` 模拟 Chrome 指纹；代理依次读 `HTTPS_PROXY`/`HTTP_PROXY` 环境变量和 Windows 系统代理，都没有时直连。这只改变网络层特征，调用的仍是官方 API 和用户自己的令牌，不涉及解答验证码。

```python
import sys, urllib.request
sys.path.insert(0, r'<skill目录>/scripts/cf-http')
from browser_http import BrowserOpener
opener = BrowserOpener()  # 不传参数时使用系统代理
with opener.open(urllib.request.Request(url, data=body, headers=headers, method='POST'), timeout=55) as r:
    print(r.status, r.read().decode())
```

只读查询也可以 `from curl_cffi import requests` 后 `requests.get(url, proxy='http://<代理地址:端口>', impersonate='chrome')`（不需要代理时省略 proxy）。

**运行时**：首次使用先 `python -m pip install curl_cffi`；不想装进全局环境时可 `python -m pip install --target "<运行时目录>" curl_cffi`，再把 `CF_HTTP_RUNTIME` 设为该目录。

## 上传统一走 [upload_release.py](../../scripts/cf-http/upload_release.py)

不要在发布目录里另写一次性上传脚本——写死运行时目录和代理的脚本换机器就报错。

```bash
python <skill>/scripts/cf-http/upload_release.py query  <发布目录>            # 标签写入 <发布目录>/game-versions.json
python <skill>/scripts/cf-http/upload_release.py upload <发布目录>/release-manifest.json --project-id <ID> --slug <slug>
```

- 清单格式 `{"files":[{"minecraft","artifact","sha256","metadata"}]}`，上传前校验 artifact 的 sha256。
- 已有 `upload-result-<版本>.json` 且带 ID 的跳过；存在 `upload-attempt-<版本>.json` 但无结果的拒绝重传，先核对线上列表。
- 运行时与代理都由 `browser_http.py` 解析（`CF_HTTP_RUNTIME` → 当前 Python 环境；环境变量或系统代理，可用 `--proxy` 覆盖）；缺 `curl_cffi` 时直接打印重装命令。

**查询已上传文件**：Upload API 没有文件列表接口，用 `https://www.curseforge.com/api/v1/mods/<项目ID>/files?pageIndex=0&pageSize=20&sort=dateCreated&sortDescending=true`（同样要模拟 Chrome）。审核中的文件不出现在这个公开列表里，不能据此判断上传失败而重复提交。

## 描述与更新说明

- 中英分块，**英文块在上、中文块在下**，中间用 `---` 分隔，不在同一段落或列表项里中英交替。
- 写功能、用途与兼容目标；MC 版本、加载器、Java 放版本标签，不重复塞进描述。
- 衍生或移植作品的英文块和中文块开头各写一次原作名、作者、项目链接与「非官方」声明，许可与源码各自放在本语言块末尾。
- 重做、移植或衍生自他人模组的，项目描述和每次更新说明都加原作者鸣谢（`## Credits` / `## 鸣谢`），放在本语言块的许可与源码之前；只写感谢与来源并请玩家支持原作，不写任何暗示原作者认可或背书的措辞。

## 结果与恢复

- HTTP 成功和文件 ID 只代表上传被接受；Processing、Baking、Under Review 都不是 Approved。已收到 ID 后查询该文件，不因等待而重复提交。
- 400 对照具体字段错误处理；401/403 区分权限、项目归属与网络拦截。响应不明时先看现有文件列表。
- 最终记录文件链接、ID、目标版本与实际状态，不承诺审核耗时。

## 网页操作特有问题

浏览器直连或控制台脚本都适用：

- 文件选择用可见 Choose File 触发的选择器；表单可能位于内部滚动容器里。
- 自动填充可能沿用上一个文件的标签；多选控件是追加而不是替换。版本名要完整匹配，1.21.1 不等于 1.21.11。
- 浏览器重连后恢复当前标签与文件列表，不要重开表单再提交一次。
