#!/usr/bin/env python3
"""Builds praterapps.com: home, all apps, one page per app, privacy. Run from anywhere."""
import html, json, os, re, shutil, sys
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(__file__))
from apps import APPS, PLUGGEDIN, SOON, WATCH, TV

SRC = os.environ.get("ASSETS_IN", "/home/claude/assets-in")
OUT = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
GEN = os.path.dirname(__file__)
LOOKUP = ({r["trackId"]: r for r in json.load(open(f"{SRC}/lookup.json"))["results"] if r.get("wrapperType") == "software"}
          if os.path.exists(f"{SRC}/lookup.json") else {})   # only the full build needs App Store data
V = 6   # cache-buster for site.css / site.js
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
    make_soon_icons()


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
<link rel="stylesheet" href="/assets/site.css?v={V}">
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
      {nav("/", "YAPPP", "home")}{nav("/#pilot", "Schools &amp; SLPs", "pilot")}{nav("/apps/", "All apps", "apps")}{nav("/#about", "About", "about")}
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


FOOTER = f"""<footer class="gf">
  <div class="wrap cols">
    <div>© 2026 Prater Apps LLC · Eastpointe, Michigan</div>
    <div class="links"><a href="/apps/">All apps</a><a href="/pluggedin/">PluggedIn</a><a href="/privacy.html">Privacy Policy</a>
      <a href="mailto:courtney@praterapps.com">courtney@praterapps.com</a>
      <a href="https://apps.apple.com/us/developer/courtney-prater/id1673042208">App Store</a>
      <a href="https://www.linkedin.com/company/praterapps/" rel="noopener" target="_blank">LinkedIn</a>
      <a href="https://www.linkedin.com/in/courtney-prater-55651a264/" rel="me noopener" target="_blank">Courtney on LinkedIn</a></div>
  </div>
</footer>
<script src="/assets/site.js?v={V}" defer></script>
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
    return APPS + SOON + [PLUGGEDIN]


FLAGSHIP = "yappp"
ICON_TAP = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M9 11.2V5.5a1.75 1.75 0 0 1 3.5 0v4.6l4.3.9c1.3.3 2.2 1.5 2 2.8l-.7 5.1A2.5 2.5 0 0 1 15.6 21h-4.2c-.8 0-1.5-.4-2-1l-3.7-4.8a1.6 1.6 0 0 1 2.3-2.2L9 14.1z"/></svg>'
ICON_PEOPLE = '<svg viewBox="0 0 24 24" fill="currentColor"><circle cx="8" cy="8" r="3.2"/><circle cx="16.5" cy="7.5" r="3.6"/><path d="M1.5 19c0-3.3 2.9-5.5 6.5-5.5 1.3 0 2.5.3 3.5.8-1.4 1.1-2.3 2.7-2.3 4.7z"/><path d="M9.5 19.5c0-3.6 3.1-6 7-6s7 2.4 7 6z"/></svg>'
ICON_CHART = '<svg viewBox="0 0 24 24" fill="currentColor"><rect x="3" y="11" width="5" height="9" rx="1.6"/><rect x="9.5" y="7.5" width="5" height="12.5" rx="1.6"/><rect x="16" y="4" width="5" height="16" rx="1.6"/></svg>'
LANE = ["yappp", "aucommadate", "wis"]          # the communication lane, in order


def lane_card(app):
    lk = LOOKUP.get(app.get("id"), {})
    price = lk.get("formattedPrice") or ""
    return f"""<a class="tile" href="{app_url(app)}" style="{theme(app)}">
  <img src="/assets/apps/{app['slug']}/icon.jpg" alt="" loading="lazy">
  <div><b>{E(app['name'])}</b><span>{E(app['tagline'])}</span><div class="meta">{E(app['cat'])} · {E(price)}</div></div>
