# 第三方依赖来源

只登记后续项目可能引用的第三方模组，不登记用户自己的模组、附属模组或个人发布项目。记录 CurseForge 项目地址、项目 ID、slug，以及已从构建文件或 Maven 元数据核对过的仓库和坐标。只记公开信息，不记 API 密钥、登录信息或其他凭据。

## 使用规则

1. 添加第三方模组依赖前，先按项目名、模组 ID、Git 仓库链接、CurseForge slug、Maven 坐标和 Minecraft 版本查找对应记录。
2. 发现 CurseForge 记录后，通过项目页或 API 返回的项目名称、作者、slug 再核对一次；发现 Maven 记录后，通过仓库元数据或当前项目构建解析结果核对完整坐标和版本，确认不是同名或相似项目。
3. CurseForge 依赖必须另外确认目标 Minecraft 版本、加载器和具体文件 ID；项目页地址和项目 ID 不能替代文件版本。
4. Maven 依赖必须记录仓库地址和完整坐标或明确的坐标模板；只记录仓库主页或不完整坐标不能作为可直接使用的依赖来源。
5. 记录缺失时，先查找公开项目页、官方 Maven 仓库或当前项目已经成功使用的依赖声明；仍然找不到就向用户索要项目 URL、数字 ID 或仓库/坐标，不要猜测。
6. 新定位到第三方模组或发现已有记录缺少来源时，只在实际核对项目页、Maven 元数据或项目构建成功后更新本文件，并记录适用版本/加载器、核对日期和验证方式。

## 已核对第三方模组

