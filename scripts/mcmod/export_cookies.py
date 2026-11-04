"""从本机浏览器的 cookie 数据库导出指定域名的 cookie。

用法：
    python export_cookies.py --domain mcmod.cn --out .narrafork/mcmod-cookie.txt
    python export_cookies.py --browser edge --domain mcmod.cn --out ...

只读本机数据库的副本，不改动浏览器数据；解出来的 cookie 写到指定文件，不打印到终端。
"""
import argparse
import base64
import ctypes
import json
import os
import shutil
import sqlite3
import sys
import tempfile
from ctypes import wintypes
from pathlib import Path
from urllib.parse import quote

BROWSER_PATHS = {
    'chrome': Path(os.environ.get('LOCALAPPDATA', '')) / 'Google/Chrome/User Data',
    'edge': Path(os.environ.get('LOCALAPPDATA', '')) / 'Microsoft/Edge/User Data',
}


class DATA_BLOB(ctypes.Structure):
    _fields_ = [('cbData', wintypes.DWORD), ('pbData', ctypes.POINTER(ctypes.c_char))]


def dpapi_decrypt(data: bytes) -> bytes:
    buffer = ctypes.create_string_buffer(data, len(data))
    blob_in = DATA_BLOB(len(data), ctypes.cast(buffer, ctypes.POINTER(ctypes.c_char)))
    blob_out = DATA_BLOB()
    if not ctypes.windll.crypt32.CryptUnprotectData(
            ctypes.byref(blob_in), None, None, None, None, 0, ctypes.byref(blob_out)):
        raise OSError('DPAPI 解密失败，可能在非当前用户环境下运行')
    try:
        return ctypes.string_at(blob_out.pbData, blob_out.cbData)
    finally:
        ctypes.windll.kernel32.LocalFree(blob_out.pbData)


def master_key(user_data: Path) -> bytes:
    state = json.loads((user_data / 'Local State').read_text(encoding='utf-8'))
    encrypted = base64.b64decode(state['os_crypt']['encrypted_key'])
    return dpapi_decrypt(encrypted[5:])  # 去掉开头的 DPAPI 标记


def decrypt_value(value: bytes, key: bytes) -> str:
    if value[:3] in (b'v10', b'v11'):
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        return AESGCM(key).decrypt(value[3:15], value[15:], None).decode('utf-8')
    if value[:3] == b'v20':
        raise SystemExit('该 cookie 使用 App-Bound 加密（v20），无法用此方法解密')
    return value.decode('utf-8', 'ignore')


def pick_db(user_data: Path) -> Path:
    candidates = [user_data / 'Default/Network/Cookies']
    candidates += sorted(user_data.glob('Profile */Network/Cookies'))
    for path in candidates:
        if path.exists():
            return path
    raise SystemExit(f'找不到 cookie 数据库：{user_data}')


def export(browser: str, domain: str, profile: str | None) -> dict[str, str]:
    user_data = BROWSER_PATHS[browser]
    if not user_data.exists():
        raise SystemExit(f'没有安装 {browser}：{user_data}')
    db = (user_data / profile / 'Network/Cookies') if profile else pick_db(user_data)
    if not db.exists():
        raise SystemExit(f'找不到 cookie 数据库：{db}')

    key = master_key(user_data)
    with tempfile.TemporaryDirectory() as tmp:
        copy = Path(tmp) / 'Cookies'
        try:
            # 浏览器运行时文件被独占，用逐块读取而不是 CopyFile，通常仍可读
            with open(db, 'rb') as src, open(copy, 'wb') as dst:
                shutil.copyfileobj(src, dst)
            conn = sqlite3.connect(copy)
        except OSError:
            uri = f'file:///{quote(db.as_posix())}?mode=ro&immutable=1'
            conn = sqlite3.connect(uri, uri=True)
        try:
            rows = conn.execute(
                'SELECT host_key, name, encrypted_value, value FROM cookies WHERE host_key LIKE ?',
                (f'%{domain}%',)).fetchall()
        finally:
            conn.close()

    jar: dict[str, str] = {}
    for host, name, encrypted, plain in rows:
        if not host.endswith(domain):
            continue
        jar[name] = plain if plain else decrypt_value(encrypted, key)
    return jar


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--browser', choices=sorted(BROWSER_PATHS), default='chrome')
    parser.add_argument('--domain', required=True)
    parser.add_argument('--profile', help='如 Default、Profile 1；不给时自动找第一个有 cookie 的')
    parser.add_argument('--out', required=True)
    args = parser.parse_args()

    if sys.platform != 'win32':
        raise SystemExit('只在 Windows 上支持')

    jar = export(args.browser, args.domain, args.profile)
    if not jar:
        raise SystemExit(f'{args.browser} 里没有 {args.domain} 的 cookie，先在浏览器登录一次')

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text('; '.join(f'{k}={v}' for k, v in jar.items()), encoding='utf-8')
    print(f'导出 {len(jar)} 个 cookie -> {out}')
    print('名称：', ', '.join(sorted(jar)))


if __name__ == '__main__':
    main()
