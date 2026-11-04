# 阶段 5：创建百科资料条目

## 分类值

添加页 `https://www.mcmod.cn/item/add/<模组ID>/` 顶部的「资料分类」共 10 种，`data-multi-value` 依次为：

| 值 | 分类 | 表单额外字段 |
|---|---|---|
| 1 | 物品/方块 | 矿物词典、最大耐久、最大堆叠、注册名、元数据 |
| 2 | 群系/群落 | 无 |
| 3 | 世界/维度 | 无 |
| 4 | 生物/实体 | 无 |
| 5 | 附魔/魔咒 | 无 |
| 6 | BUFF/DEBUFF | 无 |
| 7 | 多方块结构 | 无 |
| 8 | 自然生成 | 无 |
| 9 | 绑定热键 | 无 |
| 10 | 游戏设定 | 无 |

所有分类共有：主要名称、次要名称、资料类型、小图标 32×32、大图标 128×128、资料封面、正文、改动附言。

资料分类按注册表类型判断：方块与物品 → 1，实体 → 4，BUFF → 6，附魔 → 5。工程的注册项决定提交哪些分类。

「物品/方块」内部再分：

- **单件**：正文写完整介绍。
- **套装（盔甲）**：能成套的盔甲新建「XX套装」条目统一介绍，次要名称 `XX Suit`；套内单件正文留空，名称、注册名、耐久、堆叠、图标照填。
- **套具（工具）**：同材质成套工具新建「XX套具」，次要名称 `XX Tools`；套内单件正文留空。剑、镰刀不并入套具。
- **抽象资料不放图标**：游戏里没有对应物品的汇总条目不填图标。

颜色变体按用户确认的规则**每个颜色单独一条**，不合并。

## 条目数据

定稿整理成 JSON 数组，每条字段：`key, name, ename, regname, damage, maxstack, type, content, icon32, icon128`。

- `regname` 对物品/方块、生物/实体、BUFF、附魔、世界/维度、自然生成必填，格式 `modid:id`，审核会以「实体注册名必填」退回。
- `category` 不是 1 时额外写，`damage`/`maxstack` 留空。
- 重新提交被退回的条目加 `redo` 字段，值为资料 ID。

## 数据

| 数据 | 取法 |
|---|---|
| 名称 | `zh_cn.json` / `en_us.json` 的 `item.<modid>.<id>` / `block.<modid>.<id>` |
| 注册名 | 注册表 ID |
| 最大耐久 / 最大堆叠 | 运行时导出 |
| 资料类型 | 按物品用途判断 |
| 获取方式 | 配方、战利品表、交易、结构箱子 |

**运行时导出**：在 gametest 源集写导出测试，把每个物品的堆叠、耐久、稀有度、防火、属性修饰符（优先 `stack.getAttributeModifiers()`，取不到回退默认值）、`appendHoverText` 结果写成 JSON，跑 `gameTestServer`。

**静态解析**：配方、战利品表、世界生成、进度奖励、NPC 交易。结构箱子来源先从 `worldgen/structure/*.json` 的 `start_pool` 沿 `template_pool` 与 NBT 拼图引用找全部部件，再在部件 NBT（gzip）里匹配 `chests/...`；未被引用的战利品表不算来源。

名称发现重名或明显错译时先停下让用户决定，不自行改名。tooltip 与代码不一致以代码为准，并在汇报里列出差异。

## 正文

通用格式：

- 第一段必须是 `<p>[ban:title_menu]</p>`。
- 标题用 `<p>[h1=介绍]</p>`、`<p>[h2=属性]</p>`，不用 `<h1>`。
- 表格首行必须是 `<th>` 标题行，单元格 `style="word-break: break-all;" align="center"`。
- 正文不允许裸网址，链接一律 `<a href="地址" target="_blank" title="悬浮提示">链接文字</a>`，链接文字写站点或对象名。
- 伤害/生命值用 `[icon:health=数值,点]`。
- 盔甲穿戴部位只填 `头盔`、`胸甲`、`护腿`、`靴子`，不写头部/胸部/腿部/脚部；「胸部」会被判疑似违规词。
- 攻击伤害显示值 = 修饰符 + 1；攻击速度 = 修饰符 + 4；击退抗性 = 修饰符 × 10。
- 不写「是一种材料」这类只复述资料类型的空话；介绍段没有实质内容时整段省略。
- 属性表只剩「最大堆叠」一列时不写属性段。
- 用途可制作的物品超过 8 个时整段不写。

分类型模板见 [正文模板](content-templates.md)。

## 图标

- **平面物品**（父模型 `item/generated` / `item/handheld`）：取 `layer0`，NEAREST 放大到 32 与 128。
- **方块物品与 3D 模型**：开发客户端离屏渲染透明背景，`finish_icons.py` 裁透明边、居中、LANCZOS 缩放。实体在进入存档后的 `RenderFrameEvent.Post` 里渲染，渲染前 `setCustomName(null)`。
- 图标是隐藏字段 `#icon-32x` / `#icon-128x`，值为 base64，尺寸必须正好 32×32 / 128×128。
- 抽象资料不填图标。

## 提交

```bash
python scripts/mcmod/make_batch_js.py docs/mcmod/entries.json docs/mcmod/submit.js 0 "" [key列表]
node --check docs/mcmod/submit.js
powershell -NoProfile -Command "Get-Content -Raw -Encoding UTF8 'docs/mcmod/submit.js' | Set-Clipboard"
```

- 第 3 个参数 `1` 为试运行（只收集数据不提交），第 4 个参数是附言，默认空字符串。
- 先生成只含 1 条的测试脚本让用户试提交，确认后再给其余条目。
- 用户在添加页 F12 运行；脚本每条间隔 4 秒，`state !== 0` 时停止，结果存在 `window.__mcmodBatchResults`。
- 脚本调用页面自己的 `getEditorData()` 和 `/action/edit/doEdit/` 接口。

提交后把 `key` 与百科资料 ID 的映射写进 `docs/mcmod/entries.json` 的 `id` 字段，阶段 6 用它拼再编辑链接。