| 模组 | Minecraft / 加载器 | CurseForge 项目 ID | slug | CurseForge 项目页 | Maven 仓库 | 已核对坐标或坐标模板 | 核对日期 |
|---|---|---:|---|---|---|---|---|
| KubeJS | 1.20.1 Forge、1.21.1 NeoForge、26.1.2 NeoForge | 238086 | `kubejs` | <https://www.curseforge.com/minecraft/mc-mods/kubejs> | <https://maven.latvian.dev/releases> | `dev.latvian.mods:kubejs-neoforge:<version>`；已在 1.21.1 NeoForge、26.1.2 NeoForge 项目中核对 | 2026-08-23 |
| Jade | 1.21.1 NeoForge | 324717 | `jade` | <https://www.curseforge.com/minecraft/mc-mods/jade> | <https://www.cursemaven.com> | `curse.maven:jade-324717:8591319`；Jade 15.10.6 Release，官方文件页确认 NeoForge、1.21.1；CurseMaven POM 返回 200 | 2026-09-26 |
| Just Enough Characters（JEC） | 1.19.2 Fabric/Forge、1.20.1 Fabric/Forge、1.21.1 Fabric/NeoForge、26.1.2 NeoForge | 250702 | `just-enough-characters` | <https://www.curseforge.com/minecraft/mc-mods/just-enough-characters> | <https://www.cursemaven.com> | `curse.maven:just-enough-characters-250702:<file_id>`：8583993（1.19.2 Fabric）、8583989（1.19.2 Forge）、8770948（1.20.1 Fabric）、8771525（1.20.1 Forge）、6681788（1.21.1 Fabric）、8117474（1.21.1 NeoForge）、8413185（26.1.2 NeoForge）；对应 POM 均返回 200，模板 `compileJava` 除 1.21.1 NeoForge 受 Mojang manifest 下载失败影响外均通过 | 2026-09-27 |
| Just Enough Items（JEI） | 1.20.1 Forge、1.20.1 Fabric、1.21.1 NeoForge、1.21.1 Fabric、26.1.2 NeoForge | 238222 | `jei` | <https://www.curseforge.com/minecraft/mc-mods/jei> | <https://maven.blamejared.com/> | `mezz.jei:jei-<minecraft_version>-common:<version>`、`common-api`、`forge`/`forge-api`、`neoforge`/`neoforge-api`、`fabric`/`fabric-api`；具体版本必须按当前项目核对 | 2026-08-23 |
| Tom's Simple Storage Mod | 1.20.1 Forge | 378609 | `toms-storage` | <https://www.curseforge.com/minecraft/mc-mods/toms-storage> | <https://www.cursemaven.com> | `curse.maven:toms-storage-378609:6418133`；JAR 元数据确认 `toms_storage`，文件为 1.20-1.7.1 | 2026-08-24 |
| Polymorph | 1.20.1 Forge | 388800 | `polymorph` | <https://www.curseforge.com/minecraft/mc-mods/polymorph> | <https://www.cursemaven.com> | `curse.maven:polymorph-388800:6450982`；JAR 元数据确认 `polymorph`，文件为 0.49.10+1.20.1 | 2026-08-24 |
| Nature's Compass | 1.20.1 Forge | 252848 | `natures-compass` | <https://www.curseforge.com/minecraft/mc-mods/natures-compass> | <https://www.cursemaven.com> | `curse.maven:natures-compass-252848:7892948`；CFWidget 项目接口确认项目与文件，Gradle 依赖解析确认文件可映射 | 2026-09-01 |
| Explorer's Compass Enhance | 1.19.2 Forge、1.20.1 Forge、1.21.1 NeoForge | 1649198 | `explorers-compass-enhance` | <https://www.curseforge.com/minecraft/mc-mods/explorers-compass-enhance> | <https://www.cursemaven.com> | `curse.maven:explorers-compass-enhance-1649198:8629706`（1.19.2 Forge）、`curse.maven:explorers-compass-enhance-1649198:8761373`（1.20.1 Forge）、`curse.maven:explorers-compass-enhance-1649198:8761369`（1.21.1 NeoForge）；JAR 元数据确认 `explorerscompass`，并核对 `StructureSearchWorker` 目标签名 | 2026-09-04 |
| L_Ender's Cataclysm | 1.20.1 Forge | 551586 | `lendercataclysm` | <https://www.curseforge.com/minecraft/mc-mods/lendercataclysm> | <https://www.cursemaven.com> | `curse.maven:lendercataclysm-551586:8246047`；官方文件页确认 3.31、Release、Forge、1.20.1，Gradle 构建解析通过 | 2026-09-09 |
| Tinkers' Construct | 1.20.1 Forge | 74072 | `tinkers-construct` | <https://www.curseforge.com/minecraft/mc-mods/tinkers-construct> | <https://www.cursemaven.com> | `curse.maven:tinkers-construct-74072:7449219`；官方文件页确认 3.11.2.166、Release、Forge、1.20.1，Gradle 构建解析通过 | 2026-09-16 |
| Mantle | 1.20.1 Forge | 74924 | `mantle` | <https://www.curseforge.com/minecraft/mc-mods/mantle> | <https://www.cursemaven.com> | `curse.maven:mantle-74924:7563777`；官方文件页确认 1.11.104、Release、Forge、1.20.1，Gradle 构建解析通过 | 2026-09-16 |
| Curios API | 1.20.1 Forge | 309927 | `curios` | <https://www.curseforge.com/minecraft/mc-mods/curios> | <https://www.cursemaven.com> | `curse.maven:curios-309927:6418456`；官方文件页确认 5.14.1+1.20.1、Release、Forge，Gradle 构建解析通过 | 2026-09-09 |
| Malum | 1.20.1 Forge | 484064 | `malum` | <https://www.curseforge.com/minecraft/mc-mods/malum> | <https://www.cursemaven.com> | `curse.maven:malum-484064:6646111`；官方文件列表确认 malum-1.20.1-1.6.7.jar（1.20.1、Forge/NeoForge），Gradle 编译解析通过 | 2026-11-01 |
| Lodestone | 1.20.1 Forge | 616457 | `lodestone` | <https://www.curseforge.com/minecraft/mc-mods/lodestone> | <https://www.cursemaven.com> | `curse.maven:lodestone-616457:6213794`；官方文件列表确认 lodestone-1.20.1-1.6.4.1.jar（同名另有旧文件 5929869，取较新的 6213794），Gradle 编译解析通过 | 2026-11-01 |
| FTB Quests (Forge) | 1.20.1 Forge | 289412 | `ftb-quests-forge` | <https://www.curseforge.com/minecraft/mc-mods/ftb-quests-forge> | <https://www.cursemaven.com> | `curse.maven:ftb-quests-forge-289412:8078538`；官方文件页确认 2001.4.22、Release、Forge、1.20.1；JAR 元数据核对必需前置 Architectury、FTB Library、FTB Teams；Atum Reborn Forge 1.20.1 build 通过 | 2026-09-23 |
| FTB Library (Forge) | 1.20.1 Forge | 404465 | `ftb-library-forge` | <https://www.curseforge.com/minecraft/mc-mods/ftb-library-forge> | <https://www.cursemaven.com> | `curse.maven:ftb-library-forge-404465:8226927`；官方文件页确认 2001.2.13、Release、Forge、1.20.1；JAR 元数据确认 Architectury 必需且 Forge >=47.3；Atum Reborn Forge 1.20.1 build 通过 | 2026-09-23 |
| FTB Teams (Forge) | 1.20.1 Forge | 404468 | `ftb-teams-forge` | <https://www.curseforge.com/minecraft/mc-mods/ftb-teams-forge> | <https://www.cursemaven.com> | `curse.maven:ftb-teams-forge-404468:7499810`；官方文件页确认 2001.3.2、Release、Forge、1.20.1；JAR 元数据确认 Architectury >=9.1.12、FTB Library >=2001.2.0；Atum Reborn Forge 1.20.1 build 通过 | 2026-09-23 |
| Architectury API | 1.20.1 Forge | 419699 | `architectury-api` | <https://www.curseforge.com/minecraft/mc-mods/architectury-api> | <https://www.cursemaven.com> | `curse.maven:architectury-api-419699:5137938`；官方文件页确认 9.2.14、Release、Forge、1.20.1；JAR 元数据核对 modId `architectury`；Atum Reborn Forge 1.20.1 build 通过 | 2026-09-23 |
| Lionfish API | 1.20.1 Forge | 1001614 | `lionfish-api` | <https://www.curseforge.com/minecraft/mc-mods/lionfish-api> | <https://www.cursemaven.com> | `curse.maven:lionfish-api-1001614:8095554`；官方文件页确认 3.0、Release、Forge、1.20.1，Gradle 构建解析通过 | 2026-09-09 |
| Xaero's Minimap | 1.19.2 Fabric、1.20.1 Forge | 263420 | `xaeros-minimap` | <https://www.curseforge.com/minecraft/mc-mods/xaeros-minimap> | <https://www.cursemaven.com> | `curse.maven:xaeros-minimap-263420:8042288`（1.19.2 Fabric）、`curse.maven:xaeros-minimap-263420:8449808`（1.20.1 Forge）；官方文件页确认 1.19.2 Fabric 25.3.12 和 1.20.1 Forge 26.4.2 均为 Release，本地 JAR 元数据与路径点 API 核对，1.19.2 Fabric Gradle build 通过 | 2026-09-09 |
| Legendary Monsters | 1.21.1 NeoForge、1.20.1 Forge | 944035 | `legendary-monsters` | <https://www.curseforge.com/minecraft/mc-mods/legendary-monsters> | <https://www.cursemaven.com> | `curse.maven:legendary-monsters-944035:8715533`（1.21.1 NeoForge）、`curse.maven:legendary-monsters-944035:8715502`（1.20.1 Forge）；官方文件页确认 2.2.2、Release 及对应加载器/版本；JAR 元数据确认 `legendary_monsters`，当前 1.20.1 Forge 项目的 compileJava、processResources 和 build 均通过 | 2026-09-17 |
| EEEAB's Mobs | 1.20.1 Forge | 921600 | `eeeabs-mobs` | <https://www.curseforge.com/minecraft/mc-mods/eeeabs-mobs> | <https://www.cursemaven.com> | `curse.maven:eeeabs-mobs-921600:8073814`；官方文件页确认 1.20.1 Forge、文件 0.98.1（Beta），JAR 元数据确认 `eeeabsmobs`，并核对两种定位之眼及结构标签，当前项目 Gradle build 通过 | 2026-09-09 |
| Sophisticated Core | 1.21.1 NeoForge | 618298 | `sophisticated-core` | <https://www.curseforge.com/minecraft/mc-mods/sophisticated-core> | <https://www.cursemaven.com> | `curse.maven:sophisticated-core-618298:8838842`；官方文件页确认 1.5.1.2341、Release、NeoForge、1.21.1，当前 Storage Consolidator 的 build 与 runClient 加载通过 | 2026-09-19 |
| Sophisticated Storage | 1.21.1 NeoForge | 619320 | `sophisticated-storage` | <https://www.curseforge.com/minecraft/mc-mods/sophisticated-storage> | <https://www.cursemaven.com> | `curse.maven:sophisticated-storage-619320:8687896`；官方文件页确认 1.5.91.2127、Release、NeoForge、1.21.1，当前 Storage Consolidator 的 build 与 runClient 加载通过 | 2026-09-19 |
| Sophisticated Backpacks | 1.21.1 NeoForge | 422301 | `sophisticated-backpacks` | <https://www.curseforge.com/minecraft/mc-mods/sophisticated-backpacks> | <https://www.cursemaven.com> | `curse.maven:sophisticated-backpacks-422301:8845926`；官方文件页确认 3.26.3.2158、Release、NeoForge、1.21.1，当前 Storage Consolidator 的 build 与 runClient 加载通过 | 2026-09-19 |
| Lootr | 1.21.1 NeoForge | 361276 | `lootr` | <https://www.curseforge.com/minecraft/mc-mods/lootr> | <https://www.cursemaven.com> | `curse.maven:lootr-361276:8811105`；官方文件页确认 1.11.38.125、Release、NeoForge、1.21.1，当前 Storage Consolidator 的 build 与 runClient 加载通过 | 2026-09-19 |

