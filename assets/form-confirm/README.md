# 提交前确认表单

上传和提交之前，把即将执行的内容整块摆给用户看，允许改关键项。这是对外发布前的最后一道门。

## 用法

```bash
mkdir -p .narrafork/gen_ui/confirm
cp assets/form-confirm/App.tsx .narrafork/gen_ui/confirm/App.tsx
cp assets/form-confirm/data.example.ts .narrafork/gen_ui/confirm/data.ts
```

把生成好的清单内容填进 `data.ts`，然后 GenUI show 该目录。

## data.ts 字段

| 字段 | 内容 |
|---|---|
| `project` | 项目名、projectId、slug |
| `releases` | 每个「MC 版本 × 加载器」一条，含版本名、发布类型、Java 版本、JAR 路径、更新说明 |
| `wiki` | 百科提交内容；不发布百科时**整段删掉**，页签会自动消失 |
| `warnings` | 需要提醒用户的点，显示成橙色提示条 |

用户在表单里能改的只有版本显示名、更新说明和百科正文 —— 其余是只读展示，避免误改成不一致的状态。

## 什么时候用

| 场景 | 是否用 |
|---|---|
| 第一次发布，或一次发多个版本 | 用 |
| 只发一个版本，用户已在 form-release 里确认过 | 可以跳过，直接用 release-manifest |
| 只更新百科 | 用，只保留 wiki 段 |

## 确认之后

用户点「确认并执行」后，按 `release-manifest.json` 上传、按 `mod-config.json` 提交百科。这一步之后就产生对外发布行为，之前的表单只是配置。
