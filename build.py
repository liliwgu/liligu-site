#!/usr/bin/env python3
"""Builds the multi-page site from src/site.html (the single source of truth).
Run: python3 build.py   -> writes index.html, film.html, commercial.html, other-work.html, about.html, press.html, contact.html
"""
import re, pathlib
root = pathlib.Path(__file__).parent
src = (root / "src/site.html").read_text()

def between(a, b, s=src, start=0):
    i = s.index(a, start); j = s.index(b, i) + len(b); return s[i:j]

head = src[:src.index("<body>")]
sections = {m.group(1): m.group(0) for m in re.finditer(r'  <section class="block" id="(\w+)".*?\n  </section>\n', src, re.S)}
hero = between('  <section class="hero"', '  </section>\n')
footer = between('<footer>', '</footer>\n')
scripts = re.findall(r'<script>.*?</script>\n', src, re.S)
film_js, reel_js, fx_js, vid_js = scripts[0], scripts[1], scripts[2], scripts[3]

PAGES = [  # slug, section id, nav label, page title, tile image, tile alt
    ("film", "film", "Film", "Film & video", "haircut.jpg", "An older man in glasses peers through a green gate behind leaves"),
    ("commercial", "brand", "Commercial", "Commercial & branded", "b-microsoft.jpg", None),
    ("other-work", "other", "Other work", "Other work", "dontgiveup.jpg", None),
    ("about", "about", "About", "About", "portrait.jpg", None),
    ("press", "press", "Press", "Press & readings", None, None),
    ("contact", "contact", "Contact", "Contact", None, None),
]

def nav(current):
    items = "\n".join(
        f'        <li><a href="/{slug}"{" aria-current=\"page\"" if slug == current else ""}>{label}</a></li>'
        for slug, _, label, *_ in PAGES)
    mark = '' if current == "home" else '    <a class="mark" href="/" aria-label="Lili Gu, home"><img class="t-light" src="/img/mark.webp" alt="" width="420" height="120"><img class="t-dark" src="/img/mark-bright.webp" alt="" width="420" height="120"></a>\n'
    return f'''<header class="site{' home' if current == 'home' else ''}">
  <div class="wrap">
{mark}    <nav aria-label="Main">
      <ul>
{items}
      </ul>
    </nav>
  </div>
</header>
'''

def page_head(title, path):
    h = head
    h = h.replace("<title>Lili Gu</title>", f"<title>{title}</title>")
    h = h.replace('<meta property="og:title" content="Lili Gu">', f'<meta property="og:title" content="{title}">')
    h = h.replace('content="https://www.liligu.com/"', f'content="https://www.liligu.com/{path}"')
    h = h.replace('href="https://www.liligu.com/"', f'href="https://www.liligu.com/{path}"')
    return h

def page(title, path, current, body, js):
    return (page_head(title, path) + "<body>\n<a class=\"skip\" href=\"#main\">Skip to content</a>\n" + nav(current)
            + f'\n<main id="main" class="{"home" if current == "home" else "inner"}">\n' + body + "</main>\n\n" + footer + "\n" + "".join(js) + "</body>\n</html>\n")

# Home: hero + tiles to each section
tiles = []
for slug, sid, label, title, img, _ in PAGES:
    if not img: continue
    tiles.append(f'''      <a class="tile" href="/{slug}"><span class="ph"><img src="img/{img}" alt="" loading="lazy"></span><span class="tl">{title} <span aria-hidden="true">→</span></span></a>''')
home_body = hero + '''
  <section class="tiles-wrap" aria-label="Explore">
    <div class="wrap tiles">
''' + "\n".join(tiles) + '''
    </div>
  </section>
'''
# old one-page links like liligu.com/#about still land on the right page
redirect_js = '''<script>
(function(){var m={film:"/film",brand:"/commercial",portfolio:"/commercial",other:"/other-work",about:"/about",press:"/press",contact:"/contact",films:"/film"};var h=location.hash.slice(1);if(m[h])location.replace(m[h]);})();
</script>
'''
(root / "index.html").write_text(page("Lili Gu", "", "home", home_body, [redirect_js, reel_js, fx_js]))

for slug, sid, label, title, *_ in PAGES:
    body = sections[sid]
    js = [film_js, fx_js] if sid == "film" else [vid_js, fx_js] if sid == "brand" else [fx_js]
    (root / f"{slug}.html").write_text(page(f"{title} · Lili Gu", slug, slug, body, js))
print("built", ["index"] + [p[0] for p in PAGES])
# the old Google Sites portfolio lived at /portfolio
(root / "portfolio.html").write_text('<!doctype html><meta charset="utf-8"><title>Commercial &amp; branded · Lili Gu</title><link rel="canonical" href="https://www.liligu.com/commercial"><meta http-equiv="refresh" content="0; url=/commercial"><a href="/commercial">Commercial &amp; branded work</a>\n')
