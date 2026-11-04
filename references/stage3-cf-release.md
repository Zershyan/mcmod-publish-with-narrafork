# 阶段 3：发布 CF 版本

## 取版本标签

```bash
python scripts/cf-http/upload_release.py query curseforge
```

写到 `curseforge/game-versions.json`。版本数字 ID 只从这份文件取，不凭记忆写。

## 更新说明

按 git 提交记录整理，一次发布对应一段区间：

```bash
git log --oneline <上一个发布tag>..HEAD
```

整理成**英文块在上、`---`、中文块在下**，不在一段里中英交替。写功能、用途与兼容目标；MC 版本、加载器、Java 放版本标签，不重复塞进描述。

衍生或移植作品，两个语言块开头各写一次原作名、作者、项目链接与「非官方」声明；描述和更新说明都加 `## Credits` / `## 鸣谢`，只写感谢与来源，不写暗示原作者背书的措辞。

## 发布清单

写 `curseforge/release-manifest.json`：

```json
{
  "files": [
    {
      "minecraft": "1.21.1",
      "artifact": "build/libs/<mod_id>-<mod_version>-<minecraft_version>.jar",
      "sha256": "<脚本会校验>",
      "metadata": {
        "changelog": "<英文块 + --- + 中文块>",
        "changelogType": "markdown",
        "displayName": "<工程原始版本号，如 2.0.0-1.21.1+build.44>",
        "releaseType": "release",
        "gameVersions": ["1.21.1", "NeoForge", "Client", "Server"],
        "relations": { "projects": [] }
      }
    }
  ]
}
```

- `displayName` 用工程原始版本号，不另拼。
- `gameVersions` 用 [版本标签](#取版本标签) 里的完整名称，1.21.1 不等于 1.21.11。
- `relations.projects` 里每一项写 `{"projectId": <ID>, "type": "requiredDependency"}`。依赖从这里来：`build.gradle` 的 `curse.maven:<名>-<项目ID>:<文件ID>`，例如 `curse.maven:curios-309927:6529130` → `projectId: 309927`。`jarJar` 内置的库玩家不用另装，不声明。

## 上传

```bash
python scripts/cf-http/upload_release.py upload curseforge/release-manifest.json --project-id <ID> --slug <slug>
```

- 上传前校验 artifact 的 sha256，文件被改过就拒绝。
- 已有 `upload-result-<版本>.json` 带 ID 的跳过；存在 `upload-attempt-<版本>.json` 但没结果的拒绝重传，先去线上核对。
- 令牌只从 `CURSEFORGE_API_TOKEN` 读取。

## 状态

HTTP 成功和文件 ID 只代表上传被受理。Processing、Baking、Under Review 都不是 Approved。收到 ID 后查这个文件，不因等待重复提交。

- 400 对照字段错误处理；401/403 区分权限、项目归属与网络拦截。
- 上传 API 没有文件列表接口，查 `https://www.curseforge.com/api/v1/mods/<项目ID>/files?pageIndex=0&pageSize=20&sort=dateCreated&sortDescending=true`（同样要模拟 Chrome）。审核中的文件不出现在这个公开列表里，不能据此判断上传失败。

## 记录

把文件链接、文件 ID、目标版本和实际状态写进 `curseforge/` 的结果文件，汇报时给出。