| Bosses'Rise | 1.20.1 Forge、1.21.1 NeoForge | 1314084 | `bossesrise` | <https://www.curseforge.com/minecraft/mc-mods/bossesrise> | <https://www.cursemaven.com> | `curse.maven:bossesrise-1314084:8123166`（1.20.1 Forge 2.1.2）、`curse.maven:bossesrise-1314084:8123167`（1.21.1 NeoForge 2.1.2）；CFWidget 文件列表确认 Release 及对应加载器/版本，CurseMaven 下载文件与原始 JAR SHA256 一致，modId `block_factorys_bosses`，许可 All Rights Reserved（不要把 JAR 提交进公开仓库）；Bosses Rise Intro Skipper 两个版本 build 通过 | 2026-11-02 |
| TrashSlot | 1.20.1 Forge | 235577 | `trashslot` | <https://www.curseforge.com/minecraft/mc-mods/trashslot> | <https://www.cursemaven.com> | `curse.maven:trashslot-235577:8019497`；官方文件页确认 15.1.5、Release、Forge、1.20.1；CurseMaven POM 可访问，当前 1.20.1 Forge 附属项目 build 通过 | 2026-09-23 |
| Balm | 1.20.1 Forge | 531761 | `balm` | <https://www.curseforge.com/minecraft/mc-mods/balm> | <https://www.cursemaven.com> | `curse.maven:balm-531761:8404830`；官方文件页确认 7.3.41、Release、Forge、1.20.1；TrashSlot 15.1.5 的 mods.toml 要求 Balm >=7.3.0；CurseMaven POM 可访问，当前 1.20.1 Forge 附属项目 build 通过 | 2026-09-23 |
## 已核对 CurseMaven 文件示例

