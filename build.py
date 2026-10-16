"""Build the portfolio: page.html (artifact fragment), index.html and cleanroom.html (Vercel)."""
import pathlib

ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "src"
css = (SRC / "style.css").read_text()

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link href="https://fonts.googleapis.com/css2?family=Literata:ital,opsz,wght@0,7..72,400..800;1,7..72,400..700'
         '&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">\n')

def head(title):
    return (f'<title>{title}</title>\n'
            '<meta name="claude:viewport-fit-sides" content="cover">\n'
            '<meta name="description" content="Researcher-engineer bridging advanced process innovation with system-level architecture for next-generation 3D integration">\n'
            '<link rel="icon" type="image/svg+xml" href="assets/engineer.svg">\n'
            '<meta property="og:type" content="website">\n'
            '<meta property="og:site_name" content="Hoogwan\'s Portfolio">\n'
            '<meta property="og:title" content="Hoogwan\'s Portfolio">\n'
            '<meta property="og:description" content="Hoogwan Lee · Semiconductor Engineering · Advanced Packaging">\n'
            '<meta property="og:url" content="https://hoogwan-portfolio.vercel.app/">\n'
            '<meta property="og:image" content="https://hoogwan-portfolio.vercel.app/assets/og-image.png">\n'
            '<meta property="og:image:width" content="1200">\n'
            '<meta property="og:image:height" content="630">\n'
            '<meta name="twitter:card" content="summary_large_image">\n'
            '<meta name="twitter:title" content="Hoogwan\'s Portfolio">\n'
            '<meta name="twitter:image" content="https://hoogwan-portfolio.vercel.app/assets/og-image.png">\n'
            + FONTS + f'<style>\n{css}</style>\n')

def masthead(prefix, current=None):
    items = [("about", "Home"), ("education", "Education"), ("research", "Research"),
             ("publications", "Publications"), ("conferences", "Conferences"),
             ("cleanroom", "Cleanroom"), ("connect", "Connect")]
    links = []
    for key, label in items:
        if key == "cleanroom":
            cls = ' class="active" aria-current="page"' if current == "cleanroom" else ''
            links.append(f'<a href="cleanroom.html"{cls}>{label}</a>')
        else:
            links.append(f'<a href="{prefix}#{key}">{label}</a>')
    nav_html = "\n      ".join(links)
    return f'''<header class="masthead">
  <div class="wrap">
    <a class="brand" href="{prefix}#about" aria-label="Hoogwan Lee portfolio, back to top">
      <img src="assets/engineer.svg" alt="" width="44" height="44">
      <span>
        <span class="brand-name">Hoogwan <em>Lee</em></span>
        <span class="brand-sub">Portfolio</span>
      </span>
    </a>
    <nav class="nav" id="nav" aria-label="Sections">
      {nav_html}
    </nav>
    <a class="nb-btn" href="https://advanced-packaging-study-hg.vercel.app/" target="_blank" rel="noopener">Lab Notebook <span aria-hidden="true">↗</span></a>
  </div>
</header>
'''

FOOTER = '''<footer>
  <div class="wrap">
    <span>© 2026 Hoogwan Lee</span>
  </div>
</footer>
'''

LIGHTBOX = '''<div class="lightbox" id="lightbox" hidden role="dialog" aria-modal="true" aria-label="Enlarged figure">
  <button class="lightbox-close" type="button" id="lightbox-close">Close</button>
  <figure><img id="lightbox-img" alt=""><figcaption id="lightbox-cap"></figcaption></figure>
</div>
'''

