#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ############################################################################
# !!! PAZNJA — OVA SKRIPTA JE ZASTARELA I NE SME DA SE POKRECE !!!
#
# Jezicke verzije (/ru/ /de/ /tr/ /uk/ /sr/) su posle poslednjeg pokretanja
# dodatno rucno dorajivane. Skripta te izmene NE zna da reprodukuje.
# Ako je pokrenes, pokvarices sledece (provereno, 56 linija po fajlu):
#
#   1. JSON-LD FAQ seme se vracaju na engleski u svih 5 jezika
#   2. Interni linkovi gube prefiks jezika: /ru/pamukkale -> /pamukkale
#      (ruski posetilac zavrsi na engleskoj stranici)
#   3. Sekcija "Ostale ture" se vraca na engleski
#   4. sitemap.xml gubi excursions-from-alanya i excursions-from-side
#      i vraca .html nastavke umesto cistih URL-ova
#
# Dok se skripta ne popravi, jezicke fajlove menjaj DIREKTNO.
# Guard ispod sprecava slucajno pokretanje.
# ############################################################################
"""
generate-languages.py  (v2)  —  M.Y.V. Alanya Travel
----------------------------------------------------
Pravi visejezicke verzije sajta od engleskih "master" fajlova:
  - prevodi <title> i opis (meta)
  - UPECE prevedeni sadrzaj direktno u HTML (iz "translations" recnika u stranici)
  - doda <html lang>, canonical, hreflang mrezu
  - prebacivac jezika (zastavica) VODI na /ru/ /de/... adresu
  - osvezi sitemap.xml

KORISTI SE:  python3 generate-languages.py
Uredjuj SAMO: index.html i demre-myra-kekova.html (engleski).
Foldere /ru/ /de/ /tr/ /uk/ /sr/ NE diraj rucno (prave se automatski).
Skripta je bezbedna za ponovno pokretanje (idempotentna).
"""
import os, re, json

SITE = "https://myvalanyatravel.com"
LANGS = ["en", "ru", "de", "tr", "uk", "sr"]
OG_LOCALE = {"en":"en_US","ru":"ru_RU","de":"de_DE","tr":"tr_TR","uk":"uk_UA","sr":"sr_RS"}

PAGES = [
    {"file":"index.html",             "key":"index", "url_en":"/",                  "url_lang":"/{lang}/"},
    {"file":"demre-myra-kekova.html", "key":"demre", "url_en":"/demre-myra-kekova", "url_lang":"/{lang}/demre-myra-kekova.html"},
    {"file":"pamukkale.html",         "key":"pamukkale", "url_en":"/pamukkale",        "url_lang":"/{lang}/pamukkale.html"},
    {"file":"green-canyon.html",      "key":"greencanyon", "url_en":"/green-canyon",   "url_lang":"/{lang}/green-canyon.html"},
]

# Blog stranice: NISU visejezicne kroz "translations" (statične su, prevedene rucno u /ru/ /de/...),
# pa se NE generisu ovde — ali IDU u sitemap. Zato ih drzimo odvojeno i samo za sitemap.
# Blog koristi .html i za engleski (nema pretty URL), pa je url_en = "/blog.html".
BLOG_PAGES = [
    {"url_en":"/blog.html",                     "url_lang":"/{lang}/blog.html"},
    {"url_en":"/blog-cappadocia-balloon.html",  "url_lang":"/{lang}/blog-cappadocia-balloon.html"},
    {"url_en":"/blog-cappadocia-journey.html",  "url_lang":"/{lang}/blog-cappadocia-journey.html"},
    {"url_en":"/blog-pamukkale-guide.html",     "url_lang":"/{lang}/blog-pamukkale-guide.html"},
    {"url_en":"/blog-demre-santa-kekova.html",  "url_lang":"/{lang}/blog-demre-santa-kekova.html"},
    {"url_en":"/blog-green-canyon-guide.html",  "url_lang":"/{lang}/blog-green-canyon-guide.html"},
]

