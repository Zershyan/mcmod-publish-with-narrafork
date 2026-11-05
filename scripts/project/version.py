"""把版本号写进各分支的 gradle.properties。

用法：
    python version.py master=0.0.1 1.21.1=1.0.0 [--allow-dirty]

只改文件，不 commit、不 push。结束后回到执行前所在的分支。
默认要求工作区干净；发布前常见的其他改动（图标、描述）可以加 --allow-dirty，
但 gradle.properties 自身必须干净，否则切分支会把它冲掉。
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

PROPERTIES = Path('gradle.properties')


def git(*args, check: bool = True) -> str:
    result = subprocess.run(['git', *args], capture_output=True, text=True)
    if check and result.returncode != 0:
        raise SystemExit(f'git {" ".join(args)} 失败：{result.stderr.strip()}')
    return result.stdout


def current_branch() -> str:
    return git('rev-parse', '--abbrev-ref', 'HEAD').strip()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('pairs', nargs='+', help='branch=version，可写多个')
    parser.add_argument('--allow-dirty', action='store_true',
                        help='工作区有其他改动也继续；gradle.properties 自身仍须干净')
    args = parser.parse_args()

    pairs = []
    for item in args.pairs:
        branch, sep, version = item.partition('=')
        if not sep or not branch.strip() or not version.strip():
            raise SystemExit(f'格式应为 branch=version：{item}')
        pairs.append((branch.strip(), version.strip()))

    props_dirty = git('status', '--porcelain', '--', 'gradle.properties').strip()
    if props_dirty:
        raise SystemExit('gradle.properties 有未提交改动，先处理再回填：\n' + props_dirty)

    dirty = git('status', '--porcelain').strip()
    if dirty and not args.allow_dirty:
        raise SystemExit('工作区有其他未提交改动。确认不影响切分支就加 --allow-dirty：\n' + dirty)

    original = current_branch()
    changed = []
    try:
        for branch, version in pairs:
            print(f'切到 {branch}')
            git('checkout', branch)
            if not PROPERTIES.exists():
                raise SystemExit(f'{branch} 上没有 gradle.properties')
            text = PROPERTIES.read_text(encoding='utf-8')
            updated, count = re.subn(r'(?m)^mod_version=.*$', f'mod_version={version}', text)
            if count != 1:
                raise SystemExit(f'{branch} 的 gradle.properties 里没有唯一的 mod_version 行')
            PROPERTIES.write_text(updated, encoding='utf-8')
            changed.append((branch, version))
            print(f'  mod_version={version}')
    finally:
        if current_branch() != original:
            print(f'回到 {original}')
            git('checkout', original, check=False)

    print(f'已回填 {len(changed)} 个分支，改动未提交，确认后自行 commit')


if __name__ == '__main__':
    main()
