# 构建前确认表单

只用于装了 `zershyan-mcmod-style` 的工程。问两件事：这次的 `mod_version`，以及要发布哪些分支。

## 为什么单独一步

`mod_version` 是模组版本，不是构建编号，只能由人按发布计划给出；分支决定这次要构建和上传几份产物。这两项填错，后面全部白做。

**构建由用户自己触发**，不由 agent 跑 —— 构建环境和时间由用户掌握，agent 只负责用产物。

## 用法

```bash
mkdir -p .narrafork/gen_ui/build
cp assets/form-build/App.tsx .narrafork/gen_ui/build/App.tsx
cp assets/form-build/data.example.ts .narrafork/gen_ui/build/data.ts
```

`branches` 从工程读：

```bash
git branch -a | sed 's|remotes/origin/||;s|^[* ]*||' | sort -u
```

`currentVersion` 取 `gradle.properties` 的 `mod_version`，作为输入框的初始值。

改完 `data.ts` 后 GenUI show 该目录。

## data.ts 字段

| 字段 | 内容 |
|---|---|
| `projectName` | 显示在标题，方便用户确认是哪个工程 |
| `currentVersion` | `mod_version` 当前值，作为输入框初始值 |
| `branches` | 分支列表，多选候选 |
| `defaultBranches` | 默认勾选的分支 |
| `hints` | 需要特别说明时覆盖默认提示 |

## 用户提交之后

1. 用户自己切到各分支运行 `./gradlew build`
2. 构建完成后告诉 agent
3. agent 按分支逐个检查 `build/libs`，**只取文件名不带 `+build.N` 的 jar**
4. 用这些产物继续上传

如果某个分支只剩带编号的包，说明那边还没跑普通构建，停下来问用户，不要拿 alpha 包顶替。
