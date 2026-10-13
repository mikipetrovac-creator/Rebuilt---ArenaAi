#!/usr/bin/env python3
"""M.Y.V. Alanya Travel: static site generator (M.Y.V. 2.0 design).

Reads build/data/*.json and writes, for each of the 6 languages:
  index.html (home), the 6 tour pages, excursions-from-alanya.html, excursions-from-side.html
EN lives at the site root, other languages in /ru/, /de/, /tr/, /uk/, /sr/.

Run from the repo root:   python3 build/build.py
Standard library only. Re-running is safe: it only overwrites the pages listed above.
The old generate-languages.py must NOT be used any more.
"""
import json, os, html, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'build', 'data')


def load(n):
    with open(os.path.join(DATA, n + '.json'), encoding='utf-8') as fh:
        return json.load(fh)


SITE, TOURS, HUBS, LEGAL, REVIEWS = (load(n) for n in ('site', 'tours', 'hubs', 'legal', 'reviews'))
LANGS = SITE['langs']
DOMAIN = SITE['domain']
ORDER = TOURS['order']
T = TOURS['tours']
C = SITE['contact']
ST = SITE['stats']

LANG_NAMES = {'en': 'English', 'ru': 'Русский', 'de': 'Deutsch', 'tr': 'Türkçe', 'uk': 'Українська', 'sr': 'Srpski'}
OG_LOCALE = {'en': 'en_US', 'ru': 'ru_RU', 'de': 'de_DE', 'tr': 'tr_TR', 'uk': 'uk_UA', 'sr': 'sr_RS'}
PHONE_PH = {'en': '+44 7700 900123', 'ru': '+7 900 123 45 67', 'de': '+49 151 2345 6789', 'tr': '+90 532 123 45 67',
            'uk': '+380 67 123 4567', 'sr': '+381 64 123 4567'}
EXTRA = {
    'back': {'en': 'Back to the form', 'sr': 'Nazad na formu', 'ru': 'Вернуться к форме', 'uk': 'Повернутися до форми',
             'de': 'Zurück zum Formular', 'tr': 'Forma geri dön'},
    'heroAlt': {'en': 'Alanya peninsula with the castle and Cleopatra Beach from the air',
                'sr': 'Poluostrvo Alanje sa tvrđavom i Kleopatrinom plažom iz vazduha',
                'ru': 'Полуостров Аланьи с крепостью и пляжем Клеопатры с высоты',
                'uk': 'Півострів Аланьї з фортецею та пляжем Клеопатри з висоти',
                'de': 'Die Halbinsel von Alanya mit der Burg und dem Kleopatra-Strand aus der Luft',
                'tr': 'Alanya yarımadası, kalesi ve Kleopatra Plajı havadan'},
    'bannerAlt': {'en': 'Hot air balloons over Cappadocia at sunrise', 'sr': 'Baloni nad Kapadokijom u zoru',
                  'ru': 'Воздушные шары над Каппадокией на рассвете', 'uk': 'Повітряні кулі над Каппадокією на світанку',
                  'de': 'Heißluftballons über Kappadokien bei Sonnenaufgang', 'tr': 'Gün doğumunda Kapadokya üzerinde balonlar'},
    'video': {'en': 'Show video', 'sr': 'Prikaži video', 'ru': 'Показать видео', 'uk': 'Показати відео',
              'de': 'Video zeigen', 'tr': 'Videoyu göster'},
    'photo': {'en': 'Show photo', 'sr': 'Prikaži fotografiju', 'ru': 'Показать фото', 'uk': 'Показати фото',
              'de': 'Foto zeigen', 'tr': 'Fotoğrafı göster'},
    'revTitle': {'en': 'Google reviews', 'sr': 'Google recenzije', 'ru': 'Отзывы Google', 'uk': 'Відгуки Google',
                 'de': 'Google-Bewertungen', 'tr': 'Google yorumları'},
}
SLOTS = ['10:00 – 14:00', '16:00 – 20:00']

e = lambda s: html.escape('' if s is None else str(s), quote=True)


def ui(lang, k):
    return SITE['ui'][lang].get(k) or SITE['ui']['en'].get(k, k)


def x(k, lang):
    return EXTRA[k].get(lang) or EXTRA[k]['en']


# ------------------------------------------------------------------ URLs
PAGES = ['', *[T[i]['slug'] for i in ORDER], 'excursions-from-alanya', 'excursions-from-side']


def rel(lang, page=''):
    return ('/' if lang == 'en' else '/%s/' % lang) + page


def absu(lang, page=''):
    return DOMAIN + rel(lang, page)


def outfile(lang, page):
    name = (page or 'index') + '.html'
    return os.path.join(ROOT, name) if lang == 'en' else os.path.join(ROOT, lang, name)


def tour_url(lang, tid):
    return rel(lang, T[tid]['slug'])


def eur(n):
    return '€%s' % n


def from_txt(lang, p):
    return SITE['fromFmt'][lang].replace('{p}', p)


def t18(tid, lang):
    return T[tid]['i18n'][lang]


def from_note(tid, lang):
    return t18(tid, lang).get('fromNote') or ui(lang, 'perPerson')


def menu_price(tid, lang):
    return from_txt(lang, eur(T[tid]['fromPrice'])) + ' ' + from_note(tid, lang)


def fix_links(s, lang):
    """Old content linked to '/' (or '/xx/') for Cappadocia; point those to /cappadocia."""
    if not s:
        return s
    for pre in ('', DOMAIN):
        s = s.replace('href="%s%s"' % (pre, rel(lang)), 'href="%s"' % tour_url(lang, 'cappadocia'))
    return s


# ------------------------------------------------------------------ icons
def svg(path, size=20, stroke='currentColor', sw='1.8', fill='none', extra=''):
    return ('<svg width="%s" height="%s" viewBox="0 0 24 24" fill="%s" stroke="%s" stroke-width="%s" stroke-linecap="round" '
            'stroke-linejoin="round" aria-hidden="true"%s>%s</svg>') % (size, size, fill, stroke, sw, extra, path)


