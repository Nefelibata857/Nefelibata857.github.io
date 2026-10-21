# -*- coding: utf-8 -*-
"""生成 index.html（读 pages.json，避免手写 17 页出错）"""
import json, os, sys, shutil
from urllib.parse import quote
sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.abspath(__file__))
pages = json.load(open(os.path.join(ROOT, 'pages.json'), encoding='utf-8'))

CH = [
    dict(id='ch1', no='01', name='概念设计', en='The 3E Stitcher', rng=(0, 3),
         chips=['2025.10', '合作项目', '甘肃 · 皇城镇', '2257 ㎡', 'UIA 竞赛概念设计'],
         desc='以“韧性的催化剂”为题，选址裕固族聚居的皇城镇，讨论时间作为一种设计工具如何培养地方的韧性。'),
    dict(id='ch2', no='02', name='单体设计', en='廊院阅垣', rng=(4, 6),
         chips=['建筑单体', '体量生成', '平面 · 剖面'],
         desc='以廊、院、垣三个要素组织体量与流线，在水平向的链接中完成从体量到细节的推演。'),
    dict(id='ch3', no='03', name='社区设计', en='板筑之间', rng=(7, 11),
         chips=['2025.07', '合作项目', '西安 · 冰窖巷', '1.6 公顷', '全龄友好运动社区'],
         desc='以传统“版筑”夯土技法为原点，将层层板片与外廊结构转译为建筑语言，在底层与各层平台之间释放立体的公共空间。'),
    dict(id='ch4', no='04', name='片区设计', en='场域之间', rng=(12, 16),
         chips=['2026.09', '合作项目', '西安 · 卧龙禅寺片区', '城市更新'],
         desc='从被寺墙围合的静默历史，到向城市敞开的日常公共生活：以“场域、街、雨棚、活动”四重策略重塑老城街区。'),
]

LABELS = {
    0: '项目说明', 1: '图版', 2: '图版', 3: '图版',
    4: '廊院阅垣', 5: '体量生成与剖面', 6: '各层平面',
    7: '板筑之间', 8: '设计说明', 9: '总平面与空间节点', 10: '一层平面与底层流线', 11: '图版',
    12: '场域之间', 13: '总平面与人群分析', 14: '立面 · 剖面 · 鸟瞰', 15: '场地与构件分析', 16: '植被分析',
}
TOTAL = len(pages)

PDF_FILE = '王勇超-西建大-城市设计-作品集.pdf'      # 下载后的文件名
PDF_HREF = 'assets/' + quote(PDF_FILE)

def esc(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))

# ---------- 概览卡 ----------
cards = []
for c in CH:
    p = c['rng'][0]
    n = c['rng'][1] - c['rng'][0] + 1
    cards.append(f'''      <a class="card" href="#{c['id']}">
        <div class="thumb">
          <span class="no">{c['no']}</span>
          <img src="assets/thumbs/t{p:02d}.webp" alt="{esc(c['name'])} {esc(c['en'])}" loading="lazy" decoding="async">
        </div>
        <h3>{esc(c['name'])}<span>{esc(c['en'])}</span></h3>
        <p>{n} 页 · P{p+1:02d}–{c['rng'][1]+1:02d}</p>
      </a>''')

# ---------- 章节 ----------
chapters = []
for c in CH:
    figs = []
    for i in range(c['rng'][0], c['rng'][1] + 1):
        info = next(x for x in pages if x['page'] == i)
        w, h = info['size']
        label = LABELS.get(i, '图版')
        cap_l = f"{c['name']} · {label}" if c['no'] != '02' else f"{c['name']} · {label}"
        figs.append(f'''        <figure class="page">
          <div class="sheet">
            <img src="{info['main']}" data-full="{info['main']}" width="{w}" height="{h}"
                 alt="{esc(c['name'])} {esc(c['en'])} 第 {i+1} 页" loading="lazy" decoding="async">
          </div>
          <figcaption><b>{esc(cap_l)}</b><span>{i+1:02d} / {TOTAL}</span></figcaption>
        </figure>''')
    chips = ''.join(f'<li>{esc(x)}</li>' for x in c['chips'])
    chapters.append(f'''    <section class="chapter" id="{c['id']}">
      <div class="wrap">
        <header class="ch-head">
          <div class="ch-no">{c['no']}</div>
          <div>
            <h2 class="ch-title"><small>{esc(c['en'])}</small>{esc(c['name'])}</h2>
            <ul class="chips">{chips}</ul>
            <p class="lede" style="max-width:38em;margin-top:18px;font-size:15px">{esc(c['desc'])}</p>
          </div>
        </header>
        <div class="pages">
{chr(10).join(figs)}
        </div>
      </div>
    </section>''')

