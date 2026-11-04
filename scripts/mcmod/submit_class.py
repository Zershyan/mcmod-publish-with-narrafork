"""提交 MC百科模组条目。

用法：
    python submit_class.py <配置.json> --dry-run    # 只打印将要提交的 JSON
    python submit_class.py <配置.json>              # 真正提交

配置里用页面上的中文文本填写，脚本按 assets/mcmod-enums.json 转成提交代码。
cookie 从 .narrafork/mcmod-cookie.txt 读取。
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts' / 'cf-http'))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from browser_http import requests
from find_author import find as find_author

API = 'https://event.mcmod.cn/action/edit/doEdit/'
COOKIE_FILE = ROOT / '.narrafork' / 'mcmod-cookie.txt'
ENUMS = json.loads((ROOT / 'assets' / 'mcmod-enums.json').read_text(encoding='utf-8'))


def code_of(group: str, label: str) -> str:
    """把页面文本反查成提交用的代码值。"""
    table = ENUMS[group]
    for code, text in table.items():
        if text == label or text.split(' ')[0] == label:
            return code
    raise SystemExit(f'{group} 里没有「{label}」，可选：{", ".join(table.values())}')


def indexed(values) -> dict:
    """勾选、标签这类字段要求 {序号: 值} 形式，序号只是下标。"""
    return {str(i): v for i, v in enumerate(values)} if values else {}


def build(cfg: dict) -> dict:
    data = {
        'name': cfg['name'],
        'ename': cfg.get('ename', ''),
        'intro': cfg.get('intro', ''),
        'modid': cfg['modid'],
        'cfprojectid': str(cfg.get('cfprojectid', '')),
        'mrprojectid': str(cfg.get('mrprojectid', '')),
        'activity': {},
        'category': indexed([code_of('categoryCore', c) if c in ENUMS['categoryCore'].values()
                             else code_of('categoryExtra', c) for c in cfg.get('category', [])]),
        'platform': indexed([code_of('platform', p) for p in cfg.get('platform', ['JAVA版 (JAVA Edition)'])]),
        'api': indexed([code_of('api', a) for a in cfg.get('api', [])]),
        'mode-1': indexed([code_of('mode', cfg.get('mode1', '需装'))]),
        'mode-2': indexed([code_of('mode', cfg.get('mode2', '需装'))]),
        'status': indexed([code_of('status', cfg.get('status', '活跃'))]),
        'source': indexed([code_of('source', cfg.get('source', '开源'))]),
        'content': cfg.get('content', ''),
    }
    if cfg.get('tags'):
        data['tags'] = indexed(cfg['tags'])
    if cfg.get('links'):
        data['link'] = {
            str(i): {
                'title': link.get('title', ''),
                'custom': link.get('custom', ''),
                'href': link.get('href', ''),
                'text': link.get('text', ''),
            }
            for i, link in enumerate(cfg['links'])
        }
    if cfg.get('authors'):
        links = {}
        for i, author in enumerate(cfg['authors']):
            author_id = str(author.get('id') or '')
            if not author_id and author.get('name'):
                # 只知道名字时先查作者 ID，搜索接口免登录
                hits = find_author(author['name'])
                if not hits:
                    raise SystemExit(f'找不到作者「{author["name"]}」')
                author_id = hits[0]['id']
                print(f'作者 {author["name"]} -> ID {author_id}')
            if not author_id:
                continue
            roles = author.get('roles') or [author.get('role', '所有者')]
            codes = [r if r in ENUMS['role'] else code_of('role', r) for r in roles]
            links[str(i)] = {'select': codes, 'id': author_id}
        data['author'] = {'link': links, 'add': {}}
    return {
        'action': cfg.get('action', 'class_add'),
        'edit-id': '0',
        'class-id': str(cfg.get('classId', '0')),
        'redo-id': str(cfg.get('redoId', '0')),
        'class-data': data,
    }


def submit(payload: dict) -> dict:
    if not COOKIE_FILE.exists():
        raise SystemExit(f'缺少 cookie 文件：{COOKIE_FILE}')
    session = requests.Session(impersonate='chrome')
    session.headers['Cookie'] = COOKIE_FILE.read_text(encoding='utf-8').strip()
    response = session.post(
        API,
        data={'data': json.dumps(payload, ensure_ascii=False)},
        headers={'Referer': 'https://www.mcmod.cn/class/add/', 'X-Requested-With': 'XMLHttpRequest'},
        timeout=60,
    )
    try:
        return response.json()
    except ValueError:
        raise SystemExit(f'返回了非 JSON：{response.text[:200]}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('config')
    parser.add_argument('--dry-run', action='store_true', help='只打印提交内容，不真正发送')
    args = parser.parse_args()

    cfg = json.loads(Path(args.config).read_text(encoding='utf-8'))
    payload = build(cfg)
    text = json.dumps(payload, ensure_ascii=False, indent=1)

    if args.dry_run:
        print(text)
        print('\n（dry-run，未提交）')
        return

    print(text)
    result = submit(payload)
    print('\n返回：', json.dumps(result, ensure_ascii=False))
    if result.get('state') == 0:
        print('提交成功，地址：', result.get('url', '(无)'))
    else:
        raise SystemExit(f'提交失败：state={result.get("state")}')


if __name__ == '__main__':
    main()