# Prevedeni <title> i opis (en ostaje kako je u fajlu)
META = {
 "index": {
  "ru": ("Тур в Каппадокию из Аланьи (2 дня) | M.Y.V. Travel",
         "2-дневный тур в Каппадокию из Аланьи и Сиде — воздушные шары, долины, подземные города, Гёреме. Отель, питание и гид. Бронь онлайн, оплата при встрече."),
  "de": ("Kappadokien-Tour ab Alanya (2 Tage) | M.Y.V. Travel",
         "2-tägige Kappadokien-Tour ab Alanya und Side — Ballons, Feenkamine, unterirdische Städte, Göreme. Hotel, Mahlzeiten und Guide. Online buchen, bei Abholung zahlen."),
  "tr": ("Alanya'dan Kapadokya Turu (2 Gün) | M.Y.V. Travel",
         "Alanya ve Side'den 2 günlük Kapadokya turu — balonlar, peri bacaları, yeraltı şehirleri, Göreme. Otel, yemek ve rehber dahil. Online rezervasyon; ödemeyi alışta yapın."),
  "uk": ("Тур у Каппадокію з Аланьї (2 дні) | M.Y.V. Travel",
         "2-денний тур у Каппадокію з Аланьї та Сіде — повітряні кулі, долини, підземні міста, Гереме. Готель, харчування та гід. Бронювання онлайн, оплата при зустрічі."),
  "sr": ("Tura u Kapadokiju iz Alanje (2 dana) | M.Y.V. Travel",
         "Dvodnevna tura u Kapadokiju iz Alanje i Side — baloni, vilinski dimnjaci, podzemni gradovi, Gereme. Hotel, obroci i vodič. Rezervacija onlajn, plaćanje pri preuzimanju."),
 },
 "demre": {
  "ru": ("Тур Демре · Мира · Кекова из Аланьи | M.Y.V. Travel",
         "Однодневный тур Демре, Мира и Кекова из Аланьи и Сиде — церковь Святого Николая, ликийские гробницы и круиз над затонувшим городом Кекова. Бронь онлайн, оплата при встрече."),
  "de": ("Demre · Myra · Kekova Tour ab Alanya | M.Y.V. Travel",
         "Ganztägige Demre-, Myra- und Kekova-Tour ab Alanya und Side — Nikolauskirche, lykische Felsengräber und eine Bootsfahrt über die versunkene Stadt Kekova. Online buchen, bei Abholung zahlen."),
  "tr": ("Alanya'dan Demre · Myra · Kekova Turu | M.Y.V. Travel",
         "Alanya ve Side'den tam günlük Demre, Myra ve Kekova turu — Aziz Nikolaos Kilisesi, Likya kaya mezarları ve Kekova batık şehir tekne turu. Online rezervasyon; ödemeyi alışta yapın."),
  "uk": ("Тур Демре · Міра · Кекова з Аланьї | M.Y.V. Travel",
         "Одноденний тур Демре, Міра і Кекова з Аланьї та Сіде — церква Святого Миколая, лікійські гробниці та круїз над затонулим містом Кекова. Бронювання онлайн, оплата при зустрічі."),
  "sr": ("Tura Demre · Mira · Kekova iz Alanje | M.Y.V. Travel",
         "Celodnevna tura Demre, Mira i Kekova iz Alanje i Side — crkva Svetog Nikole, likijske grobnice i krstarenje nad potonulim gradom Kekova. Rezervacija onlajn, plaćanje pri preuzimanju."),
 },
  "pamukkale": {
  "ru": ("Тур в Памуккале из Аланьи и Сиде | M.Y.V. Travel",
         "Однодневный тур в Памуккале из Аланьи и Сиде — белоснежные травертиновые террасы, древний Иераполис и античный бассейн Клеопатры. Бронь онлайн, оплата при встрече."),
  "de": ("Pamukkale-Tour ab Alanya & Side | M.Y.V. Travel",
         "Ganztägige Pamukkale-Tour ab Alanya und Side — die weißen Sinterterrassen, das antike Hierapolis und der Antike Pool der Kleopatra. Online buchen, bei Abholung zahlen."),
  "tr": ("Alanya & Side'den Pamukkale Turu | M.Y.V. Travel",
         "Alanya ve Side'den tam günlük Pamukkale turu — beyaz travertenler, antik Hierapolis ve Kleopatra Antik Havuzu. Online rezervasyon; ödemeyi alışta yapın."),
  "uk": ("Тур у Памуккале з Аланьї та Сіде | M.Y.V. Travel",
         "Одноденний тур у Памуккале з Аланьї та Сіде — білі травертинові тераси, стародавній Ієраполіс та античний басейн Клеопатри. Бронювання онлайн, оплата при зустрічі."),
  "sr": ("Tura u Pamukkale iz Alanje i Side | M.Y.V. Travel",
         "Celodnevna tura u Pamukkale iz Alanje i Side — bele travertinske terase, antički Hijerapolis i Kleopatrin antički bazen. Rezervacija onlajn, plaćanje pri preuzimanju."),
 },
 "greencanyon": {
  "ru": ("Тур в Грин-Каньон из Аланьи и Сиде | M.Y.V. Travel",
         "Однодневный тур в Грин-Каньон из Аланьи и Сиде — прогулка на яхте по озеру Оймапынар, Большой каньон, купание и обед у Грин-Лейк. Бронь онлайн, оплата при встрече."),
  "de": ("Green-Canyon-Tour ab Alanya & Side | M.Y.V. Travel",
         "Tagestour zum Green Canyon ab Alanya und Side — Bootsfahrt auf dem Oymapınar-See, Großer Canyon, Badepause und Mittagessen am Green Lake. Online buchen, bei Abholung zahlen."),
  "tr": ("Alanya & Side'den Green Canyon Turu | M.Y.V. Travel",
         "Alanya ve Side'den günlük Green Canyon turu — Oymapınar Gölü'nde tekne turu, Büyük Kanyon, yüzme molası ve Green Lake'te öğle yemeği. Online rezervasyon; ödemeyi alışta yapın."),
  "uk": ("Тур у Грін-Каньйон з Аланьї та Сіде | M.Y.V. Travel",
         "Одноденний тур у Грін-Каньйон з Аланьї та Сіде — прогулянка на яхті озером Оймапинар, Великий каньйон, купання та обід біля Грін-Лейк. Бронювання онлайн, оплата при зустрічі."),
  "sr": ("Tura u Grin kanjon iz Alanje i Side | M.Y.V. Travel",
         "Jednodnevna tura u Grin kanjon iz Alanje i Side — krstarenje brodom po jezeru Ojmapinar, Veliki kanjon, kupanje i ručak na Grin jezeru. Rezervacija onlajn, plaćanje pri preuzimanju."),
 },
}

