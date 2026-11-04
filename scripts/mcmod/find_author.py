"""按名字查百科作者 ID。

百科的作者搜索框只认名字（或作者 ID），提交条目时用的是作者 ID。
这个接口不需要登录：

    POST https://www.mcmod.cn/object/CommonSelect/
    data = {"key": "作者名", "type": "author"}

用法：
    python find_author.py Zershyan
    python find_author.py Zershyan 折戏鸢 --json
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts' / 'cf-http'))
from browser_http import requests

API = 'https://www.mcmod.cn/object/CommonSelect/'
ROW = re.compile(
    r'<tr data-id="(\d+)"><td><b>(.*?)</b>(?:\s*-\s*<i[^>]*>(.*?)</i>)?',
    re.S,
)


def strip_tags(text: str) -> str:
    return re.sub(r'<[^>]+>', '', text or '').strip()


def find(name: str) -> list[dict]:
    session = requests.Session(impersonate='chrome')
    response = session.post(
        API,
        data={'data': json.dumps({'key': name, 'type': 'author'})},
        headers={'Referer': 'https://www.mcmod.cn/class/add/', 'X-Requested-With': 'XMLHttpRequest'},
        timeout=30,
    )
    payload = response.json()
    if payload.get('state') != 0:
        # state 109 表示没有匹配结果
        return []
    return [
        {'id': m.group(1), 'name': strip_tags(m.group(2)), 'aliases': strip_tags(m.group(3))}
        for m in ROW.finditer(payload.get('html', ''))
    ]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('names', nargs='+', help='作者名，可多个')
    parser.add_argument('--json', action='store_true', help='只输出 JSON，便于写入配置')
    args = parser.parse_args()

    result = {}
    for name in args.names:
        hits = find(name)
        result[name] = hits
        if not args.json:
            if not hits:
                print(f'{name}: 没有匹配')
            for hit in hits:
                extra = f'（{hit["aliases"]}）' if hit['aliases'] else ''
                print(f'{name}: {hit["id"]}  {hit["name"]}{extra}')

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