IC_X = svg('<path d="M6 6l12 12M18 6L6 18"/>')
IC_CLOCK = svg('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>', 15, '#A8501F')
IC_CAL = svg('<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>', 15, '#A8501F')
IC_OK = svg('<path d="M5 12l5 5 9-10"/>', 18, '#2E7D4F', '2.2')
IC_NO = svg('<path d="M6 6l12 12M18 6L6 18"/>', 18, '#B3473C', '2')
IC_BACK = svg('<path d="M19 12H5M11 6l-6 6 6 6"/>', 16)
IC_CHEV = svg('<path d="M6 9l6 6 6-6"/>', 12, sw='2.2', extra=' class="chev"')
IC_BURGER = svg('<path d="M4 7h16M4 12h16M4 17h16"/>', 26)
PLAY = lambda size=20, fill='#A8501F': '<svg width="%s" height="%s" viewBox="0 0 24 24" fill="%s" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg>' % (size, size, fill)
def brand_inner(kind):
    # home page: new Alanya badge (castle + sail); all other pages keep the original fairy-chimney mark
    src = '/images/logo-myv-badge.svg' if kind == 'home' else '/images/logo-mark.svg'
    return '<img src="%s" alt="" width="34" height="34"><span>M.Y.V. <i>Alanya Travel</i></span>' % src


# ------------------------------------------------------------------ head
FONT_URL = ('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,300;1,400;1,500'
            '&family=Jost:wght@300;400;500&display=swap')


def head(lang, page, title, desc, og_image, jsonld, og_type='website', preload=None):
    alt = '\n'.join('<link rel="alternate" hreflang="%s" href="%s">' % (l, absu(l, page)) for l in LANGS)
    alt += '\n<link rel="alternate" hreflang="x-default" href="%s">' % absu('en', page)
    loc_alt = '\n'.join('<meta property="og:locale:alternate" content="%s">' % OG_LOCALE[l] for l in LANGS if l != lang)
    lds = '\n'.join('<script type="application/ld+json">%s</script>' % json.dumps(j, ensure_ascii=False).replace('</', '<\\/') for j in jsonld)
    pre = '<link rel="preload" as="image" href="%s" fetchpriority="high"%s>\n' % (preload[0], preload[1]) if preload else ''
    g = SITE['gtag']
    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={g}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{g}');
</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{absu(lang, page)}">
{alt}
<meta name="theme-color" content="#A8501F">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="M.Y.V. Alanya Travel">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{absu(lang, page)}">
<meta property="og:image" content="{e(og_image)}">
<meta property="og:locale" content="{OG_LOCALE[lang]}">
{loc_alt}
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{e(og_image)}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
{lds}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONT_URL}">
{pre}<link rel="stylesheet" href="/assets/site.css">
</head>'''


ORG = {
    "@type": "Organization", "@id": DOMAIN + "/#business", "name": "M.Y.V. Alanya Travel", "url": DOMAIN + "/",
    "image": DOMAIN + "/images/v2/alanya-hero.jpg", "email": C['email'], "telephone": C['phones'][0]['tel'],
    "priceRange": "€€",
    "address": {"@type": "PostalAddress", "streetAddress": "Saray Mah. Macaroğlu Sok., Macaroğlu Apt. No 1/8",
                "addressLocality": "Alanya", "addressRegion": "Antalya", "postalCode": "07400", "addressCountry": "TR"},
    "areaServed": ["Alanya", "Side", "Antalya"],
    "logo": {"@type": "ImageObject", "url": DOMAIN + "/icon-512.png"},
}


def crumbs_ld(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items)]}


def faq_ld(faq):
    if not faq:
        return None
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": f['q'], "acceptedAnswer": {"@type": "Answer", "text": f['a']}} for f in faq]}


# ------------------------------------------------------------------ shared chrome
def mega_items(lang):
    out = []
    for tid in ORDER:
        t, d = T[tid], t18(tid, lang)
        new = '<span class="new">%s</span>' % e(ui(lang, 'card.new')) if t['isNew'] else ''
        out.append(f'<a class="mi" href="{tour_url(lang, tid)}"><img src="{e(t["card"])}" alt="" loading="lazy" width="120" height="80">'
                   f'<span class="mt"><span class="mn">{e(d["name"])}{new}</span><span class="ms">{e(d["short"])}</span>'
                   f'<span class="mp">{e(menu_price(tid, lang))}</span></span></a>')
    return ''.join(out)


def header(lang, page, kind):
    u = lambda k: e(ui(lang, k))
    home_cur = ' class="cur"' if kind == 'home' else ''
    tours_cur = ' cur' if kind in ('tour', 'hub') else ''
    langs = ''.join('<li><a href="%s" hreflang="%s" lang="%s"%s>%s<span>%s</span></a></li>' % (
        rel(l, page), l, l, ' aria-current="true"' if l == lang else '', LANG_NAMES[l], l) for l in LANGS)
    sheet_langs = ''.join('<a href="%s" hreflang="%s" lang="%s"%s>%s</a>' % (
        rel(l, page), l, l, ' aria-current="true"' if l == lang else '', l) for l in LANGS)
    home = rel(lang)
    hub = rel(lang, 'excursions-from-alanya')
    on = '' if kind == 'home' else ' on'
    return f'''<body class="{'has-bar' if kind == 'tour' else ('home' if kind == 'home' else '')}">
<a class="skip" href="#main">{u('skip')}</a>
<header class="hdr{on}" id="hdr">
  <div class="hdr-in">
    <a class="brand" href="{home}">{brand_inner(kind)}</a>
    <nav class="nav" aria-label="Menu">
      <a href="{home}"{home_cur}>{u('nav.home')}</a>
      <button class="nl{tours_cur}" type="button" id="megaBtn" aria-expanded="false" aria-controls="mega">{u('nav.tours')} {IC_CHEV}</button>
      <a href="{home}#about">{u('nav.about')}</a>
      <a href="{rel(lang, 'blog')}">{u('nav.blog')}</a>
      <a href="#contact">{u('nav.contact')}</a>
      <div class="langsw"><button type="button" aria-expanded="false" aria-label="{u('lang.label')}">{lang} {IC_CHEV}</button><ul hidden>{langs}</ul></div>
      <button class="btn btn-gold" type="button" data-book="">{u('nav.book')}</button>
    </nav>
    <div class="hdr-mob">
      <div class="langsw mob-lang"><button type="button" aria-expanded="false" aria-label="{u('lang.label')}">{lang} {IC_CHEV}</button><ul hidden>{langs}</ul></div>
      <button class="burger" type="button" id="burger" aria-label="{u('nav.menu')}" aria-expanded="false" aria-controls="sheet">{IC_BURGER}</button>
    </div>
  </div>
