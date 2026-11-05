# 踩坑记录

都是实际遇到并修过的。每条写清症状、原因、正确做法。

## 网络与凭据

### CF 请求返回 `Just a moment...`

**症状**：`curl`、PowerShell、Python `urllib` 请求 `minecraft.curseforge.com/api/...` 拿到 HTML 而不是 JSON，解析报错；换代理返回 000。

**原因**：Cloudflare 按 TLS/HTTP2 指纹识别非浏览器客户端，与令牌无关。

**做法**：只用 `curl_cffi` 的 `impersonate='chrome'`，即 `scripts/cf/cfhttp.py`。不涉及破解验证码，只改网络层特征。

### 拿 Studio 令牌查项目，返回 403

**症状**：用 `CURSEFORGE_API_TOKEN` 当 `x-api-key` 调 `api.curseforge.com/v1/mods/search`，返回 `{"errorCode":403,"errorMessage":"API Key missing or invalid"}`。

**原因**：这是两种凭据。Studio 令牌只能拉 Game Versions 和上传文件。

**做法**：要按名字查项目，得去 `console.curseforge.com` 申请 API Key。否则只能问用户或读 `curseforge/project.json`。

### CF 项目页抓不到

**症状**：`Browser` 打开项目页是 `Just a moment...`；`curl_cffi` 也 403。

**原因**：公开页面和网页内部 API 的防护比 Studio API 更严。

**做法**：不要在这个方向反复试。项目标识只能来自本地记录或用户。**但**文件列表例外：`GET https://www.curseforge.com/api/v1/mods/{id}/files` 免令牌可用。

### `setx` 设的环境变量读不到

**症状**：`setx CURSEFORGE_API_TOKEN` 之后，脚本仍报 `Missing CURSEFORGE_API_TOKEN`。

**原因**：已经运行的进程不会继承新设的环境变量。

**做法**：脚本里加了回退——环境变量读不到时从 `HKCU\Environment` 读。见 `scripts/cf/cfhttp.py` 的 `system_env()`。

### 上传到一半断了，重跑又传了一次

**症状**：线上出现两个同名文件。

**原因**：请求发出但没收到响应，本地没记下结果。

**做法**：上传前先写 `upload-attempt-<版本>.json`，成功后写 `upload-result-<版本>.json`。有 attempt 没 result 就拒绝重传，要求先核对线上。

## CurseForge

### 版本名格式搞错

**症状**：CF 上显示成 `1.21.1-NeoForge-模组名-0.0.1`，和工程里的版本对不上。

**原因**：按「MC-加载器-名字-版本」自己拼了。

**做法**：`displayName` 用工程 `version` 原值。不同分支规则可能不同（`2.0.0-1.21.1+build.44` vs `1.20.1-1.0.1`），逐个分支读。

### JAR 路径猜错

**症状**：找不到构建产物。

**原因**：以为文件名一定是 `${mod_id}-${version}.jar`。

**做法**：看 `build.gradle` 的 `base { archivesName }`。配了 `archivesName = mod_id` 时产物前缀是 modid（`adcore-…`），没配时用工程目录名。

### 拿 alpha 包去发布

**症状**：CurseForge 上的文件名带 `+build.5` 这类后缀，或者和同版本线的其他产物对不上。

**原因**：`build/libs` 里同时躺着普通 `build` 和 `buildAlpha` 的产物，选错了。`zershyan-mcmod-style` 规范里，带 `+build.<N>` 的是 alpha 测试构建。

**做法**：**禁止上传任何文件名带 `+build.N` 的 jar**，没有例外。挑了也不许，只剩这种包的分支直接停下报告，等正式构建完成再来。候选里都没编号时按版本号取最新。

### 依赖漏声明

**症状**：CF 上玩家装了模组但缺前置报错。

**原因**：只看 `jarJar`（内嵌，不用声明），忽略了 `localImpl` 的外部依赖。

**做法**：按 `curse.maven:` 坐标提取项目 ID；`jarJar` 和 `localRuntime` 不声明。

## MC百科

### tagsinput 直接改 `value` 不生效

**症状**：`$('#class-modid').val('<你的 modid>')` 之后，页面显示空，提交时 MODID 也是空。

**原因**：`#class-modid`、`#class-cfprojectid`、`#class-mrprojectid`、`#class-tags`、`#class-keys` 是 bootstrap-tagsinput，原 input 被 `display:none`，页面不认直接赋值。

**做法**：`$(el).tagsinput('removeAll'); $(el).tagsinput('add', 值)`。

### 勾选加载器后 MC 版本列表没出现

**症状**：脚本设 `checked = true` 勾了 NeoForge，但页面上的 MC 版本复选框不显示，以为数据没进去。

**原因**：MC 版本 input **一开始就全在 DOM 里**，按加载器分组隐藏。那个「勾选后才出现」只是 UI 显示切换。

**做法**：数据收集不看可见性，直接置 `checked = true` 就能提交。实测：

```json
"mcversion": { "13": { "0": "78" }, "1": { "0": "58" } }
```

