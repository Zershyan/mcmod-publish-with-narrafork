# mcmod-publish-with-narrafork

从 Minecraft 模组工程发布到 CurseForge 与 MC百科。所有信息取自 mod 工程本身，工程里没有的才询问用户。

## 阅读入口

- [SKILL.md](SKILL.md)：流程总览、总原则、执行方式。
- [字段来源总表](references/sources.md)：每个字段从哪取，**先看这个**。
- [正文模板](references/content-templates.md)：百科各类资料的段落结构。

## 阶段

| 阶段 | 做什么 | 文档 |
|---|---|---|
| 1 | 读工程事实 | [stage1-project.md](references/stage1-project.md) |
| 2 | 新建 CF 项目 | [stage2-cf-project.md](references/stage2-cf-project.md) |
| 3 | 发布 CF 版本 | [stage3-cf-release.md](references/stage3-cf-release.md) |
| 4 | 新建百科模组条目 | [stage4-wiki-project.md](references/stage4-wiki-project.md) |
| 5 | 创建百科资料条目 | [stage5-wiki-entries.md](references/stage5-wiki-entries.md) |
| 6 | 核对审核 | [stage6-review.md](references/stage6-review.md) |

## 脚本

| 目录 | 用途 |
|---|---|
| `scripts/cf-http/` | CF API 请求封装（`curl_cffi` 模拟 Chrome）与统一上传脚本 |
| `scripts/cf-create-fill/` | CF 创建项目页的填表脚本生成器与页面结构探针 |
| `scripts/mcmod/` | 百科条目正文/图标生成器、控制台提交模板、图标导出器示例 |

## 维护约定

- 字段来源变化时先改 `references/sources.md`，再同步脚本。
- 页面结构、选择器变化时同步改脚本与对应 stage 文档，不留两处不一致。
- 记录实测日期与验证方式；未实测的改动标明「待实测」，不写成既有保证。