- JEI 1.20.1 Forge：`curse.maven:jei-238222:8778011`，仓库 `https://www.cursemaven.com`。2026-09-08 实际下载 JAR，核对 `META-INF/mods.toml`：modId 为 `jei`、版本 `15.56.0.205`、Forge 范围 `[47.0,)`、Minecraft 范围 `[1.20.1, 1.20.2)`；文件列表标记为正式版。
- KubeJS 1.20.1 Forge：`curse.maven:kubejs-238086:5853326`，来源仓库为 `https://www.cursemaven.com`；文件版本和文件 ID 仅适用于已核对的对应 Minecraft/加载器组合。
- KubeJS 1.21.1 NeoForge：`curse.maven:kubejs-238086:8083208`，来源仓库为 `https://www.cursemaven.com`；添加依赖前仍需重新确认文件状态和目标版本。

## 维护限制

- 不把用户自己的 CurseForge 项目写入本文件；自己的项目只在具体项目的 Gradle、元数据或发布记录中维护。
- 不把本文件中的坐标模板直接当成任意 Minecraft 版本的固定坐标；每次使用都要重新核对版本、加载器、发布类型和文件是否存在。
- 发现项目 ID、slug、Maven 坐标或来源发生变化时，不要静默覆盖旧记录；保留旧值并写明变更原因和核对证据。

