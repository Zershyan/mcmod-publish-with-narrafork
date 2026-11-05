# GenUI 表单模板

四个数据驱动的表单，共用同一套用法：复制 `.tsx` 和对应的 `.data.example.ts` 到 `.narrafork/gen_ui/<名称>/`，把后者改名成 `data.ts`，只改数据，`GenUI show` 该目录。

```bash
mkdir -p .narrafork/gen_ui/<名称>
cp assets/forms/FormFull.tsx .narrafork/gen_ui/<名称>/App.tsx
cp assets/forms/FormFull.data.example.ts .narrafork/gen_ui/<名称>/data.ts
```

**不要把 `App.tsx` 改名成别的** —— GenUI 只认这个文件名。

## 有哪几个

| 文件 | 用途 | 何时用 |
|---|---|---|
| `FormBuild.tsx` | 逐行填「分支 + 版本号」，可选回填 | 装了 `zershyan-mcmod-style`，发布流程的**第一步** |
| `FormFull.tsx` | CurseForge 与百科的全部字段 | 第一次发布 |
| `FormRelease.tsx` | 只填 JAR、版本号、更新说明 | 已有项目发新版本 |
| `FormConfirm.tsx` | 把将要上传/提交的内容整块摆出来确认 | 上传或提交前的最后一道门 |

`FormConfirm` 依赖前三个的产出，不单独使用。

## 各表单的数据

文件名的 `.data.example.ts` 后缀对应各自的 `data.ts`。

### FormBuild.data.example.ts

| 字段 | 内容 |
|---|---|
| `projectName` | 显示在标题 |
| `branches` | 分支候选（Autocomplete，可自由输入） |
| `rows` | 初始行，每行 `{ branch, version }` |
| `writeBack` | 默认是否勾选「回填至项目」 |
| `hints` | 覆盖默认提示文案 |

提交结果：`{ rows: [{branch, version}], writeBack }`。

勾了回填就把各行写进对应分支的 `gradle.properties`：

```bash
python scripts/project/version.py master=0.0.1 1.21.1=1.0.0
```

脚本会检查工作区干净、逐分支改完回到原分支，**只改文件不提交**。

### FormFull.data.example.ts

见文件内注释。核心是 `defaults`（各字段的 placeholder，即调研值）和 `versions` / `authors` / `entries` / `dependencies`。

### FormRelease.data.example.ts

见文件内注释。核心是 `project`、`released`（已发布摘要）、`versions`（待发布）。

### FormConfirm.data.example.ts

见文件内注释。核心是 `project`、`releases`（每个「MC 版本 × 加载器」一条）、`wiki`（不发百科时整段删掉）、`warnings`。

## 公共约定

- 所有调研值放 **placeholder**（灰色提示），用户留空就按提示值执行
- **枚举类字段要实选**，否则用户看不出会提交什么
- 同一行的字段保持相同的描述行数，否则控件对不齐
- 文件选择用 `FileButton`，沙箱里只能拿到文件名
