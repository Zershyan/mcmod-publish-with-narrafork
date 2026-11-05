# 与 zershyan-mcmod-style 同装时

工程通常同时装了两套 skill：`zershyan-mcmod-style` 管开发和构建，本 skill 管发布。两者对**产物命名**和**资源位置**有约定，发布时必须按工程的实际情况来，不能套用通用假设。

## 怎么判断

```bash
ls ~/.agents/skills/zershyan-mcmod-style/ 2>/dev/null && echo 已安装
```

装了才适用本文；没装就按 [字段来源](field-sources.md) 的通用规则走，不要凭这条推断。

## 产物：只发不带构建编号的 jar

`versioning.md` 规定两种构建：

| 构建 | 最终 jar 名 | 性质 |
|---|---|---|
| `build` | `examplemod-0.0.1-1.21.1.jar` | 正式包 |
| `buildAlpha` | `examplemod-0.0.1-1.21.1+build.5.jar` | 带编号的测试构建 |

**发布只用文件名不带 `+build.N` 的那个。**

- 两种都在：选不带编号的
- 只剩带编号的：说明还没跑过普通 `build`，先构建，**不要拿 alpha 包顶替**
- `build/libs/obfuscate/`、`build/libs/origin/` 是中间产物，都不发

包内版本两种都带编号，所以「文件名不带编号」不影响 CF 上的显示名。

## 版本号

`mod_version` 只写模组版本（如 `0.0.1`），MC 版本单独由 `minecraft_version` 维护。Gradle 的 `version` 是 `<mod_version>-<minecraft_version>+build.<N>`。

发布时的 `displayName` 用工程 `version` 原值，不要自己拼 `MC-加载器-名字-版本`，也不要把 `+build.N` 去掉。

## 语言文件

Datagen 输出在 `src/generated/resources/assets/<modid>/lang/`，语言由 `<ModId>Lang` 基类聚合，注册项名称在 `RegistryLang`。百科的名称、英文名都从这里取。

改动过的语言要先跑：

```bash
./gradlew runData
```

再读文件，不要读旧的生成结果。

## 构建命令

工程默认用 `buildAlpha`（会递增编号并回写属性）。发布前要正式包时：

```bash
./gradlew build
```

它会产出不带编号的最终包，同时把带编号的原包归档进 `build/libs/origin/`。

改了构建逻辑或资源处理时，按 `build.md` 的要求核对产物本身，不能只看任务退出码。

## 不要做的

- 不要为了「版本号好看」去改 `mod_version` 或 Gradle `version` 的格式
- 不要把 `+build.N` 从 `displayName` 里抹掉，那是真实版本
- 不要清理 `build/libs` 里的历史产物，工程默认保留
- 不要在没有 `api/` 包的工程里假设它有，依赖声明以 `build.gradle` 为准
