"""归档上一版 CF 记录，给新一版让路。

`upload.py` 的去重键是 `curseforge/upload-result-<MC版本>.json`，**不看版本号**：
同一 MC 版本发第二版时，旧记录里的文件 ID 会让新版本被当成「已受理」直接跳过，
表现就是「跑了上传但什么都没传，回显的还是上个版本的 ID」。

发版前（生成新清单之前）先跑这个脚本，把上一版记录挪进 `curseforge/history/<版本>/`。
"""
import argparse
import json
import shutil
from pathlib import Path

WORK = Path('curseforge')
PATTERNS = ('release-manifest.json', 'upload-result-*.json',
            'upload-attempt-*.json', 'upload-response-*.txt')


def collect() -> list[Path]:
    """上一版留下的记录；project.json 与 game-versions.json 跨版本复用，不动。"""
    return [path for pattern in PATTERNS for path in sorted(WORK.glob(pattern))]


def guess_version() -> str:
    """从上一版清单的 displayName 取 mod 版本，形如 <modid>-<mod_version>-<mc版本>。"""
    try:
        data = json.loads((WORK / 'release-manifest.json').read_text(encoding='utf-8'))
        parts = data['files'][0]['metadata']['displayName'].split('-')
        return parts[-2] if len(parts) >= 3 else parts[-1]
    except (OSError, ValueError, KeyError, IndexError, TypeError):
        return ''


def free_dir(version: str) -> Path:
    """同名归档目录已存在时顺延 -2、-3。"""
    target = WORK / 'history' / version
    index = 2
    while target.exists():
        target = WORK / 'history' / f'{version}-{index}'
        index += 1
    return target


def main():
    parser = argparse.ArgumentParser(description='归档上一版 CurseForge 记录')
    parser.add_argument('--version', help='归档到 curseforge/history/<版本>/，默认从上一版清单推断')
    parser.add_argument('--dry-run', action='store_true', help='只打印要挪哪些文件')
    args = parser.parse_args()

    files = collect()
    if not files:
        print('curseforge 下没有待归档的记录')
        return 0

    version = args.version or guess_version()
    if not version:
        raise SystemExit('认不出版本号，用 --version 指定')

    target = free_dir(version)
    if args.dry_run:
        print(f'将归档到 {target}：')
        for path in files:
            print('  ', path.name)
        return 0

    target.mkdir(parents=True, exist_ok=True)
    for path in files:
        shutil.move(str(path), str(target / path.name))
    print(f'已归档 {len(files)} 个文件到 {target}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
