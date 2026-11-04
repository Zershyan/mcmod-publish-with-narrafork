import base64, json, os, sys

# 用法：python make_create_mod_js.py 模组配置.json 输出.js
# 配置字段见 references/create-mod-config.example.json；正文和封面路径相对配置文件所在目录
cfg_path = os.path.abspath(sys.argv[1])
out = sys.argv[2]
base = os.path.dirname(cfg_path)
cfg = json.load(open(cfg_path, encoding='utf-8'))

# 默认值
defaults = {
    'ename': '', 'sname': '', 'platforms': ['JAVA版 (JAVA Edition)'], 'elements': [], 'links': [],
    'cfprojectid': '', 'mrprojectid': '', 'tags': '', 'client': '需装', 'server': '需装',
    'status': '活跃', 'source': '开源', 'injectCover': False,
}
for k, v in defaults.items():
    cfg.setdefault(k, v)

# 必填项检查
for k in ('name', 'intro', 'modid', 'core', 'versions', 'content_file', 'authors'):
    if not cfg.get(k):
        sys.exit('配置缺少必填项：' + k)
for au in cfg['authors']:
    if not str(au.get('id', '')).isdigit() or int(au['id']) <= 0 or not au.get('name') or au['name'].startswith('<'):
        sys.exit('authors 需填写自己的百科作者 ID（正整数）和名称：' + json.dumps(au, ensure_ascii=False))
# 读取正文，开头默认带 [ban:title_menu]
cfg['content'] = open(os.path.join(base, cfg.pop('content_file')), encoding='utf-8').read().lstrip()
if not cfg['content'].startswith('<p>[ban:title_menu]</p>'):
    cfg['content'] = '<p>[ban:title_menu]</p>\n' + cfg['content'].replace('<p>[ban:title_menu]</p>', '')

# 正文不允许出现裸网址，链接必须是带文字和悬浮提示的超链接
import re
text_only = re.sub(r'<[^>]+>', '', cfg['content'])
if re.search(r'https?://|www\.', text_only):
    sys.exit('正文出现裸网址，请改成 <a href="地址" target="_blank" title="悬浮提示">链接文字</a>')
for a in re.findall(r'<a\b[^>]*>', cfg['content']):
    if 'title=' not in a or 'target="_blank"' not in a:
        sys.exit('超链接缺少 title 或 target="_blank"：' + a)

# 正文截图：images 为 {键: 图片路径}，正文写 <p>{{img:键}}</p>，运行时上传到百科后替换
images = {}
for key, rel in (cfg.pop('images', None) or {}).items():
    token = '{{img:%s}}' % key
    if token not in cfg['content']:
        sys.exit('正文缺少图片占位 ' + token)
    p = os.path.join(base, rel)
    images[key] = {'file': os.path.basename(p), 'data': base64.b64encode(open(p, 'rb').read()).decode()}
missing = set(re.findall(r'\{\{img:([^}]+)\}\}', cfg['content'])) - set(images)
if missing:
    sys.exit('正文图片占位没有对应文件：' + ', '.join(sorted(missing)))
cfg['images'] = images

# 读取封面，必须是 16:10
cfg['cover'] = ''
cfg['coverPath'] = ''
if cfg.get('cover_file'):
    p = os.path.join(base, cfg.pop('cover_file'))
    try:
        from PIL import Image
        w, h = Image.open(p).size
        if abs(w / h - 1.6) > 0.01:
            sys.exit(f'封面比例必须是 16:10，当前 {w}x{h}')
    except ImportError:
        pass
    cfg['coverPath'] = p
    if cfg['injectCover']:
        cfg['cover'] = base64.b64encode(open(p, 'rb').read()).decode()

template = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'create_mod_template.js'), encoding='utf-8').read()
js = template.replace('__DATA__', json.dumps(cfg, ensure_ascii=False))
open(out, 'w', encoding='utf-8', newline='\n').write(js)
print('ok', len(js))
