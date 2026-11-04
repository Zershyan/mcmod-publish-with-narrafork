---
name: mcmod-publish-with-narrafork
description: Minecraft 模组在 CurseForge 与 MC百科（mcmod.cn）的对外发布与资料提交：CF 项目创建、版本上传、CurseMaven 依赖来源登记，以及百科模组条目创建、各类资料正文撰写、图标制作、批量提交与审核核对。用户提到发布模组、上传 JAR、CurseForge 项目或文件、CurseMaven 坐标、MC百科、mcmod、百科资料、审核退回时使用；不用于模组代码开发。
---

# 模组发布与资料提交

CurseForge 负责发行与依赖坐标，MC百科负责中文资料。两条线共享同一批事实来源（源码、语言文件、数据包、JAR 元数据），所以先取证再填表是全局前提。

## 两条流水线

```
模组工程 ──┬─→ CurseForge：项目创建 → 版本上传 → 文件状态核对
           │                     └→ Project ID / slug ─┐
           └─→ MC百科：模组条目（必填 CF Project ID）←─┘
                        └→ 资料条目（正文 / 图标 / 批量提交 / 审核核对）
```

百科创建模组必须填 CurseForge Project ID，所以 CF 项目要先存在；CF 项目描述要写的功能清单则来自源码，两者互为输入。

## 总原则

- **事实先于填写**：数值、ID、文件版本现查现核，不凭记忆。数据以本地源码、数据包、语言文件、JAR 元数据为准；tooltip 与代码冲突时以代码为准，并在汇报中指出差异。
- **对外动作要授权**：提交资料、再编辑、撤回、创建 CF 版本都是对外发布，用户明确要求后才执行。只批量提交已核实定稿的条目，有疑问的进「暂缓」清单并注明原因。
- **状态不臆测**：CF 返回文件 ID 只代表上传被接受，Processing / Baking / Under Review 都不是 Approved；百科返回 `state === 0` 只代表受理，不代表审核通过。
- **凭据不落地**：CF 令牌只从 `CURSEFORGE_API_TOKEN` 读取，不写入文件、命令文本或对话输出。
- **不绕过拦截**：遇到登录、人机验证、权限拦截时停下说明缺项交给用户，不换路径硬闯。

## 执行方式

CF 的 API 调用固定走 [upload_release.py](scripts/cf-http/upload_release.py)：`curl_cffi` 模拟 Chrome 指纹，规避 Cloudflare 挑战页；用 `curl`、`urllib` 或 PowerShell 直连会拿到 `Just a moment...` 的 HTML。

页面操作默认走**控制台脚本**：生成脚本交给用户在页面 F12 里运行。开浏览器、登录、翻页面成本高，能脚本化的就不开浏览器。

1. 控制台脚本：`scripts/mcmod/` 与 `scripts/cf-create-fill/` 的生成器，**默认路径**。
2. `browsermcp`：脚本一步走不通、需要读页面状态核对，或用户已经在页面里操作时，用已登录的真实 Chrome 直接读写。
3. `Browser` 工具：需要独立会话时，自行登录。

## 路由

| 任务 | 先读 |
|---|---|
| 上传/发布 CF 版本、核对文件状态 | [CF 发布](references/curseforge/upload.md) |
| 创建 CF 项目、填项目资料 | [CF 项目](references/curseforge/project.md) |
| 查或登记 CurseMaven 依赖坐标 | [依赖来源](references/curseforge/dependencies.md) |
| 创建百科模组条目 | [百科模组](references/mcmod/project.md) |
| 从源码导出物品/实体数据 | [数据导出](references/mcmod/export.md) |
| 写资料正文 | [正文规范](references/mcmod/content.md)、[分类模板](references/mcmod/content-templates.md) |
| 制作 32/128 图标 | [图标](references/mcmod/icons.md) |
| 批量提交与核对审核 | [提交与审核](references/mcmod/submit.md) |

跨平台条款（目录、命名、产物位置、汇报格式）见 [通用约定](references/shared.md)，开工前先确认一遍。

## 需要用户决定

- 百科作者 ID（作者页地址 `https://www.mcmod.cn/author/<ID>.html` 里的数字）与作者名，不能猜。
- 发现同名物品、明显错译、或与已发布版本冲突时，先停下让用户决定。
- 脚本走不通时，是否改用浏览器直连。
