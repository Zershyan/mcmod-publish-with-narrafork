---
name: mcmod-publish-with-narrafork
description: 把 Minecraft 模组发布到 CurseForge 与 MC百科。读工程事实、判断项目是否已存在、上传 JAR、填写百科条目与资料、处理登录与验证码、核对审核附言。用户要求发布模组、上传版本、更新百科、补资料或处理退回时使用；不用于模组代码开发。
---

# 模组发布

一条流水线，两种渠道：CurseForge 必发，MC百科可选。所有信息从工程里读，读不到的才问用户。

本文是操作手册，按顺序执行。每步都写了「怎么判断」和「失败怎么办」。

## 开始前：确认三个前置

按顺序检查，缺哪个补哪个，不要跳过。

**1. 工作目录是模组工程**

```bash
ls gradle.properties build.gradle
```

两个都不在就停下来问用户工程路径，不要在错误的目录里继续。

**2. CurseForge 令牌**

```bash
python scripts/cf/upload.py query .narrafork/tmp 2>&1 | head -3
```

看到 `Versions HTTP 200` 说明可用。报 `缺少 CURSEFORGE_API_TOKEN` 就停下来：

> 需要 CurseForge API Token 才能上传。去 https://authors.curseforge.com/#/settings/api-tokens 生成（只显示一次，当场复制），然后设置环境变量 `CURSEFORGE_API_TOKEN`。设好后告诉我。

用交互式提问等用户回复，**不要自己去找令牌**。

**3. Python 运行时依赖**

```bash
python -c "import sys; sys.path.insert(0,'.narrafork/pylibs'); import curl_cffi; print('ok')"
```

报错就装：

```bash
python -m pip install --target .narrafork/pylibs curl_cffi websocket-client
```

之后所有脚本都要带 `CF_HTTP_RUNTIME` 和 `PYTHONPATH` 指向这个目录。

---

## 第 1 步：读工程事实

从工程文件读，不猜。字段对应见 [字段来源](references/field-sources.md)。

```bash
cat gradle.properties
grep -nE "^version|archivesName|toolchain|JavaLanguageVersion|id 'net\." build.gradle
git branch -a
git remote -v
ls src/main/resources/logo.png
```

要拿到：modid、英文名、版本号、MC 版本、加载器、Java 版本、许可证、作者、简介、JAR 路径规则、语言文件位置。

多分支工程**逐个分支读**，版本号规则可能不一样。

读完汇报一张表，缺的标出来。工程里永远拿不到的只有四类：**中文名、CF 分类、百科模组元素、百科作者名**。

## 第 2 步：判断走哪条路

```bash
cat curseforge/project.json 2>/dev/null || echo "无记录"
```