</header>
<div class="mega-scrim" id="megaScrim" hidden></div>
<div class="mega" id="mega" hidden>
  <div class="mega-grid">{mega_items(lang)}</div>
  <div class="mega-foot">
    <span>{u('mega.foot')}</span>
    <div><a class="btn btn-line" href="{hub}">{u('mega.all')}</a><button class="btn btn-gold" type="button" data-book="">{u('nav.book')}</button></div>
  </div>
</div>
<div class="sheet" id="sheet" hidden>
  <div class="sheet-top">
    <a class="brand" href="{home}">{brand_inner(kind)}</a>
    <button class="burger" type="button" id="sheetClose" aria-label="{u('nav.close')}">{svg('<path d="M6 6l12 12M18 6L6 18"/>', 24)}</button>
  </div>
  <div class="sheet-sec"><span class="eyebrow">{u('nav.tours')}</span><div>{mega_items(lang)}</div></div>
  <div class="sheet-sec sheet-links">
    <a href="{home}">{u('nav.home')}</a><a href="{hub}">{u('mega.all')}</a><a href="{home}#about">{u('nav.about')}</a><a href="{rel(lang, 'blog')}">{u('nav.blog')}</a><a href="#contact">{u('nav.contact')}</a>
  </div>
  <div class="sheet-langs" aria-label="{u('lang.label')}">{sheet_langs}</div>
  <button class="btn btn-gold" type="button" data-book="">{u('hero.book')}</button>
</div>
'''


def wa_link(text=''):
    return 'https://wa.me/%s' % C['whatsapp'] + ('?text=' + text if text else '')


def footer(lang, kind):
    u = lambda k: e(ui(lang, k))
    home = rel(lang)
    tours = ''.join('<a href="%s">%s</a>' % (tour_url(lang, t), e(t18(t, lang)['name'])) for t in ORDER)
    phones = ''.join('<a href="tel:%s">%s <small>(%s)</small></a>' % (p['tel'], e(p['num']), e(p['langs'])) for p in C['phones'])
    leg = LEGAL[lang]
    revn = ui(lang, 'rev.count').replace('{n}', str(ST['reviews']))
    return f'''<footer id="contact">
  <div class="fgrid">
    <div class="fcol">
      <div class="flogo">{brand_inner(kind)}</div>
      <p style="margin-top:18px">{u('foot.desc')}</p>
      <p class="rate">★ {ST['rating']} · {e(revn)}</p>
    </div>
    <div class="fcol">
      <p class="fh">{u('foot.quick')}</p>
      <div class="fl"><a href="{home}">{u('nav.home')}</a><a href="{rel(lang, 'excursions-from-alanya')}">{u('foot.prices')}</a><a href="{rel(lang, 'excursions-from-side')}">{u('foot.side')}</a><a href="{home}#about">{u('nav.about')}</a><a href="{home}#reviews">{u('foot.reviews')}</a><a href="{rel(lang, 'blog')}">{u('nav.blog')}</a></div>
    </div>
    <div class="fcol">
      <p class="fh">{u('foot.tours')}</p>
      <div class="fl">{tours}</div>
    </div>
    <div class="fcol">
      <p class="fh">{u('foot.contact')}</p>
      <div class="fc">
        <span>{e(C['address'])}</span>
        {phones}
        <a href="mailto:{C['email']}">{C['email']}</a>
        <div class="msg"><a href="{wa_link()}" target="_blank" rel="noopener" style="background:#1F7A4D">WhatsApp</a><a href="viber://chat?number=%2B{C['whatsapp']}" style="background:#5B4B9A">Viber</a><a href="https://t.me/+{C['whatsapp']}" target="_blank" rel="noopener" style="background:#1F6F99">Telegram</a><a href="{e(C['max'])}" target="_blank" rel="noopener" style="background:#fff;color:#1A0F08">MAX</a></div>
      </div>
    </div>
  </div>
  <div class="flegal">
    <span>{e(SITE['legalLine'][lang])}</span>
    <span><button type="button" data-open="termsModal">{e(leg['termsModal']['title'])}</button><button type="button" data-open="privacyModal">{e(leg['privacyModal']['title'])}</button><button type="button" data-open="cookieModal">{e(leg['cookieModal']['title'])}</button></span>
  </div>
