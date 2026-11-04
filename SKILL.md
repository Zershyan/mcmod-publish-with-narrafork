---
name: mcmod-publish-with-narrafork
description: 从 Minecraft 模组工程发布到 CurseForge 与 MC百科：读取工程信息、新建 CF 项目、发布版本、创建百科模组条目与资料条目、核对审核。所有信息取自 mod 工程本身，工程里没有的才询问用户。用户提到发布模组、上传 JAR、CurseForge 项目、百科资料、审核退回时使用；不用于模组代码开发。
---

# 模组发布

所有信息都从 mod 工程本身读取。每个字段的取值位置见 [字段来源总表](references/sources.md)；工程里确实没有的（中文名、平台分类、百科作者 ID 等）才问用户，不猜。

## 流程

CF 与百科是前后两段：百科的模组条目必须填 CurseForge Project ID，所以 CF 项目要先建。

| 阶段 | 做什么 | 文档 |
|---|---|---|
| 1 | 读工程事实 | [工程信息](references/stage1-project.md) |
| 2 | 新建 CF 项目 | [CF 项目](references/stage2-cf-project.md) |
| 3 | 发布第一个版本 | [CF 发版](references/stage3-cf-release.md) |
| 4 | 新建百科模组条目 | [百科模组](references/stage4-wiki-project.md) |
| 5 | 创建百科资料条目 | [百科资料](references/stage5-wiki-entries.md) |
| 6 | 核对审核 | [审核](references/stage6-review.md) |

后续版本只走阶段 3；新增物品时补阶段 5。

## 总原则

- **来源固定**：字段从哪取由 [字段来源总表](references/sources.md) 规定，不临场发挥。工程里没有的值问用户，并在汇报里列出问了什么。
- **对外动作要授权**：创建项目、上传版本、提交资料、再编辑都是对外发布，用户明确要求后才执行。
- **状态不臆测**：CF 返回文件 ID 只代表上传被受理，Processing / Under Review 都不是 Approved；百科 `state === 0` 只代表受理。
- **凭据不落地**：CF 令牌只从 `CURSEFORGE_API_TOKEN` 读取，不写入文件、命令或输出。

## 执行方式

页面操作默认生成**控制台脚本**，用户在自己浏览器 F12 里运行；开浏览器、登录成本高，脚本能做的就不开浏览器。

CF 的 API 请求固定走 [upload_release.py](scripts/cf-http/upload_release.py)：`curl_cffi` 模拟 Chrome 指纹，用 curl 或 PowerShell 直连会被 Cloudflare 拦成 `Just a moment...` 的 HTML。

脚本走不通、或需要读页面状态核对时，用 `browsermcp` 操作已登录的真实 Chrome 补位。

## 产物位置

| 内容 | 位置 |
|---|---|
| 百科定稿、提交脚本、资料 ID 映射 | `docs/mcmod/`（映射为 `docs/mcmod/entries.json`） |
| CF 发布清单与上传结果 | 项目 `curseforge/` |
| 临时导出、图标中间产物 | `build/mcmod/` |

## 配置确认

调研完工程后，用数据驱动的表单一次性确认所有字段，而不是逐条追问：把 [assets/publish-form](assets/publish-form/README.md) 的 `App.tsx` 和 `data.ts` 复制到 `.narrafork/gen_ui/<名称>/`，只改 `data.ts`，再用 GenUI show 出来给用户核对。工程里没有的信息（中文名、平台分类、百科作者 ID）也在表单里问。

**出表单前必须先跑一次版本查询**：

```bash
python scripts/cf-http/upload_release.py query curseforge
```

把 `curseforge/game-versions.json` 里的 MC 版本号写进 `data.ts` 的 `mcVersions`，让用户从真实可用的版本里选。没有 `CURSEFORGE_API_TOKEN` 拉不到时，省略 `mcVersions` 用兜底候选，并明确告诉用户这些版本未经 API 校验。
