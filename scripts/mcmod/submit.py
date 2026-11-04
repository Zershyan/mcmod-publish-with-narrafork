"""提交 MC百科模组条目。

用法：
    python submit.py <配置.json> --dry-run   # 只打印提交体
    python submit.py <配置.json>             # 真提交

配置里写页面上的中文文本，脚本按 assets/mcmod-enums.json 转成代码值。
cookie 由 cookies.py 生成，默认读 .narrafork/mcmod-cookie.txt。
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts' / 'cf'))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from cfhttp import requests
from author import find as find_author

API = 'https://event.mcmod.cn/action/edit/doEdit/'
ADD_PAGE = 'https://www.mcmod.cn/class/add/'
CAPTCHA_URL = 'https://www.mcmod.cn/frame/edit/EditCaptcha/?id=class_add_0'
COOKIE_FILE = ROOT / '.narrafork' / 'mcmod-cookie.txt'
VERSION_CACHE = ROOT / '.narrafork' / 'mcmod-mcversions.json'
CAPTCHA_FILE = ROOT / '.narrafork' / 'mcmod-captcha.png'
ENUMS = json.loads((ROOT / 'assets' / 'mcmod-enums.json').read_text(encoding='utf-8'))
# 添加页内嵌全部 MC 版本：var arrMCVer = $.parseJSON('[{"id":"78","name":"26.1.2"},…]')
MC_VERSION_PATTERN = re.compile(r"arrMCVer\s*=\s*\$\.parseJSON\('(\[.*?\])'\)", re.S)


def make_session():
    if not COOKIE_FILE.exists():
        raise SystemExit(f'缺少 cookie 文件：{COOKIE_FILE}，先跑 cookies.py dump')
    session = requests.Session(impersonate='chrome')
    session.headers['Cookie'] = COOKIE_FILE.read_text(encoding='utf-8').strip()
    return session


def fetch_mc_versions(session) -> dict[str, str]:
    """版本号 -> 版本 ID；每次可能变，必须现取。"""
    html = session.get(ADD_PAGE, timeout=30).text
    match = MC_VERSION_PATTERN.search(html)
    if not match:
        raise SystemExit('添加页里没找到 MC 版本列表，登录态可能已失效')
    return {item['name']: item['id'] for item in json.loads(match.group(1))}


def cached_mc_versions(session, refresh: bool = False) -> dict[str, str]:
    """缓存版本映射：提交时不再请求添加页，否则会刷新验证码。"""
    if not refresh and VERSION_CACHE.exists():
        return json.loads(VERSION_CACHE.read_text(encoding='utf-8'))
    versions = fetch_mc_versions(session)
    VERSION_CACHE.parent.mkdir(parents=True, exist_ok=True)
    VERSION_CACHE.write_text(json.dumps(versions, ensure_ascii=False, indent=1), encoding='utf-8')
    return versions


def grab_captcha(session) -> Path:
    """取一张新的验证码图片。每次请求都会刷新，取完必须紧接着提交。"""
    session.get(ADD_PAGE, timeout=30)
    response = session.get(CAPTCHA_URL, timeout=30, headers={'Referer': ADD_PAGE})
    if response.status_code >= 400 or not response.content:
        raise SystemExit(f'取验证码失败：HTTP {response.status_code}')
    CAPTCHA_FILE.parent.mkdir(parents=True, exist_ok=True)
    CAPTCHA_FILE.write_bytes(response.content)
    print(f'验证码已保存：{CAPTCHA_FILE}（{len(response.content)} 字节）')
    return CAPTCHA_FILE


def code_of(group: str, label: str) -> str:
    table = ENUMS[group]
    for code, text in table.items():
        if text == label or text.split(' ')[0] == label:
            return code
    raise SystemExit(f'{group} 里没有「{label}」，可选：{", ".join(table.values())}')


def indexed(values) -> dict:
    """勾选类字段要求 {序号: 值}，序号只是遍历下标。"""
    return {str(i): v for i, v in enumerate(values)} if values else {}


def build(cfg: dict, mc_ids: dict[str, str]) -> dict:
    data = {
        'name': cfg['name'],
        'ename': cfg.get('ename', ''),
        'intro': cfg.get('intro', ''),
        'modid': cfg['modid'],
        'cfprojectid': str(cfg.get('cfprojectid', '')),
        'mrprojectid': str(cfg.get('mrprojectid', '')),
        'activity': {},
        'category': indexed([
            code_of('categoryCore', c) if c in ENUMS['categoryCore'].values()
            else code_of('categoryExtra', c)
            for c in cfg.get('category', [])
        ]),
        'platform': indexed([code_of('platform', p) for p in cfg.get('platform', ['JAVA版 (JAVA Edition)'])]),
        'api': indexed([code_of('api', a) for a in cfg.get('api', [])]),
        'mode-1': indexed([code_of('mode', cfg.get('mode1', '需装'))]),
        'mode-2': indexed([code_of('mode', cfg.get('mode2', '需装'))]),
        'status': indexed([code_of('status', cfg.get('status', '活跃'))]),
        'source': indexed([code_of('source', cfg.get('source', '开源'))]),
        'content': cfg.get('content', ''),
    }

    if cfg.get('mcVersions'):
        # {"NeoForge": ["26.1.2"], "Forge": ["1.20.1"]}
        mc_map = {}
        for loader, versions in cfg['mcVersions'].items():
            api_code = loader if loader in ENUMS['api'] else code_of('api', loader)
            ids = []
            for version in versions:
                version_id = mc_ids.get(version)
                if not version_id:
                    raise SystemExit(f'页面里没有 MC 版本「{version}」')
                ids.append(version_id)
            mc_map[api_code] = indexed(ids)
        data['mcversion'] = mc_map

    if cfg.get('tags'):
        data['tags'] = indexed(cfg['tags'])
    if cfg.get('keys'):
        data['keys'] = indexed(cfg['keys'])

    if cfg.get('links'):
        data['link'] = {
            str(i): {'title': link.get('title', ''), 'custom': link.get('custom', ''),
                     'href': link.get('href', ''), 'text': link.get('text', '')}
            for i, link in enumerate(cfg['links'])
        }

    if cfg.get('license'):
        lic = cfg['license']
        types = lic.get('types') or [lic.get('type', '源码')]
        data['license'] = {
            '0': {
                # 页面显示「通用」时提交空字符串
                'title': '' if lic.get('title', '通用') in ('通用', '') else lic['title'],
                'list': {'0': {
                    'type': [t if t in ENUMS['licenseType'] else code_of('licenseType', t) for t in types],
                    'name': lic['name'],
                    'link': lic.get('link', ''),
                    'text': lic.get('text', ''),
                }},
            }
        }

    if cfg.get('authors'):
        links = {}
        for i, author in enumerate(cfg['authors']):
            author_id = str(author.get('id') or '')
            if not author_id and author.get('name'):
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


def submit(session, payload: dict) -> dict:
    response = session.post(
        API,
        data={'data': json.dumps(payload, ensure_ascii=False)},
        headers={'Referer': ADD_PAGE, 'X-Requested-With': 'XMLHttpRequest'},
        timeout=60)
    try:
        return response.json()
    except ValueError:
        raise SystemExit(f'返回了非 JSON：{response.text[:200]}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('config')
    parser.add_argument('--dry-run', action='store_true', help='只打印提交体，不发送')
    parser.add_argument('--captcha-url', action='store_true',
                        help='取一张验证码图片后退出，不提交')
    parser.add_argument('--captcha', help='提交时附带的验证码')
    args = parser.parse_args()

    cfg = json.loads(Path(args.config).read_text(encoding='utf-8'))
    session = make_session()

    if args.captcha_url:
        # 取图时会重新加载添加页，版本映射一并刷新并缓存
        cached_mc_versions(session, refresh=True)
        grab_captcha(session)
        print('把图片给用户识别，拿到验证码后带 --captcha 重跑，中间不要再请求添加页')
        return

    # 走缓存，避免提交前请求添加页把验证码刷掉
    payload = build(cfg, cached_mc_versions(session))
    if args.captcha:
        payload['captcha'] = args.captcha
    print(json.dumps(payload, ensure_ascii=False, indent=1))

    if args.dry_run:
        print('\n（dry-run，未提交）')
        return

    result = submit(session, payload)
    print('\n返回：', json.dumps(result, ensure_ascii=False))
    if result.get('state') == 0:
        print('提交成功：', result.get('url', '(无地址)'))
    elif result.get('state') == 117 and 'captcha' not in payload:
        raise SystemExit('state=117 且没有带验证码，可能是缺验证码；先跑 --captcha-url 取图')
    else:
        raise SystemExit(f'提交失败：state={result.get("state")}')


if __name__ == '__main__':
    main()
