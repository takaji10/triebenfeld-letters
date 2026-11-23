// GEDCOM date raw strings, spoken politely.
//
// The database keeps each date's raw text exactly as recorded ("13 MAR
// 1905", "ABT 1874", "BET 1890 AND 1900", "CAL 2 FEB 1731/32"); the UI
// wanted "March 13, 1905". This renders the common shapes into the
// interface language and falls back to the raw text for anything it
// does not recognise - the raw string is always the truth, this is
// only its costume.

const MONTHS = {
  en: ['January', 'February', 'March', 'April', 'May', 'June', 'July',
       'August', 'September', 'October', 'November', 'December'],
  de: ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli',
       'August', 'September', 'Oktober', 'November', 'Dezember'],
  pl: ['stycznia', 'lutego', 'marca', 'kwietnia', 'maja', 'czerwca',
       'lipca', 'sierpnia', 'września', 'października', 'listopada',
       'grudnia'],
}

const QUALIFIERS = {
  en: { ABT: 'about', CAL: 'calculated', EST: 'estimated',
        BEF: 'before', AFT: 'after', FROM: 'from', TO: 'to' },
  de: { ABT: 'etwa', CAL: 'berechnet', EST: 'geschätzt',
        BEF: 'vor', AFT: 'nach', FROM: 'von', TO: 'bis' },
  pl: { ABT: 'ok.', CAL: 'wyliczono', EST: 'oszacz.',
        BEF: 'przed', AFT: 'po', FROM: 'od', TO: 'do' },
}

const MON = { JAN: 1, FEB: 2, MAR: 3, APR: 4, MAY: 5, JUN: 6,
              JUL: 7, AUG: 8, SEP: 9, OCT: 10, NOV: 11, DEC: 12 }

// "13 MAR 1905" | "MAR 1905" | "1905" | "1731/32" -> parts
const SHAPE = /^(?:(ABT|CAL|EST|BEF|AFT|FROM|TO)\s+)?(?:(\d{1,2})\s+)?([A-Z]{3})?\s*(\d{4}(?:\/\d{2})?)$/

function yearOf(y) {
  // a double year "1731/32" reads as its first year
  return parseInt(y.split('/')[0], 10)
}

export function fmtDate(raw, lang = 'en') {
  if (!raw) return ''
  const months = MONTHS[lang] || MONTHS.en
  const qual = QUALIFIERS[lang] || QUALIFIERS.en

  // a range: "BET 1890 AND 1900", "FROM 1901 TO 1903", "1890-1900"
  const range = raw.match(/^(?:BET\s+|FROM\s+)?(.+?)\s+(?:AND|TO)\s+(.+)$/i)
  if (range) {
    const a = fmtDate(range[1], lang), b = fmtDate(range[2], lang)
    if (a && b) return `${a} – ${b}`
  }
  const dash = raw.match(/^(\d{4})\s*[-–]\s*(\d{4})$/)
  if (dash) return `${dash[1]} – ${dash[2]}`

  const m = raw.match(SHAPE)
  if (!m) return raw   // unrecognised: the raw text is the honest fall-back
  const [, q, d, mon, y] = m
  let out = ''
  if (mon && d && y) {
    const mi = MON[mon]
    if (lang === 'de') out = `${d}. ${months[mi - 1]} ${yearOf(y)}`
    else if (lang === 'pl') out = `${d} ${months[mi - 1]} ${yearOf(y)}`
    else out = `${months[mi - 1]} ${+d}, ${yearOf(y)}`
  } else if (mon && y) {
    out = `${months[MON[mon] - 1]} ${yearOf(y)}`
  } else {
    out = String(yearOf(y))
  }
  return q ? `${qual[q]} ${out}` : out
}
