# CurseForge

## 令牌

上传用 **API Token**，不是 API Key：

```
https://authors.curseforge.com/#/settings/api-tokens
```

生成后只显示一次。设进环境变量：

```powershell
setx CURSEFORGE_API_TOKEN "…"
```

脚本读环境变量，Windows 上读不到时会回退到注册表的用户环境变量（`setx` 设的值新进程未必继承）。

没有令牌时**停下来给链接等用户**，不要尝试其它途径。

## 请求必须用 curl_cffi

```python
from cfhttp import requests, BrowserOpener
```

`curl`、`urllib`、PowerShell 直连 `minecraft.curseforge.com/api/...` 一律返回 `<title>Just a moment...</title>`，因为 Cloudflare 按 TLS 指纹识别。`scripts/cf/cfhttp.py` 用 `curl_cffi` 的 `impersonate='chrome'` 解决。

首次使用：

```bash
python -m pip install --target <目录> curl_cffi
export CF_HTTP_RUNTIME=<目录>
```

## Studio API 能做什么

实测边界（2026-11）：

| 端点 | 结果 |
|---|---|
| `GET /api/game/versions` | ✅ 200 |
| `POST /api/projects/{id}/upload-file` | ✅ 可用 |
| `GET /api/projects` | ❌ 404 |
| `GET /api/projects/{id}` | ❌ 404 |
| `GET /api/me` | ❌ 404 |

**没有「按名字查项目」的接口。** 社区 API（`api.curseforge.com/v1`）要另一种 `x-api-key`，Studio 令牌调它返回 403。

## 版本标签

```bash
python scripts/cf/upload.py query curseforge
```

结果在 `curseforge/game-versions.json`。拉到的结构里：

- 每个 MC 大版本系列一个 `gameVersionTypeID`，`26.1.x` 是 `83806`，`1.21.x` 是 `77784`
- 加载器统一在 `68441`（Forge / Fabric / NeoForge / Quilt / Rift）
- Java 版本在 `2`（`Java 8` ~ `Java 25`）
- 环境在 `75208`（`Client` / `Server`）

`gameVersions` 里要同时给：MC 版本、加载器、Java 版本、Client/Server。名称必须与接口返回完全一致，`1.21.1` 不等于 `1.21.11`。

## 项目创建

CF 没有建项目的 API，只能网页填表。用生成器出控制台脚本：

```bash
python scripts/cf/create_project.py curseforge/cf_create_project.json
node --check curseforge/cf_create_project_fill.js
powershell -NoProfile -Command "Get-Content -Raw -Encoding UTF8 'curseforge/cf_create_project_fill.js' | Set-Clipboard"
```

用户在 Create A Project 页面 F12 粘贴运行。要求：**界面切英文、关闭浏览器翻译**，否则所有字段匹配不到。

`autoCreate` 默认 true，脚本会自己点创建按钮并读回 `projectId`/`slug`。**启用前必须用交互式提问单独确认一次**项目名、分类、许可证。

失败时跑 `scripts/cf/dom_probe.js` 抓页面结构，按实际结构改模板。

## 上传

清单格式：

```json
{
  "files": [{
    "minecraft": "1.21.1",
    "artifact": "build/libs/xxx.jar",
    "sha256": "…",
    "metadata": {
      "changelog": "英文块\n\n---\n\n中文块",
      "changelogType": "markdown",
      "displayName": "examplemod-2.0.0-1.21.1",
      "releaseType": "release",
      "gameVersions": ["1.21.1", "NeoForge", "Java 21", "Client", "Server"],
      "relations": { "projects": [{ "projectId": 309927, "type": "requiredDependency" }] }
    }
  }]
}
```

```bash
python scripts/cf/upload.py upload curseforge/release-manifest.json \
  --project-id <ID> --slug <slug>

# 只看线上已有哪些文件
python scripts/cf/upload.py list curseforge --project-id <ID>
```

- `displayName` 拼成 `<modid>-<mod_version>-<mc版本>`，即正式 jar 文件名去掉 `.jar`，例 `examplemod-2.0.0-1.21.1`
- **不要带 `+build.N`**：带编号的是 `buildAlpha` 产物，既不能上传，也不要写进显示名
- 脚本会直接拒绝 jar 名或 `displayName` 带 `+build.` 的条目
- `artifact` 上传前校验 sha256
- 一个 JAR 只对应一组「MC 版本 + 加载器」，多个组合要拆成多条
- `relations.projects[].type` 常用 `requiredDependency`、`optionalDependency`、`incompatible`

三层去重，命中任一层就跳过：

1. `upload-result-<版本>.json` 里已有 ID
2. 线上文件列表里 displayName 相同
3. 有 `upload-attempt-<版本>.json` 但没结果 → 拒绝重传，先核对线上

线上文件列表（免令牌）：

```
GET https://www.curseforge.com/api/v1/mods/{projectId}/files?pageIndex=0&pageSize=50
```

返回 `id`、`displayName`、`fileName`、`releaseType`、`status`。审核中的文件可能不在列表里，所以本地记录仍要看。

## 依赖

从 `build.gradle` 解析，写进 `relations.projects`：

| 写法 | 处理 |
|---|---|
| `curse.maven:<名>-<项目ID>:<文件ID>` | 取项目 ID |
| `jarJar` | 内嵌打包，玩家不用装，**不声明** |
| `localRuntime` | 只用于开发测试，**不声明** |
| `localImpl` / `implementation` | 通常 requiredDependency |
| `compileOnly` | 视情况 optionalDependency |

非 CF 坐标关联不到 projectId，只在描述里说明。

## 描述与更新说明

- 英文块在上、`---`、中文块在下，不交替
- MC 版本、加载器、Java 放版本标签，不重复塞进描述
- 衍生作品两个语言块开头各写一次原作名、作者、链接、「非官方」声明
- 衍生作品加 `## Credits` / `## 鸣谢`，只写感谢与来源，不写暗示原作者背书的措辞

## 状态语义

HTTP 200 和文件 ID 只代表**上传被受理**。`Processing`、`Baking`、`Under Review` 都不是 Approved。

查状态的地址：

```
公开文件列表  https://www.curseforge.com/minecraft/mc-mods/<slug>/files
作者后台      https://authors.curseforge.com/#/projects/<projectId>/files
```

**审核中的文件不出现在公开列表里**，只能从作者后台看，所以公开列表为空不等于上传失败。

- 400 对照字段错误
- 401/403 区分权限与网络拦截
- 响应不明时先查作者后台，别重传

最终汇报文件链接、ID、目标版本、实际状态。不承诺审核耗时。
