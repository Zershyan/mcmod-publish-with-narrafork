---
name: mcmod-publish-with-narrafork
description: 把 Minecraft 模组发布到 CurseForge 与 MC百科。读工程事实、判断项目是否已存在、上传 JAR、填写百科条目与资料、处理登录与验证码、核对审核附言。用户要求发布模组、上传版本、更新百科、补资料或处理退回时使用；不用于模组代码开发。
---

# 模组发布

两条对外渠道：CurseForge 管发行，MC百科管中文资料。所有信息先从工程里读，读不到的才问用户。

## 先判断走哪条路

| 情况 | 走法 |
|---|---|
| 工程里没有发布记录，用户也没说已有项目 | 建 CF 项目 → 发版本 →（可选）建百科条目 |
| 已有 CF 项目，只是发新版本 | 直接发版本 →（可选）更新百科 |
| 只是补百科资料 | 比对现有条目与工程 → 只提交差异 |

判断依据按顺序：`curseforge/project.json` → 工程里的发布记录 → 问用户。**不要自己去 CurseForge 猜**，项目页被 Cloudflare 挡着，抓不到。

## 六个阶段

```
读工程事实 → 拉版本标签 → 确认配置 → CF 发版 →（可选）百科 → 核对审核
```

| 阶段 | 做的事 | 详见 |
|---|---|---|
| 1 | 读 `gradle.properties`、`build.gradle`、语言文件、分支 | [workflow](references/workflow.md#1-读工程事实) |
| 2 | 拉 CurseForge 的 Game Versions，供版本标签用 | [curseforge](references/curseforge.md#版本标签) |
| 3 | 出配置表单给用户确认 | [workflow](references/workflow.md#3-确认配置) |
| 4 | 上传 JAR，每个「MC 版本 × 加载器」一次 | [curseforge](references/curseforge.md#上传) |
| 5 | 百科建条目、提交资料 | [mcmod](references/mcmod.md) |
| 6 | 对照审核附言修正 | [mcmod](references/mcmod.md#审核) |

## 三条硬约束

**凭据**：CF 令牌只从环境变量 `CURSEFORGE_API_TOKEN` 读，不写文件、不进命令输出。缺了就停下来给用户链接去取，然后等回复，不要自己找。

**对外动作**：发布、建项目、提交资料都是公开行为。每一步动手前先拿到明确同意。新建 CF 项目尤其要单独问一次——「发个版本」不等于「同意新建一个项目」。

**不猜**：字段从哪取由 [字段来源](references/field-sources.md) 规定。表里没有的一律问用户，宁可停下来。

## 页面操作怎么走

| 方式 | 用在哪 | 前提 |
|---|---|---|
| 纯脚本 | CF 全部上传；百科条目提交 | 有 CF 令牌 / 百科 cookie |
| 控制台脚本 | 百科没 cookie 时的兜底 | 用户自己 F12 粘贴 |
| `Browser` 工具 | 需要过登录或验证码时 | 会话存活期内有效 |

百科的 cookie 拿不到就只能退到控制台脚本，[mcmod](references/mcmod.md#登录与凭据) 里有完整的三层回退。

## 配置表单

调研完工程后，用模板出表单一次性确认，别逐条追问：

```
assets/form-full/     首次发布，覆盖 CF 与百科全部字段
assets/form-release/  只发新版本，只要 JAR、版本号、更新说明
```

复制到 `.narrafork/gen_ui/<名称>/` 后只改 `data.ts`，再用 GenUI show。用法见各目录的 `README.md`。

## 踩过的坑

这些是实际踩到并修过的，[pitfalls](references/pitfalls.md) 里有完整记录和症状：

- 百科的 tagsinput 直接改 `value` 不生效，必须调控件 API
- 百科 MC 版本的 input 全在 DOM 里但按加载器隐藏，**不要以为没出现就是没选上**
- 百科作者搜索只认名字，用户中心 ID 不是作者 ID
- CF 的版本名用工程 `version` 原值，不要自己拼格式
- CF 请求只用 `curl_cffi` 指纹，`curl`/`urllib` 一律被 Cloudflare 挡

## 参考

- [完整流程](references/workflow.md)：七个步骤的判定条件与分支
- [CurseForge](references/curseforge.md)：项目创建、上传、依赖、状态语义
- [MC百科](references/mcmod.md)：登录、提交接口、字段结构、审核
- [字段来源](references/field-sources.md)：每个字段从哪取
- [踩坑记录](references/pitfalls.md)：症状、原因、正确做法
