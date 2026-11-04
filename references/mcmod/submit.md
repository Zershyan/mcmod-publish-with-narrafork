# 批量提交与审核

## 条目数据

定稿条目整理成 JSON 数组，每条字段：`key, name, ename, regname, damage, maxstack, type, content, icon32, icon128`。

- 分类不是「物品/方块」时额外写 `category`（见 [分类模板](content-templates.md#分类值)对应的值），并把 `damage`/`maxstack` 留空。
- `regname` 对「物品/方块」「群系/群落」「生物/实体」「BUFF/DEBUFF」「附魔/魔咒」「世界/维度」「自然生成」都必填，格式 `modid:id`（审核会以「实体注册名必填」退回）；合并多个变种的条目填主体的注册名。
- 重新提交已退回的条目时加 `redo` 字段（审核列表「再编辑」链接 `/item/add/<模组ID>-<资料ID>/` 里的资料 ID），脚本会走再编辑，不产生新的重复审核项。

## 方式 A：浏览器直连（默认）

用 `browsermcp` 在添加页逐条填写：切分类标签、填名称/注册名/耐久/堆叠、`editor.setContent()` 写正文、写 `#icon-32x` / `#icon-128x`，然后**点页面的「添加资料」按钮**并在确认弹窗点「确定提交」，让页面自己走提交路径。

- 改动附言默认留空，用户明确要求时才填。
- 每提交一条就核对返回，`state !== 0` 时停下查原因，不要连着重试。
- 条目多时先提交 1 条确认无误，再继续其余条目。
- 页面上按钮点不动、或提交被权限拦截时，改用方式 B，不要绕过拦截。

## 方式 B：控制台脚本（回退）

```bash
python scripts/mcmod/make_batch_js.py 条目.json 输出.js 0 "" [逗号分隔的key列表]
node --check 输出.js
```

- 第 3 个参数 `1` 为试运行（只收集数据不提交），第 4 个参数是附言，默认传空字符串。
- 先生成只含 1 条的测试脚本让用户试提交，确认无误后再给其余条目的脚本。
- 用户在添加页按 F12 运行；脚本每条间隔 4 秒，返回 `state !== 0` 时停止，结果存在 `window.__mcmodBatchResults`。
- 脚本调用页面自己的 `getEditorData()` 和 `/action/edit/doEdit/` 接口，不构造私有凭据。

## 再编辑已提交但未通过的条目

在审核列表点「再编辑」（`/item/add/<模组ID>-<资料ID>/`）打开，按 `location.pathname` 匹配修正内容，核对主要名称后 `editor.setContent()`，交给用户自己点「完成添加」。

## 核对审核

- 自己的审核列表：`https://www.mcmod.cn/verify.html?order=createtime&selfonly=1`。
- 可用 `fetch(再编辑链接)` + `DOMParser` 读取待审内容的正文（`[id^=editor]`）和次要名称，只读不改。
- 逐条对照审核附言修正。已知审核要求：
  - 生物/实体必须填注册名，最好补渲染图标（百科推荐批量导出：1.21 NeoForge 可用 IconRenderer〔mcmod 6074〕或 LMS）。
  - 表格标题要用标题行（右键表格 → 添加标题行）。
  - 能组成一套的盔甲要建「XX套装」统一介绍，单件正文留空，次要名称 `XX Suit`；成套工具同理建「XX套具」。
  - 抽象资料（套装、套具）不需要图标。
- 尚未发布的改动（例如只在本地源码新增的配方）不写进百科，等新版本发布后再补。
