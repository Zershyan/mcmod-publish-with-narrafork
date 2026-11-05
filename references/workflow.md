# 完整流程

七个步骤，每一步都写了判定条件、动作、产物和失败处理。SKILL.md 是执行顺序，这里是细节。

## 1. 读工程事实

**动作**

```bash
cat gradle.properties
grep -nE "^version|archivesName|toolchain|JavaLanguageVersion|id 'net\." build.gradle
git branch -a && git remote -v
ls src/main/resources/logo.png
```

**要拿到**：modid、英文名、版本号、MC 版本、加载器、Java 版本、许可证、作者、简介、JAR 命名规则、语言文件位置。

**多分支工程逐个分支读**。`version` 的计算方式可能完全不同：

- `${mod_version}-${minecraft_version}+build.${n}` → `2.0.0-1.21.1+build.44`
- 直接 `version = mod_version` → `1.20.1-1.0.1`

**产物**：一张事实表，汇报给用户，缺的标出来。

## 2. 判断走哪条路

**动作**

```bash
cat curseforge/project.json 2>/dev/null
```

| 结果 | 下一步 |
|---|---|
| 有文件 | 用里面的 `projectId` 和 `slug`，跳到第 3 步 |
| 没有 | 问用户「这个模组在 CurseForge 上有现成项目吗」 |
| 用户说没有 | 走建项目流程（第 5.1 步） |
| 用户说有 | 要项目页地址：slug 从地址取，Project ID 从页面抄 |

**不要把「发布」当成「同意建项目」**。建项目是独立授权，动手前单独问一次项目名、分类、许可证。

**产物**：`curseforge/project.json`

```json
{ "projectId": "1234567", "slug": "my-mod" }
```

## 3. 拉版本标签

```bash
python scripts/cf/upload.py query curseforge
```

**产物**：`curseforge/game-versions.json`

拿不到（没令牌）就跳过，并告诉用户版本标签尚未校验。

## 4. 出配置表单

按场景选模板：

| 场景 | 模板 |
|---|---|
| 第一次发布，要给 CF 和百科建全部信息 | `assets/form-full/` |
| 已有项目，只发新版本 | `assets/form-release/` |

```bash
mkdir -p .narrafork/gen_ui/publish
cp assets/form-full/App.tsx .narrafork/gen_ui/publish/App.tsx
cp assets/form-full/data.example.ts .narrafork/gen_ui/publish/data.ts
```

改 `data.ts`，GenUI show 该目录。**只改 data.ts，不动 App.tsx**。

**产物**：

```
curseforge/release-manifest.json   每个「MC 版本 × 加载器」一条
docs/mcmod/mod-config.json         百科提交配置
```

## 5. CurseForge

### 5.1 建项目（仅在需要时）

```bash
python scripts/cf/create_project.py curseforge/cf_create_project.json
node --check curseforge/cf_create_project_fill.js
powershell -NoProfile -Command "Get-Content -Raw -Encoding UTF8 'curseforge/cf_create_project_fill.js' | Set-Clipboard"
```

用户在 Create A Project 页面 F12 粘贴运行。**界面必须切英文、关闭浏览器翻译**。

`autoCreate` 默认 true，脚本会自己点创建并读回 `projectId`/`slug`。启用前必须单独确认一次。

失败时跑 `scripts/cf/dom_probe.js` 抓页面结构再改模板。

### 5.2 确认（建议）

版本多或第一次发布时，用 `assets/form-confirm/` 把将要上传的内容整块给用户看一遍。

### 5.3 上传

```bash
python scripts/cf/upload.py upload curseforge/release-manifest.json \
  --project-id <ID> --slug <slug>
```

脚本自动三层去重：本地 `upload-result-*.json` → 线上文件列表按 displayName → 遗留的 `upload-attempt-*.json` 拒绝重传。

**产物**：`curseforge/upload-result-<版本>.json`（含文件 ID 和链接）

返回文件 ID 只代表受理，不是过审。

