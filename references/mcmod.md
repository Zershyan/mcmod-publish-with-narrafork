# MC百科

百科没有公开 API，所有提交都走页面自己的 AJAX 接口。拿到登录 cookie 之后可以完全用脚本，不需要浏览器。

## 登录与凭据

三层回退，从上往下试。

### 第一层：CDP 导出 cookie（首选）

用 `Browser` 工具 launch 一个 headed 会话，让用户在里面登录（QQ 扫码或账号密码），然后从浏览器进程读完整 cookie：

```bash
python scripts/mcmod/cookies.py dump --profile <profile目录> --out .narrafork/mcmod-cookie.txt
```

profile 目录里有 `DevToolsActivePort`，第一行是调试端口。NarraFork 启动的会话 profile 形如 `%TEMP%\puppeteer_dev_chrome_profile-*`。

**为什么不能用 `document.cookie`**：登录凭证 `dSit_2132_auth` 是 httpOnly，页面里读不到。实测 `document.cookie` 只有 5 个，CDP 能拿到 11 个。

### 第二层：控制台脚本

没有 `Browser` 工具，或用户不想登录时，出脚本让用户自己跑。脚本由 `assets/` 下的生成器产，用户在添加页 F12 粘贴。

### 第三层：手动粘贴

用户从浏览器复制 cookie，通过表单交过来。

### 账号密码登录

```
POST https://www.mcmod.cn/action/doLogin/
data={"username":"…","password":"…","remember":1,"captcha":""}
→ {"state":0} 成功
→ {"state":"logreg_password_incorrect"} 失败
```

**登录页有图形验证码**，纯脚本走不通，必须先拿到验证码。QQ 登录是 OAuth 跳转，必须人工扫码。两种情况都要用户参与。

## 提交接口

```
POST https://event.mcmod.cn/action/edit/doEdit/
Content-Type: application/x-www-form-urlencoded
data=<URL 编码的 JSON>

{"state": 0}    成功
{"state": 117}  已登录，数据有问题
{"state": 122}  未登录
```

## 提交结构

```json
{
  "action": "class_add",
  "edit-id": "0",
  "class-id": "0",
  "redo-id": "0",
  "class-data": {
    "name": "主要名称", "ename": "次要名称", "sname": "简写",
    "intro": "一句话简介", "modid": "modid",
    "cfprojectid": "", "mrprojectid": "",
    "content": "<p>[ban:title_menu]</p>…",
    "category":  { "0": "1,7" },
    "platform":  { "0": "1" },
    "api":       { "0": "13" },
    "mcversion": { "13": { "0": "78" } },
    "mode-1":    { "0": "1" },
    "mode-2":    { "0": "1" },
    "status":    { "0": "1" },
    "source":    { "0": "1" },
    "tags":      { "0": "标签" },
    "keys":      { "0": "关键词" },
    "link":   { "0": { "title": "curseforge", "custom": "", "href": "地址", "text": "" } },
    "license": { "0": { "title": "", "list": { "0": { "type": ["source"], "name": "AGPL-3.0", "link": "", "text": "" } } } },
    "author": { "link": { "0": { "select": ["owner"], "id": "<作者ID>" } }, "add": {} }
  }
}
```

类型陷阱：

| 字段 | 类型 |
|---|---|
| `api`、`platform`、`category`、`status`、`source`、`mode-*`、`tags`、`keys` | `{序号: 值}`，序号只是遍历下标，服务端只认值 |
| `mcversion` | `{加载器ID: {序号: 版本ID}}`，两层嵌套 |
| `license.0.list.0.type` | **数组** |
| `license.0.list.0.name` | 字符串 |
| `license.0.title` | 字符串，页面「通用」时提交空串 |
| `author.link.0.select` | **数组** |

## MC 版本怎么选

三组 MC 版本 input 一开始就全在 DOM 里，按加载器分组隐藏：

```
input[name="class-mcversion-1"]    Forge     86 个
input[name="class-mcversion-2"]    Fabric
input[name="class-mcversion-13"]   NeoForge
```

每个 input 的 `value` 是版本 ID，父元素文本是版本号。**数据收集不看可见性**，所以纯脚本置 `checked = true` 即可，不需要触发「勾选加载器后显示」那个联动。

版本 ID 每次可能变，从页面现取：

```
页面里有 var arrMCVer = $.parseJSON('[{"id":"78","name":"26.1.2"}, …]')
```

`scripts/mcmod/submit.py` 会自动解析并映射。

## 枚举

全部在 `assets/mcmod-enums.json`，键是提交值，值是页面文本。

- `platform` 1=JAVA版 2=基岩版
- `api` 1=Forge 2=Fabric 11=Quilt 13=NeoForge 5=数据包 10=其他
- `mode` 0=待考证 1=需装 2=可选 3=无效
- `status` 0=不确定 1=活跃 2=半弃坑 3=停更
- `source` 0=不显示 1=开源 2=闭源
- `category` 核心 9 个 `1,x`，杂项 25 个 `0,x`
- `role` owner/programmer/artist/sound/planner/writer/builder/contributor/mascot/other
- `licenseType` source/asset/artifact/other

## 作者

搜索接口免登录：

```
POST https://www.mcmod.cn/object/CommonSelect/
data={"key":"作者名","type":"author"}
→ {"state":0,"html":"<tr data-id=\"<作者ID>\"><td><b>主要名</b> - <i>别名1 / 别名2</i></td></tr>"}
```