</footer>
'''


def modal(mid, inner, wide=False, label=''):
    return (f'<div class="modal" id="{mid}" hidden><div class="dialog{" wide" if wide else ""}" role="dialog" aria-modal="true"'
            f'{(" aria-label=" + chr(34) + e(label) + chr(34)) if label else ""}>'
            f'<button class="x" type="button" data-close aria-label="close">{IC_X}</button>{inner}</div></div>\n')


def legal_modals(lang):
    out = ''
    for k in ('termsModal', 'privacyModal', 'cookieModal'):
        m = LEGAL[lang][k]
        out += modal(k, '<h2>%s</h2><div class="legalbody">%s</div>' % (e(m['title']), m['html']), True, m['title'])
    return out


def channels():
    return ('<div class="ch"><a data-ch="wa" href="%s" target="_blank" rel="noopener" style="background:#1F7A4D">WhatsApp</a>'
            '<a data-ch="vb" href="#" style="background:#5B4B9A">Viber</a>'
            '<a data-ch="tg" href="#" target="_blank" rel="noopener" style="background:#1F6F99">Telegram</a>'
            '<a data-ch="mx" href="%s" target="_blank" rel="noopener" style="background:#2D2A6E">MAX</a></div>') % (wa_link(), e(C['max']))


def booking_modal(lang):
    u = lambda k: e(ui(lang, k))
    opts = ''.join('<option value="%s">%s</option>' % (t, e(t18(t, lang)['name'])) for t in ORDER)
    slots = ''.join('<option>%s</option>' % s for s in SLOTS)
    inner = f'''<div id="mForm">
      <p class="eyebrow">{u('b.eyebrow')}</p>
      <h2 id="mTitle">{u('b.title')}</h2>
      <p class="sub">{u('b.sub')}</p>
      <form id="bookForm" novalidate>
        <div class="row" id="rowTour">
          <div class="fld"><label for="fTour">{u('b.tour')}</label><select class="inp" id="fTour">{opts}</select></div>
          <div class="fld" id="pkgFld"><label for="fPkg">{u('b.pkg')}</label><select class="inp" id="fPkg"></select></div>
        </div>
        <div class="fld"><label for="fName">{u('b.name')}</label><input class="inp" id="fName" type="text" autocomplete="name" placeholder="{u('b.namePh')}" required></div>
        <div class="row">
          <div class="fld"><label for="fPhone">{u('b.phone')}</label><input class="inp" id="fPhone" type="tel" autocomplete="tel" placeholder="{PHONE_PH[lang]}" required></div>
          <div class="fld"><label for="fDate">{u('b.date')}</label><input class="inp" id="fDate" type="date" required></div>
        </div>
        <div class="row" id="boatRow" hidden>
          <div class="fld"><label for="fSlot">{u('b.slot')}</label><select class="inp" id="fSlot">{slots}</select></div>
          <div class="fld"><label for="fPeople">{u('b.people')}</label><input class="inp" id="fPeople" type="number" min="1" max="12" value="6" inputmode="numeric"></div>
        </div>
        <div class="row three" id="paxRow">
          <div class="fld"><label for="fAd" id="lAd">{u('cat.adults')}</label><input class="inp" id="fAd" type="number" min="1" value="2" inputmode="numeric"></div>
          <div class="fld"><label for="fCh" id="lCh">{u('cat.children')}</label><input class="inp" id="fCh" type="number" min="0" value="0" inputmode="numeric"></div>
          <div class="fld"><label for="fIn" id="lIn">{u('cat.infants')}</label><input class="inp" id="fIn" type="number" min="0" value="0" inputmode="numeric"></div>
        </div>
        <div class="est"><span id="estLbl">{u('b.est')}</span><b id="estVal">€0</b></div>
        <div class="fld"><label for="fHotel">{u('b.hotel')}</label><input class="inp" id="fHotel" type="text" placeholder="{u('b.hotelPh')}" required></div>
        <div class="fld"><label for="fNotes">{u('b.notes')}</label><textarea class="inp" id="fNotes" rows="2"></textarea></div>
        <p class="err" id="err" role="alert" hidden></p>
        <button class="btn btn-gold" id="bSend" type="submit" style="margin-top:6px;min-height:56px;font-size:16px">{u('b.send')}</button>
      </form>
    </div>
    <div class="done" id="mDone" hidden>
      <svg width="58" height="58" viewBox="0 0 24 24" fill="none" stroke="#2E7D4F" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M7 12.5l3.2 3.2L17 9"/></svg>
      <h2 class="serif">{u('b.okTitle')}</h2>
      <p class="sub" id="doneText"></p>
      {channels()}
      <button class="btn btn-line" type="button" data-close>{u('b.close')}</button>
    </div>
    <div class="done" id="mFail" hidden>
      <h2 class="serif">{u('b.errTitle')}</h2>
      <p class="sub">{u('b.errText')}</p>
      {channels()}
      <button class="btn btn-line" type="button" data-back>{e(x('back', lang))}</button>
    </div>'''
    return modal('bookModal', inner, label=ui(lang, 'b.title'))


def film_box(lang):
    u = lambda k: e(ui(lang, k))
    return f'''<div class="filmbox" id="film" role="dialog" aria-modal="true" aria-label="{u('film.yt')}" hidden>
  <div class="vframe"></div>
  <button class="xx" type="button" data-close aria-label="{u('b.close')}">{IC_X}</button>
  <button class="btn btn-gold" type="button" id="filmBook" data-book="cappadocia">{u('t.book')}</button>
