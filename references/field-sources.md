# 字段来源

每个字段从哪取都写在这。表里没有的、或标「问用户」的，停下来问，不许猜。

## 工程事实

| 字段 | 取自 |
|---|---|
| modid | `gradle.properties` → `mod_id` |
| 英文名 | `gradle.properties` → `mod_name` |
| 中文名 | **问用户**（语言文件里通常没有） |
| 版本号 | `build.gradle` 里 `version` 的实际值（含 MC 版本与构建尾缀） |
| MC 版本 | `gradle.properties` → `minecraft_version` |
| 加载器 | 有 `neo_version` → NeoForge；有 `forge_version` → Forge |
| Java 版本 | `build.gradle` → `java.toolchain.languageVersion` |
| 许可证 | `gradle.properties` → `mod_license` |
| 作者 | `gradle.properties` → `mod_authors` |
| 简介 | `gradle.properties` → `mod_description` |
| JAR 名 | `base { archivesName }`，没配时用工程目录名 |

装了 `zershyan-mcmod-style` 的工程，**禁止使用文件名带 `+build.N` 的 jar**，细节见 [与 zershyan-mcmod-style 同装时](with-mcmod-style.md)。没装的按 `build.gradle` 实际命名判断。

**版本号不要拼**。有的工程是 `${mod_version}-${minecraft_version}+build.${n}`，有的直接 `version = mod_version`，多分支工程甚至每个分支都不一样。逐个分支读 `build.gradle`。

## CurseForge 项目

| 字段 | 取自 |
|---|---|
| 项目名 | `mod_name` |
| 简介 | `mod_description`，1～256 字符 |
| 详细描述 | 按 README 与源码整理 |
| 图标 | `src/main/resources/logo.png`，没有则问用户 |
| Class | 固定 `Mods` |
| 主分类 | **问用户** |
| 附加分类 | **问用户** |
| 许可证 | `mod_license` |
| 允许第三方分发 | 闭源关、开源开，可覆盖 |
| 允许评论 | `true` |
| 源码链接 | git remote |

## CurseForge 版本

| 字段 | 取自 |
|---|---|
| JAR 路径 | 装 style skill：`build/libs/<archivesName>-<mod_version>-<mc>.jar`（不带构建编号）；通用：`build/libs/<archivesName>-<version>.jar` |
| 显示名 | 工程 `version` 原值 |
| 更新说明 | `git log` 整理，英文块 + `---` + 中文块 |
| 发布类型 | 默认 `release`，不确定时问 |
| 游戏版本标签 | 第 3 步拉的 Game Versions |
| 运行环境 | 按注册项与 `Dist` 代码判断，判断不了问用户 |
| 依赖 | `build.gradle` 的 `curse.maven:` 坐标 |

## 百科模组条目

| 字段 | 取自 |
|---|---|
| 主要名称 | **问用户** |
| 次要名称 | `mod_name` |
| 一句话简介 | `mod_description` |
| MODID | `mod_id` |
| CF Project ID | `curseforge/project.json` |
| Modrinth Project ID | 有则填，没有留空 |
| 模组元素 | **问用户** |
| 支持平台 | 固定 JAVA版 |
| 运作方式 + MC 版本 | 从 CF 的「加载器 × MC 版本」组合聚合 |
| 客户端/服务端 | 按注册项与 `Dist` 代码判断 |
| 官方状态 | 按项目现状判断，多数在维护的填「活跃」；不确定时问用户 |
| 开源状态 | 按 `mod_license` 判断，ARR 类填「闭源」 |
| 许可证协议 | `mod_license` 映射到 SPDX 代码；找不到对应项时留空或填 `ARR` |
| 作者 | **问名字**，脚本查 ID |
| 相关链接 | git remote + CF 项目页 |
| 封面 | `logo.png` 转 16:10，没有则问用户 |
| 正文 | 按源码整理 |

## 百科资料条目

| 字段 | 取自 |
|---|---|
| 提交范围 | 工程内全部物品与方块 |
| 颜色变体 | 每个颜色单独一条 |
| 资料分类 | 按注册表类型（方块/物品 → 物品/方块） |
| 名称 | `zh_cn.json` |
| 英文名 | `en_us.json` |
| 注册名 | 注册表 ID `modid:path` |
| 耐久 / 堆叠 | 运行时导出 |
| 资料类型 | 按物品用途判断 |
| 图标 | 平面取 `layer0` 放大；方块走 3D 渲染 |
| 正文 | 按源码与 [正文模板](../assets/content-templates.md) |
| 改动附言 | 默认留空 |

## 只有这四类必须问用户

1. **中文名**
2. **CF 主分类 / 附加分类**
3. **百科模组元素**
4. **百科作者名**

其余都能从工程或接口拿到。用户回答后记进配置，不要重复问。
