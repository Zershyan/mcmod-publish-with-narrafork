# 版本发布表单

已经在 CurseForge 有项目、只发新版本时用这个。首次发布用 [form-full](../form-full/README.md)。

## 用法

```bash
mkdir -p .narrafork/gen_ui/<名称>
cp assets/form-release/App.tsx .narrafork/gen_ui/<名称>/App.tsx
cp assets/form-release/data.example.ts .narrafork/gen_ui/<名称>/data.ts
```

改 `data.ts`，然后 GenUI show 该目录。

## data.ts 字段

| 字段 | 内容 |
|---|---|
| `project` | 项目名、slug、projectId、许可证；从 `curseforge/project.json` 来 |
| `released` | 已发布版本摘要，只做展示；从 `curseforge/remote-files-*.json` 取 |
| `mcVersions` | Game Versions API 拉到的版本列表；省略时用模板内置的兜底候选 |
| `versions` | 待发布的版本 |

每个版本条目：

| 字段 | 内容 |
|---|---|
| `modVersion` | 构建脚本里的实际 `version`，不要自己拼 |
| `mcVersions` | 该版本支持的 MC 版本，可多个 |
| `loaders` | 加载器，可多个 |
| `javaVersion` | CurseForge 版本标签里的 Java 版本 |
| `releaseType` | release / beta / alpha |
| `env` | 双端 / 仅客户端 / 仅服务端 |
| `changelog` | 留空则按 git 提交记录整理 |

## 提交后

表单给的是「要发哪些版本组合」。真正上传时，每个「MC 版本 × 加载器」组合对应一个文件，脚本会拆开逐个校验 sha256 并上传。

清单写进 `curseforge/release-manifest.json`，格式见 [CurseForge](../../references/curseforge.md#上传)。
