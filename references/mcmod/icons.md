# 图标

百科资料的小图标 32×32、大图标 128×128，尺寸必须正好。`make_icons.py` 与 `finish_icons.py` 依赖 Pillow（`python -m pip install pillow`）。

## 平面物品

父模型是 `item/generated` / `item/handheld`：取 `layer0` 贴图，动画贴图裁第一帧，NEAREST 放大到 32 和 128。

```bash
python scripts/mcmod/make_icons.py <模组assets目录> <条目.json> <图标输出目录>
```

脚本把 base64 直接写回条目的 `icon32` / `icon128`，父模型不是平面模型的会清空图标并单独列出。

## 3D / GeckoLib 模型

在开发客户端里离屏渲染透明背景，参考 [WikiIconExporter.java.txt](../../scripts/mcmod/WikiIconExporter.java.txt)：

- 在 gametest 源集加客户端事件订阅类，在标题界面 `ScreenEvent.Render.Post` 里对每个物品用 `TextureTarget` 渲染，清屏色 `(0,0,0,0)`。
- 视野放大到 5 倍（`setOrtho(-32,48,48,-32,1000,21000)`，1280px），否则大模型的 GUI 变换会被裁切。
- 渲染出的 `*_raw.png` 用 `python scripts/mcmod/finish_icons.py <原图目录> <输出目录>` 裁掉透明边、居中、LANCZOS 缩放到 32 与 128，并生成 `_sheet.png` 预览拼图。
- 报 `EDGE` 的条目说明模型贴到了渲染边界，调小缩放重渲。

## 生物 / 实体

标题界面没有世界，实体无法创建，导出器改在进入存档后的 `RenderFrameEvent.Post` 里渲染（等约 120 帧）：

- 用 `EntityType.create(level)` 建实体，照 `InventoryScreen.renderEntityInInventory` 的变换（`rotateZ(PI)` + 相机 `rotateX` 俯角、`overrideCameraOrientation`、关阴影、光照 15728880）交给 `EntityRenderDispatcher.render`，非 LivingEntity 也能渲染。
- 渲染前 `setCustomName(null)` + `setCustomNameVisible(false)`，否则 NPC 等带名字的实体会把名牌画进图标。
- 用 `--quickPlaySingleplayer <存档名>` 自动进存档（先把一个存档复制到该运行目录的 saves）；缩放、偏航、俯角用 `key:值`（`*` 为默认）逐个覆盖。
- IconRenderer 在百科的下载需要图形验证码，不能自动下载；Modrinth 上的图标导出模组只支持物品，所以实体用自建导出器。
- 开发客户端进标题界面若因其他模组的配置翻译缺失崩溃（例如 Jade 的 `config.jade.plugin_<modid>.<uid>`），先补语言文件。

## 抽象资料

套装、套具这类在游戏里没有对应物品的汇总条目**不放图标**：生成数据时写 `"abstract": true`（或名称以「套装」「套具」结尾），`make_batch_js.py` 会自动清空。

已提交的抽象资料若带了图标：打开「再编辑」页，勾选「删除小图标」`#item-data-icon-32x-delete` 和「删除大图标」`#item-data-icon-128x-delete`，清空 `#icon-32x` / `#icon-128x`，再完成添加。

- 编辑页加载时可能弹出「编辑规范」窗口挡住点击，先关掉（或勾「我已知晓，不用再提示」），再勾删除框，并用 `checked` 确认已勾上。
- 提交按钮是左侧的「添加资料」，之后在「资料添加确认」弹窗点「确定提交」；「胸甲」等词的疑似违规警告是误报，可以忽略。

## 提交数据里的形式

图标是隐藏字段 `#icon-32x` / `#icon-128x`，值为 `data:image/png;base64,...`。