</a>"""


def build_home():
    """One product, one audience: AAC and communication tools. The full catalog lives at /apps/."""
    flag = by_slug(FLAGSHIP)
    land = [s for s, l in flag["shots"] if l]
    shots = (f'<img class="land" src="/assets/apps/{flag["slug"]}/{land[0]}" alt="YAPPP on iPad">' if land else
             "".join(f'<img src="/assets/apps/{flag["slug"]}/{flag["shots"][i][0]}" alt="YAPPP screenshot" loading="lazy">'
                     for i in (1, 0, 4) if i < len(flag["shots"])))   # caregivers · board · progress
    lane = [by_slug(s) for s in LANE[1:]]
    page = head("Prater Apps — AAC and communication apps for nonspeaking people",
                HOME_DESC, "/")
    page += "<body>\n" + header() + f"""<main id="main">
  <section class="band" style="{theme(flag)}">
   <div class="hero wrap focus">
    <p class="eyebrow"><img src="/assets/apps/{flag['slug']}/icon.jpg" alt="">YAPPP · AAC app</p>
    <h2>A voice for people who communicate differently.</h2>
    <p>Tap a tile, and YAPPP speaks. Built for nonspeaking and minimally verbal people, and for the families, teachers and speech-language pathologists who support them.</p>
    <div class="ctas">
      <a class="btn" href="{store_url(flag)}" target="_blank" rel="noopener">{APPLE}Get YAPPP on the App Store</a>
      <a class="btn ghost" href="#pilot">For schools &amp; SLPs</a>
    </div>
    <p class="plats-line">iPhone · iPad · Mac · Apple Watch · CarPlay</p>
    <div class="hero-shots" aria-hidden="true">{shots}</div>
   </div>
  </section>

  <section class="sec wrap" aria-labelledby="who">
    <div class="sec-head center"><h2 id="who">Built for everyone in the conversation</h2></div>
    <div class="three">
      <div class="panel who" style="--c:#4A9EFF"><span class="ic">{ICON_TAP}</span><h3>The person speaking</h3><p>Tap tiles to speak and build full sentences. Photo, video and emoji tiles, and the ASL sign for any word.</p></div>
      <div class="panel who" style="--c:#3DD66B"><span class="ic">{ICON_PEOPLE}</span><h3>Families &amp; caregivers</h3><p>See what your person needs in real time, with urgent messages pinned to the top.</p></div>
      <div class="panel who" style="--c:#FF9F4A"><span class="ic">{ICON_CHART}</span><h3>Teachers &amp; SLPs</h3><p>Track vocabulary growth and export reports made for therapy sessions and IEP meetings.</p></div>
    </div>
  </section>

  <section class="sec wrap" id="demo" aria-labelledby="dm">
    <div class="demo">
      <div class="demo-video">
        <video src="/media/yappp-promo.mp4" poster="/media/yappp-promo.jpg" controls muted playsinline preload="metadata"
               aria-label="60-second demo: making a Dad photo tile and a Thank You sign-language video tile in YAPPP"></video>
      </div>
      <div class="demo-copy">
        <p class="eyebrow-dark">See it in 60 seconds</p>
        <h2 id="dm">Make any word a tile.</h2>
        <ol>
          <li><b>New Tile.</b> Settings → Add Cards → New Tile.</li>
          <li><b>Label and emoji.</b> Type the word, pick an emoji.</li>
          <li><b>Your photo or video.</b> Add a real photo of Dad, or a video of someone signing in ASL.</li>
          <li><b>Tap to speak.</b> It's on the board. Tap it and YAPPP says the word, and video tiles sign it too.</li>
        </ol>
        <a class="btn" href="{store_url(flag)}" target="_blank" rel="noopener" style="{theme(flag)}">Get YAPPP on the App Store</a>
      </div>
    </div>
  </section>

  <section class="sec wrap" id="pilot" aria-labelledby="pl">
    <div class="panel cta-panel" style="{theme(flag)}">
      <h3 id="pl">Bring YAPPP to your classroom or practice</h3>
      <p>We're working with a small group of speech-language pathologists, special-education teachers and families. Tell us who you support and what you use today, and we'll set you up and listen to everything you say.</p>
      <a class="btn" href="mailto:courtney@praterapps.com?subject=YAPPP%20pilot&body=I%20am%20a%20(SLP%20%2F%20teacher%20%2F%20parent)%20and%20I%20support%3A%20">Join the pilot</a>
    </div>
  </section>

  <section class="sec wrap" aria-labelledby="more">
    <div class="sec-head"><h2 id="more">More communication tools</h2></div>
    <div class="grid">{''.join(lane_card(a) for a in lane)}</div>
  </section>

  <section class="sec wrap" id="about" aria-labelledby="ab">
    <div class="about">
      <div class="panel">
        <h3 id="ab">About Prater Apps</h3>
        <p>Prater Apps LLC is an independent studio in Eastpointe, Michigan, founded by Courtney Prater. Our focus is communication technology for nonspeaking and minimally verbal people and the people who support them.</p>
        <p>Courtney has built and shipped {len(APPS)} apps to the App Store as a solo founder, across iPhone, iPad, Mac, Apple Watch, Apple TV and CarPlay. YAPPP is where that work comes together.</p>
        <p><a href="/apps/">See every Prater Apps app →</a></p>
      </div>
      <div class="panel" id="support">
        <h3>Contact</h3>
        <ul>
          <li>Support and schools: <a href="mailto:courtney@praterapps.com">courtney@praterapps.com</a></li>
          <li>Investors and partners: <a href="mailto:courtney@praterapps.com?subject=Investing%20in%20Prater%20Apps">courtney@praterapps.com</a></li>
          <li><a href="/privacy.html">Privacy Policy</a></li>
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


