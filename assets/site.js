// Prater Apps: menu, search and app filters.
(() => {
  const APPS = [{"n": "Cleanee", "t": "Hotel laundry pickup and delivery for production crews.", "c": "Productivity", "u": "/apps/cleanee/", "i": "/assets/apps/cleanee/icon.jpg", "k": "cleanee laundry wash fold production staff crew hotel pickup billing support"}, {"n": "YAPPP", "t": "Accessible speech tiles for everyday communication.", "c": "Communication", "u": "/apps/yappp/", "i": "/assets/apps/yappp/icon.jpg", "k": "yappp yappp - aac accessible speech tiles for everyday communication. communication"}, {"n": "PASSEE", "t": "Greeting cards that move. Turn your photos into beautiful postcards.", "c": "Social", "u": "/apps/passee/", "i": "/assets/apps/passee/icon.jpg", "k": "passee  greeting cards that move. turn your photos into beautiful postcards. social"}, {"n": "Hawt Potato", "t": "A fast, fun hot-potato party game.", "c": "Games", "u": "/apps/hawt-potato/", "i": "/assets/apps/hawt-potato/icon.jpg", "k": "hawt potato hawt potato a fast, fun hot-potato party game. games"}, {"n": "Au'commadate", "t": "A touch-only communication board and family support app.", "c": "Communication", "u": "/apps/aucommadate/", "i": "/assets/apps/aucommadate/icon.jpg", "k": "au'commadate  a touch-only communication board and family support app. communication"}, {"n": "StoreeMail", "t": "Your email, told as stories you can watch and hear.", "c": "Productivity", "u": "/apps/storeemail/", "i": "/assets/apps/storeemail/icon.jpg", "k": "storeemail  your email, told as stories you can watch and hear. productivity"}, {"n": "Ahem.", "t": "Video messages in your own voice, for when a text isn't enough.", "c": "Communication", "u": "/apps/ahem/", "i": "/assets/apps/ahem/icon.jpg", "k": "ahem.  video messages in your own voice, for when a text isn't enough. communication"}, {"n": "W.I.S.", "t": "Who Is Speaking: say what you mean, and be heard.", "c": "Communication", "u": "/apps/wis/", "i": "/assets/apps/wis/icon.jpg", "k": "w.i.s.  who is speaking: say what you mean, and be heard. communication"}, {"n": "WHO IS TALKING2?", "t": "See the shape of a conversation, not just the words.", "c": "Communication", "u": "/apps/who-is-talking/", "i": "/assets/apps/who-is-talking/icon.jpg", "k": "who is talking2?  see the shape of a conversation, not just the words. communication"}, {"n": "CHECKFINEPRINT", "t": "Read contracts and long forms before you sign.", "c": "Productivity", "u": "/apps/checkfineprint/", "i": "/assets/apps/checkfineprint/icon.jpg", "k": "checkfineprint  read contracts and long forms before you sign. productivity"}, {"n": "CHECKTHESHELF", "t": "Before you buy it, check it. Recalls and date codes in a scan.", "c": "Productivity", "u": "/apps/checktheshelf/", "i": "/assets/apps/checktheshelf/icon.jpg", "k": "checktheshelf  before you buy it, check it. recalls and date codes in a scan. productivity"}, {"n": "TRUSS", "t": "Crew push-to-talk that runs the whole production day.", "c": "Productivity", "u": "/apps/truss/", "i": "/assets/apps/truss/icon.jpg", "k": "truss truss: crew push to talk crew push-to-talk that runs the whole production day. productivity"}, {"n": "PeWhipee", "t": "Memory games made from your own photos.", "c": "Games", "u": "/apps/pewhipee/", "i": "/assets/apps/pewhipee/icon.jpg", "k": "pewhipee  memory games made from your own photos. games"}, {"n": "Double Jumpx", "t": "A stylish jump-rope rhythm game.", "c": "Games", "u": "/apps/double-jumpx/", "i": "/assets/apps/double-jumpx/icon.jpg", "k": "double jumpx  a stylish jump-rope rhythm game. games"}, {"n": "Wink One", "t": "Note-passing for real life.", "c": "Social", "u": "/apps/wink-one/", "i": "/assets/apps/wink-one/icon.jpg", "k": "wink one  note-passing for real life. social"}, {"n": "ROOZER!", "t": "Send energy, mood and reaction without typing a paragraph.", "c": "Social", "u": "/apps/roozer-signals/", "i": "/assets/apps/roozer-signals/icon.jpg", "k": "roozer!  send energy, mood and reaction without typing a paragraph. social"}, {"n": "ROOZER", "t": "Face, eye and voice challenge games. Don't flinch.", "c": "Games", "u": "/apps/roozer/", "i": "/assets/apps/roozer/icon.jpg", "k": "roozer  face, eye and voice challenge games. don't flinch. games"}, {"n": "GEE-14", "t": "Don't Flinch: fast reflex and focus games.", "c": "Games", "u": "/apps/gee-14/", "i": "/assets/apps/gee-14/icon.jpg", "k": "gee-14  don't flinch: fast reflex and focus games. games"}, {"n": "Honey Badger", "t": "Honey Badger: The Last Hive. A cartoon action adventure.", "c": "Games", "u": "/apps/honey-badger/", "i": "/assets/apps/honey-badger/icon.jpg", "k": "honey badger honeybadger game honey badger: the last hive. a cartoon action adventure. games"}, {"n": "GORMEE", "t": "Scan, save and check receipts, labels and warranty terms.", "c": "Productivity", "u": "/apps/gormee/", "i": "https://is1-ssl.mzstatic.com/image/thumb/Purple221/v4/7c/cc/d1/7cccd14c-9f1e-c337-d316-310c2390a028/AppIcon-0-0-1x_U007epad-0-1-85-220.png/512x512bb.jpg", "k": "gormee scan, save and check receipts, labels and warranty terms. productivity receipt label barcode warranty agreement"}, {"n": "OWWL", "t": "Private messaging you can answer with your face.", "c": "Social", "u": "/apps/owwl/", "i": "/assets/apps/owwl/icon.jpg", "k": "owwl private messaging you can answer with your face. social coming soon iphone ipad"}, {"n": "Doozer", "t": "Say it with your face. Messages without typing.", "c": "Communication", "u": "/apps/doozer/", "i": "/assets/apps/doozer/icon.jpg", "k": "doozer say it with your face. messages without typing. communication coming soon iphone"}, {"n": "Prater", "t": "One game across your iPhone, Apple Watch and headphones.", "c": "Games", "u": "/apps/prater/", "i": "/assets/apps/prater/icon.jpg", "k": "prater one game across your iphone, apple watch and headphones. games coming soon iphone ipad apple watch apple tv"}, {"n": "HEROLES", "t": "Race the clock through the maze. Heroes against villains.", "c": "Games", "u": "/apps/heroles/", "i": "/assets/apps/heroles/icon.jpg", "k": "heroles race the clock through the maze. heroes against villains. games coming soon iphone"}, {"n": "PluggedIn", "t": "Hire local help or earn on your schedule. Every job verified.", "c": "Productivity", "u": "/pluggedin/", "i": "/assets/apps/pluggedin/icon.jpg", "k": "pluggedin  hire local help or earn on your schedule. every job verified. productivity"}];
  const $ = (s, r = document) => r.querySelector(s);

  // Mobile menu
  const gh = $("#gh"), menuBtn = $("#menuBtn");
  menuBtn && menuBtn.addEventListener("click", () => {
    const open = gh.classList.toggle("open");
    menuBtn.setAttribute("aria-expanded", open);
  });

  // Search overlay (like apple.com): quick links, then live results as you type.
  const search = $("#search"), q = $("#q"), results = $("#results"), label = $("#qlabel");
  let lastFocus = null;
  const esc = s => s.replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const row = a => `<li><a href="${a.u}"><img src="${a.i}" alt=""><div><b>${esc(a.n)}</b><span>${esc(a.t)}</span></div></a></li>`;
  function render() {
    const term = q.value.trim().toLowerCase();
    const list = term ? APPS.filter(a => term.split(/\s+/).every(w => a.k.includes(w))) : APPS.slice(0, 6);
    label.textContent = term ? `${list.length} result${list.length === 1 ? "" : "s"}` : "Quick links";
    results.innerHTML = list.length ? list.map(row).join("") : `<li class="none">No apps match “${esc(q.value)}”.</li>`;
  }
  function openSearch() {
    lastFocus = document.activeElement;
    search.classList.add("open");
    document.body.style.overflow = "hidden";
    render();
    setTimeout(() => q.focus(), 30);
  }
  function closeSearch() {
    search.classList.remove("open");
    document.body.style.overflow = "";
    q.value = "";
    lastFocus && lastFocus.focus();
  }
  const sBtn = $("#searchBtn");
  sBtn && sBtn.addEventListener("click", openSearch);
  search && search.addEventListener("click", e => { if (e.target.closest("[data-close]")) closeSearch(); });
  q && q.addEventListener("input", render);
  q && q.addEventListener("keydown", e => {
    if (e.key === "Enter") { const first = results.querySelector("a"); if (first) location.href = first.href; }
  });
  document.addEventListener("keydown", e => {
    if (e.key === "Escape" && search.classList.contains("open")) closeSearch();
    if (e.key === "/" && !search.classList.contains("open") && !/input|textarea/i.test(document.activeElement.tagName)) { e.preventDefault(); openSearch(); }
  });

  // Category chips on the app grid
  document.querySelectorAll(".filters").forEach(group => {
    const grid = group.parentElement.querySelector(".grid");
    group.addEventListener("click", e => {
      const chip = e.target.closest(".chip");
      if (!chip) return;
      group.querySelectorAll(".chip").forEach(c => c.setAttribute("aria-pressed", c === chip));
      const cat = chip.dataset.filter;
      grid.querySelectorAll(".tile").forEach(t => { t.hidden = cat !== "All" && t.dataset.cat !== cat; });
    });
  });

  // Close the mobile menu after picking an in-page link
  document.querySelectorAll('.gh nav a[href^="/#"]').forEach(a => a.addEventListener("click", () => gh.classList.remove("open")));
})();
