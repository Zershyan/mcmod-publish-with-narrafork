# 完整配置表单

首次发布时用，覆盖 CurseForge 与 MC百科的全部字段。只发新版本用 [form-release](../form-release/README.md)。

## 用法

```bash
mkdir -p .narrafork/gen_ui/<名称>
cp assets/form-full/App.tsx .narrafork/gen_ui/<名称>/App.tsx
cp assets/form-full/data.example.ts .narrafork/gen_ui/<名称>/data.ts
```

改 `data.ts`，然后 GenUI show 该目录。`App.tsx` 不用动。

## 生成表单之前

先拉一次版本标签，把结果写进 `data.ts` 的 `mcVersions`：

```bash
python scripts/cf/upload.py query curseforge
```

拿不到令牌时省略 `mcVersions`，用模板兜底候选，并告诉用户这些版本未经验证。

## data.ts 字段

| 字段 | 内容 |
|---|---|
| `modName` | 模组英文名，显示在标题 |
| `badge` | 右上角角标，一般是许可证简称 |
| `extraLicenses` | 项目特有许可证，追加到内置列表 |
| `mcVersions` | API 拉到的版本列表，优先于兜底候选 |
| `iconHint` / `coverHint` | 两个文件选择框的提示，写默认文件与尺寸 |
| `entriesEmptyText` | 没有资料条目时的说明 |
| `defaults` | 所有字段的 placeholder，即调研值 |
| `versions` | 默认版本列表 |
| `authors` | 默认作者 |
| `entries` | 资料条目 |
| `dependencies` | CurseForge 依赖 |

## defaults 键名

| 键 | 对应 |
|---|---|
| `cfName` / `cfSummary` / `cfDescription` | CF 项目名、简介、详细描述 |
| `cfLicense` / `cfCategory` / `cfExtraCategories` | 许可证、主分类、附加分类 |
| `cfSourceUrl` | 源码链接 |
| `wName` / `wEname` / `wIntro` | 百科主要名称、次要名称、简介 |
| `wModid` / `wCfId` / `wMrId` | MODID、CF 项目 ID、Modrinth 项目 ID |
| `wCore` / `wExtra` | 核心元素、杂项元素 |
| `wStatus` / `wSource` | 官方状态、开源状态 |
| `wLicenseType` / `wLicenseName` | 协议类型、协议名称 |
| `wTags` / `wKeys` | 模组标签、搜索关键词 |
| `wRelations` / `wLinks` | 模组关系、相关链接 |
| `wAuthorName` | 作者名 |

取值规则见 [字段来源](../../references/field-sources.md)。

## 交互

- 顶部勾选「同时发布到 MC百科」才出现百科页签
- 留空的项按 placeholder 执行
- 版本、作者、资料条目、依赖都可增删改
- 百科的「运作方式与版本」默认跟随 CF 的「加载器 × MC 版本」组合，手动改过后停止同步

## 提交之后

拿到的是完整配置。落成两份文件：

```
curseforge/release-manifest.json   CF 上传清单
docs/mcmod/mod-config.json         百科提交配置
```