</div>
'''


FORM_FIELDS = ['tour', 'package', 'name', 'phone', 'email', 'date', 'hotel', 'adults', 'children', 'infants', 'slot', 'people', 'total', 'notes', 'lang']


def netlify_forms():
    out = []
    for tid in ORDER:
        for name, hp in ((T[tid]['form'], 'bot-field'), (T[tid]['askForm'], 'bot-field-ask')):
            fields = ''.join('<input name="%s">' % f for f in FORM_FIELDS)
            out.append('<form name="%s" data-netlify="true" data-netlify-honeypot="%s" hidden><input name="%s">%s</form>' % (name, hp, hp, fields))
    return '\n'.join(out)


def config(lang, kind, tid=None):
    tours = []
    for t in ORDER:
        d, td = T[t], t18(t, lang)
        item = {'id': t, 'name': td['name'], 'form': d['form'], 'kind': d['kind']}
        if d['kind'] == 'boat':
            p = d['packages'][0]
            item.update(pk=[{'name': td['packages'][0]['name'], 'adult': p['base'], 'child': 0, 'ages': []}],
                        base=p['base'], extra=p['extra'], baseN=p['baseN'], max=p['max'])
        else:
            item['pk'] = [{'name': td['packages'][i]['name'], 'adult': p['adult'], 'child': p['child'], 'ages': p['ages']}
                          for i, p in enumerate(d['packages'])]
        tours.append(item)
    keys = ['cat.adults', 'cat.children', 'cat.infants', 'b.est', 'b.estBoat', 'b.errReq', 'b.errPhone', 'b.sending', 'b.okText', 'ask.ok', 'ask.err']
    cfg = {'lang': lang, 'page': kind, 'tour': tid, 'tourName': t18(tid, lang)['name'] if tid else '',
           'ui': {k: ui(lang, k) for k in keys}, 'tours': tours,
           'contact': {'whatsapp': C['whatsapp'], 'max': C['max']}}
    return '<script>window.MYV=%s;</script>' % json.dumps(cfg, ensure_ascii=False).replace('</', '<\\/')


def tail(lang, kind, tid=None, bar=''):
    return (bar + footer(lang, kind) + film_box(lang) + modal('stopModal', '<div id="smBody"></div>') +
            booking_modal(lang) + legal_modals(lang) + netlify_forms() + '\n' + config(lang, kind, tid) +
            '\n<script src="/assets/site.js" defer></script>\n</body>\n</html>\n')


# ------------------------------------------------------------------ reviews
def rev_card(r):
    return ('<div class="rcard"><div class="rh"><span class="rn">%s</span><span class="rd">%s</span></div><div class="rs" aria-label="5/5">★★★★★</div>%s</div>'
            % (e(r['name']), e(r['date']), '<p class="rt">%s</p>' % e(r['text']) if r.get('text') else ''))


def reviews_section(lang, tid, sec_id=''):
    allr = REVIEWS.get(tid) or []
    if not allr:
        return '', ''
    u = lambda k: e(ui(lang, k))
    feat = [r for r in allr if r.get('featured')][:3] or allr[:3]
    n = ST['reviews']
    btn = ''
    mod = ''
    if len(allr) > len(feat):
        btn = '<button class="btn btn-line" type="button" data-open="revModal">%s</button>' % e(ui(lang, 'rev.all').replace('{n}', str(len(allr))))
        mod = modal('revModal', '<p class="eyebrow">%s</p><h2>%s %s</h2><p class="sub">★★★★★ %s · %s. %s</p><div class="allrevs">%s</div>' % (
            e(x('revTitle', lang)), u('rev.h2a'), u('rev.h2b'), ST['rating'], e(ui(lang, 'rev.count').replace('{n}', str(n))),
            u('rev.note'), ''.join(rev_card(r) for r in allr)), True, x('revTitle', lang))
    sid = ' id="%s"' % sec_id if sec_id else ''
    sec = f'''<section class="revs"{sid}><div class="inner">
    <div class="revs-head">
      <div><p class="eyebrow">{u('rev.eyebrow')}</p><h2>{u('rev.h2a')} <span>{u('rev.h2b')}</span></h2></div>
      <div class="score"><b>{ST['rating']}</b><span><i>★★★★★</i>{e(ui(lang, 'rev.count').replace('{n}', str(n)))}</span></div>
    </div>
    <div class="rgrid">{''.join(rev_card(r) for r in feat)}</div>
    <div class="revs-acts">{btn}<a class="gl" href="{C['googleReview']}" target="_blank" rel="noopener">{u('rev.rate')}</a></div>
  </div></section>'''
    return sec, mod


# ------------------------------------------------------------------ home
def about_legal(lang):
    t = SITE['aboutLegal'][lang]
    i = t.find('. M.Y.V.')
    return t[i + 2:] if i > 0 else t


HERO_SRCSET = '/images/v2/alanya-hero-900.jpg 900w, /images/v2/alanya-hero.jpg 1600w, /images/v2/alanya-hero-2560.jpg 2560w'


def build_home(lang):
    u = lambda k: e(ui(lang, k))
    meta = SITE['homeMeta'][lang]
    cap = T['cappadocia']
    vt = t18('cappadocia', lang)['videoText'] or {}
    ld = [{"@context": "https://schema.org", "@graph": [
        {"@type": "WebSite", "@id": DOMAIN + "/#website", "url": DOMAIN + "/", "name": "M.Y.V. Alanya Travel",
         "publisher": {"@id": DOMAIN + "/#business"}, "inLanguage": lang}, ORG]},
        {"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": t18(t, lang)['name'], "url": absu(lang, T[t]['slug'])} for i, t in enumerate(ORDER)]}]
    h = head(lang, '', meta['title'], meta['desc'], DOMAIN + '/images/v2/alanya-hero.jpg', ld,
             preload=('/images/v2/alanya-hero.jpg', ' imagesrcset="%s" imagesizes="100vw"' % HERO_SRCSET))
    strip = ''.join('<a href="%s">%s</a>' % (tour_url(lang, t), e(t18(t, lang)['name'])) for t in ORDER)
    pills = ''.join('<div class="pil"><span class="n">%s</span><div><h3>%s</h3><p>%s</p></div></div>' % (n, u('p%d.t' % i), u('p%d.p' % i))
                    for i, n in zip(range(1, 5), ('I', 'II', 'III', 'IV')))
    rsec, rmod = reviews_section(lang, 'cappadocia', 'reviews')
    hub = rel(lang, 'excursions-from-alanya')
    pill = e(ui(lang, 'hero.pill'))
    body = f'''<main id="main">
  <section class="hero">
    <img src="/images/v2/alanya-hero.jpg" srcset="{HERO_SRCSET}" sizes="100vw" alt="{e(x('heroAlt', lang))}" fetchpriority="high" width="1600" height="1067">
    <div class="hero-in">
      <h1 class="h1-first">{u('hero.h1a')} <span>{u('hero.h1b')}</span></h1>
      <p class="lead">{u('hero.lead')}</p>
      <div class="hero-ctas">
        <button class="btn btn-gold" type="button" data-book="">{u('hero.book')}</button>
        <a class="btn btn-white" href="{hub}">{u('hero.tours')}</a>
      </div>
      <button class="film" type="button" data-film="{cap['video']['yt']}" data-tour="cappadocia" data-title="{e(vt.get('title', ''))}">
        <span class="dot">{PLAY()}</span>
        <span class="ft"><small>{u('hero.filmSmall')}</small><em>{e(vt.get('title', ''))}</em></span>
      </button>
    </div>
    <div class="hstats">
      <div><b>{ST['rating']}</b><span>{u('stat.rating')}</span></div>
      <div><b>{ST['reviews']}</b><span>{u('stat.reviews')}</span></div>
      <div><b>{ST['years']}</b><span>{u('stat.years')}</span></div>
      <div><b>{ST['tours']}</b><span>{u('stat.tours')}</span></div>
    </div>
    <nav class="strip" aria-label="{u('nav.tours')}">{strip}</nav>
  </section>
  <section class="about" id="about"><div class="inner">
    <div>
      <p class="eyebrow">{u('about.eyebrow')}</p>
      <h2>{u('about.h2a')} <span>{u('about.h2b')}</span></h2>
      <p class="body">{u('about.body')}</p>
      <p class="legal">{e(about_legal(lang))}</p>
    </div>
    <div>
      <p class="eyebrow" style="margin-bottom:10px">{u('about.why')}</p>
      {pills}
    </div>
  </div></section>
  {rsec}
  <section class="banner">
    <img src="/images/cappadocia-hero-D-1920.jpg" alt="{e(x('bannerAlt', lang))}" loading="lazy" width="1920" height="1280">
    <div class="inner"><div class="bx">
      <span class="chip-gold">{u('banner.chip')}</span>
      <h2>{u('banner.h2a')} <span>{u('banner.h2b')}</span></h2>
      <p>{u('banner.p')}</p>
      <div class="chips"><span>WhatsApp</span><span>Viber</span><span>Telegram</span><span>MAX</span></div>
      <div class="ctas"><button class="btn btn-gold" type="button" data-book="">{u('hero.book')}</button><a class="btn btn-white" href="{hub}">{u('banner.tours')}</a></div>
    </div></div>
  </section>
