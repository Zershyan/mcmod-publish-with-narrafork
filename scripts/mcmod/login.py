"""登录 mcmod.cn 并保存 cookie 到文件。

用法：
    python login.py --username <账号> --password <密码> --out .narrafork/mcmod-cookie.txt

密码只用于这一次请求，不写进任何文件；输出只报告 cookie 数量与登录态检查结果。
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'cf-http'))
from browser_http import requests

LOGIN_PAGE = 'https://www.mcmod.cn/login/'
LOGIN_API = 'https://www.mcmod.cn/action/doLogin/'
ADD_PAGE = 'https://www.mcmod.cn/class/add/'


def login(username: str, password: str):
    session = requests.Session(impersonate='chrome')
    session.get(LOGIN_PAGE, timeout=30)
    payload = json.dumps({
        'username': username,
        'password': password,
        'remember': 1,
        'captcha': '',
    })
    response = session.post(
        LOGIN_API,
        data={'data': payload},
        headers={'Referer': LOGIN_PAGE, 'X-Requested-With': 'XMLHttpRequest'},
        timeout=30,
    )
    try:
        result = response.json()
    except ValueError:
        raise SystemExit(f'登录接口返回了非 JSON：{response.text[:120]}')
    if result.get('state') != 0:
        raise SystemExit(f'登录失败：{result.get("state")}')
    return session


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', required=True)
    parser.add_argument('--password', required=True)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()

    session = login(args.username, args.password)
    cookies = '; '.join(f'{c.name}={c.value}' for c in session.cookies.jar)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(cookies, encoding='utf-8')

    page = session.get(ADD_PAGE, timeout=30)
    has_editor = 'editor' in page.text
    print(f'登录成功，保存 {len(session.cookies.jar)} 个 cookie -> {out}')
    print('添加页可编辑：', '是' if has_editor else '否（cookie 可能没拿到或账号无权限）')


if __name__ == '__main__':
    main()
