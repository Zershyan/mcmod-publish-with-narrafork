# mcmod-publish-with-narrafork

把 Minecraft 模组发布到 CurseForge 与 MC百科：读工程事实、判断项目是否存在、上传 JAR、填写百科条目、处理登录与验证码、核对审核附言。

## 入口

| 文档 | 内容 |
|---|---|
| [SKILL.md](SKILL.md) | 走哪条路、六个阶段、硬约束 |
| [完整流程](references/workflow.md) | 七个步骤的判定条件与产物 |
| [CurseForge](references/curseforge.md) | 令牌、上传、依赖、状态语义 |
| [MC百科](references/mcmod.md) | 登录、提交接口、字段结构、审核 |
| [字段来源](references/field-sources.md) | 每个字段从哪取 |
| [踩坑记录](references/pitfalls.md) | 症状、原因、正确做法 |

## 目录

```
SKILL.md
references/          流程与平台细节
assets/
  form-full/         首次发布的完整配置表单
  form-release/      只发新版本的简化表单
  mcmod-enums.json   百科提交的枚举对照
  content-templates.md  百科正文模板
scripts/
  cf/                CurseForge：请求封装、上传、建项目脚本生成
  mcmod/             百科：cookie、作者查询、条目提交
```

## 表单

两个 GenUI 模板，数据驱动的：`App.tsx` 通用，项目差异只写 `data.ts`。

```bash
mkdir -p .narrafork/gen_ui/<名称>
cp assets/form-full/App.tsx .narrafork/gen_ui/<名称>/App.tsx
cp assets/form-full/data.example.ts .narrafork/gen_ui/<名称>/data.ts
```

改 `data.ts` 后 GenUI show 该目录。详见各目录的 `README.md`。

## 运行依赖

```bash
python -m pip install --target .narrafork/pylibs curl_cffi
python -m pip install --target .narrafork/pylibs websocket-client   # 只有从 CDP 读 cookie 时需要
export CF_HTTP_RUNTIME=$PWD/.narrafork/pylibs
export PYTHONPATH=$PWD/.narrafork/pylibs
```

`curl_cffi` 用于所有 CurseForge 请求（Cloudflare 按 TLS 指纹拦截普通客户端）。

## 凭据

| 凭据 | 来源 | 存放 |
|---|---|---|
| CurseForge 令牌 | `https://authors.curseforge.com/#/settings/api-tokens` | 环境变量 `CURSEFORGE_API_TOKEN` |
| 百科 cookie | 浏览器登录后经 CDP 导出 | `.narrafork/mcmod-cookie.txt` |

两者都不进 git。`.narrafork/` 已在 `.gitignore` 里。

## 维护

- 平台改动时先更新 `references/`，再同步脚本；不要只改一处
- 枚举、接口、字段结构都标注了实测时间，失效时按文档里的方法重新取
- 未实测的能力在文档里明确标注，不写成既有保证
