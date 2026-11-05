# mcmod-publish-with-narrafork

把 Minecraft 模组发布到 CurseForge，可选同步到 MC百科：读工程事实、判断项目是否存在、构建正式包、创建或复用 CF 项目、上传版本文件、填写百科条目与资料、处理登录与验证码、跟进审核退回。

要执行发布，直接看 [SKILL.md](SKILL.md)——开局一条 `preflight.py`，之后按输出走。这份 README 是给维护者和第一次接触的人看的。

## 入口

先跑一条命令，后面照输出走：

```bash
python scripts/preflight.py
```

| 文档 | 内容 |
|---|---|
| [SKILL.md](SKILL.md) | 执行手册：开局一条命令，然后七步走完 |
| [产物与数据流](references/workflow.md) | 每一步留下什么文件、下一步读什么 |
| [CurseForge](references/curseforge.md) | 令牌、建项目、上传、依赖、状态语义 |
| [MC百科](references/mcmod.md) | 登录、提交接口、字段结构、审核 |
| [字段来源](references/field-sources.md) | 每个字段从哪取 |
| [踩坑记录](references/pitfalls.md) | 症状、原因、正确做法 |
| [与 zershyan-mcmod-style 同装时](references/with-mcmod-style.md) | 工程符合 style 规范时的产物、版本与资源约定 |

## 目录

```
SKILL.md
references/          流程与平台细节
assets/
  forms/             四个 GenUI 表单模板，用途见其 README
  mcmod-enums.json   百科提交的枚举对照
  content-templates.md  百科正文模板
scripts/
  preflight.py       开局体检：工程事实、构建规范、凭据、下一步
  cf/                CurseForge：请求封装、上传、清单生成、建项目、补链接
  mcmod/             百科：cookie、作者查询、条目提交
  mcmod/console/     百科控制台脚本模板（没有 cookie 时的兜底）
  project/           工程侧：版本号回填、占位图标生成与样式存档（.narrafork/icon-style.json）
```

百科的提交通道按环境能力降级：有 browsermcp 就在页面里跑控制台脚本（不需要 cookie），有 `Browser` 工具就 dump cookie 走 `submit.py`，都没有就把脚本给用户手动粘贴。细节见 SKILL.md 第 6 步。

## 表单

四个数据驱动的 GenUI 模板，只改 `data.ts`，`App.tsx` 不动。用法与字段见 [assets/forms/README.md](assets/forms/README.md)，流程约束（必须带 `wait`、缺工具怎么降级）见 SKILL.md 开局段。

```bash
mkdir -p .narrafork/gen_ui/<名称>
cp assets/forms/FormFull.tsx .narrafork/gen_ui/<名称>/App.tsx
cp assets/forms/FormFull.data.example.ts .narrafork/gen_ui/<名称>/data.ts
```

改完 `data.ts` 用 `GenUI render({path: 该目录, wait: true})` 打开。

## 依赖

```bash
python -m pip install --target .narrafork/pylibs curl_cffi
python -m pip install --target .narrafork/pylibs websocket-client   # 只有从 CDP 读 cookie 时需要
python -m pip install Pillow                                        # 生成占位图标、处理封面
```

脚本会自己找 `.narrafork/pylibs`（`cfhttp.py` 里探测），不用手动设 `CF_HTTP_RUNTIME`。`curl_cffi` 用来伪装 TLS 指纹，普通客户端会被 Cloudflare 拦。

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
