# 阶段 4：新建百科模组条目

添加页 `https://www.mcmod.cn/class/add/`，分「基本信息」「扩展信息」「官方信息」三页，正文在页面下方的编辑器（全局 `editor`）。

## 字段

按 [字段来源](sources.md#阶段-4百科模组条目)取。要点：

- **MODID `#class-modid` 必填**，取 `mod_id`，大小写敏感。
- **CurseForge Project ID `#class-cfprojectid` 必须填**，来自阶段 2。
- **作者 ID 必须用户提供**：作者页地址 `https://www.mcmod.cn/author/<ID>.html` 里的数字，职位默认「所有者」。
- 封面是 `logo.png` 转 16:10（最大 720×450），透明底横幅要垫对比明显的底色。

工程里没有、必须问的：中文名、核心元素、杂项元素、作者 ID。

## 页面控件坑点

- `#class-modid`、`#class-cfprojectid`、`#class-mrprojectid`、`#class-tags` 是 bootstrap-tagsinput，原输入框 `display:none`：改 `value` 页面不认，必须 `$(el).tagsinput('removeAll'); $(el).tagsinput('add', 值)`。这是控件 API，不是绕过页面限制。
- 支持 MC 版本的复选框要先勾运作方式才出现，名字是 `class-mcversion-<运作方式编号>`（NeoForge 为 13），按 label 文字匹配版本号。
- 模组元素是 `a[data-multi-id=category]`：核心元素 `data-multi-value` 为 `1,x`（实用 `1,23`、科技 `1,1`、魔法 `1,2`、冒险 `1,3`、农业 `1,4`、装饰 `1,5`、LIB `1,7`），杂项元素按文字匹配。
- 作者：点 `.author-link`，在 `.common-select .find-key` 填作者 ID 后点 `.find-btn`，再点结果 `tr[data-id=ID]`；职位下拉是 `.author-row select.author-head-select`（selectpicker 多选）。
- 相关链接：点 `#link-frame .link-add` 新建一行，`select.link-head-select` 用 selectpicker 选站点（`curseforge`、`modrinth`、`github`），地址填 `.link-text-href`。
- 最终「完成添加」由用户点。

## 填表脚本

配置写 `docs/mcmod/mod_config.json`（示例见 `references/mod-config.example.json`），正文写 `docs/mcmod/intro.html`。

```bash
python scripts/mcmod/make_create_mod_js.py docs/mcmod/mod_config.json docs/mcmod/create_mod_page.js
node --check docs/mcmod/create_mod_page.js
powershell -NoProfile -Command "Get-Content -Raw -Encoding UTF8 'docs/mcmod/create_mod_page.js' | Set-Clipboard"
```

用户在添加页 F12 粘贴运行，脚本结束打印核对表（名称、简介、MODID、CF ID、作者）和需手动处理的警告。封面不注入，由用户点「上传封面」选择。

## 正文

- 第一段必须是 `<p>[ban:title_menu]</p>`。
- 标题用 `<p>[h1=介绍]</p>`、`<p>[h2=属性]</p>`，不用 `<h1>`。
- 表格首行必须是 `<th>` 标题行。
- 正文不允许出现裸网址，链接一律 `<a href="地址" target="_blank" title="悬浮提示">链接文字</a>`。
- 只写已公开发布的版本和功能，本地未发布的改动要提醒用户。

## 提交字段

表单提交走 `POST https://event.mcmod.cn/action/edit/doEdit/`，参数是 `data=<JSON 字符串>`。结构：

```json
{
  "action": "class_add",
  "edit-id": "0",
  "class-id": "0",
  "redo-id": "0",
  "class-data": {
    "name": "主要名称", "ename": "次要名称", "sname": "简写",
    "intro": "一句话简介", "modid": "modid",
    "cfprojectid": "123456", "mrprojectid": "",
    "content": "<p>[ban:title_menu]</p>…",
    "category": { "0": "1,7" },
    "platform": { "0": "1" },
    "api": { "0": "13" },
    "mode-1": { "0": "1" },
    "mode-2": { "0": "1" },
    "status": { "0": "1" },
    "source": { "0": "1" },
    "tags": { "0": "标签" },
    "link": { "0": { "title": "curseforge", "custom": "", "href": "地址", "text": "" } },
    "author": { "link": { "0": { "select": ["owner"], "id": "作者ID" } } }
  }
}
```

- 文本字段直接是字符串；勾选、标签、分类是 `{序号: 值}` 形式，**序号只是遍历下标，服务端只认值**。
- `author.link` 关联已有作者（按作者页数字 ID），`author.add` 直接写名字新建。
- 枚举取值见 [mcmod-enums.json](../assets/mcmod-enums.json)，例如 `api` 的 `13` 是 NeoForge、`status` 的 `1` 是活跃、`source` 的 `2` 是闭源。

## 产出

记下百科模组 ID（资料添加页地址 `/item/add/<模组ID>/` 里的数字），阶段 5 要用。
