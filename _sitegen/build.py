#!/usr/bin/env python3
"""Builds praterapps.com: home, all apps, one page per app, privacy. Run from anywhere."""
import html, json, os, re, shutil, sys
from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))
from apps import APPS, PLUGGEDIN

SRC = "/home/claude/assets-in"
OUT = "/home/claude/codeprater.github.io"
GEN = os.path.dirname(__file__)
LOOKUP = {r["trackId"]: r for r in json.load(open(f"{SRC}/lookup.json"))["results"] if r.get("wrapperType") == "software"}
E = html.escape


def lum(hexc):
    r, g, b = (int(hexc[i:i + 2], 16) / 255 for i in (1, 3, 5))
    f = lambda c: c / 12.92 if c <= .03928 else ((c + .055) / 1.055) ** 2.4
    return .2126 * f(r) + .7152 * f(g) + .0722 * f(b)


def darken(hexc, k):
    r, g, b = (int(hexc[i:i + 2], 16) for i in (1, 3, 5))
    return "#%02x%02x%02x" % tuple(int(c * k) for c in (r, g, b))


def theme(app):
    a = app["accent"]
    text = a
    while lum(text) > 0.16:          # readable on white
        text = darken(text, 0.88)
    on = "#111111" if lum(a) > 0.35 else "#ffffff"
    return f'--accent:{a};--deep:{app["deep"]};--tint:{app["tint"]};--accentText:{text};--onAccent:{on}'


# ---------- assets ----------
def prepare_assets():
    dst = f"{OUT}/assets/apps"
    if os.path.isdir(dst):
        shutil.rmtree(dst)
    for app in APPS:
        d = f"{dst}/{app['slug']}"
        os.makedirs(d, exist_ok=True)
        src = f"{SRC}/{app['id']}"
        Image.open(f"{src}/icon.jpg").convert("RGB").resize((512, 512), Image.LANCZOS).save(f"{d}/icon.jpg", quality=88)
        shots = []
        for i in range(1, 7):
            p = f"{src}/shot{i}.jpg"
            if os.path.exists(p):
                im = Image.open(p).convert("RGB")
                land = im.width > im.height
                if land and im.width > 1000:
                    im = im.resize((1000, round(im.height * 1000 / im.width)), Image.LANCZOS)
                im.save(f"{d}/shot{i}.jpg", quality=82, optimize=True)
                shots.append((f"shot{i}.jpg", land))
        app["shots"] = shots
    # PluggedIn
    d = f"{dst}/pluggedin"
    os.makedirs(d, exist_ok=True)
    Image.open(f"{SRC}/pluggedin/icon.png").convert("RGB").resize((512, 512), Image.LANCZOS).save(f"{d}/icon.jpg", quality=88)
    PLUGGEDIN["shots"] = []
    for i in range(1, 3):
        p = f"{SRC}/pluggedin/PluggedIn-iPhone-0{i}.jpg"
        if os.path.exists(p):
            im = Image.open(p).convert("RGB")
            im = im.resize((600, round(im.height * 600 / im.width)), Image.LANCZOS)
            im.save(f"{d}/shot{i}.jpg", quality=82, optimize=True)
            PLUGGEDIN["shots"].append((f"shot{i}.jpg", False))


# ---------- shared chrome ----------
LOGO = ('<svg class="p" viewBox="0 0 64 64" aria-hidden="true"><defs><linearGradient id="lg" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#FFE27A"/><stop offset=".55" stop-color="#F7A21B"/><stop offset="1" stop-color="#C8560A"/></linearGradient></defs>'
        '<path d="M14 6h22c11 0 18 7 18 17s-7 17-18 17h-8v18H14z" fill="#9A3F0A" transform="translate(2 3)"/>'
        '<path d="M14 6h22c11 0 18 7 18 17s-7 17-18 17h-8v18H14zM28 18v11h7c3.6 0 6-2.2 6-5.5S38.6 18 35 18z" fill="url(#lg)" fill-rule="evenodd"/></svg>')
