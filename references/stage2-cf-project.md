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

用户在 Create A Project 的 General 页按 F12 粘贴运行。脚本按 `create/general` → `create/description` → `create/license` 逐步填写并点 Next，有字段没填上就停在当前步骤。

**界面必须是英文，并关闭 Edge 网页翻译**——翻译后标签变中文，所有字段都匹配不到。

### 自动创建

默认开启（`"autoCreate": true`）。脚本填完最后一步会自己点创建按钮，并打印创建后的 URL、slug，以及从页面读到的 Project ID。

**开启自动创建时，必须在生成脚本之前用交互式提问向用户申请一次**，说明将要创建的项目名、分类、许可证，得到明确同意后再继续。这是必需步骤，不能因为"用户已经说要发布"就跳过——发布和新建项目是两个授权。

用户不同意自动创建时，把配置改成 `"autoCreate": false`，脚本会停在最后一步等人点。

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

建完项目把标识写进 `curseforge/project.json`：

```json
{ "projectId": "1757115", "slug": "caged-mobs-reborn" }
```

阶段 3、4 都从这里读；第二次发布就不用再问。开了 `autoCreate` 时脚本会打印这两个值。

## 项目已存在时

不用再建，但上传仍需要 `projectId`。按顺序找：

1. 工程里的 `curseforge/project.json`。
2. `curseforge/` 下的 `release-manifest.json`、`upload-result-*.json`，或 README 里记过的地址。
3. 用户提供的项目页地址——slug 就在地址里（`.../mc-mods/<slug>`），Project ID 在页面上显示。
4. **不要尝试自动抓取**：项目页和 `curseforge.com/api/v1/mods/search` 都被 Cloudflare 挡住，`curl_cffi` 指纹同样返回 403。直接问用户，别在这个方向反复试。

slug 能从地址看出，projectId 不能，必须问用户或读页面。拿到后立刻写进 `curseforge/project.json`，下次直接读。