| 情况 | 走法 |
|---|---|
| 有 `project.json` | 直接用里面的 `projectId` / `slug`，跳到第 3 步 |
| 没有记录 | 问用户：「这个模组在 CurseForge 上有现成项目吗？」 |
| 用户回答没有 | 先建项目（见 [建项目](references/curseforge.md#项目创建)），再继续 |
| 用户回答有 | 要项目页地址，从地址取 slug，从页面上抄 Project ID，写进 `project.json` |

**不要自己去 CurseForge 搜项目**——项目页被 Cloudflare 挡着，抓不到。

建项目之前必须单独问一次项目名、分类、许可证，拿到同意再动手。「发个版本」不等于「同意新建项目」。

## 第 3 步：拉版本标签

```bash
python scripts/cf/upload.py query curseforge
```

结果在 `curseforge/game-versions.json`。里面的 `name` 就是后面 `gameVersions` 能用的值，`1.21.1` 和 `1.21.11` 是两个东西。

## 第 4 步：出配置表单让用户确认

不要逐条追问，一次性给全：

```bash
mkdir -p .narrafork/gen_ui/publish
cp assets/form-full/App.tsx .narrafork/gen_ui/publish/App.tsx
cp assets/form-full/data.example.ts .narrafork/gen_ui/publish/data.ts
```

改 `.narrafork/gen_ui/publish/data.ts`，把第 1 步拿到的事实填进 `defaults`（作为 placeholder）和 `versions`。

然后 `GenUI show .narrafork/gen_ui/publish`。

表单是数据驱动的，**只改 `data.ts`，不要改 `App.tsx`**。字段说明见 [form-full](assets/form-full/README.md)。

用户提交后，把结果落成：

```
curseforge/release-manifest.json   CF 上传清单
docs/mcmod/mod-config.json         百科提交配置
```

已有项目只发新版本时，改用更短的 `assets/form-release/`。

## 第 5 步：上传到 CurseForge

版本多、或第一次发布时，先用 `assets/form-confirm/` 把将要上传的内容整块给用户确认一遍。只有一个版本且用户刚在 form-release 里确认过可以跳过。

```bash
python scripts/cf/upload.py upload curseforge/release-manifest.json \
  --project-id <ID> --slug <slug>
```

脚本会自动做三层去重（本地结果 → 线上文件列表 → 遗留的 attempt 记录），命中就跳过。

想看线上已有哪些文件：

```bash
python scripts/cf/upload.py list curseforge --project-id <ID>
```

**返回文件 ID 只代表上传被受理**，不是过审。汇报时说「已受理」并附链接，不要承诺审核耗时。

## 第 6 步：发布到 MC百科（用户勾选才做）

### 6.1 拿 cookie

```bash
ls .narrafork/mcmod-cookie.txt
```

文件在就跳到 6.2。不在，按下面顺序试：

**A. 有 `Browser` 工具时**——launch 一个可见会话打开百科登录页，让用户用 QQ 扫码或账号密码登录，然后从浏览器进程读 cookie：

```bash
python scripts/mcmod/cookies.py dump --profile <profile目录> --out .narrafork/mcmod-cookie.txt
```

profile 目录里有 `DevToolsActivePort` 文件，形如 `%TEMP%\puppeteer_dev_chrome_profile-*`。找不到就用 `ls -d "$TEMP"/puppeteer_dev_chrome_profile-*` 列一下。

**B. 没有 `Browser` 工具，也不想在本地留 cookie**——用控制台脚本兜底：

```bash
python scripts/mcmod/console.py docs/mcmod/mod-config.json
```

生成的 JS 在百科页面里运行，浏览器自带登录态和验证码，不需要导出 cookie。用户先填好验证码再 F12 粘贴运行。详见 [mcmod](references/mcmod.md#兜底控制台脚本)。

**C. 都不行**——让用户从 F12 的 Network 里复制 `Cookie` 请求头，用交互式提问收过来。**不要用 `document.cookie`**，那个拿不到 httpOnly 的登录凭证。

拿到后验证：

```bash
python scripts/mcmod/submit.py docs/mcmod/mod-config.json --dry-run
```

能打印出 JSON 就说明 cookie 有效。

### 6.2 判断百科是否已有条目

问用户，或看他给的项目地址。已有条目时**先对比差异**再决定改什么，不要整条重提。

### 6.3 提交（需要验证码）

百科提交要图形验证码，纯脚本也躲不过。

```bash
# 第一步：取一张验证码，同时把版本映射缓存下来
python scripts/mcmod/submit.py docs/mcmod/mod-config.json --captcha-url
```

把 `.narrafork/mcmod-captcha.png` 给用户看，**用交互式提问索要验证码**，不要发一条普通消息等回复。拿到字符后立刻提交：

```bash
python scripts/mcmod/submit.py docs/mcmod/mod-config.json --captcha <字符>
```

验证码每次请求都会刷新，**取图和提交之间不要再去请求添加页**，所以版本映射走缓存。

成功返回 `{"state": 0, "url": "/verify.html?..."}`。**返回的 url 是审核列表，不是条目地址。**

### 6.4 资料条目（可选）

模组条目建好后，按物品、方块、生物等提交资料。配置写 `"kind": "item"`，流程同上，验证码换成 `item_add_<模组ID>`。字段、分类与再编辑见 [mcmod](references/mcmod.md#资料条目)。

改已有资料时带 `redo-id=<资料ID>`，提交会**替换**原条目而不是新建。

## 第 7 步：核对审核

用户把退回附言贴过来，按资料 ID 找到条目再改：

```
已通过再编辑  /item/edit/<资料ID>/
待审再编辑    /item/add/<模组ID>-<资料ID>/
审核列表      https://www.mcmod.cn/verify.html?order=createtime&selfonly=1
```

常见退回原因见 [mcmod](references/mcmod.md#审核)。

---

## 汇报必须带审核链接

每次发布结束，汇报里都要附上可以点进去看进度的链接，不能让用户自己去找。

| 渠道 | 链接 |
|---|---|
| CurseForge 公开文件列表 | `https://www.curseforge.com/minecraft/mc-mods/<slug>/files` |
| CurseForge 作者后台 | `https://authors.curseforge.com/#/projects/<projectId>/files` |
| MC百科审核列表 | `https://www.mcmod.cn/verify.html?order=createtime&selfonly=1` |

两点必须说清楚：

- **CurseForge**：审核中的文件不会出现在公开列表里，要从作者后台看。拿到文件 ID 只代表受理，不是过审。
- **MC百科**：条目在审核列表里能看到状态和退回附言。通过之前，模组页上的资料数量不会变。

## 什么时候该停下来问

只在这几种情况停，其余自己往下走：

- 缺令牌、缺 cookie，且所有回退路径都不可用
- 需要新建 CF 项目
- 四类工程里读不到的信息
- 需要验证码或登录凭据
- 线上已有同名条目但内容不同
- 某个「MC 版本 × 加载器」组合找不到对应 JAR

**凡是需要用户输入的内容（验证码、令牌、cookie、作者名），一律用交互式提问，不要发普通消息等对方回复。**

## 参考

| 文档 | 什么时候看 |
|---|---|
| [完整流程](references/workflow.md) | 想看七个步骤的完整判定与产物 |
| [CurseForge](references/curseforge.md) | 令牌、上传、依赖、版本标签、状态语义 |
| [MC百科](references/mcmod.md) | 登录、提交接口、字段结构、枚举、审核 |
| [字段来源](references/field-sources.md) | 某个字段该从哪取 |
| [踩坑记录](references/pitfalls.md) | 报错或行为不符预期时先查这里 |
| [form-full](assets/form-full/README.md) | 首次发布的完整表单怎么用 |
| [form-release](assets/form-release/README.md) | 只发新版本的简化表单怎么用 |
| [form-confirm](assets/form-confirm/README.md) | 提交前确认表单怎么用 |
