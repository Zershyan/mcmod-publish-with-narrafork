# CurseForge 通用上传脚本：按发布清单逐个上传，运行时与代理统一由 browser_http 解析，不在各项目脚本里写死路径。
# 用法：
#   python upload_release.py query  <输出目录>                      # 拉取版本标签到 <输出目录>/game-versions.json
#   python upload_release.py upload <release-manifest.json> --project-id <ID> --slug <项目slug>
# 清单格式：{"files": [{"minecraft": "1.20.1", "artifact": "<jar路径>", "sha256": "...", "metadata": {...}}]}
# 令牌只从环境变量 CURSEFORGE_API_TOKEN 读取。
import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from browser_http import requests, system_proxy
from curl_cffi import CurlMime

BASE = 'https://minecraft.curseforge.com/api'

parser = argparse.ArgumentParser()
parser.add_argument('mode', choices=['query', 'upload'])
parser.add_argument('path')
parser.add_argument('--project-id')
parser.add_argument('--slug')
parser.add_argument('--proxy', help='覆盖系统代理，形如 127.0.0.1:端口')
args = parser.parse_args()

token = os.environ.get('CURSEFORGE_API_TOKEN')
if not token:
    raise SystemExit('Missing CURSEFORGE_API_TOKEN')

# 会话：模拟 Chrome 指纹，代理默认取系统代理
proxy = args.proxy or system_proxy()
session = requests.Session(impersonate='chrome')
if proxy:
    session.proxies = {'http': 'http://' + proxy, 'https': 'http://' + proxy}
session.headers['X-Api-Token'] = token

# 查询模式：保存完整版本标签，供清单按数字 ID 选择
if args.mode == 'query':
    out = Path(args.path)
    out.mkdir(parents=True, exist_ok=True)
    response = session.get(BASE + '/game/versions', timeout=40)
    print('Versions HTTP', response.status_code, response.headers.get('content-type', ''))
    response.raise_for_status()
    (out / 'game-versions.json').write_text(json.dumps(response.json(), ensure_ascii=False, indent=2), encoding='utf-8')
    raise SystemExit(0)

if not args.project_id or not args.slug:
    raise SystemExit('upload needs --project-id and --slug')

# 上传模式：已取得文件 ID 的不重复上传；结果不明的必须先核对线上列表
manifest_path = Path(args.path)
root = manifest_path.parent
manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
for release in manifest['files']:
    label = release['minecraft']
    result_path = root / f'upload-result-{label}.json'
    attempt_path = root / f'upload-attempt-{label}.json'
    if result_path.exists():
        result = json.loads(result_path.read_text(encoding='utf-8'))
        if result.get('id'):
            print(label, 'already accepted', result['id'])
            continue
    if attempt_path.exists():
        raise SystemExit(f'Unresolved upload attempt for {label}; inspect remote files before retrying')
    artifact = Path(release['artifact'])
    digest = hashlib.sha256(artifact.read_bytes()).hexdigest()
    if digest != release['sha256']:
        raise SystemExit(f'Artifact checksum changed for {label}')
    attempt_path.write_text(json.dumps({'startedUtc': datetime.now(timezone.utc).isoformat(), 'sha256': digest, 'metadata': release['metadata']}, ensure_ascii=False, indent=2), encoding='utf-8')
    multipart = CurlMime()
    multipart.addpart(name='metadata', content_type='application/json', data=json.dumps(release['metadata'], ensure_ascii=False).encode('utf-8'))
    multipart.addpart(name='file', filename=artifact.name, content_type='application/java-archive', local_path=str(artifact))
    response = session.post(f'{BASE}/projects/{args.project_id}/upload-file', multipart=multipart, timeout=100)
    print(label, 'Upload HTTP', response.status_code)
    (root / f'upload-response-{label}.txt').write_text(response.text, encoding='utf-8')
    response.raise_for_status()
    result = response.json()
    if not result.get('id'):
        raise SystemExit(f'No accepted file ID returned for {label}')
    result['minecraft'] = label
    result['sha256'] = digest
    result['status'] = 'accepted; approval not checked'
    result['url'] = f"https://www.curseforge.com/minecraft/mc-mods/{args.slug}/files/{result['id']}"
    result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False))