MAIN_JS = '''<script>
(function () {
  // Scroll-spy for in-page sections
  var links = Array.prototype.slice.call(document.querySelectorAll('#nav a[href^="#"]'));
  var sections = links.map(function (a) { return document.querySelector(a.getAttribute('href')); }).filter(Boolean);
  function setActive(id) {
    links.forEach(function (a) {
      var on = a.getAttribute('href') === '#' + id;
      a.classList.toggle('active', on);
      if (on) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current');
    });
  }
  function update() {
    var mh = parseInt(getComputedStyle(document.documentElement).getPropertyValue('--masthead-h'), 10) || 72;
    var y = mh + 40, current = sections[0].id;
    sections.forEach(function (s) { if (s.getBoundingClientRect().top - y <= 0) current = s.id; });
    if (window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 4) current = sections[sections.length - 1].id;
    setActive(current);
  }
  window.addEventListener('scroll', update, { passive: true });
  window.addEventListener('resize', update);
  update();

  // Tabs: About me / Education / Research Interests
  var tabs = Array.prototype.slice.call(document.querySelectorAll('.tab'));
  function select(tab) {
    tabs.forEach(function (t) {
      var on = t === tab;
      t.setAttribute('aria-selected', on ? 'true' : 'false');
      t.tabIndex = on ? 0 : -1;
      document.getElementById(t.getAttribute('aria-controls')).hidden = !on;
    });
  }
  tabs.forEach(function (t, i) {
    t.addEventListener('click', function () { select(t); });
    t.addEventListener('keydown', function (e) {
      var n = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
      if (!n) return;
      var next = tabs[(i + n + tabs.length) % tabs.length]; select(next); next.focus();
    });
  });

  // Lightbox for figures
  var box = document.getElementById('lightbox'), img = document.getElementById('lightbox-img'), cap = document.getElementById('lightbox-cap'), lastBtn = null;
  function close() { box.hidden = true; img.removeAttribute('src'); if (lastBtn) lastBtn.focus(); }
  Array.prototype.forEach.call(document.querySelectorAll('.zoom'), function (btn) {
    btn.addEventListener('click', function () {
      var src = btn.querySelector('img');
      img.src = src.getAttribute('src'); img.alt = src.alt; cap.textContent = btn.getAttribute('data-cap') || '';
      lastBtn = btn; box.hidden = false; document.getElementById('lightbox-close').focus();
    });
  });
  document.getElementById('lightbox-close').addEventListener('click', close);
  box.addEventListener('click', function (e) { if (e.target === box) close(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !box.hidden) close(); });

  // Copy email
  var btn = document.getElementById('copy-email');
  btn.addEventListener('click', function () {
    var text = btn.getAttribute('data-copy');
    function done() { btn.textContent = 'Copied'; setTimeout(function () { btn.textContent = 'Copy'; }, 1600); }
    function fallback() {
      var r = document.createRange(); r.selectNodeContents(document.getElementById('email'));
      var s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
    }
    try { navigator.clipboard.writeText(text).then(done, fallback); } catch (e) { fallback(); }
  });
})();
</script>
'''

def full(head_html, body_html, body_class=""):
    cls = f' class="{body_class}"' if body_class else ''
    return ('<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">\n'
            + head_html + f'</head>\n<body{cls}>\n' + body_html + '</body>\n</html>\n')

main_body = masthead("") + (SRC / "main.html").read_text() + FOOTER + LIGHTBOX + MAIN_JS
clean_body = masthead("./", "cleanroom") + (SRC / "cleanroom.html").read_text() + FOOTER

main_head = head("Hoogwan Lee")
clean_head = head("Cleanroom Operations · Hoogwan Lee")

(ROOT / "page.html").write_text(main_head + main_body)            # artifact fragment
(ROOT / "index.html").write_text(full(main_head, main_body))      # Vercel
(ROOT / "cleanroom.html").write_text(full(clean_head, clean_body, "cleanroom-page"))
print("built", [p.name for p in ROOT.glob("*.html")])

# ---- Engineering Projects blog posts (content to be added) ----
POSTS = [
    (1, "[1] Micro-Patterning for Cu Interconnects", "Process flow from lithography to electroplating on SiO2 over Si"),
    (2, "[2] Fab Infrastructure &amp; ICP-CVD Implementation", "Open process chamber of a deposition tool"),
    (3, "[3] S-fab Operations: Equipment Maintenance &amp; User Training", "EVG 501 wafer bonder in the yellow-light cleanroom"),
]
POST_JS = '''<script>
(function () {
  var box = document.getElementById('lightbox'), img = document.getElementById('lightbox-img'), cap = document.getElementById('lightbox-cap'), last = null;
  function close() { box.hidden = true; img.removeAttribute('src'); if (last) last.focus(); }
  Array.prototype.forEach.call(document.querySelectorAll('.zoom'), function (btn) {
    btn.addEventListener('click', function () {
      var src = btn.querySelector('img');
      img.src = src.getAttribute('src'); img.alt = src.alt; cap.textContent = btn.getAttribute('data-cap') || '';
      last = btn; box.hidden = false; document.getElementById('lightbox-close').focus();
    });
  });
  document.getElementById('lightbox-close').addEventListener('click', close);
  box.addEventListener('click', function (e) { if (e.target === box) close(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !box.hidden) close(); });
})();
</script>
'''
for n, title, alt in POSTS:
    src = SRC / f"blog-{n}.html"
    if src.exists():
        inner = '<div class="post-body">\n' + src.read_text() + '    </div>'
    else:
        inner = (f'<figure class="post-hero"><img src="assets/blog-{n}.jpg" alt="{alt}"></figure>\n'
                 '    <div class="post-body">\n      <p class="post-pending">Write-up coming soon.</p>\n    </div>')
    body = (masthead("./", "cleanroom") +
        f'''<main>
  <article class="wrap page-head">
    <a class="back" href="cleanroom.html#blog">← Engineering Projects &amp; Insight</a>
    <div class="kicker" style="margin-top:18px">Blog · Engineering Projects</div>
    <h1>{title}</h1>
    {inner}
  </article>
</main>
''' + FOOTER + (LIGHTBOX + POST_JS if src.exists() else ""))
    (ROOT / f"blog-{n}.html").write_text(full(head(title.replace("&amp;", "&") + " · Hoogwan Lee"), body, "cleanroom-page"))
print("posts built")