走浏览器点击路线时才需要先让它显示。

### 作者搜不到

**症状**：拿一个数字 ID 搜作者，返回 `state: 109` 找不到。

**原因**：用户中心 ID（`center.mcmod.cn/<ID>/`）不是作者 ID，两者不同。搜索框只认名字。

**做法**：用名字搜，从结果行取 `data-id`，那个才是提交用的作者 ID。

### 拿到的 cookie 用不了

**症状**：从 `document.cookie` 复制 cookie，Python 请求添加页还是未登录状态。

**原因**：登录凭证 `dSit_2132_auth` 是 httpOnly，`document.cookie` 读不到。实测页面只有 5 个 cookie，实际有 11 个。

**做法**：用 CDP 的 `Storage.getCookies` 从浏览器进程读，见 `scripts/mcmod/cookies.py`。

### 登录一直失败

**症状**：`doLogin` 返回 `logreg_password_incorrect`，但密码没错。

**原因**：登录页有图形验证码，脚本传了空 `captcha`，服务端校验失败后统一返回密码错误。

**做法**：先拿验证码再登录，或走浏览器人工登录后导 cookie。

### 枚举值写错

**症状**：提交失败或字段变成默认值。

**原因**：凭印象写，没从页面取。

**做法**：全部从页面实测，见 `assets/mcmod-enums.json`。之前写错过 5 处：

| 字段 | 错的 | 对的 |
|---|---|---|
| 官方状态 | 活跃/停更/合并/重制/分割 | 不确定/活跃/半弃坑/停更 |
| 开源状态 | 开源/闭源/部分开源 | 不显示/开源/闭源 |
| 核心元素 | 缺魔改、辅助 | 9 个 |
| 作者职位 | 开发者/音乐/测试/搬运/鸣谢 | 程序/音效/建筑/贡献者/吉祥物/自定义 |
| 许可协议 | 完全没写 | 见下 |

### 许可协议字段找不到

**症状**：抓 `#license-frame` 是空的，没有 `.license-list`。

**原因**：要先点「新建协议组」（`.license-group-add`），再点「[添加]」（`.license-add-button`），结构才出现。

**做法**：两次点击之后才有 `select.license-type-select` 和 `select.license-name-select`。注意 `type` 提交时是**数组**，`name` 是字符串。

### 弹窗挡住操作

**症状**：点不到页面元素。

**原因**：CF 有头像裁剪框；百科有「编辑规范」弹窗。

**做法**：先关掉弹窗，或用 `stopPropagation` 处理。

## 表单 UI

### 同一行的控件对不齐

**症状**：Switch 比旁边的输入框低一截。

**原因**：`TextInput` 只有 label，`Switch` 带 description，两者高度不同，控件起点自然错开。

**做法**：同一行的字段保持相同的描述行数；Switch 用 `Input.Wrapper` 包成和输入框一样的结构，说明文字放到开关右侧。

### Badge 显示成大写

**症状**：`NeoForge 26.1.2` 显示成 `NEOFORGE 26.1.2`。

**原因**：Mantine Badge 默认 `text-transform: uppercase`。

**做法**：加 `tt="none"`。

### 折叠面板初始不展开

**症状**：`Collapse` 设 `in={true}` 但内容不显示。

**原因**：初始渲染时测不到高度。

**做法**：用条件渲染 `{open && (...)}` 代替 Collapse。

## 流程与授权

### 用普通消息索要用户输入

**症状**：发一条「验证码是多少」，然后结束本轮等用户主动回复。

**原因**：把需要用户输入的东西当成普通信息汇报。

**做法**：验证码、令牌、cookie、作者名这类必须由用户提供的内容，一律用交互式提问（AskUserQuestion）发起，而不是口头问完就结束。

### 跨域调接口被拦

**症状**：GenUI 表单里 `fetch('https://www.mcmod.cn/object/CommonSelect/')` 失败。

**原因**：响应头 `access-control-allow-origin: https://www.mcmod.cn`，只放行自家域名。

**做法**：浏览器端调不了。要么先用脚本查好写进 `data.ts`，要么走 Python。

### 本地端口收不到 cookie

**症状**：部署环境下让用户访问 `127.0.0.1:端口`，浏览器报 `ERR_CONNECTION_REFUSED`。

**原因**：NarraFork 跑在服务器上，`127.0.0.1` 指向服务器，用户的浏览器在另一台机器。

**做法**：放弃本地端口方案，用 CDP 从浏览器进程读。

### 把「发版本」当成「同意建项目」

**症状**：用户说「发布一下」，脚本直接把项目建了。

**原因**：混淆了两个授权。

**做法**：新建 CF 项目前必须单独交互式确认一次项目名、分类、许可证。

### 上传成功就汇报「已发布」

**症状**：跟用户说发布成功，实际还在审核。

**原因**：把 HTTP 200 和文件 ID 当成过审。

**做法**：只说「上传已受理」，附文件链接和 ID，不承诺审核耗时。
