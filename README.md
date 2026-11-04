# mcmod-publish-with-narrafork

Minecraft 模组的对外发布与资料提交 skill：CurseForge 项目创建、版本上传、CurseMaven 依赖来源登记，以及 MC百科（mcmod.cn）模组条目创建、资料正文撰写、图标制作、批量提交与审核核对。

## 阅读入口

- [SKILL.md](SKILL.md)：两条流水线的关系、总原则、执行方式与任务路由。
- [通用约定](references/shared.md)：目录、版本命名、事实来源优先级、汇报格式。

## 模块

| 模块 | 入口 | 内容 |
|---|---|---|
| CurseForge 发布 | [upload.md](references/curseforge/upload.md) | Upload API、Cloudflare 挑战页处理、文件状态与恢复 |
| CurseForge 项目 | [project.md](references/curseforge/project.md) | 新建项目、页面结构、填表脚本 |
| 依赖来源 | [dependencies.md](references/curseforge/dependencies.md) | 已核对的第三方模组 CF 项目 ID 与 CurseMaven 坐标 |
| 百科模组 | [project.md](references/mcmod/project.md) | 创建模组条目、页面控件坑点 |
| 数据导出 | [export.md](references/mcmod/export.md) | 运行时导出与静态解析 |
| 正文 | [content.md](references/mcmod/content.md)、[content-templates.md](references/mcmod/content-templates.md) | 通用写作规范与分类模板 |
| 图标 | [icons.md](references/mcmod/icons.md) | 平面/3D/实体图标与抽象资料规则 |
| 提交与审核 | [submit.md](references/mcmod/submit.md) | 批量提交、再编辑、审核核对 |

## 脚本

| 目录 | 用途 |
|---|---|
| `scripts/cf-http/` | `curl_cffi` 模拟 Chrome 指纹的请求封装与统一上传脚本 |
| `scripts/cf-create-fill/` | CF 创建项目页的填表脚本生成器与页面结构探针 |
| `scripts/mcmod/` | 百科条目正文/图标生成器、控制台提交模板、图标导出器示例 |

## 维护约定

- 页面结构、选择器和 API 行为变化时，同步改脚本与对应 reference，不留下两处描述不一致。
- 依赖来源表只在核对成功后追加，保留旧值与变更原因，不静默覆盖。
- 记录实测日期与验证方式；未实测的改动标明「待实测」，不写成既有保证。
