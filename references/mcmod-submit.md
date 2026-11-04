# 百科提交技术细节

从 mcmod.cn 添加页实测取得，用于纯脚本提交。改动前先按本文验证，别凭印象改。

## 登录与 cookie

登录接口（账号密码，页面有验证码时纯脚本走不通）：

```
POST https://www.mcmod.cn/action/doLogin/
data={"username":"…","password":"…","remember":1,"captcha":""}
→ {"state":0} 成功；{"state":"logreg_password_incorrect"} 失败
```

QQ 登录走 `https://www.mcmod.cn/plugs/loginConnect/qqConnect/oauth/index.php`，必须人工扫码。

cookie 里 `dSit_2132_auth` 是登录凭证且为 **httpOnly**，`document.cookie` 读不到。用 CDP 从浏览器进程取：

```bash
python scripts/mcmod/dump_cookies_cdp.py --profile <profile目录> --domain mcmod.cn --out .narrafork/mcmod-cookie.txt
```

## 提交接口

```
POST https://event.mcmod.cn/action/edit/doEdit/
Content-Type: application/x-www-form-urlencoded
data=<URL 编码的 JSON>

{"state": 0}         成功
{"state": 117}       已登录但数据有问题
{"state": 122}       未登录
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
    "author": { "link": { "0": { "select": ["owner"], "id": "36340" } }, "add": {} }
  }
}
```

字段类型容易搞错的地方：

| 字段 | 类型 | 说明 |
|---|---|---|
| `api` / `platform` / `category` / `status` / `source` / `mode-*` | `{序号: 值}` | 序号是遍历下标，服务端只认值 |
| `mcversion` | `{加载器ID: {序号: 版本ID}}` | 两层嵌套，见下 |
| `license.0.list.0.type` | **数组** | `["source"]` |
| `license.0.list.0.name` | 字符串 | SPDX 代码 |
| `license.0.title` | 字符串 | 页面「通用」时提交空串 |
| `author.0.select` | **数组** | `["owner"]` |

## MC 版本怎么选（关键）

三组 MC 版本 input 一开始就全在 DOM 里，按加载器分组隐藏，**数据收集不看可见性**：

```
input[name="class-mcversion-1"]    Forge
input[name="class-mcversion-2"]    Fabric
input[name="class-mcversion-13"]   NeoForge
```

每个 input 的 `value` 是版本数字 ID，父元素文本是版本号：

```
id="class-data-mcversion-13-78"  value="78"  父元素文本 "26.1.2"
id="class-data-mcversion-13-65"  value="65"  父元素文本 "1.21.1"
```

所以纯脚本只要置 `checked = true`，不需要触发任何显示联动。提交出来是：

```json
"mcversion": { "13": { "0": "78" } }
```

**注意**：勾选加载器后页面不刷新 MC 版本列表这个行为只影响人工操作，不影响数据。反过来说，如果走浏览器点击路线，才需要先让那组显示出来。

版本 ID 与版本号的对应关系每次都可能变，**必须从页面现取**，不能写死。

## 枚举取值

见 [mcmod-enums.json](../assets/mcmod-enums.json)：

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
→ {"state":0,"html":"<tr data-id=\"36340\"><td><b>折戏鸢</b> - <i>Zershyan / …</i></td></tr>"}
```

`state:109` 表示没找到。搜索框只认名字，用户中心 ID（`center.mcmod.cn/<ID>/`）不是作者 ID。

## 页面控件的真实行为

- `#class-modid`、`#class-cfprojectid`、`#class-mrprojectid`、`#class-tags`、`#class-keys` 是 bootstrap-tagsinput，底层 input 的 id 才是提交键
- 分类是 `a[data-multi-id=category]`，取 `data-multi-value`
- 许可协议要先点 `.license-group-add` 再点 `.license-add-button` 才有结构

## 一键填入的思路

有了上面这些，纯脚本只需要：

1. 从页面取一次 `版本号 → 版本ID` 映射（每次可能变）
2. 按配置组装 JSON
3. POST 到 `doEdit`

不需要浏览器参与。`submit_class.py` 已实现前两步，版本 ID 映射还需要补一个抓取函数。
