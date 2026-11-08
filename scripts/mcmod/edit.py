"""编辑 MC 百科已有的模组条目。

用法：
    python edit.py --class-id 30945 --payload class-data.json
    python edit.py --class-id 30945 --payload class-data.json --content-file new.html
    python edit.py --class-id 30945 --payload class-data.json --dry-run

payload 可以是整份提交体（带 class-data），也可以只是 class-data；
--content-file 覆盖 class-data.content。
cookie 默认读当前目录的 .narrafork/mcmod-cookie.txt，内容是浏览器里的 document.cookie 原文。
"""
import argparse
import json
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from deps import ensure_deps

ensure_deps()

API = 'https://event.mcmod.cn/action/edit/doEdit/'
DRAFT_API = 'https://event.mcmod.cn/action/edit/doSave/'


def ssl_context():
    """系统 Python 常常没有 CA 包，有 certifi 就用它。"""
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except Exception:
        return ssl.create_default_context()


def load_payload(path: str, class_id: str) -> dict:
    """补齐外层字段：doEdit 靠 action / class-id / edit-id / redo-id 定位条目。"""
    data = json.loads(Path(path).read_text(encoding='utf-8'))
    if 'class-data' in data:
        data.setdefault('class-id', str(class_id))
        return data
    return {
        'action': 'class_add',
        'edit-id': '0',
        'class-id': str(class_id),
        'redo-id': '0',
        'class-data': data,
    }


def main():
    parser = argparse.ArgumentParser(description='提交 MC 百科模组条目的编辑')
    parser.add_argument('--class-id', required=True, help='模组条目 ID，例如 30945')
    parser.add_argument('--payload', required=True, help='class-data JSON 文件')
    parser.add_argument('--content-file', help='HTML 正文文件，覆盖 payload 里的 content')
    parser.add_argument('--cookie', default='.narrafork/mcmod-cookie.txt', help='cookie 文件路径')
    parser.add_argument('--dry-run', action='store_true', help='只打印提交体，不发送')
    parser.add_argument('--draft', action='store_true',
                        help='只保存草稿（doSave），不送审；参数取自页面，未端到端实测')
    args = parser.parse_args()

    data = load_payload(args.payload, args.class_id)
    if args.content_file:
        data['class-data']['content'] = Path(args.content_file).read_text(encoding='utf-8').strip()

    if args.draft:
        body = urllib.parse.urlencode({
            'actionType': 'class_edit',
            'actionID': str(args.class_id),
            'data': json.dumps(data, ensure_ascii=False),
        }).encode('utf-8')
        api = DRAFT_API
    else:
        body = urllib.parse.urlencode({
            'data': json.dumps(data, ensure_ascii=False),
        }).encode('utf-8')
        api = API

    if args.dry_run:
        print(json.dumps(data, ensure_ascii=False, indent=2)[:2000])
        print('\n（dry-run，未提交）')
        return 0

    cookie = Path(args.cookie)
    if not cookie.exists():
        sys.exit(f'缺少 cookie 文件：{cookie}（内容是浏览器里的 document.cookie）')

    request = urllib.request.Request(api, data=body, method='POST', headers={
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': cookie.read_text(encoding='utf-8').strip(),
        'Origin': 'https://www.mcmod.cn',
        'Referer': 'https://www.mcmod.cn/',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    })
    try:
        with urllib.request.urlopen(request, timeout=30, context=ssl_context()) as response:
            text = response.read().decode('utf-8')
    except urllib.error.HTTPError as error:
        detail = error.read().decode('utf-8', 'replace')[:500]
        sys.exit(f'提交失败：HTTP {error.code}\n{detail}')
    except Exception as error:
        sys.exit(f'提交失败：{error}')

    try:
        result = json.loads(text)
    except ValueError:
        sys.exit(f'返回了非 JSON（多半是登录态失效）：{text[:300]}')

    print('返回：', json.dumps(result, ensure_ascii=False))
    if result.get('state') != 0:
        print('提交失败，提交体没有变，改完可以直接重跑')
        return 1
    print('提交成功，等待审核')
    return 0


if __name__ == '__main__':
    sys.exit(main())