</main>
'''
    return h + '\n' + header(lang, '', 'home') + body + rmod + tail(lang, 'home')


# ------------------------------------------------------------------ tour page
def cats_rows(lang, tid, i):
    d = T[tid]
    p = d['packages'][i]
    tp = t18(tid, lang)['packages'][i]
    if d['kind'] == 'boat':
        return [(c[0], c[1], c[2]) for c in tp.get('cats', [])]
    a = p['ages']
    return [(ui(lang, 'cat.adults'), a[0], eur(p['adult'])), (ui(lang, 'cat.children'), a[1], eur(p['child'])),
            (ui(lang, 'cat.infants'), a[2], ui(lang, 'cat.free'))]


def pkg_price(tid, i):
    p = T[tid]['packages'][i]
    return eur(p['base'] if T[tid]['kind'] == 'boat' else p['adult'])


def packages_html(lang, tid):
    u = lambda k: e(ui(lang, k))
    tps = t18(tid, lang)['packages']
    tabs = ''
    if len(tps) > 1:
        tabs = '<div class="tabs" role="group" aria-label="%s">%s</div>' % (u('b.pkg'), ''.join(
            '<button class="tab" type="button" data-pkg="%d" aria-pressed="%s">%s · %s</button>' % (i, 'true' if i == 0 else 'false', e(p['name']), pkg_price(tid, i))
            for i, p in enumerate(tps)))
    panels = []
    for i, p in enumerate(tps):
        unit = p.get('unit') or '/ ' + ui(lang, 'perPerson')
        rows = ''.join('<div><span>%s <em>%s</em></span><b>%s</b></div>' % (e(a), e(b), e(c)) for a, b, c in cats_rows(lang, tid, i))
        title = '<p class="ptitle">%s</p>' % e(p['title']) if p.get('title') and p['title'] != p['name'] else ''
        desc = '<p class="pdesc">%s</p>' % e(p['desc']) if p.get('desc') else ''
        hh = f'''<div class="pkg">
      <div class="pkg-top"><span class="nm">{e(p['name'])}</span><span><b>{pkg_price(tid, i)}</b> <small>{e(unit)}</small></span></div>
      {title}{desc}
      {'<p class="note">%s</p>' % e(p['note']) if p.get('note') else ''}
      <div class="rows">{rows}</div>
    </div>'''
        if p.get('included'):
            hh += '<h2 class="h2">%s</h2><ul class="list">%s</ul>' % (u('t.included'), ''.join('<li>%s<span>%s</span></li>' % (IC_OK, e(v)) for v in p['included']))
        if p.get('excluded'):
            hh += '<h2 class="h2 h2s">%s</h2><ul class="list no">%s</ul>' % (u('t.excluded'), ''.join('<li>%s<span>%s</span></li>' % (IC_NO, e(v)) for v in p['excluded']))
        if p.get('bring'):
            hh += '<h2 class="h2">%s</h2><ul class="list two">%s</ul>' % (u('t.bring'), ''.join('<li><i>●</i><span>%s</span></li>' % e(v) for v in p['bring']))
        panels.append('<div class="pkgpanel"%s>%s</div>' % ('' if i == 0 else ' hidden', hh))
    return tabs + ''.join(panels)


def itinerary_html(lang, tid):
    u = lambda k: e(ui(lang, k))
    d = t18(tid, lang)
    out, tpls = [], []
    for di, day in enumerate(d['itinerary']):
        stops = []
        for si, s in enumerate(day['stops']):
            if s.get('info'):
                sid = 'stop-%d-%d' % (di, si)
                stops.append('<button class="stop stopbtn" type="button" data-stop="%s"><span class="mk">%s</span><span class="sn"><small>%s</small><span>%s<i>%s</i></span></span></button>'
                             % (sid, e(s.get('mark')), u('t.highlight'), e(s['name']), u('t.more')))
                i = s['info']
                img = (i.get('imgs') or [None])[0] or i.get('img')
                tpls.append('<template id="%s">%s<h2>%s</h2>%s%s%s<div class="sm-acts"><button class="btn btn-gold" type="button" data-book="%s">%s</button><button class="btn btn-line" type="button" data-close>%s</button></div></template>' % (
                    sid, '<img class="sm-img" src="%s" alt="%s" loading="lazy">' % (e(img), e(i['title'])) if img else '', e(i['title']),
                    '<p class="sm-badge">%s</p>' % e(i['badge']) if i.get('badge') else '',
                    ''.join('<p class="sm-p">%s</p>' % e(p) for p in i.get('p', [])),
                    '<div class="sm-facts">%s</div>' % ''.join('<span>%s</span>' % e(f) for f in i['facts']) if i.get('facts') else '',
                    tid, u('t.book'), u('t.gotIt')))
            else:
                stops.append('<div class="stop"><span class="mk">%s</span><span class="sn">%s</span></div>' % (e(s.get('mark')), e(s['name'])))
        out.append('<h2 class="h2">%s</h2><div class="stops">%s</div>' % (e(day['title']), ''.join(stops)))
    return ''.join(out), ''.join(tpls)


def build_tour(lang, tid):
    u = lambda k: e(ui(lang, k))
    t, d = T[tid], t18(tid, lang)
    page = t['slug']
    meta = d['meta']
    og = meta.get('ogImage') or t.get('ogImage') or DOMAIN + t['card']
    url = absu(lang, page)
    hub_name = SITE['ui'][lang]['foot.prices']
    ld = [{"@context": "https://schema.org", "@graph": [ORG, {
        "@type": "Product", "name": d['product']['name'], "description": d['product']['description'], "image": og,
        "brand": {"@type": "Brand", "name": "M.Y.V. Alanya Travel"},
        "offers": {"@type": "Offer", "price": str(t['fromPrice']), "priceCurrency": "EUR",
                   "availability": "https://schema.org/InStock", "url": url}}]},
        crumbs_ld([(ui(lang, 'nav.home'), absu(lang)), (hub_name, absu(lang, 'excursions-from-alanya')), (d['crumb'], url)])]
    fl = faq_ld(d['faq'])
    if fl:
        ld.append(fl)
    media = t['media']
    first = media[0]
    pre = None
    if first['type'] == 'video':
        main_media = '<video src="%s" poster="%s" autoplay muted loop playsinline preload="metadata" data-autoplay></video>' % (e(first['src']), e(first['thumb'].replace('-sm.jpg', '.jpg')))
    else:
        main_media = '<img src="%s" alt="%s" fetchpriority="high">' % (e(first['src']), e(d['name']))
        pre = (first['src'], '')
    h = head(lang, page, meta['title'], meta['desc'], og, ld, preload=pre)
    caps = d.get('galleryCaps') or []
    thumbs = ''
    if len(media) > 1:
        bt = []
        for i, m in enumerate(media):
            alt = caps[i] if i < len(caps) else d['name']
            lbl = x('video', lang) if m['type'] == 'video' else '%s %d' % (x('photo', lang), i + 1)
            inner = ('<img src="%s" alt="" loading="lazy"><span class="play">%s</span>' % (e(m['thumb']), PLAY(30, '#fff'))) if m['type'] == 'video' else '<img src="%s" alt="" loading="lazy">' % e(m['thumb'])
            bt.append('<button class="thumb" type="button" data-media="%s" data-type="%s" data-alt="%s" aria-pressed="%s" aria-label="%s">%s</button>'
                      % (e(m['src']), m['type'], e(alt), 'true' if i == 0 else 'false', e(lbl), inner))
        thumbs = '<h2 class="h2">%s</h2><div class="thumbs">%s</div><p class="hint">%s</p>' % (u('t.gallery'), ''.join(bt), u('t.tapThumb'))
    video = ''
    vt = d.get('videoText')
    if t.get('video') and vt:
        video = ('<h2 class="h2">%s</h2><button class="vcard" type="button" data-film="%s" data-tour="%s" data-title="%s"><img src="%s" alt="" loading="lazy">'
                 '<span class="vc"><span>%s</span><em>%s</em></span></button><p class="vsub">%s</p>') % (
            e(vt['title']), t['video']['yt'], tid, e(vt['title']), e(t['card']), PLAY(24), u('t.watch'), e(vt['sub']))
    about = ''
    if d.get('about'):
        a = d['about']
        about = '<h2 class="h2">%s</h2><div class="dest">%s</div>' % (e(a['title']), ''.join('<p>%s</p>' % e(p) for p in a['p']))
    itin, tpls = itinerary_html(lang, tid)
    rsec, rmod = reviews_section(lang, tid)
    faq = ''
    if d.get('faq'):
        faq = '<h2 class="h2">%s</h2><div class="faq">%s</div>' % (u('t.faq'), ''.join(
            '<details><summary>%s</summary><p>%s</p></details>' % (e(f['q']), fix_links(f.get('a_html'), lang) or e(f['a'])) for f in d['faq']))
    ask = f'''<section class="ask">
        <h2>{u('ask.h')}</h2><p class="sub">{u('ask.p')}</p>
        <form id="askForm" data-form="{t['askForm']}" novalidate>
          <div class="row"><div class="fld"><label for="aName">{u('ask.name')}</label><input class="inp" id="aName" type="text" autocomplete="name"></div>
          <div class="fld"><label for="aContact">{u('ask.contact')}</label><input class="inp" id="aContact" type="text" autocomplete="email"></div></div>
          <div class="fld"><label for="aMsg">{u('ask.msg')}</label><textarea class="inp" id="aMsg" rows="3"></textarea></div>
          <button class="btn btn-line" type="submit">{u('ask.send')}</button>
          <p class="msg" id="aOut" role="status" hidden></p>
        </form>
      </section>'''
    price_txt = from_txt(lang, '<b>%s</b>' % eur(t['fromPrice']))
    body = f'''<main id="main">
  <div class="detail">
    <div class="media" id="mediaBox">
      {main_media}
      <div class="glass pricebox"><span>{price_txt}</span><small>{e(from_note(tid, lang))}</small></div>
    </div>
    <div class="content">
      <a class="back" href="{rel(lang, 'excursions-from-alanya')}">{IC_BACK} {u('t.back')}</a>
      <span class="eyebrow">{e(d['tagline'])}</span>
      <h1>{e(d['name'])}</h1>
      <div class="facts"><span>{IC_CLOCK}{e(d['duration'])}</span><span>{IC_CAL}{e(d['days'])}</span></div>
      <div class="cta-row" id="book-now"><button class="btn btn-gold" type="button" data-book="{tid}">{u('t.book')}</button><span>{u('t.noPrepay')}</span></div>
      <div class="hr"></div>
      <div class="desc">{''.join('<p>%s</p>' % e(p) for p in d['desc'])}{'<p>%s</p>' % e(d['schedule']) if d['schedule'] != d['days'] else ''}</div>
      {video}
      <h2 class="h2">{u('t.prices')}</h2>
      {packages_html(lang, tid)}
      {itin}
      {about}
      {thumbs}
      {'<div class="revwrap">%s</div>' % rsec if rsec else ''}
      {faq}
      {ask}
      <button class="btn btn-gold full" type="button" data-book="{tid}">{u('t.bookFull')}</button>
    </div>
  </div>
  {tpls}