# ---------- coming soon, Apple Watch and Apple TV ----------
HERO_P = "AAC and communication apps for nonspeaking people, their families and the professionals who support them."
HOME_DESC = ("YAPPP is an AAC app for iPhone, iPad, Mac and Apple Watch from Prater Apps: speech tiles, ASL support, "
             "caregiver tools and SLP reports for nonspeaking and minimally verbal people.")
WATCH_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" aria-hidden="true"><rect x="6.5" y="6" width="11" height="12" rx="3.2"/><path d="M9 6l.6-3h4.8L15 6M9 18l.6 3h4.8l.6-3M17.5 10.5h1.2"/></svg>'
TV_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2.5" y="4.5" width="19" height="12.5" rx="2.2"/><path d="M8 20.5h8"/></svg>'


def by_slug(slug):
    return next(a for a in all_apps() if a["slug"] == slug)


def plat_rows(items):
    out = []
    for it in items:
        a = by_slug(it["slug"])
        pill = '<span class="pill live">Available</span>' if it["live"] else '<span class="pill">Coming soon</span>'
        out.append(f"""<li><a class="prow" href="{app_url(a)}" style="{theme(a)}">
        <img src="/assets/apps/{a['slug']}/icon.jpg" alt="" loading="lazy">
        <div><b>{E(a['name'])}{pill}</b><span>{E(it['note'])}</span></div></a></li>""")
    return "".join(out)


def soon_card(a):
    plats = "".join(f"<span>{E(p)}</span>" for p in a.get("platforms", ["iPhone"]))
    lead = next((t for h, t in a.get("about", []) if isinstance(t, str)), a["tagline"])
    return f"""<a class="scard" href="{app_url(a)}" style="{theme(a)}">
      <div class="top"><img src="/assets/apps/{a['slug']}/icon.jpg" alt="" loading="lazy"><div><h3>{E(a['name'])}</h3><p class="tg">{E(a['tagline'])}</p></div></div>
      <p>{E(lead)}</p>
      <div class="chips">{plats}</div>
    </a>"""


PLUGGEDIN.setdefault("platforms", ["iPhone"])
PLUGGEDIN.setdefault("about", [("", "PluggedIn connects neighbors who need a hand with local workers who want to earn on their own schedule, with every job verified.")])


def extra_sections():
    return f"""<!--extra-->
  <section class="sec wrap" id="platforms" aria-labelledby="pf">
    <div class="sec-head"><h2 id="pf">Beyond the iPhone</h2></div>
    <p class="lede">Some moments don't happen on a phone. A game belongs on the biggest screen in the room, and a call for help belongs on your wrist. These are the Prater Apps you can use on Apple Watch and Apple TV, and the ones on the way.</p>
    <div class="plats">
      <div class="panel plat">
        <h3>{WATCH_ICON}Apple Watch apps</h3>
        <p>For quick moments when pulling out a phone is too slow: one tap to speak, talk to your crew or stay in the game.</p>
        <ul>{plat_rows(WATCH)}</ul>
      </div>
      <div class="panel plat">
        <h3>{TV_ICON}Apple TV apps</h3>
        <p>For game night. Put it on the TV and everyone in the room is part of it.</p>
        <ul>{plat_rows(TV)}</ul>
        <p class="fine">More Apple TV apps are on the way.</p>
      </div>
    </div>
  </section>

  <section class="sec wrap" id="soon" aria-labelledby="cs">
    <div class="sec-head"><h2 id="cs">Coming soon</h2><a href="mailto:courtney@praterapps.com?subject=Tell%20me%20about%20new%20Prater%20Apps">Get launch news →</a></div>
    <p class="lede">What we're building now. Each one has its own page, and you can ask to be told the day it launches.</p>
    <div class="soon">{''.join(soon_card(a) for a in SOON + [PLUGGEDIN])}</div>
  </section>
  <!--/extra-->"""