def page_url(page, lang):
    return SITE + (page["url_en"] if lang=="en" else page["url_lang"].format(lang=lang))

def extract_translations(html):
    start = html.index('const translations')
    end_all = html.index('let currentLang', start)
    pos = []
    for lg in LANGS:
        m = re.search(r'\b'+lg+r'\s*:\s*\{', html[start:end_all])
        if m: pos.append((m.start()+start, lg))
    pos.sort()
    kv = re.compile(r'"((?:[^"\\]|\\.)*)"\s*:\s*"((?:[^"\\]|\\.)*)"')
    def dec(s):
        try: return json.loads('"'+s+'"')
        except Exception: return s
    out = {}
    for i,(p,lg) in enumerate(pos):
        e = pos[i+1][0] if i+1<len(pos) else end_all
        out[lg] = {dec(k):dec(v) for k,v in kv.findall(html[p:e])}
    return out

def bake_body(html, lang_dict):
    open_re = re.compile(r'<([a-zA-Z0-9]+)([^>]*\bdata-i18n="([^"]+)"[^>]*)>')
    spans = []
    for m in open_re.finditer(html):
        tag, key = m.group(1), m.group(3)
        close = html.find('</%s>' % tag, m.end())
        if close == -1: continue
        spans.append((m.start(), m.end(), close, key))
    def nested(oe, ce):
        return any(s2 > oe and s2 < ce for (s2,_,_,_) in spans)
    work = [(oe,ce,k) for (s,oe,ce,k) in spans if not nested(oe,ce)]
    for oe,ce,k in sorted(work, key=lambda x:-x[0]):
        v = lang_dict.get(k)
        if v is not None:
            html = html[:oe] + v + html[ce:]
    return html

def match_braces(s, open_idx):
    depth=0; i=open_idx; inStr=False; q=''; esc=False
    while i < len(s):
        c = s[i]
        if inStr:
            if esc: esc=False
            elif c=='\\': esc=True
            elif c==q: inStr=False
        else:
            if c in '"\'`': inStr=True; q=c
            elif c=='{': depth+=1
            elif c=='}':
                depth-=1
                if depth==0: return i
        i+=1
    return -1

def replace_changeLanguage(html, urlmap):
    js_map = "{" + ",".join("%s:'%s'" % (lg, urlmap[lg]) for lg in LANGS) + "}"
    newfn = ("function changeLanguage(lang){var U=%s;"
             "if(U[lang]){_saveLangScroll();window.location.href=U[lang];}else{setLanguage(lang);}}" % js_map)
    idx = html.find('function changeLanguage(lang)')
    if idx == -1: return html
    brace = html.index('{', idx)
    close = match_braces(html, brace)
    return html[:idx] + newfn + html[close+1:]

def hreflang_block(page):
    out = ["<!-- HREFLANG:START (auto) -->"]
    for lg in LANGS:
        out.append('<link rel="alternate" hreflang="%s" href="%s">' % (lg, page_url(page, lg)))
    out.append('<link rel="alternate" hreflang="x-default" href="%s">' % page_url(page, "en"))
    out.append("<!-- HREFLANG:END -->")
    return "\n".join(out)