## HP End Expansion 开发依赖核对（2026-09-05）

- Jade：项目 ID 324717，https://www.curseforge.com/minecraft/mc-mods/jade 。现有 libs/Jade-1.21.1-NeoForge-15.10.5.jar（文件名带中文前缀）通过 JAR 内 neoforge.mods.toml 核对 modId=jade 和 NeoForge 要求；复用当前本地依赖，不重复添加 Maven JAR。
- JEI：项目 ID 238222，文件 ID 7391682，https://www.curseforge.com/minecraft/mc-mods/jei/files/7391682 ，坐标 curse.maven:jei-238222:7391682，CurseMaven 仓库 https://www.cursemaven.com 。官方页确认 19.27.0.336、Release、2025-12-29、Minecraft 1.21.1 NeoForge；两个工作目录 compileJava processResources 均通过。JAR 的 Minecraft 范围为 [1.21, 1.21.1)，已核对本地 FML 4.0.42 源码 VersionSupportMatrix 对 1.21.1 接受 1.21 的兼容规则。

- 同日补充：HP End Expansion 两个工作树的 Jade 文件统一重命名为 libs/Jade-1.21.1-NeoForge-15.10.5.jar，移除中文及表情符号前缀以避开本机 Java 工具路径编码错误；重命名前后 SHA256 一致。后续引用使用此纯 ASCII 文件名。


## Alex 洞穴开发依赖（2026-09-10 核对）

- Alex’s Caves：项目 924854，文件 5848216，2.0.2，Minecraft 1.20.1 Forge；`curse.maven:alexs-caves-924854:5848216`；https://www.curseforge.com/minecraft/mc-mods/alexs-caves/files/5848216
- Citadel：项目 331936，文件 6702068，2.6.2，Minecraft 1.20.1 Forge；`curse.maven:citadel-331936:6702068`；https://www.curseforge.com/minecraft/mc-mods/citadel/files/6702068
- GeckoLib：项目 388172，文件 7025129，4.8.2，Minecraft 1.20.1 Forge；`curse.maven:geckolib-388172:7025129`；https://www.curseforge.com/minecraft/mc-mods/geckolib/files/7025129
- GeckoLib（2026-11-02 补充，Bosses Rise Intro Skipper 核对）：4.8.3 Minecraft 1.20.1 Forge 文件 7553267，`curse.maven:geckolib-388172:7553267`；4.9.2 Minecraft 1.21.1 NeoForge 文件 8350073，`curse.maven:geckolib-388172:8350073`；CFWidget 文件列表确认 Release，CurseMaven 下载与原始 JAR SHA256 一致，两个版本 build 通过。
- 仓库：https://www.cursemaven.com 。以上通过文件页、原始 JAR 元数据和 Forge 47.4.23 / Java 17 构建核对。Alex’s Caves 2.0.2 原始元数据要求 Citadel >=2.6.0。
