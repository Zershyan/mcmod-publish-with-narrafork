# 发布配置表单

数据驱动的 GenUI 表单：`App.tsx` 是通用模板，项目差异只写在 `data.ts`。

## 用法

```bash
mkdir -p .narrafork/gen_ui/<名称>
cp assets/publish-form/App.tsx .narrafork/gen_ui/<名称>/App.tsx
cp assets/publish-form/data.example.ts .narrafork/gen_ui/<名称>/data.ts
```

改 `data.ts` 为该项目的数据，然后 `GenUI show` 该目录。`App.tsx` 不需要改动。

调研完工程后应该只写一个 `data.ts`，不再重复生成整个表单。

## data.ts 字段

| 字段 | 内容 |
|---|---|
| `modName` | 模组英文名，显示在标题 |
| `badge` | 右上角角标，一般是许可证简称 |
| `extraLicenses` | 项目特有许可证，追加到内置列表（如 `GPL-3.0-with-additional-terms`） |
| `iconHint` / `coverHint` | 两个文件选择框的提示文字，写默认文件与尺寸 |
| `entriesEmptyText` | 没有资料条目时的说明 |
| `defaults` | 所有字段的 placeholder，即调研值；键名见下方 |
| `versions` | 默认版本列表，每条含 `modVersion`、`mcVersions`、`loaders`、`releaseType`、`env`、`changelog` |
| `authors` | 默认作者列表，`id` 留空等用户填 |
| `entries` | 资料条目，没有内容物时留空数组 |

## defaults 键名

| 键 | 对应 |
|---|---|
| `cfName` | CF 项目名 |
| `cfSummary` | CF 简介 |
| `cfDescription` | CF 详细描述 |
| `cfLicense` | 许可证 |
| `cfCategory` | CF 主分类（英文选项） |
| `cfExtraCategories` | 附加分类 |
| `cfSourceUrl` | 源码链接 |
| `wName` | 百科主要名称（中文） |
| `wEname` | 百科次要名称 |
| `wIntro` | 一句话简介 |
| `wModid` | MODID |
| `wCfId` | CF Project ID |
| `wCore` | 核心元素 |
| `wExtra` | 杂项元素 |
| `wStatus` | 官方状态 |
| `wAuthorName` | 作者名 |
| `wLinks` | 相关链接 |

取值规则见 [字段来源](../../references/sources.md)。

## 版本号

`modVersion` 填构建脚本里的实际 `version`，不要按统一规则拼。不同分支可能不同：

- 有的分支是 `${mod_version}-${minecraft_version}+build.${build_number}`
- 有的分支直接 `version = mod_version`

按每个分支 `build.gradle` 的实际写法填。

`data.ts` 里的 `mcVersions` 可以写任意版本号，包括模板下拉列表里没有的（例如 `26.1.2`）。模板里的版本候选只是给下拉提供几个能点的项，不追求完整、也不随新版本维护——真实版本列表以 CurseForge Game Versions API 为准。

## 交互

- 顶部勾选「同时发布到 MC百科」才出现百科页签
- 留空的项按 placeholder 执行
- 版本、作者、资料条目都可增删改，弹窗编辑
- 百科的运作方式与版本默认跟随 CF 的「加载器 × MC 版本」组合，手动改过后停止同步