## 6. MC百科（用户勾选才做）

### 6.1 拿 cookie

```bash
ls .narrafork/mcmod-cookie.txt
```

按顺序回退：

| 条件 | 做法 |
|---|---|
| 有 `Browser` 工具 | launch 可见会话 → 用户登录 → `cookies.py dump` |
| 没有 `Browser`、或不想留 cookie | `console.py` 生成控制台脚本，用户在页面填好验证码后 F12 运行 |
| 都不行 | 让用户从 F12 的 Network 复制 `Cookie` 请求头，交互式提问收过来 |

**验证码**：百科登录页有图形验证码，账号密码纯脚本走不通；QQ 登录必须人工扫码。两种都要用户参与。

已有 cookie 时验证一下：

```bash
python scripts/mcmod/submit.py docs/mcmod/mod-config.json --dry-run
```

能打印 JSON 就有效。

### 6.2 判断百科是否已有条目

已有条目时**不要整条重提**，先对比：

| 对比项 | 变化时怎么办 |
|---|---|
| 名称、简介、元素 | 走再编辑 |
| 支持版本 / 运作方式 | 更新版本组合 |
| 作者、链接、许可证 | 按实际改 |
| 正文 | 有实质改动才改 |
| 资料条目数量 | 新增物品才补条目 |

没有条目就直接新建。

### 6.3 提交

需要验证码，取图和提交必须连着做：

```bash
python scripts/mcmod/submit.py docs/mcmod/mod-config.json --captcha-url
# 把 .narrafork/mcmod-captcha.png 给用户看
python scripts/mcmod/submit.py docs/mcmod/mod-config.json --captcha <字符>
```

验证码每次请求都刷新，中间不要请求添加页（脚本已用缓存规避）。

**产物**：提交成功后从审核列表取到条目或资料 ID，记进 `docs/mcmod/entries.json`，后续再编辑要用。

### 6.4 资料条目（可选）

模组条目建好后，按物品、方块、生物等逐个提交资料。配置里写 `"kind": "item"`，其余流程与上面一致，验证码 id 换成 `item_add_<模组ID>`。字段与分类见 [MC百科](mcmod.md#资料条目)。

颜色变体、成套装备这类，先看 [正文模板](../assets/content-templates.md) 和 [MC百科](mcmod.md#审核) 里的退回原因，别一次全提。

## 7. 核对审核

发布完成后，汇报里必须附上下面这些链接：

```
CurseForge 公开列表  https://www.curseforge.com/minecraft/mc-mods/<slug>/files
CurseForge 作者后台  https://authors.curseforge.com/#/projects/<projectId>/files
MC百科审核列表       https://www.mcmod.cn/verify.html?order=createtime&selfonly=1
已通过再编辑         /item/edit/<资料ID>/
待审再编辑           /item/add/<模组ID>-<资料ID>/
```

CF 的文件在审核中不会出现在公开列表，要看作者后台。百科条目在审核列表里能看到状态和退回附言。

用户把退回附言贴过来，按资料 ID 定位条目再改。常见退回原因见 [MC百科](mcmod.md#审核)。

## 数据在步骤之间怎么传

```
curseforge/project.json          projectId + slug
curseforge/game-versions.json    版本标签
curseforge/release-manifest.json 上传清单
curseforge/upload-result-*.json  文件 ID 与链接
docs/mcmod/mod-config.json       百科提交配置
docs/mcmod/entries.json          条目 ID 映射
.narrafork/mcmod-cookie.txt      百科登录态
.narrafork/mcmod-mcversions.json 版本 ID 缓存
```

## 中途停下来问用户的情况

- 缺令牌、缺 cookie，且所有回退都不可用
- 需要新建 CF 项目
- 四类工程里读不到的信息（中文名、CF 分类、百科元素、百科作者名）
- 线上已有同名条目但内容不同
- 某个「MC 版本 × 加载器」找不到对应 JAR

其余情况自己往下走。