def sub1(html, pat, repl):
    return re.sub(pat, repl, html, count=1)

def transform(master, page, lang, translations):
    h = master
    h = re.sub(r'\n?<!-- HREFLANG:START.*?<!-- HREFLANG:END -->', '', h, flags=re.DOTALL)
    h = sub1(h, r'<html lang="[^"]*">', '<html lang="%s">' % lang)
    if lang != "en":
        title, desc = META[page["key"]][lang]
        h = sub1(h, r'<title>.*?</title>', lambda m: '<title>%s</title>' % title)
        for pat in [r'(<meta name="description" content=")[^"]*(">)',
                    r'(<meta property="og:description" content=")[^"]*(">)',
                    r'(<meta name="twitter:description" content=")[^"]*(">)']:
            h = sub1(h, pat, lambda m: m.group(1)+desc+m.group(2))
        for pat in [r'(<meta property="og:title" content=")[^"]*(">)',
                    r'(<meta name="twitter:title" content=")[^"]*(">)']:
            h = sub1(h, pat, lambda m: m.group(1)+title+m.group(2))
    h = sub1(h, r'(<meta property="og:locale" content=")[^"]*(">)', lambda m: m.group(1)+OG_LOCALE[lang]+m.group(2))
    url = page_url(page, lang)
    h = sub1(h, r'(<link rel="canonical" href=")[^"]*(">)', lambda m: m.group(1)+url+m.group(2))
    h = sub1(h, r'(<meta property="og:url" content=")[^"]*(">)', lambda m: m.group(1)+url+m.group(2))
    h = sub1(h, r'(<link rel="canonical" href="[^"]*">)', lambda m: m.group(1)+"\n"+hreflang_block(page))
    h = sub1(h, r"let currentLang = [^;\n]+;", "let currentLang = '%s';" % lang)
    urlmap = {lg: (page_url(page, lg).replace(SITE, "") or "/") for lg in LANGS}
    h = replace_changeLanguage(h, urlmap)
    if lang != "en":
        h = bake_body(h, translations[lang])
    return h

def _blog_url(page, lang):
    return SITE + (page["url_en"] if lang == "en" else page["url_lang"].format(lang=lang))

def write_sitemap():
    items = []
    # 1) glavne (visejezicne) tur-stranice
    for page in PAGES:
        for lang in LANGS:
            alts = "".join('\n    <xhtml:link rel="alternate" hreflang="%s" href="%s"/>' % (lg, page_url(page, lg)) for lg in LANGS)
            alts += '\n    <xhtml:link rel="alternate" hreflang="x-default" href="%s"/>' % page_url(page, "en")
            items.append("  <url>\n    <loc>%s</loc>%s\n  </url>" % (page_url(page, lang), alts))
    # 2) blog stranice (staticne, prevedene rucno) — samo u sitemap, isti hreflang format
    for page in BLOG_PAGES:
        for lang in LANGS:
            alts = "".join('\n    <xhtml:link rel="alternate" hreflang="%s" href="%s"/>' % (lg, _blog_url(page, lg)) for lg in LANGS)
            alts += '\n    <xhtml:link rel="alternate" hreflang="x-default" href="%s"/>' % _blog_url(page, "en")
            items.append("  <url>\n    <loc>%s</loc>%s\n  </url>" % (_blog_url(page, lang), alts))
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
           '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(items) + "\n</urlset>\n")
    open("sitemap.xml","w",encoding="utf-8").write(xml)

def build():
    masters, trans = {}, {}
    for p in PAGES:
        masters[p["file"]] = open(p["file"], encoding="utf-8").read()
        trans[p["file"]] = extract_translations(masters[p["file"]])
    written = []
    for lang in LANGS:
        for page in PAGES:
            out = transform(masters[page["file"]], page, lang, trans[page["file"]])
            path = page["file"] if lang=="en" else os.path.join(lang, page["file"])
            if lang != "en": os.makedirs(lang, exist_ok=True)
            open(path, "w", encoding="utf-8").write(out)
            written.append(path)
    write_sitemap()
    return written

if __name__ == "__main__":
    import sys
    if "--zaista-hocu" not in sys.argv:
        print(__doc__ if False else "")
        print("ZAUSTAVLJENO: skripta je zastarela i pokvarila bi jezicke verzije.")
        print("Detalji su u komentaru na vrhu fajla.")
        print("Ako stvarno znas sta radis: python3 generate-languages.py --zaista-hocu")
        sys.exit(1)
    files = build()
    print("Generisano %d HTML + sitemap.xml:" % len(files))
    for f in files: print("  ", f)
