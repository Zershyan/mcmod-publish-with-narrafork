# 完整流程

七个步骤，按顺序走。每一步都写清了判定条件和失败后的处理。

## 1. 读工程事实

从工程文件里读，不猜。字段对应见 [字段来源](field-sources.md)。

```
gradle.properties   mod_id / mod_name / mod_version / mod_license /
                    mod_authors / mod_description / minecraft_version
build.gradle        加载器（neo_version 还是 forge_version）、version 计算方式、
                    java toolchain、依赖坐标、base.archivesName
分支                多分支工程要逐个分支读，版本号规则可能不同
语言文件            src/generated/resources 或 src/main/resources 下的 lang
logo                src/main/resources/logo.png
```

读完先汇报一张事实表，缺的标出来问用户。

工程里拿不到、必须问的只有四类：中文名、CF 主分类、百科模组元素、百科作者。

## 2. 拉版本标签

```bash
python scripts/cf/upload.py query curseforge
```

写到 `curseforge/game-versions.json`。版本标签的 ID 只从这里取，不凭记忆写。

拉不到（没令牌）时不要硬试，直接进入第 3 步并告诉用户版本标签尚未校验。

## 3. 确认配置

出表单让用户核对，不要逐条追问：

```
assets/form-full/      首次发布
assets/form-release/   只发新版本
```

做法：复制模板到 `.narrafork/gen_ui/<名称>/`，只改 `data.ts`，GenUI show 出来。

表单里所有调研值放在 placeholder（灰色提示），用户留空就按提示值执行。**枚举类字段要实选**，否则用户看不出会提交什么。

用户提交表单后，把结果落成两份配置：

```
curseforge/release-manifest.json   CF 上传用
docs/mcmod/mod-config.json         百科提交用
```

## 4. CF 发版

两条前置：

1. 有没有 `curseforge/project.json`？没有就先建项目
2. 令牌在不在？不在就给用户链接等回复

**建项目**（仅在需要时）：

```bash
python scripts/cf/create_project.py curseforge/cf_create_project.json
```

生成控制台脚本，用户在 Create A Project 页面 F12 运行。脚本按 General → Description → License 填完并点 Next；`autoCreate` 为 true 时连创建按钮一起点。

**动手前必须单独问一次**项目名、分类、许可证，拿到同意再生成脚本。

完成后把 `projectId` 和 `slug` 写进 `curseforge/project.json`。

**发版本**：

```bash
python scripts/cf/upload.py upload curseforge/release-manifest.json --project-id <ID> --slug <slug>
```

三层去重：本地 `upload-result-*.json` → 线上文件列表按 displayName → 遗留的 `upload-attempt-*.json` 拒绝重传。

返回文件 ID 只代表上传被受理，不是过审。

## 5. 百科（可选）

用户勾了才做。三步：检查 cookie → 建/查条目 → 提交资料。详见 [MC百科](mcmod.md)。

**cookie 是第一道门**。没有就按三层回退：CDP 导出 → 控制台脚本 → 让用户手动粘贴。

**已有条目时先比对差异**，不要整条重提。对比维度：名称、简介、元素、支持版本、作者、正文、资料条目数量。

## 6. 核对审核

用户把退回附言贴过来，按资料 ID 找到条目再改。地址：

```
已通过再编辑  /item/edit/<资料ID>/
待审再编辑    /item/add/<模组ID>-<资料ID>/
审核列表      https://www.mcmod.cn/verify.html?order=createtime&selfonly=1
```

## 各步骤的产物

| 步骤 | 产物 |
|---|---|
| 1 | 事实表（汇报给用户） |
| 2 | `curseforge/game-versions.json` |
| 3 | `curseforge/release-manifest.json`、`docs/mcmod/mod-config.json` |
| 4 | `curseforge/project.json`、`upload-result-*.json` |
| 5 | `docs/mcmod/entries.json`（资料 ID 映射） |
| 6 | 修正后的条目 |

## 中途停下来问用户的情况

只在这几种情形停：

- 缺 `CURSEFORGE_API_TOKEN`，或需要新建 CF 项目
- 工程里读不到的四类信息（中文名、分类、元素、作者）
- 百科需要登录或填验证码
- 线上已有同名条目但内容不同
- 某个「MC 版本 × 加载器」找不到对应的 JAR

其余情况自己往下走，不要每步都确认。
