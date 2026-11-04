# 阶段 1：读工程事实

所有值来自工程文件，读完汇报，缺的再问用户。

## gradle.properties

| 键 | 用途 |
|---|---|
| `mod_id` | modid、注册名前缀 |
| `mod_name` | 英文名、CF 项目名 |
| `mod_version` | 模组版本号 |
| `mod_build_number` | 构建编号，拼进版本 |
| `mod_license` | 许可证、开源状态判断 |
| `mod_authors` | 作者 |
| `mod_description` | 简介 |
| `minecraft_version` | 目标 MC 版本 |
| `neo_version` / `forge_version` | 加载器判定 |

## 加载器

按 `gradle.properties` 里存在哪个键判断，再用 `build.gradle` 的 plugin 复核：

| 条件 | 结论 |
|---|---|
| `neo_version` + `net.neoforged.moddev` | NeoForge |
| `forge_version` + `net.neoforged.moddev.legacyforge` | Forge |

两者都不匹配时不要硬套，报告工程结构后询问用户。

## 版本

工程的版本拼法是 `${mod_version}-${minecraft_version}+build.${mod_build_number}`，例如 `2.0.0-1.21.1+build.44`。

这个字符串就是 CF 的版本显示名，不要另拼 `MC-加载器-名字-版本` 格式。

## JAR 产物

发布包在 `build/libs/${mod_id}-${mod_version}-${minecraft_version}.jar`，例如 `build/libs/hojojutsu-2.0.0-1.21.1.jar`。

发布包名不含构建编号（包内版本号带），`buildAlpha` 例外。`build/libs/` 下如果同时有 `origin/`、`obfuscate/` 子目录，那是中间产物，不要拿来上传。

## 语言文件

Datagen 工程的资源在 `src/generated/resources/assets/<modid>/lang/`，普通工程在 `src/main/resources/assets/<modid>/lang/`。中英文名、资料条目名称都从这里取。

## 工程里没有的

中文名、CF 分类、百科模组元素、百科作者 ID 这四类信息工程里没有，必须问用户。问完把答案记在汇报里，不要重复问同一个问题。
