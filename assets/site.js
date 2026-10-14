/* M.Y.V. Alanya Travel — shared site script (all pages, all languages).
   Page data comes from window.MYV, written into each page by build/build.py. */
(function () {
  'use strict';
  var C = window.MYV || {};
  var U = C.ui || {};
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var body = document.body;

  /* ---------- full-height hero ---------- */
  var hero = document.querySelector('.hero');
  /* the booking button is always a bit bigger than the button next to it (any language, any screen) */
  function sizeCtas() {
    Array.prototype.forEach.call(document.querySelectorAll('.cta-pair'), function (c) {
      var bk = c.querySelector('.btn-gold'), other = c.querySelector('.btn:not(.btn-gold)');
      if (!bk || !other) return;
      c.classList.remove('stack'); bk.style.minWidth = ''; other.style.minWidth = '';
      bk.style.minWidth = Math.ceil(other.offsetWidth * 1.15) + 'px';
      var a = bk.getBoundingClientRect(), o = other.getBoundingClientRect();
      if (o.top >= a.bottom - 1 || a.top >= o.bottom - 1) c.classList.add('stack');
    });
  }
  function fitHero() {
    sizeCtas();
    if (!hero) return;
    var s = 1, max = window.innerHeight + 2;
    hero.style.setProperty('--hs', '1');
    while (hero.offsetHeight > max && s > 0.6) { s -= 0.03; hero.style.setProperty('--hs', s.toFixed(2)); }
  }
  function setFullH() { document.documentElement.style.setProperty('--fullh', window.innerHeight + 'px'); fitHero(); }
  setFullH();
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(fitHero);
  window.addEventListener('load', fitHero);

  /* ---------- scroll lock helpers ---------- */
  var openLayers = 0;
  function lock() { openLayers++; body.style.overflow = 'hidden'; }
  function unlock() { openLayers = Math.max(0, openLayers - 1); if (!openLayers) body.style.overflow = ''; }

  /* ---------- generic modal ---------- */
  var lastFocus = null;
  function openModal(el) {
    if (!el || !el.hidden) return;
    lastFocus = document.activeElement;
    el.hidden = false; lock(); onScroll();
    var f = el.querySelector('input,select,textarea,button:not(.x),a[href]');
    if (f) setTimeout(function () { try { f.focus({ preventScroll: true }); } catch (e) {} }, 40);
  }
  function closeModal(el) {
    if (!el || el.hidden) return;
    el.hidden = true; unlock(); onScroll();
    var fr = el.querySelector('iframe'); if (fr) fr.remove();
    if (lastFocus && lastFocus.focus) { try { lastFocus.focus({ preventScroll: true }); } catch (e) {} }
  }
  function openLayer() { return $$('.modal:not([hidden]), .filmbox:not([hidden])').pop(); }

  /* ---------- header, mega menu, mobile sheet, language menu ---------- */
  var hdr = $('#hdr'), mega = $('#mega'), scrim = $('#megaScrim'), megaBtn = $('#megaBtn');
  function setMega(open) {
    if (!mega) return;
    mega.hidden = !open; if (scrim) scrim.hidden = !open;
    if (megaBtn) megaBtn.setAttribute('aria-expanded', String(open));
    onScroll();
  }
  if (megaBtn) megaBtn.addEventListener('click', function () { setMega(mega.hidden); });
  if (scrim) scrim.addEventListener('click', function () { setMega(false); });

  var sheet = $('#sheet'), burger = $('#burger');
  function setSheet(open) {
    if (!sheet) return;
    if (open === !sheet.hidden) return;
    sheet.hidden = !open; burger.setAttribute('aria-expanded', String(open));
    if (open) lock(); else unlock();
  }
  if (burger) burger.addEventListener('click', function () { setSheet(true); });
  var sc = $('#sheetClose'); if (sc) sc.addEventListener('click', function () { setSheet(false); });
  if (sheet) sheet.addEventListener('click', function (e) { if (e.target.closest('a')) setSheet(false); });

  $$('.langsw').forEach(function (w) {
    var b = w.querySelector('button'), list = w.querySelector('ul');
    b.addEventListener('click', function (e) { e.stopPropagation(); list.hidden = !list.hidden; b.setAttribute('aria-expanded', String(!list.hidden)); });
    document.addEventListener('click', function () { if (!list.hidden) { list.hidden = true; b.setAttribute('aria-expanded', 'false'); } });
  });

  /* ---------- booking bar ---------- */
  var bar = $('#bar'), foot = $('footer');
  function onScroll() {
    var y = window.scrollY;
    if (hdr) hdr.classList.toggle('on', C.page !== 'home' || y > 40 || (mega && !mega.hidden));
    if (bar) {
      var fTop = foot ? foot.getBoundingClientRect().top : 1e9;
      var on = y > 350 && fTop > window.innerHeight - 20 && !openLayer();
      bar.classList.toggle('on', on);
      bar.setAttribute('aria-hidden', String(!on));
      var bb = bar.querySelector('button'); if (bb) bb.tabIndex = on ? 0 : -1;
    }
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', function () { setFullH(); onScroll(); });

  /* ---------- package tabs ---------- */
  var pkgIdx = 0;
  $$('[data-pkg]').forEach(function (b) {
    b.addEventListener('click', function () {
      pkgIdx = +b.dataset.pkg;
      $$('[data-pkg]').forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
      $$('.pkgpanel').forEach(function (p, i) { p.hidden = i !== pkgIdx; });
    });
  });

  /* ---------- gallery -> main media ---------- */
  var mediaBox = $('#mediaBox');
  function mediaEl(type, src, alt) {
    if (type === 'video') {
      var v = document.createElement('video');
      v.src = src; v.autoplay = true; v.muted = true; v.loop = true; v.playsInline = true; v.setAttribute('playsinline', ''); v.preload = 'metadata';
      return v;
    }
    var i = document.createElement('img'); i.src = src; i.alt = alt || ''; return i;
  }
  $$('[data-media]').forEach(function (b) {
    b.addEventListener('click', function () {
      if (!mediaBox) return;
      var old = mediaBox.querySelector('img,video');
      var el = mediaEl(b.dataset.type, b.dataset.media, b.dataset.alt);
      if (old) old.replaceWith(el); else mediaBox.prepend(el);
      $$('[data-media]').forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
      if (window.innerWidth < 1024) mediaBox.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  });
  $$('video[data-autoplay]').forEach(function (v) { v.muted = true; var p = v.play(); if (p && p.catch) p.catch(function () {}); });

  /* ---------- stop details ---------- */
  var stopModal = $('#stopModal');
  $$('[data-stop]').forEach(function (b) {
    b.addEventListener('click', function () {
      var tpl = document.getElementById(b.dataset.stop);
      if (!tpl || !stopModal) return;
      $('#smBody').innerHTML = '';
      $('#smBody').appendChild(tpl.content.cloneNode(true));
      openModal(stopModal);
    });
  });

  /* ---------- reviews, legal, film ---------- */
  $$('[data-open]').forEach(function (b) {
    b.addEventListener('click', function () { openModal(document.getElementById(b.dataset.open)); });
  });
  // delegated: also works for buttons added later (e.g. inside the "special highlight" window)
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-close]');
    if (b) closeModal(b.closest('.modal, .filmbox'));
  });
  $$('.modal, .filmbox').forEach(function (m) {
    m.addEventListener('click', function (e) { if (e.target === m) closeModal(m); });
  });
  var film = $('#film');
  $$('[data-film]').forEach(function (b) {
    b.addEventListener('click', function () {
      if (!film) return;
      var box = $('.vframe', film);
      box.innerHTML = '';
      var f = document.createElement('iframe');
      f.src = 'https://www.youtube-nocookie.com/embed/' + b.dataset.film + '?autoplay=1&rel=0&modestbranding=1&playsinline=1';
      f.title = b.dataset.title || 'Video';
      f.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
      f.allowFullscreen = true;
      box.appendChild(f);
      var fb = $('#filmBook'); if (fb && b.dataset.tour) { fb.dataset.book = b.dataset.tour; }
      openModal(film);
    });
  });

  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    var m = openLayer();
    if (m) { closeModal(m); return; }
    if (mega && !mega.hidden) { setMega(false); return; }
    setSheet(false);
  });

  /* ---------- booking ---------- */
  var tours = C.tours || [];
  var byId = {}; tours.forEach(function (t) { byId[t.id] = t; });
  var modal = $('#bookModal');
  var f = {
    tour: $('#fTour'), pkg: $('#fPkg'), pkgFld: $('#pkgFld'), rowTour: $('#rowTour'), name: $('#fName'), phone: $('#fPhone'),
    date: $('#fDate'), slot: $('#fSlot'), people: $('#fPeople'), ad: $('#fAd'), ch: $('#fCh'), inf: $('#fIn'),
    hotel: $('#fHotel'), notes: $('#fNotes'), est: $('#estVal'), estLbl: $('#estLbl'), err: $('#err'), send: $('#bSend')
  };
  function fmt(s, n) { return String(s || '').replace('{n}', n); }
  function curPkg(t) { return t.pk[Math.min(+(f.pkg && f.pkg.value) || 0, t.pk.length - 1)]; }
  function sync() {
    if (!f.tour) return;
    var t = byId[f.tour.value] || tours[0];
    var boat = t.kind === 'boat', multi = t.pk.length > 1;
    f.pkgFld.hidden = !multi; f.rowTour.classList.toggle('one', !multi);
    if (f.pkg.dataset.tour !== t.id) {
      f.pkg.innerHTML = t.pk.map(function (p, i) { return '<option value="' + i + '">' + p.name + ' · €' + p.adult + '</option>'; }).join('');
      f.pkg.dataset.tour = t.id;
    }
    var p = curPkg(t);
    $('#boatRow').hidden = !boat; $('#paxRow').hidden = boat;
    if (!boat) {
      var a = p.ages || [];
      $('#lAd').textContent = U['cat.adults'] + (a[0] ? ' (' + a[0] + ')' : '');
      $('#lCh').textContent = U['cat.children'] + (a[1] ? ' (' + a[1] + ')' : '');
      $('#lIn').textContent = U['cat.infants'] + (a[2] ? ' (' + a[2] + ')' : '');
    }
    var v;
    if (boat) {
      var n = Math.max(1, Math.min(t.max, parseInt(f.people.value, 10) || 1));
      v = t.base + Math.max(0, n - t.baseN) * t.extra; f.estLbl.textContent = U['b.estBoat'];
    } else {
      var ad = Math.max(0, parseInt(f.ad.value, 10) || 0), ch = Math.max(0, parseInt(f.ch.value, 10) || 0);
      v = ad * p.adult + ch * p.child; f.estLbl.textContent = U['b.est'] + (multi ? ' (' + p.name + ')' : '');
    }
    f.est.textContent = '€' + v;
  }
  if (modal) {
    ['change', 'input'].forEach(function (ev) { $('#bookForm').addEventListener(ev, sync); });
    try { f.date.min = new Date().toISOString().slice(0, 10); } catch (e) {}
  }
  function openBooking(id, pkg) {
    if (!modal) return;
    setMega(false); setSheet(false);
    var fl = openLayer(); if (fl && fl !== modal) closeModal(fl);
    f.tour.value = byId[id] ? id : tours[0].id; f.pkg.dataset.tour = ''; sync();
    f.pkg.value = String(Math.min(pkg || 0, byId[f.tour.value].pk.length - 1)); sync();
    $('#mForm').hidden = false; $('#mDone').hidden = true; $('#mFail').hidden = true; f.err.hidden = true;
    openModal(modal);
  }
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-book]');
    if (!b) return;
    e.preventDefault();
    var id = b.dataset.book || C.tour || (tours[0] && tours[0].id);
    openBooking(id, id === C.tour ? pkgIdx : 0);
  });

  function normalizePhone(v) {
    v = String(v || '').trim();
    if (!v || /[A-Za-z]/.test(v)) return '';
    v = v.replace(/[\s()\-.]/g, '');
    if (v.indexOf('00') === 0) v = '+' + v.slice(2);
    if (!/^\+[1-9][0-9]{9,14}$/.test(v)) return '';
    return v;
  }
  function bad(el, on) { if (el) el.classList.toggle('bad', !!on); }
  function postForm(name, data) {
    var payload = { 'form-name': name };
    payload[name.indexOf('ask-') === 0 ? 'bot-field-ask' : 'bot-field'] = '';
    Object.keys(data).forEach(function (k) { payload[k] = data[k]; });
    return fetch('/', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: new URLSearchParams(payload).toString() })
      .then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r; });
  }
  function channelLinks(box, msg) {
    var c = C.contact || {}, num = c.whatsapp || '905331429037', enc = encodeURIComponent(msg || '');
    $$('a[data-ch]', box).forEach(function (a) {
      var k = a.dataset.ch;
      a.href = k === 'wa' ? 'https://wa.me/' + num + (enc ? '?text=' + enc : '') :
               k === 'vb' ? 'viber://chat?number=%2B' + num :
               k === 'tg' ? 'https://t.me/+' + num : (c.max || '#');
    });
  }
  if (modal) $('#bookForm').addEventListener('submit', function (e) {
    e.preventDefault();
    var t = byId[f.tour.value], p = curPkg(t), boat = t.kind === 'boat';
    var req = [f.name, f.phone, f.date, f.hotel], miss = false;
    req.forEach(function (el) { var m = !el.value.trim(); bad(el, m); if (m) miss = true; });
    if (miss) { f.err.textContent = U['b.errReq']; f.err.hidden = false; return; }
    var phone = normalizePhone(f.phone.value);
    if (!phone) { bad(f.phone, true); f.err.textContent = U['b.errPhone']; f.err.hidden = false; f.phone.focus(); return; }
    f.err.hidden = true;
    var data = {
      tour: t.name, package: boat ? '' : p.name + ' (€' + p.adult + ')', name: f.name.value.trim(), phone: phone, date: f.date.value,
      hotel: f.hotel.value.trim(), adults: boat ? '' : f.ad.value, children: boat ? '' : f.ch.value, infants: boat ? '' : f.inf.value,
      slot: boat ? f.slot.value : '', people: boat ? f.people.value : '', total: f.est.textContent, notes: f.notes.value.trim(), lang: C.lang
    };
    var msg = '*' + t.name + '*' + (data.package ? ' — ' + data.package : '') + '\n' + data.name + ' · ' + phone + '\n' + data.date +
      (boat ? ' · ' + data.slot + ' · ' + data.people + ' pax' : ' · ' + data.adults + '+' + data.children + '+' + data.infants) +
      '\n' + data.hotel + '\n' + data.total + (data.notes ? '\n' + data.notes : '') + '\nmyvalanyatravel.com';
    f.send.disabled = true; var lbl = f.send.textContent; f.send.textContent = U['b.sending'];
    postForm(t.form, data).then(function () {
      if (typeof window.gtag === 'function') window.gtag('event', 'booking_success', { tour_name: t.name, package_name: data.package || t.name, booking_language: C.lang });
      $('#doneText').textContent = t.name + ' — ' + U['b.okText'];
      channelLinks($('#mDone'), msg);
      $('#mForm').hidden = true; $('#mDone').hidden = false;
    }).catch(function () {
      channelLinks($('#mFail'), msg);
      $('#mForm').hidden = true; $('#mFail').hidden = false;
    }).then(function () { f.send.disabled = false; f.send.textContent = lbl; });
  });
  $$('[data-back]').forEach(function (b) { b.addEventListener('click', function () { $('#mFail').hidden = true; $('#mForm').hidden = false; }); });

  /* ---------- ask form ---------- */
  var ask = $('#askForm');
  if (ask) ask.addEventListener('submit', function (e) {
    e.preventDefault();
    var n = $('#aName'), c = $('#aContact'), m = $('#aMsg'), out = $('#aOut');
    var miss = false;
    [n, c, m].forEach(function (el) { var x = !el.value.trim(); bad(el, x); if (x) miss = true; });
    if (miss) return;
    var v = c.value.trim(), isMail = v.indexOf('@') > 0;
    var btn = ask.querySelector('button[type=submit]'); btn.disabled = true;
    postForm(ask.dataset.form, { name: n.value.trim(), email: isMail ? v : '', phone: isMail ? '' : v, notes: m.value.trim(), tour: C.tourName || '', lang: C.lang })
      .then(function () { out.textContent = U['ask.ok']; out.className = 'msg ok'; ask.reset(); })
      .catch(function () { out.textContent = U['ask.err']; out.className = 'msg no'; })
      .then(function () { out.hidden = false; btn.disabled = false; });
  });

  onScroll();
})();
