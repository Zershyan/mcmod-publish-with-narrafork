"""通过 CDP 从正在运行的浏览器进程读出指定域名的完整 cookie（包含 httpOnly）。

用法：
    python dump_cookies_cdp.py --profile <浏览器 profile 目录> --domain mcmod.cn --out .narrafork/mcmod-cookie.txt

profile 目录里有 DevToolsActivePort 文件，第一行就是调试端口。
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'cf-http'))
import websocket


def cdp_cookies(port: int) -> list[dict]:
    # 先拿 browser 的调试入口
    import urllib.request
    with urllib.request.urlopen(f'http://127.0.0.1:{port}/json/version', timeout=5) as r:
        endpoint = json.loads(r.read())['webSocketDebuggerUrl']
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--profile', required=True, help='浏览器 profile 目录，含 DevToolsActivePort')
    parser.add_argument('--domain', required=True)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()

    port_file = Path(args.profile) / 'DevToolsActivePort'
    if not port_file.exists():
        raise SystemExit(f'找不到 {port_file}，浏览器可能已关闭')
    port = int(port_file.read_text().splitlines()[0].strip())

    cookies = cdp_cookies(port)
    picked = [c for c in cookies if c.get('domain', '').lstrip('.').endswith(args.domain)]
    if not picked:
        raise SystemExit(f'浏览器里没有 {args.domain} 的 cookie，先在上面登录一次')

    jar = '; '.join(f"{c['name']}={c['value']}" for c in picked)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(jar, encoding='utf-8')

    http_only = [c['name'] for c in picked if c.get('httpOnly')]
    print(f'导出 {len(picked)} 个 cookie -> {out}')
    print('名称：', ', '.join(sorted(c['name'] for c in picked)))
    print('其中 httpOnly：', ', '.join(sorted(http_only)) or '无')


if __name__ == '__main__':
    main()
