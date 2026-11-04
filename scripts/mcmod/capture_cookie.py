"""启动本地接收端口，等浏览器页面把 cookie 发过来。

用法：
    python capture_cookie.py [端口] [输出文件]

启动后把下面这行粘到 mcmod.cn 的地址栏或控制台即可：
    javascript:fetch('http://127.0.0.1:<端口>/',{method:'POST',mode:'no-cors',body:document.cookie});void(0)

收到一次就退出。
"""
import http.server
import sys
import threading
from pathlib import Path

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 18765
OUT = Path(sys.argv[2] if len(sys.argv) > 2 else '.narrafork/mcmod-cookie.txt')


class Handler(http.server.BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_POST(self):
        size = int(self.headers.get('Content-Length') or 0)
        body = self.rfile.read(size).decode('utf-8', 'ignore').strip()
        if body:
            OUT.parent.mkdir(parents=True, exist_ok=True)
            OUT.write_text(body, encoding='utf-8')
            print(f'收到 cookie：{len(body)} 字符，已写入 {OUT}', flush=True)
        self.send_response(204)
        self._cors()
        self.end_headers()
        threading.Thread(target=self.server.shutdown, daemon=True).start()

    def log_message(self, *args):
        pass


def main():
    server = http.server.HTTPServer(('127.0.0.1', PORT), Handler)
    print(f'监听 http://127.0.0.1:{PORT}/ ，等待浏览器发送 cookie', flush=True)
    server.serve_forever()
    server.server_close()


if __name__ == '__main__':
    main()
