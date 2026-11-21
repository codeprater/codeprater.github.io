// Prater Apps: menu, search and app filters.
(() => {
  const APPS = /*APPS*/[];
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