```bash
python scripts/mcmod/author.py <作者名>
```

`state:109` 表示没找到。**搜索框只认名字**，用户中心 ID（`center.mcmod.cn/<ID>/`）不是作者 ID，拿它搜会返回 109。

## 提交

**百科提交需要图形验证码**，纯脚本也躲不过：

```
输入框  #edit-captcha-value
图片    https://www.mcmod.cn/frame/edit/EditCaptcha/?id=class_add_0
```

验证码每次请求都会刷新，所以必须「取图 → 用户识别 → 立刻提交」一气呵成，中间不能再去请求添加页。

```bash
# 1. 取图（同时缓存版本映射，避免提交时再请求添加页）
python scripts/mcmod/submit.py docs/mcmod/mod-config.json --captcha-url

# 2. 把 .narrafork/mcmod-captcha.png 给用户看，拿到字符

# 3. 带验证码提交
python scripts/mcmod/submit.py docs/mcmod/mod-config.json --captcha <字符>
```

没有验证码时可先 `--dry-run` 只看提交体。

配置里写页面上的中文文本，脚本按枚举表转成代码值。`state: 0` 成功并返回条目地址。

**尚未验证的部分**：用错误验证码提交返回的是 `117`（和「数据有问题」同一个码），说明验证码校验在数据校验之后，或者两者混用同一个状态码。所以第一次真提交时如果返回 117，先怀疑数据字段，再怀疑验证码。

## 资料条目

资料条目是另一套页面和字段，地址 `/item/add/<模组ID>/`。结构已摸清，**提交行为尚未实测**。

### 分类

`data-multi-name="item-data"`、`data-multi-id="category"` 的 `a` 元素，`data-multi-value` 取值：

| 值 | 分类 |
|---|---|
| 1 | 物品/方块 |
| 2 | 群系/群落 |
| 3 | 世界/维度 |
| 4 | 生物/实体 |
| 5 | 附魔/魔咒 |
| 6 | BUFF/DEBUFF |
| 7 | 多方块结构 |
| 8 | 自然生成 |
| 9 | 绑定热键 |
| 10 | 游戏设定 |

页面上的 `(数字)` 是该项目已有的资料数量，不是分类编号。

### 字段

提交对象是 `item-data`，键名来自控件的 `data-multi-id`：

| 键 | 对应 |
|---|---|
| `name` | 主要名称 |
| `ename` | 次要名称 |
| `remark` | 改动附言 |
| `category` | 分类，`{序号: 分类值}` |
| `type` | 资料类型（`#item-type-select` 或自定义 `#item-type-custom`） |
| `regname` | 注册名 `modid:path` |
| `damage` | 最大耐久 |
| `maxstack` | 最大堆叠 |
| `oredict` | 矿物词典 |
| `metadata` | 元数据 |
| `icon-32x-data` / `icon-128x-data` | 图标 base64 |
| `cover-data` | 资料封面 |
| `content` | 正文 HTML |
| `tools` | 关联工具，可空 |

### 提交

```json
{
  "action": "item_add",
  "edit-id": "<模组ID>",
  "class-id": "<模组ID>",
  "redo-id": "0",
  "captcha": "…",
  "item-data": { "name": "…", "category": { "0": "1" }, "content": "…" }
}
```

端点与模组条目相同（`event.mcmod.cn/action/edit/doEdit/`）。验证码图片的 `id` 是 `item_add_<模组ID>`，取图 URL：

```
https://www.mcmod.cn/frame/edit/EditCaptcha/?id=item_add_<模组ID>
```

页面上的提交按钮：`#edit-submit-button`，`data-type="item_add"`、`edit-id="<模组ID>"`、`redo-id="0"`。

### 脚本支持

配置里写 `"kind": "item"` 就走资料条目，验证码 id 自动按 `item_add_<模组ID>` 取：

```bash
python scripts/mcmod/submit.py docs/mcmod/item-test.json --dry-run
python scripts/mcmod/submit.py docs/mcmod/item-test.json --captcha-url
python scripts/mcmod/submit.py docs/mcmod/item-test.json --captcha <字符>
```

配置示例：

```json
{
  "kind": "item",
  "classId": "3828",
  "name": "中文名",
  "ename": "English Name",
  "category": "物品/方块",
  "type": "道具",
  "regname": "modid:path",
  "maxstack": "64",
  "damage": "",
  "content": "<p>[ban:title_menu]</p><p>正文</p>"
}
```

`category` 写中文，脚本按 [mcmod-enums.json](../assets/mcmod-enums.json) 的 `itemCategory` 转成数字。

### 还没确认的

- `item-data` 里未列出的键（图标 lock/delete 标记等）在什么场景下需要
- 提交成功后的返回结构（`state: 0` 是否同样带 `url`）
- 批量提交时验证码是否每次都要重新取

第一次真提交时先只发一条，确认返回再批量。

## 审核

```
自己的审核列表  https://www.mcmod.cn/verify.html?order=createtime&selfonly=1
已通过再编辑    /item/edit/<资料ID>/
待审再编辑      /item/add/<模组ID>-<资料ID>/
```

附言由用户提供。已知退回原因：

- 生物/实体没填注册名
- 表格缺标题行（首行要用 `<th>`）
- 能成套的盔甲没建「XX套装」汇总条目
- 抽象资料（套装、套具）带了图标
- 正文出现裸网址

本地源码里新增但没发布的内容不写进百科，等新版本上线再补。
