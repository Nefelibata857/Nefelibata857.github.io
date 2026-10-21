# -*- coding: utf-8 -*-
"""导出网页素材：以「作品集图片」文件夹（用户从 PDF 整页导出的全分辨率 JPG）为母版，
压缩成 WebP 主图 + 缩略图。

为什么不用 page.extract_image()：
  PDF 每页是「铺底位图 + 独立矢量文字层」，抽图只能拿到位图，文字会整层丢失。
  用户导出的整页 JPG 是已经合成好的，含文字，且分辨率最高（最宽 6549px）。
"""
import os, re, sys, json
from PIL import Image
sys.stdout.reconfigure(encoding='utf-8')

SRC_DIR = r'E:\Desktop\简历\作品集2\作品集图片'
ROOT = r'D:\WorkBuddy\portfolio-site'
PG = os.path.join(ROOT, 'assets', 'pages')
TH = os.path.join(ROOT, 'assets', 'thumbs')
os.makedirs(PG, exist_ok=True)
os.makedirs(TH, exist_ok=True)

W_MAIN, W_THUMB = 2600, 460
Q_MAIN, Q_THUMB = 85, 80


def page_no(p):
    nums = re.findall(r'\d+', os.path.splitext(os.path.basename(p))[0])
    return int(nums[-1]) if nums else 0


files = sorted((f for f in os.listdir(SRC_DIR) if f.lower().endswith(('.jpg', '.jpeg', '.png'))),
               key=lambda f: page_no(f))
assert files, f'没找到图片：{SRC_DIR}'

info = []
for i, f in enumerate(files):
    im = Image.open(os.path.join(SRC_DIR, f)).convert('RGB')
    w0, h0 = im.size
    if w0 > W_MAIN:
        im = im.resize((W_MAIN, round(h0 * W_MAIN / w0)), Image.LANCZOS)
    im.save(os.path.join(PG, f'p{i:02d}.webp'), 'WEBP', quality=Q_MAIN, method=6)

    t = im.copy()
    t.thumbnail((W_THUMB, W_THUMB), Image.LANCZOS)
    t.save(os.path.join(TH, f't{i:02d}.webp'), 'WEBP', quality=Q_THUMB, method=6)

    tiny = im.copy()
    tiny.thumbnail((24, 24))
    px = list(tiny.getdata())
    avg = [sum(c[k] for c in px) // len(px) for k in range(3)]

    info.append(dict(page=i, size=list(im.size), ratio=round(im.size[0] / im.size[1], 4),
                     main=f'assets/pages/p{i:02d}.webp', thumb=f'assets/thumbs/t{i:02d}.webp',
                     avg='#%02X%02X%02X' % tuple(avg)))
    print(f'P{i:02d} {w0}x{h0} -> {im.size[0]}x{im.size[1]} '
          f'{os.path.getsize(os.path.join(PG, f"p{i:02d}.webp")) // 1024}KB  ({f})')

json.dump(info, open(os.path.join(ROOT, 'pages.json'), 'w'), ensure_ascii=False, indent=1)
tot = sum(os.path.getsize(os.path.join(PG, f)) for f in os.listdir(PG) if f.endswith('.webp'))
print('total main', round(tot / 1048576, 1), 'MB')
print('ratios', sorted({i['ratio'] for i in info}))
