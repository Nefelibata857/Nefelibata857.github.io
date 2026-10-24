# -*- coding: utf-8 -*-
"""生成作品集网站二维码：纯二维码 PNG/SVG + 深色名片卡 PNG。
二维码内容为永久地址 https://nefelibata857.github.io
"""
import os
import sys

sys.path.insert(0, r'D:\WorkBuddy\tools\pylib')   # 本地 vendored segno
import segno
from PIL import Image, ImageDraw, ImageFont

URL = 'https://nefelibata857.github.io'
OUT_DIR = r'E:\Desktop\简历\作品集2'
TMP = r'D:\WorkBuddy\portfolio-site\_qr_tmp.png'

INK = (26, 26, 24)
GOLD = (165, 129, 79)
GOLD_SOFT = (146, 110, 62)
MUTED = (138, 134, 126)
LINE = (222, 215, 202)
BG = (246, 243, 237)

MSYH = r'C:\Windows\Fonts\msyh.ttc'
MSYH_BD = r'C:\Windows\Fonts\msyhbd.ttc'
GEORGIA = r'C:\Windows\Fonts\georgia.ttf'
GEORGIA_IT = r'C:\Windows\Fonts\georgiai.ttf'


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.truetype(MSYH, size)


def tracked(draw, xy, text, f, fill, tracking=0.0, anchor_left=True):
    """手动字距：PIL 没有 letter-spacing，逐字画。返回结束 x。"""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=f, fill=fill)
        x += draw.textlength(ch, font=f) + tracking
    return x


def tracked_w(draw, text, f, tracking=0.0):
    return sum(draw.textlength(c, font=f) + tracking for c in text) - (tracking if text else 0)


def main():
    qr = segno.make(URL, error='h')          # 30% 纠错，抗污抗压缩
    print('qr version', qr.version, 'ecc', qr.error, 'modules', qr.symbol_size(scale=1, border=0)[0])

    # ---- 1) 纯二维码 PNG：2400px，4 模块静区 ----
    png = os.path.join(OUT_DIR, '作品集二维码_纯图.png')
    qr.save(png, scale=50, border=4, dark='#000000', light='#FFFFFF')
    print('pure png ->', png, Image.open(png).size)

    # ---- 2) 矢量 SVG（印刷无损） ----
    svg = os.path.join(OUT_DIR, '作品集二维码_矢量.svg')
    qr.save(svg, scale=1, border=4, dark='#000000', light='#FFFFFF', xmldecl=True, svgns=True)
    print('svg ->', svg, os.path.getsize(svg), 'B')

    # ---- 3) 米白名片卡 ----
    W, H = 1980, 1180
    im = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(im)

    # 极淡暖金光晕：径向渐变 + 高斯模糊，避免出现硬边弧线
    import numpy as np
    from PIL import ImageFilter
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    cx, cy = W * 0.22, H * 0.34
    r = np.sqrt(((xx - cx) / (W * 0.72)) ** 2 + ((yy - cy) / (H * 0.82)) ** 2)
    a = np.clip(1.0 - r, 0.0, 1.0) ** 1.9 * 13.0
    mask = Image.fromarray(a.astype(np.uint8), 'L').filter(ImageFilter.GaussianBlur(90))
    warm = Image.new('RGB', (W, H), (200, 162, 104))
    im = Image.composite(warm, im, mask.point(lambda v: min(255, int(v * 2.4))))
    d = ImageDraw.Draw(im)

    # 外框细线
    d.rectangle([44, 44, W - 45, H - 45], outline=LINE, width=2)
    d.rectangle([64, 64, W - 65, H - 65], outline=(232, 226, 214), width=1)

    # 左侧文字
    x0 = 132
    f_eyebrow = font(MSYH, 26)
    tracked(d, (x0, 168), 'PORTFOLIO 2027', f_eyebrow, GOLD, tracking=9)

    f_name = font(MSYH_BD, 128)
    d.text((x0 - 4, 226), '王勇超', font=f_name, fill=INK)

    f_sub = font(MSYH, 40)
    d.text((x0, 396), '城市设计 · 建筑', font=f_sub, fill=(74, 72, 68))

    # 基本信息：与网站首屏口径一致
    f_tag = font(MSYH, 27)
    d.text((x0, 470), '男 · 22 岁 · INTJ　｜　西安建筑科技大学 · 2027 届', font=f_tag, fill=MUTED)

    # 金色短线
    d.line([x0, 528, x0 + 96, 528], fill=GOLD, width=3)

    f_body = font(MSYH, 31)
    d.text((x0, 564), '五个项目 · 二十页图版', font=f_body, fill=INK)
    d.text((x0, 618), '概念设计 / 单体设计 / 社区设计 / 片区设计 / 驻场实践', font=f_body, fill=MUTED)

    # URL
    f_url = font(GEORGIA, 34)
    d.text((x0, 730), 'nefelibata857.github.io', font=f_url, fill=GOLD_SOFT)
    f_tip = font(MSYH, 24)
    tracked(d, (x0, 788), 'SCAN TO OPEN', f_tip, MUTED, tracking=6)

    # 右下角小字
    f_foot = font(MSYH, 24)
    d.text((x0, H - 132), '2414926363@qq.com', font=f_foot, fill=MUTED)
    d.text((x0, H - 96), '188 2916 9388', font=f_foot, fill=MUTED)

    # 右侧二维码白块
    qr.save(TMP, scale=14, border=1, dark='#1A1A18', light='#FFFFFF')
    q = Image.open(TMP).convert('RGB')
    side = 620
    q = q.resize((side, side), Image.NEAREST)
    pad = 46
    bx = (W - q.width) - 150 - pad
    by = (H - side) // 2 - pad
    d.rectangle([bx, by, bx + side + 2 * pad, by + side + 2 * pad], fill=(255, 255, 255))
    d.rectangle([bx, by, bx + side + 2 * pad, by + side + 2 * pad], outline=LINE, width=2)
    im.paste(q, (bx + pad, by + pad))

    card = os.path.join(OUT_DIR, '作品集二维码_名片.png')
    im.save(card, 'PNG')
    print('card ->', card, im.size)
    os.remove(TMP)

    # ---- 4) 站点用的小图（页脚/分享卡） ----
    site_qr = r'D:\WorkBuddy\portfolio-site\assets\qr.png'
    qr.save(site_qr, scale=12, border=2, dark='#1A1A18', light='#FFFFFF')
    print('site qr ->', site_qr, Image.open(site_qr).size)


if __name__ == '__main__':
    main()
