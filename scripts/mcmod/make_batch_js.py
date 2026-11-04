import json, os, sys

# 用法：python make_batch_js.py 条目.json 输出.js [试运行0/1] [附言，默认空] [逗号分隔的key列表]
src = sys.argv[1]
out = sys.argv[2]
dry = len(sys.argv) > 3 and sys.argv[3] == '1'
remark = ''
if len(sys.argv) > 4:
    remark = sys.argv[4]
only = None
if len(sys.argv) > 5 and sys.argv[5]:
    only = sys.argv[5].split(',')

entries = json.load(open(src, encoding='utf-8'))
if only:
    by_key = {e['key']: e for e in entries}
    missing = [k for k in only if k not in by_key]
    if missing:
        sys.exit('找不到条目：' + ','.join(missing))
    entries = [by_key[k] for k in only]

# 抽象资料（套装、套具等汇总条目）不放图标
for e in entries:
    if e.get('abstract') or e['name'].endswith(('套装', '套具')):
        if e.get('icon32') or e.get('icon128'):
            print('abstract entry, icons cleared:', e['key'])
        e['icon32'] = ''
        e['icon128'] = ''

# 套装/套具内的单件正文必须为空，汇总条目必须带 [ban:title_menu]
for e in entries:
    content = e.get('content', '')
    if content and '[ban:title_menu]' not in content:
        sys.exit('正文缺少 [ban:title_menu]：' + e['name'])
    if '<table' in content and '<th' not in content:
        sys.exit('表格缺少标题行 <th>：' + e['name'])
    import re
    if re.search(r'https?://|www\.', re.sub(r'<[^>]+>', '', content)):
        sys.exit('正文出现裸网址，请改成带 title 的超链接：' + e['name'])
    for a in re.findall(r'<a\b[^>]*>', content):
        if 'title=' not in a or 'target="_blank"' not in a:
            sys.exit('超链接缺少 title 或 target="_blank"：' + e['name'])

template = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'batch_template.js'), encoding='utf-8').read()
if dry:
    template = template.replace('__DRY_RUN__', 'true')
else:
    template = template.replace('__DRY_RUN__', 'false')
template = template.replace('__ENTRIES__', json.dumps(entries, ensure_ascii=False))
template = template.replace('__REMARK__', json.dumps(remark, ensure_ascii=False))
open(out, 'w', encoding='utf-8').write(template)
print(len(entries), 'entries', len(template), 'chars')
