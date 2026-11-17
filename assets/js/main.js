(function () {
  var D = window.I18N, T = D.t, root = document.documentElement;
  var lang = root.dataset.lang || "pt";
  var store = { get: function () { try { return localStorage.getItem("lang"); } catch (e) { return null; } },
                set: function (v) { try { localStorage.setItem("lang", v); } catch (e) {} } };

  function waLink(key) { return "https://wa.me/" + D.wa + "?text=" + encodeURIComponent(T[key][lang]); }
  function setMeta(sel, attr, val) { var el = document.querySelector(sel); if (el) el.setAttribute(attr, val); }

  function apply(l, push) {
    if (!T["meta.title"][l]) return;
    lang = l; root.dataset.lang = l; root.lang = D.htmlLang[l];
    document.querySelectorAll("[data-i18n]").forEach(function (el) { var v = T[el.dataset.i18n]; if (v && v[l] != null) el.innerHTML = v[l]; });
    document.querySelectorAll("[data-i18n-alt]").forEach(function (el) { el.alt = T[el.dataset.i18nAlt][l]; });
    document.querySelectorAll("[data-i18n-aria]").forEach(function (el) { el.setAttribute("aria-label", T[el.dataset.i18nAria][l]); });
    document.querySelectorAll("[data-i18n-ph]").forEach(function (el) { el.placeholder = T[el.dataset.i18nPh][l]; });
    document.querySelectorAll("[data-gcap]").forEach(function (el) { el.alt = D.caps[el.dataset.gcap][l]; });
    document.querySelectorAll("[data-wa]").forEach(function (el) { el.href = waLink(el.dataset.wa); });
    document.querySelectorAll(".lang a").forEach(function (a) { a.setAttribute("aria-current", a.dataset.lang === l ? "true" : "false"); });
    document.title = T["meta.title"][l];
    var url = D.site + "/" + D.paths[l] + "/";
    setMeta('meta[name="description"]', "content", T["meta.desc"][l]);
    setMeta('meta[name="keywords"]', "content", T["meta.keywords"][l]);
    setMeta('meta[property="og:title"]', "content", T["meta.title"][l]);
    setMeta('meta[property="og:description"]', "content", T["meta.desc"][l]);
    setMeta('meta[property="og:url"]', "content", url);
    setMeta('link[rel="canonical"]', "href", url);
    store.set(l);
    if (push) { try { history.pushState({ lang: l }, "", "../" + D.paths[l] + "/" + location.hash); } catch (e) {} }
  }

  document.querySelectorAll(".lang a").forEach(function (a) {
    a.addEventListener("click", function (e) { e.preventDefault(); if (a.dataset.lang !== lang) apply(a.dataset.lang, true); });
  });
  window.addEventListener("popstate", function (e) { if (e.state && e.state.lang) apply(e.state.lang, false); });
  try { history.replaceState({ lang: lang }, ""); } catch (e) {}
  store.set(lang);

  // header / menu
  var header = document.querySelector(".header"), burger = document.getElementById("burger"), nav = document.getElementById("nav");
  var toTop = document.getElementById("toTop");
  function onScroll() { header.classList.toggle("scrolled", scrollY > 40); if (toTop) toTop.classList.toggle("show", scrollY > 600); }
  addEventListener("scroll", onScroll, { passive: true }); onScroll();
  burger.addEventListener("click", function () {
    var o = nav.classList.toggle("open"); burger.setAttribute("aria-expanded", o);
  });
  nav.querySelectorAll("a").forEach(function (a) { a.addEventListener("click", function () { nav.classList.remove("open"); burger.setAttribute("aria-expanded", false); }); });

  var reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  // "Início", logo e seta: rolam até o topo
  function goTop(e) { e.preventDefault(); window.scrollTo({ top: 0, behavior: reduce ? "auto" : "smooth" }); nav.classList.remove("open"); burger.setAttribute("aria-expanded", false); }
  document.querySelectorAll('a[href="#top"]').forEach(function (a) { a.addEventListener("click", goTop); });

  // reveal
  var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } }); }, { threshold: .12 });
  document.querySelectorAll(".reveal").forEach(function (el) { io.observe(el); });

  var reduce = matchMedia("(prefers-reduced-motion: reduce)").matches, fine = matchMedia("(pointer: fine)").matches;

  // 3D tilt
  if (!reduce && fine) document.querySelectorAll(".tilt").forEach(function (el) {
    var base = getComputedStyle(el).transform; base = base === "none" ? "" : base;
    el.addEventListener("mousemove", function (e) {
      var r = el.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
      el.style.transform = base + " perspective(900px) rotateY(" + x * 10 + "deg) rotateX(" + -y * 10 + "deg) translateZ(6px)";
    });
    el.addEventListener("mouseleave", function () { el.style.transform = ""; });
  });

  // parallax
  if (!reduce) {
    var layers = document.querySelectorAll("[data-depth]");
    addEventListener("scroll", function () {
      layers.forEach(function (l) { var r = l.parentElement.getBoundingClientRect(); l.style.transform = "translate3d(0," + (-r.top * l.dataset.depth) + "px,0)"; });
    }, { passive: true });
  }


  // capa: clicar numa foto gira e traz para frente; clicar na da frente manda para trás
  var stack = document.getElementById("stack");
  if (stack) {
    var order = ["p0", "p1", "p2"], timer;
    var pics = [].slice.call(stack.querySelectorAll("img"));
    function rotateTo(img) {
      var cur = pics.map(function (p) { return p.className.match(/p\d/)[0]; });
      var i = pics.indexOf(img), pos = cur[i], newPos;
      if (pos === "p0") { // frente vai para o fundo, as outras sobem
        pics.forEach(function (p, k) { newPos = { p0: "p1", p1: "p2", p2: "p0" }[cur[k]]; p.className = newPos; });
      } else {
        pics.forEach(function (p, k) {
          p.className = k === i ? "p0" : (cur[k] === "p0" ? pos : cur[k]);
        });
      }
      var front = pics.filter(function (p) { return p.className === "p0"; })[0];
      if (!reduce) { front.classList.add("spin"); setTimeout(function () { front.classList.remove("spin"); }, 950); }
    }
    pics.forEach(function (p) { p.addEventListener("click", function () { rotateTo(p); restart(); }); });
    function restart() { clearInterval(timer); if (!reduce) timer = setInterval(function () { rotateTo(pics.filter(function (p) { return p.className.indexOf("p0") === 0; })[0]); }, 5000); }
    restart();
  }

  // carrossel de depoimentos
  var rt = document.getElementById("revTrack");
  if (rt) {
    var step = function () { var c = rt.querySelector(".rev"); return c ? c.getBoundingClientRect().width + 18 : 300; };
    document.querySelector(".rev-nav.prev").addEventListener("click", function () { rt.scrollBy({ left: -step(), behavior: "smooth" }); });
    document.querySelector(".rev-nav.next").addEventListener("click", function () {
      if (rt.scrollLeft + rt.clientWidth >= rt.scrollWidth - 8) rt.scrollTo({ left: 0, behavior: "smooth" });
      else rt.scrollBy({ left: step(), behavior: "smooth" });
    });
  }

  // gallery filters
  var items = [].slice.call(document.querySelectorAll(".g-item"));
  document.querySelectorAll(".filters button").forEach(function (b) {
    b.addEventListener("click", function () {
      document.querySelectorAll(".filters button").forEach(function (x) { x.classList.toggle("active", x === b); });
      var f = b.dataset.filter;
      items.forEach(function (it) { it.classList.toggle("hide", f !== "all" && it.dataset.cat.split(" ").indexOf(f) < 0); });
    });
  });

  // lightbox
  var lb = document.getElementById("lb"), lbImg = lb.querySelector("img"), lbCap = lb.querySelector("figcaption"), idx = 0, lastFocus;
  function visible() { return items.filter(function (i) { return !i.classList.contains("hide"); }); }
  function show(i) {
    var v = visible(); idx = (i + v.length) % v.length;
    var b = v[idx].querySelector("button"), img = b.querySelector("img");
    lbImg.src = b.dataset.full; lbImg.alt = img.alt; lbCap.textContent = img.alt;
  }
  items.forEach(function (it) {
    it.querySelector("button").addEventListener("click", function () {
      lastFocus = this; show(visible().indexOf(it)); lb.hidden = false; lb.querySelector(".lb-x").focus(); document.body.style.overflow = "hidden";
    });
  });
  function close() { lb.hidden = true; document.body.style.overflow = ""; if (lastFocus) lastFocus.focus(); }
  lb.querySelector(".lb-x").onclick = close;
  lb.querySelector(".lb-p").onclick = function () { show(idx - 1); };
  lb.querySelector(".lb-n").onclick = function () { show(idx + 1); };
  lb.addEventListener("click", function (e) { if (e.target === lb) close(); });
  addEventListener("keydown", function (e) {
    if (lb.hidden) return;
    if (e.key === "Escape") close(); if (e.key === "ArrowLeft") show(idx - 1); if (e.key === "ArrowRight") show(idx + 1);
  });

  // pickup form -> WhatsApp
  var L = { pt: ["Nome", "Data", "Pessoas", "Local de busca", "Passeio", "Horário"], en: ["Name", "Date", "People", "Pickup location", "Tour", "Time"], es: ["Nombre", "Fecha", "Personas", "Lugar de recogida", "Paseo", "Hora"] };
  // o botão é um link real: o endereço é refeito a cada campo preenchido
  var form = document.getElementById("pickForm"), pickBtn = document.getElementById("pickBtn");
  function val(id) { var el = document.getElementById(id); return el ? el.value.trim() : ""; }
  function updatePick() {
    var k = L[lang], lines = [T["wa.pick"][lang], ""];
    if (val("f-name")) lines.push(k[0] + ": " + val("f-name"));
    if (val("f-date")) lines.push(k[1] + ": " + val("f-date").split("-").reverse().join("/"));
    if (val("f-time")) lines.push(k[5] + ": " + val("f-time"));
    if (val("f-people")) lines.push(k[2] + ": " + val("f-people"));
    if (val("f-place")) lines.push(k[3] + ": " + val("f-place"));
    lines.push(k[4] + ": " + T[val("f-tour")][lang]);
    pickBtn.href = "https://wa.me/" + D.wa + "?text=" + encodeURIComponent(lines.join("\n"));
  }
  form.addEventListener("input", updatePick);
  form.addEventListener("change", updatePick);
  form.addEventListener("submit", function (e) { e.preventDefault(); updatePick(); pickBtn.click(); });
  pickBtn.addEventListener("mousedown", updatePick);
  pickBtn.addEventListener("click", updatePick);
  pickBtn.addEventListener("touchstart", updatePick, { passive: true });
  document.querySelectorAll(".lang a").forEach(function (a) { a.addEventListener("click", function () { setTimeout(updatePick, 0); }); });
  updatePick();

  document.getElementById("yr").textContent = new Date().getFullYear();
})();