SEARCH_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><circle cx="10.5" cy="10.5" r="6.5"/><path d="m20 20-4.6-4.6"/></svg>'
MENU_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>'
APPLE = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M16.4 12.6c0-2.6 2.1-3.8 2.2-3.9-1.2-1.8-3.1-2-3.7-2-1.6-.2-3.1.9-3.9.9-.8 0-2-.9-3.4-.9-1.7 0-3.3 1-4.2 2.6-1.8 3.1-.5 7.7 1.3 10.2.9 1.2 1.9 2.6 3.2 2.6 1.3-.1 1.8-.8 3.3-.8 1.6 0 2 .8 3.4.8 1.4 0 2.3-1.3 3.1-2.5 1-1.4 1.4-2.8 1.4-2.9-.1 0-2.7-1-2.7-4.1zM13.9 5c.7-.9 1.2-2 1.1-3.2-1 0-2.3.7-3 1.6-.7.8-1.3 2-1.1 3.1 1.1.1 2.3-.6 3-1.5z"/></svg>'
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@100..125,800..900&display=swap">')


def head(title, desc, canonical, extra=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="https://praterapps.com{canonical}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta name="theme-color" content="#FBF3E6">
<link rel="icon" href="/assets/favicon.png">
{FONTS}
<link rel="stylesheet" href="/assets/site.css?v=3">
{extra}
</head>
"""


def header(current=""):
    def nav(href, label, key):
        cur = ' aria-current="page"' if key == current else ""
        return f'<a class="nl" href="{href}"{cur}>{label}</a>'
    return f"""<a class="sr" href="#main">Skip to content</a>
<header class="gh" id="gh">
  <div class="wrap bar">
    <a class="logo" href="/" aria-label="Prater Apps home">{LOGO}<span>Prater Apps</span></a>
    <nav aria-label="Site">
      {nav("/apps/", "Apps", "apps")}{nav("/#about", "About", "about")}{nav("/#support", "Support", "support")}
      <button class="icon-btn" id="searchBtn" aria-label="Search apps">{SEARCH_ICON}</button>
      <button class="icon-btn menu-btn" id="menuBtn" aria-label="Menu" aria-expanded="false">{MENU_ICON}</button>
    </nav>
  </div>
</header>
<div class="search" id="search" role="dialog" aria-modal="true" aria-label="Search apps">
  <div class="scrim" data-close></div>
  <div class="panel">
    <div class="field">{SEARCH_ICON.replace('<svg', '<svg width="22" height="22"')}
      <input id="q" type="search" placeholder="Search Prater Apps" autocomplete="off" aria-label="Search apps">
      <button class="icon-btn" data-close aria-label="Close search"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M6 6l12 12M18 6 6 18"/></svg></button>
    </div>
    <h4 id="qlabel">Quick links</h4>
    <ul class="results" id="results"></ul>
  </div>
</div>
"""


FOOTER = """<footer class="gf">
  <div class="wrap cols">
    <div>© 2026 Prater Apps LLC · Eastpointe, Michigan</div>
    <div class="links"><a href="/apps/">All apps</a><a href="/pluggedin/">PluggedIn</a><a href="/privacy.html">Privacy Policy</a>
      <a href="mailto:courtney@praterapps.com">courtney@praterapps.com</a>
      <a href="https://apps.apple.com/us/developer/courtney-prater/id1673042208">App Store</a></div>
  </div>
</footer>
<script src="/assets/site.js?v=3" defer></script>
</body>
</html>
"""


def store_button(url, big=True):
    return (f'<a class="store" href="{url}" target="_blank" rel="noopener">{APPLE}'
            f'<span><small>Download on the</small><b>App Store</b></span></a>')


def app_url(app):
    return app.get("url") or f"/apps/{app['slug']}/"


def store_url(app):
    return LOOKUP[app["id"]]["trackViewUrl"].split("?")[0] if "id" in app else None


# ---------- home ----------
def featured_card(app):
    shots = app["shots"][:2]
    if shots and shots[0][1]:
        imgs = f'<img class="land" src="/assets/apps/{app["slug"]}/{shots[0][0]}" alt="" loading="lazy">'
    else:
        imgs = "".join(f'<img src="/assets/apps/{app["slug"]}/{s}" alt="" loading="lazy">' for s, _ in shots)
    return f"""<a class="fcard" href="{app_url(app)}" style="{theme(app)}">
  <div class="txt">
    <div class="ttl"><img src="/assets/apps/{app['slug']}/icon.jpg" alt=""><h3>{E(app['name'])}</h3></div>
    <p>{E(app['tagline'])}</p>
    <span class="go">Learn more ›</span>
  </div>
  <div class="shots" aria-hidden="true">{imgs}</div>
</a>"""


def tile(app):
    lk = LOOKUP.get(app.get("id"), {})
    price = "Coming soon" if app.get("soon") else (lk.get("formattedPrice") or "")
    badge = '<span class="badge">Soon</span>' if app.get("soon") else ""
    return f"""<a class="tile" href="{app_url(app)}" style="{theme(app)}" data-cat="{E(app['cat'])}" data-name="{E((app['name'] + ' ' + app.get('full', '') + ' ' + app['tagline']).lower())}">
  <img src="/assets/apps/{app['slug']}/icon.jpg" alt="" loading="lazy">
  <div><b>{E(app['name'])}{badge}</b><span>{E(app['tagline'])}</span><div class="meta">{E(app['cat'])} · {E(price)}</div></div>
</a>"""


def all_apps():
    return APPS + [PLUGGEDIN]


def build_home():
    feats = sorted([a for a in APPS if a.get("featured")], key=lambda a: a["featured"])
    cats = ["All"] + sorted({a["cat"] for a in all_apps()})
    chips = "".join(f'<button class="chip" aria-pressed="{"true" if c == "All" else "false"}" data-filter="{E(c)}">{E(c)}</button>' for c in cats)
    page = head("Prater Apps — Different apps for everyday life",
                "Independent iPhone apps by Courtney Prater: communication, accessibility, games and tools for everyday life.", "/")
    page += "<body>\n" + header() + f"""<main id="main">
  <section class="hero wrap">
    <h1 class="wordmark" aria-label="Prater Apps"><span class="depth" aria-hidden="true">Prater Apps</span><span class="face" aria-hidden="true">Prater Apps</span></h1>
    <h2>Different apps for everyday life.</h2>
    <p>Independent iPhone apps by Courtney Prater.</p>
    <a class="btn" href="#apps">Explore apps</a>
  </section>

  <section class="sec wrap" aria-labelledby="feat">
    <div class="sec-head"><h2 id="feat">Featured apps</h2><a href="/apps/">View all apps →</a></div>
    <div class="featured">{''.join(featured_card(a) for a in feats)}</div>
  </section>

  <section class="sec wrap" id="apps" aria-labelledby="all">
    <div class="sec-head"><h2 id="all">All apps</h2><a href="https://apps.apple.com/us/developer/courtney-prater/id1673042208" target="_blank" rel="noopener">See them on the App Store ↗</a></div>
    <div class="filters" role="group" aria-label="Filter apps">{chips}</div>
    <div class="grid" id="grid">{''.join(tile(a) for a in all_apps())}</div>
  </section>

  <section class="sec wrap" id="about" aria-labelledby="ab">
    <div class="about">
      <div class="panel">
        <h3 id="ab">About Prater Apps</h3>
        <p>Prater Apps LLC is an independent studio in Eastpointe, Michigan, run by Courtney Prater. We build iPhone apps for real, everyday moments: tools that help people communicate, stay safe and get work done, and games that bring people together.</p>
        <p>Many of our apps are made for people who are often left out of mainstream technology: nonspeaking and minimally verbal people, their families and caregivers, and neighbors in Detroit and beyond.</p>
      </div>
      <div class="panel" id="support">
        <h3>Support</h3>
        <p>Questions about an app, a purchase or your data? We answer every message.</p>
        <ul>
          <li>Email <a href="mailto:courtney@praterapps.com">courtney@praterapps.com</a></li>
          <li>Read our <a href="/privacy.html">Privacy Policy</a></li>
          <li>PluggedIn help: <a href="/pluggedin/support">PluggedIn Support</a></li>
        </ul>
      </div>
    </div>
  </section>
</main>
""" + FOOTER
    open(f"{OUT}/index.html", "w").write(page)


def build_apps_index():
    cats = ["All"] + sorted({a["cat"] for a in all_apps()})
    chips = "".join(f'<button class="chip" aria-pressed="{"true" if c == "All" else "false"}" data-filter="{E(c)}">{E(c)}</button>' for c in cats)
    page = head("All apps — Prater Apps", "Every Prater Apps app for iPhone, with links to the App Store.", "/apps/")
    page += "<body>\n" + header("apps") + f"""<main id="main">
  <section class="sec wrap" aria-labelledby="all" style="padding-top:40px">
    <div class="sec-head"><h2 id="all">All apps</h2><a href="https://apps.apple.com/us/developer/courtney-prater/id1673042208" target="_blank" rel="noopener">See them on the App Store ↗</a></div>
    <div class="filters" role="group" aria-label="Filter apps">{chips}</div>
    <div class="grid" id="grid">{''.join(tile(a) for a in all_apps())}</div>
  </section>
</main>
""" + FOOTER
    os.makedirs(f"{OUT}/apps", exist_ok=True)
    open(f"{OUT}/apps/index.html", "w").write(page)


# ---------- app pages ----------
def description_html(text):
    out, items = [], []

    def flush():
        if items:
            out.append("<ul>" + "".join(f"<li>{E(i)}</li>" for i in items) + "</ul>")
            items.clear()
    for raw in text.replace("\r", "").split("\n"):
        line = raw.strip()
        if not line:
            flush()
            continue
        bullet = re.match(r"^[•\-\*·]\s*(.+)$", line)
        if bullet:
            items.append(bullet.group(1))
            continue
        flush()
        letters = re.sub(r"[^A-Za-z]", "", line)
        if letters and letters.isupper() and len(line) <= 48:
            out.append(f"<h3>{E(line.title() if len(letters) > 3 else line)}</h3>")
        elif len(line) <= 34 and not line.endswith((".", "!", "?", ":")) and len(line.split()) <= 5:
            out.append(f"<h3>{E(line)}</h3>")
        else:
            out.append(f"<p>{E(line)}</p>")
    flush()
    return "\n".join(out)


def stars(r):
    full = int(round(r))
    return "★" * full + "☆" * (5 - full)


def build_app(app):
    lk = LOOKUP[app["id"]]
    url = store_url(app)
    shots = app["shots"]
    if shots:
        s0, land = shots[0]
        visual = f'<div class="phone{" land" if land else ""}"><img src="shot1.jpg" alt="{E(app["name"])} on iPhone" width="600"></div>'.replace("shot1.jpg", s0)
    else:
        visual = '<img class="bigicon" src="icon.jpg" alt="">'
    facts = [lk.get("primaryGenreName", app["cat"]), lk.get("formattedPrice", ""), f'Ages {lk.get("contentAdvisoryRating", "4+")}']
    if lk.get("userRatingCount"):
        facts.append(f'{stars(lk["averageUserRating"])} {lk["averageUserRating"]:.1f}')
    facts_html = "".join(f"<span>{E(f)}</span>" for f in facts if f)
    gallery = ""
    if shots:
        figs = "".join(f'<figure class="{"land" if l else ""}"><img src="{s}" alt="{E(app["name"])} screenshot {i + 1}" loading="lazy"></figure>'
                       for i, (s, l) in enumerate(shots))
        gallery = f'<section class="asec wrap" id="screens" aria-labelledby="sh"><h2 id="sh">Screenshots</h2><div class="gallery">{figs}</div></section>'
    others = [a for a in APPS if a["slug"] != app["slug"]]
    same = [a for a in others if a["cat"] == app["cat"]][:3]
    more = (same + [a for a in others if a not in same])[:6]
    size = lk.get("fileSizeBytes")
    size_txt = f"{int(size) / 1e6:.0f} MB" if size else "—"
    info = [("Developer", "Prater Apps LLC"), ("Category", lk.get("primaryGenreName", app["cat"])), ("Price", lk.get("formattedPrice", "")),
            ("Age rating", lk.get("contentAdvisoryRating", "")), ("Size", size_txt), ("Version", lk.get("version", "")),
            ("Requires", f'iOS {lk.get("minimumOsVersion", "")} or later')]
    info_html = "".join(f"<dt>{E(k)}</dt><dd>{E(str(v))}</dd>" for k, v in info if v)
    title = f'{app["name"]} — Prater Apps'
    page = head(title, app["tagline"], f'/apps/{app["slug"]}/',
                f'<meta property="og:image" content="https://praterapps.com/assets/apps/{app["slug"]}/icon.jpg">'
                f'<meta name="apple-itunes-app" content="app-id={app["id"]}">')
    page = page.replace('<meta name="theme-color" content="#FBF3E6">', f'<meta name="theme-color" content="{app["deep"]}">')
    page += f'<body style="{theme(app)}">\n' + header() + f"""<div class="appnav">
  <div class="wrap bar">
    <a class="nm" href="#top"><img src="icon.jpg" alt="">{E(app['name'])}</a>
    <nav class="links" aria-label="{E(app['name'])}">
      <a href="#top">Overview</a>{'<a href="#screens">Screenshots</a>' if shots else ''}<a href="#about-app">Features</a><a href="#info">Information</a><a href="#support-app">Support</a>
    </nav>
    <a class="get" href="{url}" target="_blank" rel="noopener">{'Get' if lk.get('price', 0) == 0 else E(lk.get('formattedPrice', 'Get'))}</a>
  </div>
</div>
<main id="main">
  <section class="ahero" id="top">
    <div class="wrap">
      <div>
        <img class="icon" src="icon.jpg" alt="{E(app['name'])} app icon" width="132" height="132">
        <div class="kicker">{E(app['cat'])}</div>
        <h1>{E(app['name'])}</h1>
        <p class="tag">{E(app['tagline'])}</p>
        {store_button(url)}
        <div class="facts">{facts_html}</div>
      </div>
      {visual}
    </div>
  </section>
  {gallery}
  <section class="asec wrap" id="about-app" aria-labelledby="ft">
    <h2 id="ft">About {E(app['name'])}</h2>
    <div class="desc">
      <div class="copy">{description_html(lk.get('description', ''))}</div>
      <aside class="info" id="info" aria-label="Information">
        <dl>{info_html}</dl>
        <div class="links" id="support-app">
          <a href="{url}" target="_blank" rel="noopener">View on the App Store <span>↗</span></a>
          <a href="mailto:courtney@praterapps.com?subject={E(app['name'])}%20support">Get support <span>›</span></a>
          <a href="/privacy.html">Privacy Policy <span>›</span></a>
        </div>
      </aside>
    </div>
  </section>
  <section class="more wrap" aria-labelledby="mo">
    <div class="sec-head"><h2 id="mo">More from Prater Apps</h2><a href="/apps/">See all →</a></div>
    <div class="grid">{''.join(tile(a) for a in more)}</div>
  </section>
</main>
""" + FOOTER
    base = f"/assets/apps/{app['slug']}/"
    page = re.sub(r'src="((?:icon|shot\d)\.jpg)"', lambda m: f'src="{base}{m.group(1)}"', page)
    d = f"{OUT}/apps/{app['slug']}"
    os.makedirs(d, exist_ok=True)
    open(f"{d}/index.html", "w").write(page)


# ---------- privacy ----------
def build_privacy():
    src = open(f"{OUT}/privacy.html").read()
    m = re.search(r'<div class="wrap">(.*?)</div>\s*</body>', src, re.S) or re.search(r'<main[^>]*>(.*?)</main>', src, re.S)
    body = m.group(1) if m else ""
    body = re.sub(r'<p class="back">.*?</p>', "", body, flags=re.S)
    page = head("Privacy Policy — Prater Apps", "How Prater Apps LLC handles information in its apps and on this website.", "/privacy.html")
    page += "<body>\n" + header() + f'<main id="main" class="wrap" style="max-width:780px;padding-top:36px;padding-bottom:40px"><div class="panel">{body}</div></main>\n' + FOOTER
    open(f"{OUT}/privacy.html", "w").write(page)


def build_js():
    data = [dict(n=a["name"], t=a["tagline"], c=a["cat"], u=app_url(a), i=f'/assets/apps/{a["slug"]}/icon.jpg',
                 k=(a["name"] + " " + a.get("full", "") + " " + a["tagline"] + " " + a["cat"]).lower()) for a in all_apps()]
    js = open(f"{GEN}/site.js").read().replace("/*APPS*/[]", json.dumps(data, ensure_ascii=False))
    open(f"{OUT}/assets/site.js", "w").write(js)


def build_favicon():
    Image.open(f"{GEN}/favicon.png").save(f"{OUT}/assets/favicon.png") if os.path.exists(f"{GEN}/favicon.png") else None


if __name__ == "__main__":
    os.makedirs(f"{OUT}/assets", exist_ok=True)
    prepare_assets()
    shutil.copy(f"{GEN}/site.css", f"{OUT}/assets/site.css")
    build_js()
    build_favicon()
    build_home()
    build_apps_index()
    for a in APPS:
        build_app(a)
    if not os.path.exists(f"{GEN}/.privacy_done"):
        build_privacy()
        open(f"{GEN}/.privacy_done", "w").write("1")
    print("built", len(APPS), "app pages")
