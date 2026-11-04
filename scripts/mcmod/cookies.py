"""MC百科登录凭据。

用法：
    python cookies.py dump  --profile <浏览器profile目录> --out .narrafork/mcmod-cookie.txt
    python cookies.py login --username <账号> --password <密码> --out <文件>

dump 通过 CDP 从运行中的浏览器读完整 cookie（含 httpOnly），是首选方式。
login 走账号密码接口，但登录页有图形验证码，没有 captcha 时会被拒。
"""
import argparse
import json
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'cf'))
from cfhttp import requests

LOGIN_PAGE = 'https://www.mcmod.cn/login/'
LOGIN_API = 'https://www.mcmod.cn/action/doLogin/'
DOMAIN = 'mcmod.cn'


def cdp_cookies(port: int) -> list[dict]:
    import websocket
    with urllib.request.urlopen(f'http://127.0.0.1:{port}/json/version', timeout=5) as response:
        endpoint = json.loads(response.read())['webSocketDebuggerUrl']
    ws = websocket.create_connection(endpoint, timeout=15)
    try:
        ws.send(json.dumps({'id': 1, 'method': 'Storage.getCookies'}))
        while True:
            message = json.loads(ws.recv())
            if message.get('id') == 1:
                if 'error' in message:
                    raise SystemExit(f"CDP 返回错误：{message['error']}")
                return message['result']['cookies']
    finally:
        ws.close()


def dump(profile: Path, out: Path) -> None:
    port_file = profile / 'DevToolsActivePort'
    if not port_file.exists():
        raise SystemExit(f'找不到 {port_file}，浏览器可能已关闭')
    port = int(port_file.read_text().splitlines()[0].strip())

    picked = [c for c in cdp_cookies(port)
              if c.get('domain', '').lstrip('.').endswith(DOMAIN)]
    if not picked:
        raise SystemExit(f'浏览器里没有 {DOMAIN} 的 cookie，先登录一次')

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text('; '.join(f"{c['name']}={c['value']}" for c in picked), encoding='utf-8')
    http_only = sorted(c['name'] for c in picked if c.get('httpOnly'))
    print(f'导出 {len(picked)} 个 cookie -> {out}')
    print('其中 httpOnly：', ', '.join(http_only) or '无')


def login(username: str, password: str, out: Path) -> None:
    session = requests.Session(impersonate='chrome')
    session.get(LOGIN_PAGE, timeout=30)
    response = session.post(
        LOGIN_API,
        data={'data': json.dumps({'username': username, 'password': password,
                                  'remember': 1, 'captcha': ''})},
        headers={'Referer': LOGIN_PAGE, 'X-Requested-With': 'XMLHttpRequest'},
        timeout=30)
    try:
        result = response.json()
    except ValueError:
        raise SystemExit(f'登录接口返回非 JSON：{response.text[:120]}')
    if result.get('state') != 0:
        raise SystemExit(f'登录失败：{result.get("state")}（登录页有验证码，纯脚本通常走不通）')

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text('; '.join(f'{c.name}={c.value}' for c in session.cookies.jar), encoding='utf-8')
    print(f'登录成功，{len(session.cookies.jar)} 个 cookie -> {out}')


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest='mode', required=True)

    p_dump = sub.add_parser('dump', help='从运行中的浏览器导出 cookie')
    p_dump.add_argument('--profile', required=True, help='含 DevToolsActivePort 的 profile 目录')

    p_login = sub.add_parser('login', help='账号密码登录')
    p_login.add_argument('--username', required=True)
    p_login.add_argument('--password', required=True)

    for p in (p_dump, p_login):
        p.add_argument('--out', required=True)

    args = parser.parse_args()
    if args.mode == 'dump':
        dump(Path(args.profile), Path(args.out))
    else:
        login(args.username, args.password, Path(args.out))


if __name__ == '__main__':
    main()