</main>
'''
    bar = f'''<div class="bar" id="bar" aria-hidden="true">
  <span class="bt"><span class="bn">{e(d['name'])}</span> <span class="bp">{from_txt(lang, eur(t['fromPrice']))}</span></span>
  <button class="btn btn-gold" type="button" data-book="{tid}" tabindex="-1">{u('nav.book')}</button>
</div>
'''
    return h + '\n' + header(lang, page, 'tour') + body + rmod + tail(lang, 'tour', tid, bar)


# ------------------------------------------------------------------ hub pages
def tour_cards(lang, ids):
    u = lambda k: e(ui(lang, k))
    out = []
    for tid in ids:
        t, d = T[tid], t18(tid, lang)
        url = tour_url(lang, tid)
        out.append(f'''<article class="tcard">
      <a class="ph" href="{url}" aria-label="{e(d['name'])}"><img src="{e(t['card'])}" alt="" loading="lazy">{'<span class="new">%s</span>' % u('card.new') if t['isNew'] else ''}<span class="from">{from_txt(lang, '<b>%s</b>' % eur(t['fromPrice']))} {e(from_note(tid, lang))}</span></a>
      <div class="tb">
        <span class="meta">{e(d['duration'])} · {e(d['days'])}</span>
        <h2><a href="{url}">{e(d['name'])}</a></h2>
        <p class="sh">{e(d['short'])}</p>
        <a class="btn btn-line" href="{url}">{u('card.details')}</a>
      </div>
    </article>''')
    return ''.join(out)


def build_hub(lang, key):
    u = lambda k: e(ui(lang, k))
    page = 'excursions-from-' + key
    hd = HUBS[key][lang]
    meta = hd['meta']
    url = absu(lang, page)
    ids = [r['tour'] for r in hd['rows'] if r.get('tour') in T] or ORDER
    ld = [{"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": t18(t, lang)['name'], "url": absu(lang, T[t]['slug'])} for i, t in enumerate(ids)]},
        crumbs_ld([(ui(lang, 'nav.home'), absu(lang)), (hd['h1'], url)])]
    fl = faq_ld(hd.get('faq'))
    if fl:
        ld.append(fl)
    h = head(lang, page, meta['title'], meta['desc'], DOMAIN + '/images/v2/alanya-hero.jpg', ld)
    sw = ''.join('<a href="%s"%s>%s</a>' % (rel(lang, s['href'].rstrip('/').split('/')[-1]), ' class="on" aria-current="page"' if s['on'] else '', e(s['label'])) for s in hd['switch'])
    th = ''.join('<th scope="col">%s</th>' % e(c) for c in hd['th'])
    rows = []
    for r in hd['rows']:
        href = tour_url(lang, r['tour']) if r.get('tour') in T else r.get('href', '#')
        c = r['cells']
        cells = ['<td class="nm"><a href="%s">%s</a></td>' % (href, e(c[0]))]
        for j, v in enumerate(c[1:-1], 1):
            cls = ' class="pr"' if j >= len(c) - 3 else ''
            cells.append('<td%s>%s</td>' % (cls, e(v)))
        cells.append('<td class="go"><a href="%s">%s</a></td>' % (href, e(c[-1])))
        rows.append('<tr>%s</tr>' % ''.join(cells))
    secs = ''.join('<section><h2>%s</h2>%s%s</section>' % (e(s['h']), '<p>%s</p>' % e(s['p']) if s.get('p') else '',
                   '<ul>%s</ul>' % ''.join('<li>%s</li>' % e(li) for li in s['li']) if s.get('li') else '') for s in hd.get('sections', []))
    faq = ''
    if hd.get('faq'):
        faq = '<div class="hubfaq"><h2 class="h2">%s</h2><div class="faq">%s</div></div>' % (u('t.faq'), ''.join(
            '<details><summary>%s</summary><p>%s</p></details>' % (e(f['q']), fix_links(f.get('a_html'), lang) or e(f['a'])) for f in hd['faq']))
    cta = ''
    if hd.get('cta'):
        ct = hd['cta']
        cta = ('<div class="hubcta"><h2>%s</h2><p>%s</p><div class="chs">'
               '<a href="%s" target="_blank" rel="noopener" style="background:#1F7A4D">WhatsApp</a>'
               '<a href="viber://chat?number=%%2B%s" style="background:#5B4B9A">Viber</a>'
               '<a href="https://t.me/+%s" target="_blank" rel="noopener" style="background:#1F6F99">Telegram</a>'
               '<a href="%s" target="_blank" rel="noopener" style="background:#2D2A6E">MAX</a></div></div>') % (
            e(ct['h']), e(ct['p']), e(ct['href']), C['whatsapp'], C['whatsapp'], e(C['max']))
    body = f'''<main id="main">
  <section class="thero">
    <img src="/images/v2/alanya-hero.jpg" srcset="{HERO_SRCSET}" sizes="100vw" alt="">
    <div class="inner">
      <div class="thead">
        <p class="eyebrow">{u('tours.eyebrow')}</p>
        <h1>{e(hd['h1'])}</h1>
        <p>{e(hd['sub'])}</p>
        <div class="hubswitch">{sw}</div>
      </div>
      <div class="choice">
        <div class="glass">
          <p class="eyebrow">{u('choice.g.eyebrow')}</p>
          <h2>{u('choice.g.h')}</h2>
          <p>{u('choice.g.p')}</p>
          <button class="btn btn-gold" type="button" data-book="cappadocia">{u('choice.g.btn')}</button>
        </div>
        <div class="glass">
          <p class="eyebrow">{u('choice.p.eyebrow')}</p>
          <h2>{u('choice.p.h')}</h2>
          <p>{u('choice.p.p')}</p>
          <button class="btn btn-line" type="button" data-book="boat">{u('choice.p.btn')}</button>
        </div>
      </div>
    </div>
  </section>
  <section class="cards"><div class="inner">{tour_cards(lang, ORDER)}</div></section>
  <section class="hub hub-after"><div class="inner">
    {'<p class="upd">%s</p>' % e(hd['upd']) if hd.get('upd') else ''}
    <div class="tablewrap"><table><thead><tr>{th}</tr></thead><tbody>{''.join(rows)}</tbody></table></div>
    <div class="hubcards">{secs}</div>
    {faq}
    {cta}
  </div></section>
