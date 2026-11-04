# CurseForge API 请求封装：用 curl_cffi 模拟 Chrome 的 TLS/HTTP2 指纹，避免被 Cloudflare 挑战页拦截。
# 用法：sys.path.insert(0, r'<本目录>'); from browser_http import BrowserOpener, system_proxy
import io
import os
import sys
import urllib.error

# curl_cffi 运行时目录：设置环境变量 CF_HTTP_RUNTIME 时优先从该目录加载，否则使用当前 Python 环境
RUNTIME = os.environ.get('CF_HTTP_RUNTIME')
if RUNTIME and RUNTIME not in sys.path:
    sys.path.insert(0, RUNTIME)
try:
    from curl_cffi import requests
except ImportError as error:
    hint = f'python -m pip install --target "{RUNTIME}" curl_cffi' if RUNTIME else 'python -m pip install curl_cffi'
    raise SystemExit(f'curl_cffi not found; install with: {hint}') from error


# 读取系统代理（形如 127.0.0.1:端口）：先看 HTTPS_PROXY/HTTP_PROXY 环境变量，Windows 上再读系统代理设置，都没有时返回 None
def system_proxy():
    for name in ('HTTPS_PROXY', 'https_proxy', 'HTTP_PROXY', 'http_proxy'):
        value = os.environ.get(name)
        if value:
            return value.split('://', 1)[-1].rstrip('/')
    if sys.platform != 'win32':
        return None
    import winreg
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Internet Settings') as handle:
            enabled = winreg.QueryValueEx(handle, 'ProxyEnable')[0]
            proxy = winreg.QueryValueEx(handle, 'ProxyServer')[0] if enabled else None
    except OSError:
        return None
    if proxy and '=' in proxy:
        entries = dict(item.split('=', 1) for item in proxy.split(';') if '=' in item)
        proxy = entries.get('https') or entries.get('http')
    return proxy or None


# 与 urllib 的 opener 接口兼容：open(urllib.request.Request) 返回带 status 的响应，>=400 抛 HTTPError
class BrowserOpener:
    def __init__(self, proxy=None):
        self.proxy = proxy or system_proxy()

    def open(self, req, timeout=55):
        response = requests.request(
            req.get_method(), req.full_url,
            headers=dict(req.header_items()), data=req.data,
            proxy=('http://' + self.proxy) if self.proxy else None,
            impersonate='chrome', timeout=timeout, allow_redirects=False)
        if response.status_code >= 400:
            raise urllib.error.HTTPError(req.full_url, response.status_code, 'HTTP failure', {}, io.BytesIO(response.content))
        result = _Response(response.content)
        result.status = response.status_code
        return result


# BytesIO 本身不能挂自定义属性，需要子类承载 status
class _Response(io.BytesIO):
    pass
