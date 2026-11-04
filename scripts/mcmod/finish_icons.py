# 用法：python finish_icons.py 原图目录(*_raw.png) 输出目录（按不透明区域裁剪居中后缩放到 32/128，并生成 _sheet.png 预览）
import os, sys
from PIL import Image
SRC = sys.argv[1]
OUT = sys.argv[2]
os.makedirs(OUT, exist_ok=True)
names = sorted(f[:-8] for f in os.listdir(SRC) if f.endswith('_raw.png'))
W = 6
sheet = Image.new('RGBA', (W * 136, ((len(names) + W - 1) // W) * 136), (255, 0, 255, 255))
for i, key in enumerate(names):
    im = Image.open(os.path.join(SRC, key + '_raw.png')).convert('RGBA')
    box = im.getchannel('A').getbbox()
    edge = box[0] == 0 or box[1] == 0 or box[2] == im.width or box[3] == im.height
    im = im.crop(box)
    side = int(max(im.size) * 1.04)
    sq = Image.new('RGBA', (side, side), (0, 0, 0, 0))
    sq.paste(im, ((side - im.width) // 2, (side - im.height) // 2))
    for size in (32, 128):
        sq.resize((size, size), Image.LANCZOS).save(os.path.join(OUT, key + '_' + str(size) + '.png'))
    sheet.alpha_composite(Image.open(os.path.join(OUT, key + '_128.png')), ((i % W) * 136 + 4, (i // W) * 136 + 4))
    print(key, box, 'EDGE' if edge else '')
sheet.save(os.path.join(OUT, '_sheet.png'))
