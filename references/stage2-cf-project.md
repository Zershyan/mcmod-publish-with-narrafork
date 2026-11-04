# 阶段 2：新建 CF 项目

在 CurseForge 作者后台创建项目，拿到 `projectId` 和 `slug`——阶段 3、4 都要用。

## 资料

按 [字段来源](sources.md#阶段-2cf-项目)取，写进项目 `curseforge/cf_create_project.json`：

| 字段 | 说明 |
|---|---|
| `name` | `mod_name` |
| `summary` | `mod_description`，CF 限 1～256 字符 |
| `description` | Markdown 文件；英文块在上、`---`、中文块在下 |
| `icon` | PNG，超过 400px 会缩到 400×400 |
| `dropdowns` | `[["Class","Mods"],["Main category","…"],["Additional categories","…"]]`，文字与 CF 英文选项一致 |
| `license` | `mod_license`，选项包含该文字即可 |
| `distribution` | 闭源 `Allow distribution to 3rd party` 改为不允许 |
| `allowComments` | `true` |

## 填表脚本

```bash
python scripts/cf-create-fill/build_fill_js.py curseforge/cf_create_project.json
node --check curseforge/cf_create_project_fill.js
powershell -NoProfile -Command "Get-Content -Raw -Encoding UTF8 'curseforge/cf_create_project_fill.js' | Set-Clipboard"
```

用户在 Create A Project 的 General 页按 F12 粘贴运行。脚本按 `create/general` → `create/description` → `create/license` 逐步填写并点 Next，有字段没填上就停在当前步骤，**不会点最终的 Create**。

**界面必须是英文，并关闭 Edge 网页翻译**——翻译后标签变中文，所有字段都匹配不到。

脚本某步匹配不到字段时，用 `browsermcp` 在页面上补，再到 [页面结构](#页面结构) 核对选择器。

## 页面结构

MUI + react-admin，实测于 2026-10-31：

- Class 是 MUI Select（`div[role="combobox"]`），只响应 `button=0` 的 `mousedown`，`click()` 打不开。
- Main / Additional categories 是 Autocomplete（`input[role="combobox"]`），选项要等 Class 选定后才加载。只输入撇号前的前缀过滤，避开直引号与弯引号不一致。
- Allow Comments 是真实 checkbox；头像上传后弹出裁剪框，确认按钮为 `Save as logo`。
- License 步骤标签是 `Project License` 与 `Project distribution`，标签和下拉框之间隔着约 130～180px 说明文字，按「标签下方 90px」找不到；先沿祖先找只含一个 combobox 的容器，再退回 260px 范围查找。

## 失败排查

先看控制台表格的「说明」列（当前步骤没有该字段、可见选项、控件类型）。仍不清楚时在失败的步骤运行 `scripts/cf-create-fill/dom_probe.js`，它只读页面结构并复制到剪贴板。

名称已等于目标名称时视为已运行过，跳过图标上传，避免重复弹裁剪框。

## 产出

记下 `projectId`（数字）和 `slug`（地址栏最后一段），阶段 3、4 直接用。
