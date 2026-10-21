/* ===== 作品集站点 · 交互 ===== */
(function () {
  'use strict';

  /* 1. 顶栏 + 进度条 */
  const top = document.querySelector('.top');
  const bar = document.querySelector('.progress');
  function onScroll() {
    const y = window.scrollY || document.documentElement.scrollTop;
    const h = document.documentElement.scrollHeight - window.innerHeight;
    if (bar) bar.style.width = (h > 0 ? (y / h) * 100 : 0) + '%';
    if (top) top.classList.toggle('solid', y > 40);
  }
  addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* 2. 图片淡入 */
  document.querySelectorAll('figure.page img').forEach(function (img) {
    const done = () => img.classList.add('loaded');
    if (img.complete && img.naturalWidth) done();
    else img.addEventListener('load', done, { once: true });
  });

  /* 3. 章节高亮 */
  const links = Array.from(document.querySelectorAll('.nav a[data-ch]'));
  const secs = links.map(a => document.getElementById(a.dataset.ch)).filter(Boolean);
  if ('IntersectionObserver' in window && secs.length) {
    const io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        links.forEach(a => a.classList.toggle('on', a.dataset.ch === e.target.id));
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    secs.forEach(s => io.observe(s));
  }

  /* 4. 灯箱 */
  const figs = Array.from(document.querySelectorAll('figure.page'));
  if (!figs.length) return;

  const items = figs.map(function (f) {
    const img = f.querySelector('img');
    return {
      src: img.getAttribute('data-full') || img.src,
      alt: img.alt || '',
      cap: (f.querySelector('figcaption') || {}).textContent || ''
    };
  });

  const lb = document.createElement('div');
  lb.className = 'lb';
  lb.innerHTML =
    '<button class="close" aria-label="关闭">×</button>' +
    '<button class="nav-btn prev" aria-label="上一页">‹</button>' +
    '<img alt="">' +
    '<button class="nav-btn next" aria-label="下一页">›</button>' +
    '<div class="cap"></div>';
  document.body.appendChild(lb);

  const lbImg = lb.querySelector('img');
  const lbCap = lb.querySelector('.cap');
  let cur = 0, open = false;

  function show(i) {
    cur = (i + items.length) % items.length;
    const it = items[cur];
    lbImg.classList.remove('zoom');
    lbImg.src = it.src;
    lbImg.alt = it.alt;
    lbCap.textContent = it.cap.trim();
    // 预取相邻页
    [cur + 1, cur - 1].forEach(function (k) {
      const j = (k + items.length) % items.length;
      const p = new Image(); p.src = items[j].src;
    });
  }
  function openLb(i) {
    show(i); lb.classList.add('on'); open = true;
    document.body.style.overflow = 'hidden';
  }
  function closeLb() {
    lb.classList.remove('on'); open = false; lbImg.classList.remove('zoom');
    document.body.style.overflow = '';
  }

  figs.forEach(function (f, i) {
    const sheet = f.querySelector('.sheet');
    (sheet || f).addEventListener('click', function () { openLb(i); });
  });
  lb.querySelector('.close').addEventListener('click', closeLb);
  lb.querySelector('.prev').addEventListener('click', function (e) { e.stopPropagation(); show(cur - 1); });
  lb.querySelector('.next').addEventListener('click', function (e) { e.stopPropagation(); show(cur + 1); });
  lb.addEventListener('click', function (e) { if (e.target === lb) closeLb(); });
  lbImg.addEventListener('click', function () { lbImg.classList.toggle('zoom'); });

  addEventListener('keydown', function (e) {
    if (!open) return;
    if (e.key === 'Escape') closeLb();
    else if (e.key === 'ArrowRight') show(cur + 1);
    else if (e.key === 'ArrowLeft') show(cur - 1);
  });

  /* 5. 触摸滑动 */
  let tx = 0, ty = 0;
  lb.addEventListener('touchstart', function (e) {
    tx = e.touches[0].clientX; ty = e.touches[0].clientY;
  }, { passive: true });
  lb.addEventListener('touchend', function (e) {
    const dx = e.changedTouches[0].clientX - tx;
    const dy = e.changedTouches[0].clientY - ty;
    if (Math.abs(dx) > 60 && Math.abs(dx) > Math.abs(dy)) show(cur + (dx < 0 ? 1 : -1));
  }, { passive: true });
  /* 6. 邮箱拼装（避免被 CDN 的邮件混淆机制改写） */
  document.querySelectorAll('a.mail[data-u][data-d]').forEach(function (a) {
    const addr = a.dataset.u + '@' + a.dataset.d;
    a.setAttribute('href', 'mailto:' + addr);
    a.setAttribute('aria-label', addr);
  });
})();
