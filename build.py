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
    mark = '' if current == "home" else '    <a class="mark" href="/" aria-label="Lili Gu, home"><img class="t-light" src="/img/mark.webp" alt="" width="526" height="120"><img class="t-dark" src="/img/mark-bright.webp" alt="" width="526" height="120"></a>\n'
    return f'''<header class="site{' home' if current == 'home' else ''}">
  <div class="wrap">
{mark}    <nav aria-label="Main">
      <ul>
{items}
        <li class="reel-li"><a class="reel-btn" href="https://vimeo.com/158287395" data-reel aria-haspopup="dialog"><span class="pl" aria-hidden="true"></span>Reel</a></li>
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

REEL_POP = '''<dialog class="reel-pop" id="reel-pop" aria-label="Video"><div class="rp-in"><button class="rp-x" type="button" aria-label="Close video">×</button><div class="rp-frame"></div></div></dialog>
<script>
(function(){var d=document.getElementById('reel-pop');if(!d||!d.showModal)return;var fr=d.querySelector('.rp-frame');
function pop(src,title){fr.innerHTML='';var f=document.createElement('iframe');f.src=src;f.title=title||'Video';f.allow='autoplay; fullscreen; picture-in-picture';f.allowFullscreen=true;fr.appendChild(f);d.showModal();}
window.lgPop=pop;window.lgVimeo=function(id,t){pop('https://player.vimeo.com/video/'+id+'?autoplay=1&title=0&byline=0&portrait=0&dnt=1'+(t?'#t='+t+'s':''));};
function open(e){e.preventDefault();lgVimeo(this.getAttribute('data-reel')||'158287395');}
function close(){d.close();}
d.addEventListener('close',function(){if(!d.open)fr.innerHTML='';});
d.querySelector('.rp-x').addEventListener('click',close);
d.addEventListener('click',function(e){if(e.target===d)close();});
document.querySelectorAll('[data-reel]').forEach(function(a){a.addEventListener('click',open);});})();
// pop-out players lift off the page: the player flies up from the tile you clicked, kicking up ink specks, and settles back into it on close
(function(){if(!Element.prototype.animate)return;var calm=matchMedia('(prefers-reduced-motion: reduce)').matches,src=null;
document.addEventListener('click',function(e){var t=e.target.closest&&e.target.closest('.vid,.ph[data-embed],.mv,#pvm,[data-reel],a,button');if(t&&!t.closest('dialog'))src=t},true);
var top=document.createElement('div');top.className='fx-l';document.body.appendChild(top);
function rnd(a,b){return a+Math.random()*(b-a)}
var plain=!!document.getElementById('brand');// Commercial gets a clean lift, no specks (Lili, 2026-11-25)
function specks(L,x,y,n,o){if(plain)return Promise.resolve();var ps=[];for(var i=0;i<n;i++){var s=document.createElement('span');s.className='speck';var z=rnd(o.min||3,o.max||11);s.style.width=z+'px';s.style.height=(z*rnd(.8,1.15))+'px';L.appendChild(s);
var a=o.dir!=null?o.dir+rnd(-o.spread,o.spread):rnd(0,6.283),d=rnd(o.near,o.far),sx=x+rnd(-o.jx,o.jx),sy=y+rnd(-(o.jy||0),o.jy||0);
var an=s.animate([{transform:'translate('+(sx-z/2)+'px,'+(sy-z/2)+'px) scale(.3)',opacity:0},{opacity:1,offset:.15},{transform:'translate('+(sx+Math.cos(a)*d-z/2)+'px,'+(sy+Math.sin(a)*d+rnd(0,30)-z/2)+'px) scale(1)',opacity:.9,offset:.7},{transform:'translate('+(sx+Math.cos(a)*d*1.05-z/2)+'px,'+(sy+Math.sin(a)*d+rnd(10,40)-z/2)+'px) scale(.9)',opacity:0}],{duration:o.dur,delay:rnd(0,120),easing:'cubic-bezier(.15,.75,.3,1)',fill:'both'});
(function(s,an){ps.push(an.finished.then(function(){s.remove()},function(){s.remove()}))})(s,an)}return Promise.all(ps)}
function tileOf(t){return t&&t.isConnected&&t.querySelector('img')&&t.getBoundingClientRect().width>40?t:null}
document.querySelectorAll('dialog.reel-pop').forEach(function(d){var pl=d.querySelector('.rp-frame'),x=d.querySelector('.rp-x'),sc=document.createElement('div'),L=document.createElement('div'),tile=null,busy=false;
sc.className='rp-scrim';L.className='fx-l';d.insertBefore(sc,d.firstChild);d.appendChild(L);sc.addEventListener('click',function(){d.close()});
function geo(){var T=tile.getBoundingClientRect(),P=pl.getBoundingClientRect(),s=T.width/P.width;return {T:T,s:s,dx:T.left+T.width/2-(P.left+P.width/2),dy:T.top+T.height/2-(P.top+P.height/2),tx:T.left+T.width/2,ty:T.top+T.height/2}}
function opened(){tile=tileOf(src);src=null;
if(calm||!tile){sc.animate([{opacity:0},{opacity:1}],{duration:calm?200:300});pl.animate([{opacity:0},{opacity:1}],{duration:calm?200:300});return}
var g=geo();tile.classList.add('lifted');
specks(L,g.tx,g.ty,16,{near:g.T.width*.45,far:g.T.width*.9,dur:700,jx:g.T.width*.3,jy:g.T.height*.25});
sc.animate([{opacity:0},{opacity:1}],{duration:500});x.animate([{opacity:0},{opacity:0,offset:.7},{opacity:1}],{duration:750});
pl.animate([{transform:'translate('+g.dx+'px,'+g.dy+'px) scale('+g.s+')',boxShadow:'0 2px 6px rgba(0,0,0,.2)'},
{transform:'translate('+g.dx*.35+'px,'+(g.dy*.35-24)+'px) scale('+(g.s+(1-g.s)*.62)+') rotate(-1.6deg)',boxShadow:'0 50px 90px rgba(0,0,0,.5)',offset:.55},
{transform:'none',boxShadow:'0 30px 80px rgba(0,0,0,.45)'}],{duration:750,easing:'cubic-bezier(.3,.7,.2,1)'})}
new MutationObserver(function(){if(d.open&&!busy)opened()}).observe(d,{attributes:true,attributeFilter:['open']});
var shut=HTMLDialogElement.prototype.close;
function done(){busy=false;if(tile)tile.classList.remove('lifted');shut.call(d)}
d.close=function(){if(busy||!d.open)return;busy=true;
if(calm||!tileOf(tile)){Promise.all([sc.animate([{opacity:1},{opacity:0}],{duration:200,fill:'forwards'}).finished,pl.animate([{opacity:1},{opacity:0}],{duration:200,fill:'forwards'}).finished]).then(done,done);return}
var g=geo();x.animate([{opacity:1},{opacity:0}],{duration:200,fill:'forwards'});
Promise.all([sc.animate([{opacity:1},{opacity:0}],{duration:450,delay:150,fill:'forwards'}).finished,
pl.animate([{transform:'none'},{transform:'translate('+g.dx*.55+'px,'+(g.dy*.55-18)+'px) scale('+(g.s+(1-g.s)*.45)+') rotate(1.2deg)',offset:.5},{transform:'translate('+g.dx+'px,'+g.dy+'px) scale('+g.s+')',boxShadow:'0 0 0 rgba(0,0,0,0)'}],{duration:620,easing:'cubic-bezier(.5,0,.3,1)',fill:'forwards'}).finished]).then(function(){
var t=tile;done();var T=t.getBoundingClientRect();specks(top,T.left+T.width/2,T.top+T.height*.9,10,{dir:-1.57,spread:1.2,near:20,far:60,dur:600,jx:T.width*.4,min:2,max:7})},done)};
d.addEventListener('close',function(){d.getAnimations({subtree:true}).forEach(function(a){a.cancel()});busy=false;if(tile)tile.classList.remove('lifted')});
d.addEventListener('cancel',function(e){e.preventDefault();d.close()});});})();
</script>
'''

def page(title, path, current, body, js):
    js = list(js) + [REEL_POP]
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
