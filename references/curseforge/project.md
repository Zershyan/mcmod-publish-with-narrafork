# CurseForge 项目创建

从作者后台新建项目并填完 General / Description / License 三个步骤。**最终的 Create 按钮永远由用户点**。

## 资料准备

写到项目 `curseforge/cf_create_project.json`：

| 字段 | 说明 |
|---|---|
| `name` | 项目名 |
| `summary` | 简介，1～256 字符 |
| `description` | Markdown 文件路径，按 [发布说明](upload.md#描述与更新说明)的中英分块格式写 |
| `icon` | PNG 路径，超过 400px 自动缩到 400×400 |
| `dropdowns` | `[["Class","Mods"],["Main category","…"],["Additional categories","…"]]`，文字必须与 CF 英文选项一致，Additional categories 可写多行 |
| `license` | 如 `MIT`，选项包含该文字即可 |
| `distribution` | 默认 `Allow distribution to 3rd party` |
| `allowComments` | 默认 `true` |

相对路径以 JSON 所在目录为基准。示例见 [project.example.json](../../scripts/cf-create-fill/project.example.json)。

## 浏览器直连（默认）

1. 用 `browsermcp` 打开用户已登录的作者后台，进入 Create A Project 的 General 步骤。
2. **界面切英文，关闭 Edge 网页翻译**——翻译后标签变中文，所有字段匹配不到。
3. 按上面的资料逐项填写：项目名、简介、Class/分类下拉、Allow Comments；上传图标后等裁剪框出现再确认。
4. Description 步骤优先切到 Markdown 文本模式，没有就把 Markdown 转成 HTML 写进富文本编辑器（表格排版需人工复核）。
5. License 步骤填 Project License 与 Project distribution。
6. 每完成一步只点 Next，不点 Create；字段没填上就停在当前步骤，报告缺项。

## 控制台脚本（回退）

前一步走不通、或用户要求和老流程一致时用生成器：

```bash
python <skill>/scripts/cf-create-fill/build_fill_js.py curseforge/cf_create_project.json
node --check curseforge/cf_create_project_fill.js
powershell -NoProfile -Command "Get-Content -Raw -Encoding UTF8 '<脚本路径>' | Set-Clipboard"
```

脚本内嵌图标，体积约 100～150KB，不直接贴进对话。用户在 Create A Project 的 General 页按 F12，粘贴运行一次；脚本按 URL 中的 `create/general`、`create/description`、`create/license` 逐步填写并自动点 Next，有字段未填上就停在当前步骤，处理后可再运行，不会点最终的 Create。

## 页面结构（MUI + react-admin，2026-10-31 探针与实测）

- Class 是 MUI Select（`div[role="combobox"]`），只响应 `button=0` 的 `mousedown`，`click()` 或发给外层容器都打不开。
- Main category / Additional categories 是 MUI Autocomplete（`input[role="combobox"]`），选项要等 Class 选定后才加载；Class 失败会连带两者显示「可见选项：无」。只输入撇号前的前缀过滤，避免直引号与弯引号不一致。
- Allow Comments 是真实 checkbox；头像上传后弹出裁剪框，确认按钮为 `Save as logo`。
- License 步骤的标签是 `Project License` 与 `Project distribution`，标签和下拉框之间隔着约 130～180px 的说明文字，按「标签下方 90px 内」找不到；先沿祖先找只含一个 combobox 的字段容器，再退回 260px 范围的几何查找。

**实测状态**（2026-10-31，Tinkers KubeJS Arsenal）：General 全部字段、头像裁剪确认、自动 Next、Description 填写通过；Project License 改为按标签匹配后，Project distribution 待下次实测。

## 失败排查

- 先看控制台表格的「说明」列：当前步骤没有该字段、可见选项列表、控件类型。
- 仍不清楚时，在失败的步骤运行 [dom_probe.js](../../scripts/cf-create-fill/dom_probe.js)，它只读页面结构并把结果复制到剪贴板，按实际结构调整。
- 名称已等于目标名称时视为已运行过，跳过图标上传，避免重复弹出裁剪框。
