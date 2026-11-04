# CurseForge 创建项目填表脚本生成器
# 用法：python build_fill_js.py <项目资料.json> [输出.js]
# 项目资料 JSON 字段见同目录 project.example.json；相对路径以 JSON 所在目录为基准
import base64
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


# 读取图标，超过 400px 时缩放到 400×400 以控制脚本体积
def load_icon(path):
    try:
        from PIL import Image
        image = Image.open(path).convert("RGBA")
        if max(image.size) > 400:
            image = image.resize((400, 400), Image.LANCZOS)
        buffer = io.BytesIO()
        image.save(buffer, "PNG", optimize=True)
        return base64.b64encode(buffer.getvalue()).decode()
    except ImportError:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()


def main():
    if len(sys.argv) < 2:
        sys.exit("用法：python build_fill_js.py <项目资料.json> [输出.js]")
    config_path = os.path.abspath(sys.argv[1])
    base = os.path.dirname(config_path)
    with open(config_path, encoding="utf-8") as f:
        config = json.load(f)

    # 解析描述与图标路径
    resolve = lambda p: p if os.path.isabs(p) else os.path.join(base, p)
    with open(resolve(config["description"]), encoding="utf-8") as f:
        description = f.read()
    icon = load_icon(resolve(config["icon"])) if config.get("icon") else ""

    # 组装注入数据
    data = {
        "name": config["name"],
        "summary": config["summary"],
        "license": config.get("license", ""),
        "dropdowns": config.get("dropdowns", []),
        "distribution": config.get("distribution", "Allow distribution to 3rd party"),
        "allowComments": config.get("allowComments", True),
        "description": description,
        "iconBase64": icon,
        # 为 true 时脚本会自己点最后的创建按钮；默认留给人确认
        "autoCreate": bool(config.get("autoCreate", False)),
    }
    if not 1 <= len(data["summary"]) <= 256:
        sys.exit(f"summary 长度 {len(data['summary'])}，CF 限制 256 字符")

    # 填充模板并输出
    with open(os.path.join(HERE, "template.js"), encoding="utf-8") as f:
        template = f.read()
    script = template.replace("__TITLE__", config["name"]).replace("__DATA__", json.dumps(data, ensure_ascii=False))
    out = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else os.path.join(base, "cf_create_project_fill.js")
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(script)
    print(f"已生成 {out}（{len(script) // 1024} KB）")


if __name__ == "__main__":
    main()
