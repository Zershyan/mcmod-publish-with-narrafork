# 字段来源

每个字段的取值位置都在这里规定。表里没有来源、或标注「询问用户」的，必须先问，不许猜。

## 阶段 1：工程事实

| 字段 | 来源 |
|---|---|
| modid | `gradle.properties` → `mod_id` |
| 英文名 | `gradle.properties` → `mod_name` |
| 中文名 | 询问用户（语言文件里没有） |
| 模组版本号 | `gradle.properties` → `mod_version` |
| 目标 MC 版本 | `gradle.properties` → `minecraft_version` |
| 加载器 | 自动分辨，见 [工程信息](stage1-project.md#加载器) |
| 许可证 | `gradle.properties` → `mod_license` |
| 作者 | `gradle.properties` → `mod_authors` |

## 阶段 2：CF 项目

| 字段 | 来源 |
|---|---|
| 项目名 name | `mod_name` |
| 简介 summary | `mod_description` |
| 详细描述 description | 按工程源码整理 |
| 图标 icon | `src/main/resources/logo.png`；不存在则询问用户 |
| Class | 固定 `Mods` |
| Main category | 询问用户 |
| Additional categories | 询问用户 |
| 许可证 license | `mod_license` |
| 分发许可 distribution | 闭源 → 不允许分发；开源 → 允许第三方分发 |
| 允许评论 allowComments | `true` |

## 阶段 3：CF 版本

| 字段 | 来源 |
|---|---|
| JAR 路径 | `build/libs/${mod_id}-${mod_version}-${minecraft_version}.jar` |
| 版本显示名 displayName | mod 原始版本号（构建脚本里的 `version`），不另拼 MC-加载器-名字 |
| changelog | 按 git 提交记录整理，中英文分块 |
| releaseType | `release`；不确定时询问用户 |
| 支持 MC 版本 | `minecraft_version` |
| 加载器 | 自动分辨 |
| 运行环境 | 按注册项与 `Dist` 代码判断，判断不了询问用户 |
| 依赖关系 relations | `build.gradle` 的 `dependencies` 里 `curse.maven:<名>-<项目ID>:<文件ID>` |

## 阶段 4：百科模组条目

| 字段 | 来源 |
|---|---|
| 主要名称（中文） | 询问用户 |
| 次要名称（英文） | `mod_name` |
| 一句话简介 | `mod_description` |
| MODID | `mod_id` |
| CurseForge Project ID | 阶段 2 建项目后得到 |
| 模组元素（核心/杂项） | 询问用户 |
| 支持平台 | 固定「JAVA版 (JAVA Edition)」 |
| 运作方式 | 自动分辨 |
| 支持 MC 版本 | `minecraft_version` |
| 客户端/服务端 | 按注册项与 `Dist` 代码判断 |
| 作者 ID | 询问用户（作者页地址里的数字） |
| 作者名 | `mod_authors` |
| 职位 | 固定「所有者」（`owner`） |
| 官方状态 | 固定「活跃」 |
| 开源状态 | 按 `mod_license` 判断 |
| 相关链接 | git remote（GitHub）+ CF 项目页；其他链接询问用户 |
| 封面 | `logo.png` 加底色转 16:10；不存在则询问用户 |
| 正文 | 按工程源码整理 |

## 阶段 5：百科资料条目

| 字段 | 来源 |
|---|---|
| 提交范围 | 工程内全部物品与方块 |
| 16 色变体 | 每个颜色单独一条，不合并 |
| 资料分类 | 按注册表类型（方块/物品 → 物品/方块），见 [分类值](stage5-wiki-entries.md#分类值) |
| 主要名称 | `zh_cn.json` |
| 次要名称 | `en_us.json` |
| 注册名 | 注册表 ID `modid:path` |
| 最大耐久 / 最大堆叠 | 运行时导出 |
| 资料类型 | 按物品用途判断 |
| 小图标 / 大图标 | 平面物品取 `layer0` 放大；方块物品 3D 离屏渲染 |
| 资料封面 | 不填 |
| 正文 | 按工程源码整理 |
| 矿物词典 / 元数据 | 空 |
| 改动附言 | 留空 |

## 阶段 6：审核

| 项 | 规则 |
|---|---|
| 审核列表 | `https://www.mcmod.cn/verify.html?order=createtime&selfonly=1` |
| 附言 | 由用户提供，不自行抓取 |
| 未通过 | 打开再编辑链接，按 `location.pathname` 匹配后改正文 |
| 资料 ID 映射 | `docs/mcmod/entries.json` |

## 语言文件位置

Datagen 工程的资源在 `src/generated/resources/assets/<modid>/lang/`；没有 datagen 的在 `src/main/resources/assets/<modid>/lang/`。两处都找不到时问用户。
