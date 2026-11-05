"""生成 CurseForge 建项目的控制台脚本。

用法：
    python create_project.py <项目资料.json> [输出.js]

资料格式见同目录的 project.example.json。相对路径以 JSON 所在目录为基准。
"""
import argparse
import base64
import io
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE / 'create_project_template.js'


def load_icon(path: Path) -> str:
    """图标转 base64；超过 400px 缩到 400×400 控制脚本体积。"""
    try:
        from PIL import Image
        image = Image.open(path).convert('RGBA')
        if max(image.size) > 400:
            image = image.resize((400, 400), Image.LANCZOS)
        buffer = io.BytesIO()
        image.save(buffer, 'PNG', optimize=True)
        return base64.b64encode(buffer.getvalue()).decode()
    except ImportError:
        return base64.b64encode(path.read_bytes()).decode()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('config')
    parser.add_argument('output', nargs='?')
    parser.add_argument('--no-icon', action='store_true',
                        help='不把图标塞进脚本，体积小很多，图标另行上传')
    parser.add_argument('--step', action='store_true',
                        help='单步模式：每次只推进一个页面，适合会被超时打断的自动化工具')
    args = parser.parse_args()

    config_path = Path(args.config).resolve()
    base = config_path.parent
    config = json.loads(config_path.read_text(encoding='utf-8'))
    resolve = lambda p: Path(p) if Path(p).is_absolute() else base / p

    description = resolve(config['description']).read_text(encoding='utf-8')
    icon = ''
    if config.get('icon') and not args.no_icon:
        icon = load_icon(resolve(config['icon']))

    data = {
        'name': config['name'],
        'summary': config['summary'],
        'license': config.get('license', ''),
        'dropdowns': config.get('dropdowns', []),
        'distribution': config.get('distribution', 'Allow distribution to 3rd party'),
        'allowComments': config.get('allowComments', True),
        'description': description,
        'iconBase64': icon,
        # 默认自动点创建按钮；启用前必须先用交互式提问向用户确认
        'autoCreate': bool(config.get('autoCreate', True)),
        'singleStep': bool(config.get('singleStep', False)) or args.step,
    }
    if not 1 <= len(data['summary']) <= 256:
        raise SystemExit(f'简介长度 {len(data["summary"])}，CurseForge 限制 256 字符')

    script = (TEMPLATE.read_text(encoding='utf-8')
              .replace('__TITLE__', data['name'])
              .replace('__DATA__', json.dumps(data, ensure_ascii=False)))
    output = Path(args.output) if args.output else base / 'cf_create_project_fill.js'
    output.write_text(script, encoding='utf-8', newline='\n')
    print(f'已生成 {output}（{len(script) // 1024} KB），node --check 后再投入浏览器')


if __name__ == '__main__':
    main()