ix = ''.join(
    f'<a href="#{c["id"]}"><b>{c["no"]}</b>{c["name"]}</a>' for c in CH
)
nav = ''.join(f'<a href="#{c["id"]}" data-ch="{c["id"]}">{c["no"]} {c["name"]}</a>' for c in CH)
nav += '<a href="#contact">联系</a>'

html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>王勇超 · 作品集 2027 | 城市设计 · 建筑</title>
<meta name="description" content="王勇超的建筑与城市设计作品集：概念设计 The 3E Stitcher、单体设计廊院阅垣、社区设计板筑之间、片区设计场域之间。">
<meta name="theme-color" content="#F6F3ED">
<meta property="og:title" content="王勇超 · 作品集 2027">
<meta property="og:description" content="城市设计 · 建筑 —— 四个项目，十七页图版。">
<meta property="og:type" content="website">
<script>document.documentElement.className+=" js";</script>
<link rel="stylesheet" href="assets/css/site.css">
<link rel="preload" as="image" href="assets/pages/p00.webp">
</head>
<body>
<div class="progress"></div>

<header class="top">
  <a class="brand" href="#top"><b>王勇超</b><span>Portfolio 2027</span></a>
  <nav class="nav">
    {nav}
    <a class="dl" href="{PDF_HREF}" download="{PDF_FILE}">下载 PDF</a>
  </nav>
</header>

<main id="top">
  <section class="hero">
    <div class="wrap">
      <div class="kicker"><i></i>Architecture · Urban Design</div>
      <h1><em>Selected Works</em>王勇超</h1>
      <p class="lede">城市设计背景，关注居住、社区与城市更新中的公共空间如何被重新组织。这里收录四个项目——从西北小镇的韧性概念，到西安老城的街区更新。</p>
      <p class="facts">西安建筑科技大学 · 城市设计 · 2027 届<span>四个项目 · {TOTAL} 页图版</span></p>
      <div class="scroll-hint"><i></i>SCROLL</div>
      <nav class="hero-ix" aria-label="项目索引">{ix}</nav>
    </div>
  </section>

  <section class="index" id="index">
    <div class="wrap">
      <div class="sec-head">
        <h2>项目索引</h2>
        <p>点击进入 · 或直接向下滚动</p>
      </div>
      <div class="cards">
{chr(10).join(cards)}
      </div>
    </div>
  </section>

{chr(10).join(chapters)}
</main>

<footer class="foot" id="contact">
  <div class="wrap">
    <h2>王勇超 · 作品集</h2>
    <p class="sub">城市设计 / 建筑 · 2027 届 · 西安建筑科技大学</p>
    <div class="contact-grid">
      <div class="c-item">
        <span class="c-lb">Email</span>
        <a class="mail" href="#" data-u="2414926363" data-d="qq.com"><span>2414926363</span><span class="at">&#64;</span><span>qq.com</span></a>
      </div>
      <div class="c-item">
        <span class="c-lb">Phone</span>
        <a href="tel:+8618829169388">188 2916 9388</a>
      </div>
      <div class="c-item">
        <span class="c-lb">Portfolio</span>
        <a href="{PDF_HREF}" download="{PDF_FILE}">下载完整 PDF · {TOTAL} 页</a>
      </div>
      <div class="c-item c-qr">
        <span class="c-lb">Scan</span>
        <img src="assets/qr.png" alt="扫码在手机打开本站" width="112" height="112" loading="lazy" decoding="async">
      </div>
    </div>
    <div class="row">
      <div class="copy">© 2026 王勇超 · 保留所有权利</div>
      <a class="totop" href="#top">回到顶部 ↑</a>
    </div>
  </div>
</footer>

<script src="assets/js/site.js"></script>
</body>
</html>
'''

open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(html)
print('index.html', round(os.path.getsize(os.path.join(ROOT, 'index.html')) / 1024, 1), 'KB')

# 拷贝网申版 PDF 作为下载文件
src = next((x for x in [r'E:\Desktop\简历\作品集2\王勇超作品集.pdf',
                        r'E:\Desktop\简历\作品集2\作品集_配色统一_网申版.pdf']
             if os.path.exists(x)), '')
dst = os.path.join(ROOT, 'assets', PDF_FILE)
old = os.path.join(ROOT, 'assets', 'portfolio.pdf')
if os.path.exists(old):
    os.remove(old)
if src and os.path.exists(src):
    shutil.copy2(src, dst)
    try:                                     # 写元数据：HR 在阅读器里看到的标题
        import pymupdf
        d = pymupdf.open(dst)
        d.set_metadata(dict(d.metadata,
            title='王勇超 - 西安建筑科技大学 城市设计 作品集 2027',
            author='王勇超',
            subject='建筑 / 城市设计作品集 · 四个项目 十七页图版',
            keywords='城市设计,建筑设计,作品集,2027届,西安建筑科技大学'))
        d.saveIncr()
        d.close()
    except Exception as e:
        print('meta skip:', e)
    print('pdf', round(os.path.getsize(dst) / 1048576, 1), 'MB')