</main>
'''
    return h + '\n' + header(lang, page, 'hub') + body + tail(lang, 'hub')


# ------------------------------------------------------------------ main
def write(path, s):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(s)


BLOG = ['blog', 'blog-cappadocia-balloon', 'blog-cappadocia-journey', 'blog-pamukkale-guide', 'blog-demre-santa-kekova', 'blog-green-canyon-guide']


def sitemap():
    import datetime
    today = datetime.date.today().isoformat()
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
           '        xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for page in PAGES + BLOG:
        alts = ''.join('\n    <xhtml:link rel="alternate" hreflang="%s" href="%s"/>' % (l, absu(l, page)) for l in LANGS)
        alts += '\n    <xhtml:link rel="alternate" hreflang="x-default" href="%s"/>' % absu('en', page)
        for lang in LANGS:
            out.append('  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>%s\n  </url>' % (absu(lang, page), today, alts))
    out.append('</urlset>\n')
    with open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(out))


def main():
    n = 0
    for lang in LANGS:
        write(outfile(lang, ''), build_home(lang)); n += 1
        for tid in ORDER:
            write(outfile(lang, T[tid]['slug']), build_tour(lang, tid)); n += 1
        for key in ('alanya', 'side'):
            write(outfile(lang, 'excursions-from-' + key), build_hub(lang, key)); n += 1
    sitemap()
    print('built %d pages + sitemap.xml' % n)


if __name__ == '__main__':
    main()
