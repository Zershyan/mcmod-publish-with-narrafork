# 用法：python make_icons.py 模组assets目录 条目.json 图标输出目录（平面模型写入 icon32/icon128，3D 模型清空图标并列出）
import json, os, sys, base64, io
from PIL import Image

ASSETS = sys.argv[1]
ENTRIES = sys.argv[2]
OUTDIR = sys.argv[3]
FLAT_PARENTS = ('item/generated', 'item/handheld', 'minecraft:item/generated', 'minecraft:item/handheld')

os.makedirs(OUTDIR, exist_ok=True)
entries = json.load(open(ENTRIES, encoding='utf-8'))
report = {'flat': [], 'model': []}
for e in entries:
    key = e['key']
    m = json.load(open(os.path.join(ASSETS, 'models/item', key + '.json'), encoding='utf-8'))
    if m.get('parent') not in FLAT_PARENTS:
        e.pop('icon32', None)
        e.pop('icon128', None)
        report['model'].append(key)
        continue
    tex = m['textures']['layer0'].split(':')[1]
    img = Image.open(os.path.join(ASSETS, 'textures', tex + '.png')).convert('RGBA')
    w, h = img.size
    if h > w:
        img = img.crop((0, 0, w, w))
    out = {}
    for size in (32, 128):
        icon = img.resize((size, size), Image.NEAREST)
        icon.save(os.path.join(OUTDIR, key + '_' + str(size) + '.png'))
        buf = io.BytesIO()
        icon.save(buf, 'PNG')
        out[size] = 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode()
    e['icon32'] = out[32]
    e['icon128'] = out[128]
    report['flat'].append(key)
json.dump(entries, open(ENTRIES, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps({k: len(v) for k, v in report.items()}))
print('model:', ','.join(report['model']))
