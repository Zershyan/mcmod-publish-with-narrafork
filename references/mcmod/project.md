# 百科模组条目

添加页 `https://www.mcmod.cn/class/add/`，分「基本信息」「扩展信息」「官方信息」三页，正文在页面下方的编辑器（全局 `editor`）。

## 建前核对

1. 先在百科搜索原模组、同名移植版，确认不重复；已有同版本定位的移植版时，正文要写清本版独有的改动。
2. 在 CurseForge / Modrinth 项目页的 More Details 取 Project ID、支持版本、加载器、许可证；只填已公开发布的版本和功能，本地未发布的改动要提醒用户。
3. 作者 ID 必须由用户提供（作者页地址 `https://www.mcmod.cn/author/<ID>.html` 里的数字），职位默认「所有者」`owner`；用户没给就先问，不要猜。

## 字段

**基本信息**：主要名称（中文）、次要名称（英文）、相关链接（CurseForge、GitHub 等）、模组元素（核心元素只选一个，参考同类模组）、支持平台、运作方式、支持 MC 版本、封面（16:10，最大 720×450）。

**扩展信息**：一句话简介 `#class-intro`、**MODID `#class-modid`（必填）**、客户端/服务端运行环境、模组关系（JEI/Jade 等代码联动）。

**官方信息**：Mod 作者、官方状态、开源状态、**CurseForge Project ID `#class-cfprojectid`（有 CF 页面就必须填）**。

MODID 取 `neoforge.mods.toml` / `mods.toml` 的 `modId` 或 `fabric.mod.json` 的 `id`，即物品注册名冒号前的部分，大小写敏感。

## 页面控件坑点

- `#class-modid`、`#class-cfprojectid`、`#class-mrprojectid`、`#class-tags` 是 bootstrap-tagsinput，原输入框 `display:none`：直接改 `value` 页面不认，必须 `$(el).tagsinput('removeAll'); $(el).tagsinput('add', 值)`。这是控件 API，不是绕过页面限制。
- 支持 MC 版本的复选框要先勾运作方式才出现，名字是 `class-mcversion-<运作方式编号>`（NeoForge 为 13），按 label 文字匹配版本号。
- 模组元素是 `a[data-multi-id=category]`：核心元素 `data-multi-value` 为 `1,x`（实用 `1,23`、科技 `1,1`、魔法 `1,2`、冒险 `1,3`、农业 `1,4`、装饰 `1,5`、LIB `1,7`），杂项元素按文字匹配。
- 作者：点 `.author-link`，在 `.common-select .find-key` 填作者 ID 后点 `.find-btn`，再点结果 `tr[data-id=ID]`；职位下拉是 `.author-row select.author-head-select`（selectpicker 多选）。
- 相关链接：点 `#link-frame .link-add` 新建一行，`select.link-head-select` 用 selectpicker 选站点（`curseforge`、`modrinth`、`github` 等），地址填 `.link-text-href`。
- 封面：logo 是透明底横幅时要放到对比明显的底色上；默认让用户点「上传封面」手动选 16:10 图片，确认裁剪框覆盖整张图再点「更新封面」。
- 最终「完成添加」交给用户点。

## 浏览器直连（默认）

用 `browsermcp` 打开添加页，按「基本信息 → 扩展信息 → 官方信息」逐项填写：文本字段直接 `fill`，tagsinput 与 selectpicker 用 `evaluate` 调它们自己的 API，元素/作者/链接按上面的选择器点选。设计稿正文用 `editor.setContent()` 或直接点进编辑器粘贴。

## 控制台脚本（回退）

1. 复制 [create-mod-config.example.json](create-mod-config.example.json) 到项目 `docs/mcmod/upload/mod_config.json`，改名称、简介、MODID、CF/Modrinth ID、元素、版本、链接；正文写 `intro.html`，封面 `cover.png`。
   - 正文第一段默认是 `<p>[ban:title_menu]</p>`，脚本缺了会自动补到最前面。
   - 要放截图时在正文写 `<p>{{img:键}}</p>`，配置加 `"images": {"键": "图片路径"}`；脚本用编辑器的 UEditor 上传接口把图传到百科再替换成 `<img>`，失败处留「请手动插入图片」文字并列进警告。2026-11-03 新增，尚未实测。
2. `python scripts/mcmod/make_create_mod_js.py mod_config.json create_mod_page.js`，再 `node --check create_mod_page.js`。
3. `powershell -NoProfile -Command "Get-Content -Raw -Encoding UTF8 create_mod_page.js | Set-Clipboard"` 交给用户。
4. 用户在 `https://www.mcmod.cn/class/add/` 按 F12，Edge/Chrome 首次粘贴前要先**手动输入** `允许粘贴`（英文界面 `allow pasting`）再粘贴运行。
5. 脚本结束会打印核对表（名称、简介、MODID、CF ID、作者）和需手动处理的警告；核对后手动上传封面、点「完成添加」。