def build_soon(app):
    name = app["name"]
    blocks = []
    for h, body in app["about"]:
        if h:
            blocks.append(f"<h3>{E(h)}</h3>")
        blocks.append("<ul>" + "".join(f"<li>{E(i)}</li>" for i in body) + "</ul>" if isinstance(body, list) else f"<p>{E(body)}</p>")
    plats = app.get("platforms", ["iPhone"])
    notify = f'mailto:courtney@praterapps.com?subject=Tell%20me%20when%20{E(name)}%20launches'
    info = [("Developer", "Prater Apps LLC"), ("Category", app["cat"]), ("Status", "In development"), ("Platforms", ", ".join(plats))]
    info_html = "".join(f"<dt>{E(k)}</dt><dd>{E(v)}</dd>" for k, v in info)
    more = [a for a in SOON if a["slug"] != app["slug"]] + [PLUGGEDIN]
    page = head(f"{name} — Coming soon from Prater Apps", app["tagline"], f'/apps/{app["slug"]}/',
                f'<meta property="og:image" content="https://praterapps.com/assets/apps/{app["slug"]}/icon.jpg">')
    page = page.replace('<meta name="theme-color" content="#FBF3E6">', f'<meta name="theme-color" content="{app["deep"]}">')
    icon = f'/assets/apps/{app["slug"]}/icon.jpg'
    page += f'<body style="{theme(app)}">\n' + header() + f"""<div class="appnav">
  <div class="wrap bar">
    <a class="nm" href="#top"><img src="{icon}" alt="">{E(name)}</a>
    <nav class="links" aria-label="{E(name)}"><a href="#top">Overview</a><a href="#about-app">What's coming</a><a href="#info">Information</a></nav>
    <a class="get" href="{notify}">Notify me</a>
  </div>
</div>
<main id="main">
  <section class="ahero" id="top">
    <div class="wrap">
      <div>
        <img class="icon" src="{icon}" alt="{E(name)} app icon" width="132" height="132">
        <div class="kicker">Coming soon · {E(app['cat'])}</div>
        <h1>{E(name)}</h1>
        <p class="tag">{E(app['tagline'])}</p>
        <a class="store notify" href="{notify}"><span><small>Not on the App Store yet</small><b>Tell me when it launches</b></span></a>
        <div class="facts">{''.join(f'<span>{E(p)}</span>' for p in plats)}</div>
      </div>
      <img class="bigicon dup" src="{icon}" alt="">
    </div>
  </section>
  <section class="asec wrap" id="about-app" aria-labelledby="ft">
    <h2 id="ft">About {E(name)}</h2>
    <div class="desc">
      <div class="copy">{''.join(blocks)}<p class="fine">{E(name)} is still being built, so features can change before launch.</p></div>
      <aside class="info" id="info" aria-label="Information">
        <dl>{info_html}</dl>
        <div class="links">
          <a href="{notify}">Tell me when it launches <span>›</span></a>
          <a href="mailto:courtney@praterapps.com?subject={E(name)}">Ask about {E(name)} <span>›</span></a>
          <a href="/privacy.html">Privacy Policy <span>›</span></a>
        </div>
      </aside>
    </div>
  </section>
  <section class="more wrap" aria-labelledby="mo">
    <div class="sec-head"><h2 id="mo">Also coming soon</h2><a href="/apps/">See all apps →</a></div>
    <div class="grid">{''.join(tile(a) for a in more)}</div>
  </section>
</main>
""" + FOOTER
    d = f"{OUT}/apps/{app['slug']}"
    os.makedirs(d, exist_ok=True)
    open(f"{d}/index.html", "w").write(page)


