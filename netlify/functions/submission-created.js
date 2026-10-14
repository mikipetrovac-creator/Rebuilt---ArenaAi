// Netlify pokreće ovu funkciju za svaku uspešnu formu (rezervacija ili pitanje).
// Šalje: 1) mejl preko Resend-a, 2) poruku na Telegram i/ili WhatsApp (ako su podešeni).
//
// Podešavanja (Netlify → Project configuration → Environment variables):
//   RESEND_API_KEY      – obavezno (već postoji)
//   EXTRA_TO            – nije obavezno: dodatne adrese za mejl, odvojene zarezom (npr. tvoj Gmail)
//   TELEGRAM_BOT_TOKEN  – nije obavezno: token Telegram bota (od @BotFather)
//   TELEGRAM_CHAT_ID    – nije obavezno: tvoj Telegram chat ID (ili više, odvojeno zarezom)
//   CALLMEBOT_PHONE     – nije obavezno: tvoj WhatsApp broj, npr. +905331429037
//   CALLMEBOT_APIKEY    – nije obavezno: ključ koji ti CallMeBot pošalje na WhatsApp
// Ako neka promenljiva nije upisana, taj kanal se jednostavno preskače.

const env = (k) => (process.env[k] || '').trim();

// Uklanja emoji i višak razmaka iz onoga što gost upiše.
const clean = (s) => String(s == null ? '' : s)
  .replace(/[\p{Extended_Pictographic}️‍]/gu, '')
  .replace(/\s+/g, ' ').trim().slice(0, 600);
const num = (s) => parseInt(clean(s), 10) || 0;

exports.handler = async (event) => {
  const payload = JSON.parse(event.body).payload;
  const data = payload.data || {};
  const formName = payload.form_name; // 'booking-*' ili 'ask-*'
  const isAsk = typeof formName === 'string' && formName.startsWith('ask-');
  const isBooking = typeof formName === 'string' && formName.startsWith('booking-');

  // Zaštita na serveru: broj telefona mora imati pozivni broj države (E.164).
  if (isBooking) {
    const raw = String(data.phone || '').trim();
    let phone = /[A-Za-z]/.test(raw) ? '' : raw.replace(/[\s()\-.]/g, '');
    if (phone.startsWith('00')) phone = '+' + phone.slice(2);
    if (!/^\+[1-9][0-9]{9,14}$/.test(phone)) {
      console.warn('Invalid booking phone rejected:', phone);
      return { statusCode: 200, body: 'Booking ignored: invalid phone format' };
    }
  }

  // ---------- jednostavan tekst rezervacije (isti za mejl i telefon) ----------
  const L = [];
  const add = (label, v) => { v = clean(v); if (v) L.push(`${label}: ${v}`); };
  add('Izlet', data.tour);
  add('Paket', data.package);
  add('Ime', data.name);
  add('Telefon', data.phone);
  add('Email', data.email);
  add('Datum', data.date);
  add('Termin', data.slot);
  add('Broj osoba', data.people);
  add('Hotel', data.hotel || data.pickup);
  if (num(data.adults)) L.push(`Odrasli: ${num(data.adults)}`);
  if (num(data.children)) L.push(`Deca: ${num(data.children)}`);
  if (num(data.infants)) L.push(`Bebe: ${num(data.infants)}`);
  add('Ukupno', data.total);
  add(isAsk ? 'Pitanje' : 'Poruka', data.notes);
  add('Jezik', data.lang);

  const title = isAsk ? 'Novo pitanje' : 'Nova rezervacija';
  const subject = isAsk
    ? `Novo pitanje - ${clean(data.name)}`
    : `Nova rezervacija: ${clean(data.tour) || 'izlet'} - ${clean(data.name)}`;
  const msg = `${title}\n\n${L.join('\n')}`;

  // ---------- 1) mejl: običan tekst, bez slika i dizajna ----------
  const to = ['info@myvalanyatravel.com', ...env('EXTRA_TO').split(',').map((s) => s.trim()).filter(Boolean)];
  const guestMail = clean(data.email);
  const mail = { from: 'M.Y.V. Booking <system@myvalanyatravel.com>', to, subject, text: msg };
  if (/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(guestMail)) mail.reply_to = guestMail;

  const sendMail = fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${env('RESEND_API_KEY')}` },
    body: JSON.stringify(mail)
  }).then(async (r) => { if (!r.ok) throw new Error('Resend: ' + (await r.text())); return 'mail ok'; });

  const jobs = [sendMail];

  if (env('TELEGRAM_BOT_TOKEN') && env('TELEGRAM_CHAT_ID')) {
    for (const chat of env('TELEGRAM_CHAT_ID').split(',').map((s) => s.trim()).filter(Boolean)) {
      jobs.push(fetch(`https://api.telegram.org/bot${env('TELEGRAM_BOT_TOKEN')}/sendMessage`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ chat_id: chat, text: msg, disable_web_page_preview: true })
      }).then(async (r) => { if (!r.ok) throw new Error('Telegram: ' + (await r.text())); return 'telegram ok'; }));
    }
  }

  if (env('CALLMEBOT_PHONE') && env('CALLMEBOT_APIKEY')) {
    const url = 'https://api.callmebot.com/whatsapp.php?phone=' + encodeURIComponent(env('CALLMEBOT_PHONE')) +
      '&text=' + encodeURIComponent(msg) + '&apikey=' + encodeURIComponent(env('CALLMEBOT_APIKEY'));
    jobs.push(fetch(url).then(async (r) => { if (!r.ok) throw new Error('CallMeBot: ' + (await r.text())); return 'whatsapp ok'; }));
  }

  // Svaki kanal radi nezavisno: ako jedan padne, ostali i dalje stignu.
  const results = await Promise.allSettled(jobs);
  results.forEach((r) => { if (r.status === 'rejected') console.error(r.reason && r.reason.message); else console.log(r.value); });
  const mailOk = results[0].status === 'fulfilled';
  return { statusCode: mailOk ? 200 : 500, body: results.map((r) => r.status).join(',') };
};
