---
name: mcmod-publish-with-narrafork
description: 把 Minecraft 模组发布到 CurseForge 与 MC百科。读工程事实、判断项目是否已存在、上传 JAR、填写百科条目与资料、处理登录与验证码、核对审核附言。用户要求发布模组、上传版本、更新百科、补资料或处理退回时使用；不用于模组代码开发。
---

# 模组发布

一条流水线：CurseForge 必发，MC百科可选。信息从工程读，读不到的才问用户。

每步都是**跑 → 看 → 过**三段。照着做，不需要自己判断走哪条分支。

## 开局：一条命令拿到全部状态

```bash
python scripts/preflight.py
```

它一次给出工程事实、构建规范、可用凭据、已有记录，末尾列出「下一步」。**按那个顺序做，做完再跑一次，直到没有 ✗。**

三条规则覆盖所有分支，不用再判断：

| 情况 | 做法 |
|---|---|
| 输出「构建规范 符合」 | 只上传不带 `+build.N` 的 jar；不符合就按 `build.gradle` 的实际产物命名 |
| 要出表单 | 有 GenUI 就 `render({path, wait: true})`；没有或调用失败就**逐项询问**，不要停 |
| 缺令牌 / 依赖 / cookie | 见 preflight 的「下一步」，逐条补 |

**没有 GenUI 不要停**：直接降级成逐项询问——有交互式提问就按表单字段分组问，每次不超过 4 项；连提问工具都没有，就用普通消息把问题列成清单让用户一次回完。这条让 skill 不依赖 NarraFork 也能跑，只是慢一点。

有 GenUI 时一律 `render` 带 `wait: true`：**`show` 不支持 `wait`**，画完就能接着跑，流程里不要用。

## 第 1 步：版本与构建（装了 style skill 才有这一步）

省掉判断：preflight 输出「构建规范 符合」就走这段，否则跳到第 2 步。

```bash
git branch -a | sed 's|remotes/origin/||;s|^[* ]*||' | sort -u
```

用 `assets/forms/FormBuild.tsx` 出表单，让用户逐行填分支和 `mod_version`：

```bash
mkdir -p .narrafork/gen_ui/build
cp assets/forms/FormBuild.tsx .narrafork/gen_ui/build/App.tsx
cp assets/forms/FormBuild.data.example.ts .narrafork/gen_ui/build/data.ts
# 改 data.ts 的 branches / rows，然后
# GenUI render({path: '.narrafork/gen_ui/build', wait: true})
```

拿到提交结果（`JSON.parse(values.payload)`）后再动手：

- 勾了「回填至项目」→ `python scripts/project/version.py main=0.0.1 1.20.1=0.0.1 --commit`。**多分支必须加 `--commit`**：git 不允许带着未提交的 `gradle.properties` 切分支，不提交就只有第一个分支改得动
- **自己跑 `./gradlew build`**，绝不跑 `buildAlpha`（后者递增编号并回写属性，属开发动作）
- 构建失败就如实报告停下，不要改用 `buildAlpha` 绕过

多分支工程逐个分支读、逐个构建，`mod_version` 与 `minecraft_version` 可能不一样。

## 第 2 步：项目存不存在

```bash
cat curseforge/project.json 2>/dev/null || echo "无记录"
```

| 结果 | 做法 |
|---|---|
| 有记录 | 直接用里面的 `projectId` / `slug`，跳到第 3 步 |
| 无记录 | 问用户「这个模组在 CurseForge 上有现成项目吗？」 |
| 用户说没有 | **记成「待建」，先不动手**，项目名/分类/许可证由第 4 步表单收集，第 5 步确认后再建 |
| 用户说有 | 要项目页地址：从地址取 slug，从页面抄 Project ID，写进 `project.json` |

**不要自己去 CurseForge 搜项目**，公开页有 Cloudflare 人机校验。

建项目是唯一不可逆的动作，所以它排在第 5 步 `FormConfirm` 之后：用户确认清单时才一并授权。脚本优先用 browsermcp 在用户已登录的 Chrome 里跑，没有 MCP 才回落人工粘贴。

## 第 3 步：版本标签

```bash
python scripts/cf/upload.py query curseforge
```

产物 `curseforge/game-versions.json`。manifest 的 `gameVersions` **写名称**（`"1.20.1"`），`upload.py` 上传前自己换成整型 ID——照抄 `name`，别编 ID，`1.21.1` 和 `1.21.11` 是两个东西。

## 第 4 步：出配置表单

一次问全，不要逐条追问：