def make_soon_icons():
    """Placeholder icons drawn in each app's colors. A real icon saved as _sitegen/icons/<slug>.png wins."""
    S = 1024
    rgb = lambda h: tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))
    mix = lambda a, b, t: tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))
    for app in SOON:
        d = f"{OUT}/assets/apps/{app['slug']}"
        os.makedirs(d, exist_ok=True)
        real = f"{GEN}/icons/{app['slug']}.png"
        if os.path.exists(real):
            Image.open(real).convert("RGB").resize((512, 512), Image.LANCZOS).save(f"{d}/icon.jpg", quality=90)
            continue
        acc, deep, white = rgb(app["accent"]), rgb(app["deep"]), (255, 255, 255)
        im = Image.new("RGB", (S, S), deep)
        g = ImageDraw.Draw(im)
        top = mix(deep, acc, .38)
        for y in range(S):
            g.line([(0, y), (S, y)], fill=mix(top, deep, y / S))
        s = app["slug"]
        if s == "owwl":
            for cx in (330, 694):
                g.ellipse([cx - 190, 300, cx + 190, 680], fill=white)
                g.ellipse([cx - 118, 372, cx + 118, 608], fill=acc)
                g.ellipse([cx - 58, 432, cx + 58, 548], fill=deep)
            g.polygon([(452, 660), (572, 660), (512, 800)], fill=acc)
            g.polygon([(140, 250), (330, 230), (210, 400)], fill=acc)
            g.polygon([(884, 250), (694, 230), (814, 400)], fill=acc)
        elif s == "doozer":
            g.ellipse([150, 150, 874, 874], fill=acc)
            g.ellipse([330, 380, 440, 490], fill=deep)
            g.arc([570, 370, 710, 510], 200, 340, fill=deep, width=44)
            g.arc([300, 340, 724, 740], 25, 155, fill=deep, width=52)
        elif s == "prater":
            g.rounded_rectangle([402, 260, 622, 764], 56, fill=white)
            g.rounded_rectangle([432, 310, 592, 714], 26, fill=deep)
            g.ellipse([462, 462, 562, 562], fill=acc)
            for k, w in ((0, 46), (1, 40)):
                r = 300 + k * 120
                g.arc([512 - r, 512 - r, 512 + r, 512 + r], 140, 220, fill=acc, width=w)
                g.arc([512 - r, 512 - r, 512 + r, 512 + r], -40, 40, fill=acc, width=w)
        elif s == "heroles":
            w = 54
            pts = [(210, 814), (210, 210), (814, 210), (814, 814), (360, 814), (360, 360), (664, 360), (664, 664), (512, 664), (512, 512)]
            g.line(pts, fill=white, width=w, joint="curve")
            for x, y in pts[:1] + pts[-1:]:
                g.ellipse([x - w // 2, y - w // 2, x + w // 2, y + w // 2], fill=white)
            g.ellipse([452, 452, 572, 572], fill=acc)
        elif s == "gormee":
            g.polygon([(512, 150), (300, 560), (724, 560)], fill=acc)
            g.ellipse([272, 400, 752, 880], fill=acc)
            g.arc([352, 480, 672, 800], 100, 170, fill=white, width=40)
        im.resize((512, 512), Image.LANCZOS).save(f"{d}/icon.jpg", quality=90)


def patch_soon():
    """Adds the coming-soon apps and the Watch / TV sections to the published site without the
    App Store data a full build needs: python3 build.py soon"""
    make_soon_icons()
    shutil.copy(f"{GEN}/site.css", f"{OUT}/assets/site.css")
    for a in SOON:
        build_soon(a)
    tiles = "<!--soon-tiles-->" + "".join(tile(a) for a in SOON) + "<!--/soon-tiles-->"
    cats = ["All"] + sorted({a["cat"] for a in all_apps()})
    chips = "".join(f'<button class="chip" aria-pressed="{"true" if c == "All" else "false"}" data-filter="{E(c)}">{E(c)}</button>' for c in cats)
    for rel in ("index.html", "apps/index.html"):
        s = open(f"{OUT}/{rel}").read()
        s = re.sub(r"<!--soon-tiles-->.*?<!--/soon-tiles-->", "", s, flags=re.S)
        assert s.count('<a class="tile" href="/pluggedin/"') == 1, rel
        s = s.replace('<a class="tile" href="/pluggedin/"', tiles + '<a class="tile" href="/pluggedin/"')
        s, n = re.subn(r'(<div class="filters"[^>]*>).*?</div>', lambda m: m.group(1) + chips + "</div>", s, flags=re.S)
        assert n == 1, rel
        if rel == "index.html":
            s = re.sub(r"\s*<!--extra-->.*?<!--/extra-->", "", s, flags=re.S)
            mark = '  <section class="sec wrap" id="about"'
            assert s.count(mark) == 1
            s = s.replace(mark, "  " + extra_sections() + "\n" + mark)
            s = s.replace("<p>Independent iPhone apps by Courtney Prater.</p>", f"<p>{HERO_P}</p>")
            s = s.replace(E("Independent iPhone apps by Courtney Prater: communication, accessibility, games and tools for everyday life."), E(HOME_DESC))
            s = s.replace("We build iPhone apps for real, everyday moments", "We build apps for iPhone, iPad, Apple Watch and Apple TV, made for real, everyday moments")
        open(f"{OUT}/{rel}", "w").write(s)
    # search data
    p = f"{OUT}/assets/site.js"
    js = open(p).read()
    m = re.search(r"const APPS = (\[.*?\]);\n", js, re.S)
    data = [d for d in json.loads(m.group(1)) if d["u"] not in {app_url(a) for a in SOON}]
    new = [dict(n=a["name"], t=a["tagline"], c=a["cat"], u=app_url(a), i=f'/assets/apps/{a["slug"]}/icon.jpg',
                k=(a["name"] + " " + a["tagline"] + " " + a["cat"] + " coming soon " + " ".join(a["platforms"])).lower()) for a in SOON]
    at = next((i for i, d in enumerate(data) if d["u"] == "/pluggedin/"), len(data))
    data[at:at] = new
    open(p, "w").write(js[:m.start(1)] + json.dumps(data, ensure_ascii=False) + js[m.end(1):])
    # nav links and cache-buster on every generated page
    nav_new = '<a class="nl" href="/#platforms">Watch &amp; TV</a><a class="nl" href="/#soon">Coming soon</a>'
    n = 0
    for root, _, files in os.walk(OUT):
        if "/pluggedin" in root or "/.git" in root or "/_sitegen" in root:
            continue
        for f in files:
            if f.endswith(".html"):
                fp = os.path.join(root, f)
                s = open(fp).read()
                t = re.sub(r"(/assets/site\.(?:css|js))\?v=\d+", rf"\1?v={V}", s)
                if nav_new not in t:
                    t = t.replace('<a class="nl" href="/#about"', nav_new + '<a class="nl" href="/#about"')
                if t != s:
                    open(fp, "w").write(t)
                    n += 1
    print("soon pages:", len(SOON), "· pages touched:", n)


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


def build_home_only():
    """Rebuilds the homepage and the header nav on every generated page from the assets already in
    the repo (no App Store download needed). Set ASSETS_IN to a folder with lookup.json for prices/links."""
    for app in APPS:
        d = f"{OUT}/assets/apps/{app['slug']}"
        app["shots"] = [(f, Image.open(f"{d}/{f}").width > Image.open(f"{d}/{f}").height)
                        for f in sorted(os.listdir(d)) if f.startswith("shot")] if os.path.isdir(d) else []
    shutil.copy(f"{GEN}/site.css", f"{OUT}/assets/site.css")
    build_home()
    nav_re = re.compile(r'(<nav aria-label="Site">\s*).*?(\s*<button class="icon-btn" id="searchBtn")', re.S)
    links = re.search(r'<nav aria-label="Site">\s*(.*?)\s*<button', header(), re.S).group(1)
    n = 0
    for root, _, files in os.walk(OUT):
        if "/pluggedin" in root or "/.git" in root or "/_sitegen" in root:
            continue
        for f in files:
            if f.endswith(".html") and not (root == OUT and f == "index.html"):
                fp = os.path.join(root, f)
                s = open(fp).read()
                t = nav_re.sub(lambda m: m.group(1) + links + m.group(2), s, count=1)
                t = re.sub(r"(/assets/site\.(?:css|js))\?v=\d+", rf"\1?v={V}", t)
                if t != s:
                    open(fp, "w").write(t)
                    n += 1
    print("home rebuilt · pages touched:", n)


if __name__ == "__main__":
    if sys.argv[1:] == ["home"]:
        build_home_only()
        sys.exit()
    if sys.argv[1:] == ["soon"]:
        patch_soon()
        sys.exit()
    os.makedirs(f"{OUT}/assets", exist_ok=True)
    prepare_assets()
    shutil.copy(f"{GEN}/site.css", f"{OUT}/assets/site.css")
    build_js()
    build_favicon()
    build_home()
    build_apps_index()
    for a in APPS:
        build_app(a)
    for a in SOON:
        build_soon(a)
    if not os.path.exists(f"{GEN}/.privacy_done"):
        build_privacy()
        open(f"{GEN}/.privacy_done", "w").write("1")
    print("built", len(APPS), "app pages")