```bash
mkdir -p .narrafork/gen_ui/publish
cp assets/forms/FormFull.tsx .narrafork/gen_ui/publish/App.tsx
cp assets/forms/FormFull.data.example.ts .narrafork/gen_ui/publish/data.ts
# 改 data.ts：defaults 填第 1 步的事实作为 placeholder，versions 填版本条目
# GenUI render({path: '.narrafork/gen_ui/publish', wait: true})
```

- **只改 `data.ts`，不动 `App.tsx`**（GenUI 只认这个文件名）
- 已有项目只发新版本时改用 `assets/forms/FormRelease.tsx`
- 字段说明见 [表单模板](assets/forms/README.md)

### 占位图标

工程没有图标时用它，样式可以在表单面板里调：

1. 出表单前先读 skill 的 `.narrafork/icon-style.json`，有内容就填进 `data.ts` 的 `iconStyle`
2. 用户在图标那行点「编辑样式」打开面板：左侧实时预览，右侧两行文本、两行排版开关、字体（Segoe UI / Arial / Calibri / Impact / Bahnschrift / Georgia / Consolas）、字号、行距、字距、对齐、全部大写、边框、导出尺寸、文字色与背景色
3. 用户点「保存为默认」会发来一条 `保存图标样式：{…}`，把里面的 JSON 写回 `.narrafork/icon-style.json`，下次发布其他模组直接复用
4. 提交结果里带 `cfAutoIcon` 与 `cfIconStyle`，勾着且工程确实没有图标时生成 PNG：

```bash
python scripts/project/make_icon.py <模组英文名> --out src/main/resources/logo.png
```

样式文件会被自动读取；要临时覆盖就加 `--font georgiab.ttf --font-size 56 --fg "#3b1f0e"` 这类参数，加 `--save-style` 则一并写回配置。多行用 `--lines "Forge|Attachment"`。

没收到提交结果（超时、被中断、用户关掉）＝还没确认：不构建、不上传、不提交百科，也不要发普通消息问一遍来代替等待。

### 提交结果怎么变成清单

表单返回 `{"payload": "<JSON 字符串>"}`，还原后存成 `.narrafork/gen_ui/publish/payload.json`。

里面 `changed` **只装用户改过的字段**，没改的沿用 `data.ts` 里的默认值——把两者合并成完整配置再往下走。不整份回传是因为工具显示层会截断长内容，几千字的描述一塞进去，后面的字段就看不见了。

```bash
python scripts/cf/make_manifest.py .narrafork/gen_ui/publish/payload.json \
  --out curseforge/release-manifest.json
```

它按工程实际情况挑包、算 sha256、拼 `displayName`（= jar 文件名去掉 `.jar`）与 `gameVersions`。**不要手写 manifest**。

## 第 5 步：确认，然后建项目、上传

**先过 `FormConfirm`**——它是整个流程唯一的确认点。清单里要有项目名、分类、许可证、项目是否待建、每个要上传的文件：

```bash
mkdir -p .narrafork/gen_ui/confirm
cp assets/forms/FormConfirm.tsx .narrafork/gen_ui/confirm/App.tsx
cp assets/forms/FormConfirm.data.example.ts .narrafork/gen_ui/confirm/data.ts
# 改 data.ts 后
# GenUI render({path: '.narrafork/gen_ui/confirm', wait: true})
```

用户提交后才动手，顺序固定：

1. `project.json` 不存在 → 按 [建项目](references/curseforge.md#项目创建) 建，拿到 `projectId` / `slug`
2. 上传：

```bash
python scripts/cf/upload.py upload curseforge/release-manifest.json \
  --project-id <ID> --slug <slug>
```

- 自动三层去重：本地结果 → 线上列表 → 遗留 attempt 记录，命中就跳过
- 上传被拒会直接打印 `errorMessage` 并清掉 attempt，修好后可以立刻重传
- 想看线上已有文件：`python scripts/cf/upload.py list curseforge --project-id <ID>`（这个端点可能被 Cloudflare 挡，失败不影响上传）

**返回文件 ID 只代表受理，不是过审。**汇报时说「已受理」，不要承诺审核耗时。

## 第 6 步：MC百科（用户要发才做）

### 6.1 选提交通道

```bash
ls .narrafork/mcmod-cookie.txt
```

有 cookie → 走 6.3 的 `submit.py` 流程。

没有 cookie → 按顺序选通道，**前面的能用就不要往下走**：

| 顺序 | 条件 | 做法 |
|---|---|---|
| 1 | 有 browsermcp | 打开百科确认已登录（没登录就让用户登），`console.py` 生成脚本后 `eval` 执行——浏览器自带登录态，不需要 cookie |
| 2 | 有 `Browser` 工具 | 起可见会话让用户登录，再 `python scripts/mcmod/cookies.py dump --profile <目录> --out .narrafork/mcmod-cookie.txt`，之后走 `submit.py` |
| 3 | 都没有 | `console.py` 生成脚本，用户自己在百科页面 F12 粘贴运行 |

第 3 层也可以让用户从 F12 的 Network 复制 `Cookie` 请求头交过来，写进 `.narrafork/mcmod-cookie.txt` 后走 `submit.py`。**不要用 `document.cookie`**，拿不到 httpOnly 凭证。

拿到 cookie 时验证一下：`python scripts/mcmod/submit.py docs/mcmod/mod-config.json --dry-run` 能打印 JSON 就是有效。

### 6.2 有没有现成条目

问用户或看他给的项目地址。已有条目**先对比差异**再改，不要整条重提。

### 6.3 提交（要验证码）

**有 cookie 时**走 `submit.py` 本地提交：

```bash
python scripts/mcmod/submit.py docs/mcmod/mod-config.json --captcha-url
```

把 `.narrafork/mcmod-captcha.png`（同时出 4 倍放大图 `mcmod-captcha-4x.png`）给用户看，**用交互式提问索要验证码**，拿到后立刻：

```bash
python scripts/mcmod/submit.py docs/mcmod/mod-config.json --captcha <字符>
```

验证码每次请求都刷新，取图和提交之间不要再请求添加页，版本映射走缓存。

**没 cookie 时**走控制台脚本：验证码由用户直接在页面上填，不用取图也不用问。

两种方式的成功标志都是 `{"state": 0, "url": "/verify.html?..."}`——**这个 url 是审核列表，不是条目地址**。

### 6.4 资料条目（可选）

配置写 `"kind": "item"`，验证码换成 `item_add_<模组ID>`。改已有资料带 `redo-id=<资料ID>`，会**替换**而不是新建。字段与正文见 [mcmod](references/mcmod.md#资料条目)、[正文模板](assets/content-templates.md)。

## 第 7 步：核对审核

用户把退回附言贴过来，按资料 ID 找到条目再改：

```
已通过再编辑  /item/edit/<资料ID>/
待审再编辑    /item/add/<模组ID>-<资料ID>/
审核列表      https://www.mcmod.cn/verify.html?order=createtime&selfonly=1
```

常见退回原因见 [mcmod](references/mcmod.md#审核)。

## 汇报必须带三条链接

每次结束都附上，不让用户自己找：

| 渠道 | 链接 |
|---|---|
| CurseForge 公开文件列表 | `https://www.curseforge.com/minecraft/mc-mods/<slug>/files` |
| CurseForge 作者后台 | `https://authors.curseforge.com/#/projects/<projectId>/files` |
| MC百科审核列表 | `https://www.mcmod.cn/verify.html?order=createtime&selfonly=1` |

- **CurseForge**：审核中的文件不在公开列表，要从作者后台看；文件 ID 只代表受理
- **MC百科**：条目在审核列表里能看到状态和退回附言

## 什么时候停下来问

只有这几种情况停，其余自己往下走：

- preflight 里的 ✗ 补不上（令牌、依赖、cookie）
- 工程里读不到的四类信息：中文名、CF 分类、百科模组元素、百科作者名（能放进表单的一律放进表单问）
- 需要验证码或登录凭据
- 线上已有同名条目但内容不同
- 某个「MC 版本 × 加载器」组合找不到 JAR

**需要用户输入的一律用交互式提问**，不要发普通消息等回复。

## 参考

| 文档 | 什么时候看 |
|---|---|
| [完整流程](references/workflow.md) | 想看七步的完整判定与产物 |
| [CurseForge](references/curseforge.md) | 令牌、建项目、上传、依赖、版本标签、状态语义 |
| [MC百科](references/mcmod.md) | 登录、提交接口、字段结构、枚举、审核 |
| [字段来源](references/field-sources.md) | 某个字段该从哪取 |
| [踩坑记录](references/pitfalls.md) | 报错或行为不符预期时先查这里 |
| [与 zershyan-mcmod-style 同装时](references/with-mcmod-style.md) | 工程符合 style 规范时的产物、版本与资源约定 |
| [表单模板](assets/forms/README.md) | 四个 GenUI 表单的用途与数据格式 |
