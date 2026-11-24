/* The one search bar (the editor, 2026-11-24; docs/SITE_OVERHAUL_PLAN.md, Phase 2).
   Used on /documents/, on a holding's page and on the four lists (Manuscripts,
   Newspapers, Literature, Maps), in both languages. No dependencies.

   window.BROWSE_CFG (set by _includes/browse.html):
     kind   documents | newspapers | literature | maps   (which index is searched)
     list   true on a list page: its cards (.sources) stand until the reader
            types or sets a filter, then a list of matching documents / items /
            passages / maps takes their place; Reset brings the cards back
     unit   a holding's slug: the list is that holding's documents alone

   Indexes: the documents' (search-index.json) and the other kinds' are loaded
   at once on a page that lists them, and on a list page at the first touch of
   the bar; the English texts (search-<kind>-en.json) only when a search asks
   for them. Matching is by regular expression built from the query, so the
   highlight is made on the original text itself (no folded copy to keep in
   step with it). */
(function () {
  'use strict';
  var CFG = window.BROWSE_CFG || {kind: 'documents', list: false, unit: ''};
  var T = window.I18N || {};
  var LANG = window.LANG || 'en';
  var KIND = CFG.kind || 'documents';
  var LIST = !!CFG.list;
  var WORK = CFG.work || '';   // a work's own page: its passages alone, links within the page
  var LAZY = LIST || !!WORK;   // the index is fetched at the first touch of the bar
  var FIXED_UNIT = CFG.unit || window.BROWSE_UNIT || '';
  var PAGE = 150;
  function s_(k, d) { return (T && T[k] != null) ? T[k] : d; }
  function $(id) { return document.getElementById(id); }
  function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }

  var DATA = [];            // the rows of this kind (and holding)
  var FACETS = null;
  var els = {};
  var TERM = '';            // a glossary entry, from ?term=
  var LOADED = false, LOADING = false;
  var EN_STATE = 0;         // 0 not asked, 1 loading, 2 loaded
  var shown = PAGE;
  var yearLo, yearHi, limLo = CFG.yearMin, limHi = CFG.yearMax;
  var ms = {};              // the two multi-selects
  var cards = [];           // a list page's cards
  var coll = (typeof Intl !== 'undefined' && Intl.Collator) ? new Intl.Collator('en', {numeric: true}) : null;

  /* ------------------------------------------------------------ text helpers */

  // Accent-insensitive groups: any letter of a group stands for the group.
  var GROUPS = ['aąäàáâãåā', 'eęéèêëē', 'iíìîïī', 'oóöòôõō', 'uüúùûū', 'cćčç', 'nńñ',
                'sśšßſ', 'zźżž', 'lł', 'yý', 'dď', 'rř', 'tť'];
  var GROUP_OF = {};
  GROUPS.forEach(function (g) {
    Array.prototype.forEach.call(g, function (ch) { GROUP_OF[ch] = g; });
  });
  function fold(s) {
    // For sorting and for the names in the type-ahead (not for matching text).
    var out = '';
    s = String(s || '').toLowerCase();
    for (var i = 0; i < s.length; i++) {
      var g = GROUP_OF[s.charAt(i)];
      out += g ? g.charAt(0) : s.charAt(i);
    }
    return out;
  }
  function reEsc(ch) { return /[\\^$.*+?()[\]{}|\/]/.test(ch) ? '\\' + ch : ch; }

  function classFor(ch, ci, accents) {
    var low = ch.toLowerCase();
    var g = accents ? GROUP_OF[low] : null;
    if (!g) return reEsc(ch);
    var members = Array.prototype.slice.call(g);
    if (!ci) {
      var up = ch !== low;
      members = members.map(function (m) { return up ? m.toUpperCase() : m; })
        .filter(function (m) { return m.length === 1; });
    }
    return '[' + members.map(reEsc).join('') + ']';
  }

  function termSource(term, o) {
    var out = '';
    var chars = Array.from(term);
    for (var i = 0; i < chars.length; i++) {
      var ch = chars[i];
      if (/\s/.test(ch)) {
        while (i + 1 < chars.length && /\s/.test(chars[i + 1])) i++;
        out += '\\s+';
      } else out += classFor(ch, !o.cs, o.accents);
    }
    if (o.whole) out = '(?<![\\p{L}\\p{N}])(?:' + out + ')(?![\\p{L}\\p{N}])';
    return out;
  }

  function parseQuery(q, o) {
    q = (q || '').trim();
    if (!q) return [];
    if (o.phrase) return [q.replace(/"/g, '').replace(/\s+/g, ' ').trim()].filter(Boolean);
    var out = [], re = /"([^"]+)"|(\S+)/g, m;
    while ((m = re.exec(q))) {
      var t = (m[1] != null ? m[1] : m[2]).replace(/"/g, '').trim();
      if (t) out.push(t);
    }
    return out;
  }

  /* --------------------------------------------------------------- the state */

  function opts() {
    return {
      phrase: els.phrase.checked, any: els.any.checked, whole: els.whole.checked,
      accents: els.accents.checked, cs: els.cs.checked,
      inOrig: els.inOrig.checked, inEn: els.inEn.checked, inSum: els.inSum.checked
    };
  }

  function rowEn(it) { return (EN_MAP && EN_MAP[KIND === 'documents' ? it.uid : it.id]) || ''; }
  var EN_MAP = null;

  function sumOf(it) {
    var s = (LANG === 'de' && it.summary_de) ? it.summary_de : (it.summary || it.summary_de || '');
    if (KIND === 'newspapers' || KIND === 'maps') {
      var ti = (LANG === 'de' && it.title_de) ? it.title_de : (it.title_en || it.title || '');
      s = [ti, it.orig_title, s].filter(Boolean).join(' — ');
    }
    return s;
  }

  function fieldsOf(it, o) {
    var f = [];
    if (o.inOrig && it.text) f.push(['orig', it.text]);
    if (o.inEn) { var e = rowEn(it); if (e) f.push(['en', e]); }
    if (o.inSum) { var s = sumOf(it); if (s) f.push(['sum', s]); }
    return f;
  }

  function buildMatcher(q, o) {
    var terms = parseQuery(q, o);
    if (!terms.length) return null;
    var flags = (o.cs ? '' : 'i') + 'u';
    var srcs = terms.map(function (t) { return termSource(t, o); });
    return {
      tests: srcs.map(function (s) { return new RegExp(s, flags); }),
      any: o.any && terms.length > 1,
      mark: new RegExp(srcs.join('|'), 'g' + flags),
      terms: terms
    };
  }

  function matchText(it, mt, o) {
    // -> the field name of the first field showing a hit, or '' for no match.
    var fs = fieldsOf(it, o);
    var found = null, all = true, some = false;
    for (var k = 0; k < mt.tests.length; k++) {
      var hit = false;
      for (var j = 0; j < fs.length; j++) {
        if (mt.tests[k].test(fs[j][1])) {
          hit = true;
          if (!found) found = fs[j];
        }
      }
      if (hit) some = true; else all = false;
    }
    if (!(mt.any ? some : all)) return null;
    // the field to show: the first with any term in it
    for (var m = 0; m < fs.length; m++) {
      mt.mark.lastIndex = 0;
      if (mt.mark.test(fs[m][1])) return fs[m];
    }
    return found;
  }

  function snippet(text, mt) {
    var re = mt.mark, hits = [], m;
    re.lastIndex = 0;
    while ((m = re.exec(text)) && hits.length < 400) {
      if (m[0].length === 0) { re.lastIndex++; continue; }
      hits.push([m.index, m.index + m[0].length]);
    }
    if (!hits.length) return esc(text.slice(0, 200)) + (text.length > 200 ? '…' : '');
    var start = Math.max(0, hits[0][0] - 70);
    var end = Math.min(text.length, hits[0][1] + 130);
    var out = '', pos = start;
    for (var i = 0; i < hits.length; i++) {
      if (hits[i][1] <= start) continue;
      if (hits[i][0] >= end) break;
      var a = Math.max(hits[i][0], start), b = Math.min(hits[i][1], end);
      out += esc(text.slice(pos, a)) + '<mark>' + esc(text.slice(a, b)) + '</mark>';
      pos = b;
    }
    out += esc(text.slice(pos, end));
    return (start > 0 ? '…' : '') + out.replace(/\s*\n\s*/g, ' ') + (end < text.length ? '…' : '');
  }

  /* ----------------------------------------------------------------- filters */

  function eraOf(it) {
    if (it.era) return it.era;
    var y = parseInt(it.year, 10);
    if (isNaN(y) || !FACETS) return '';
    for (var i = 0; i < FACETS.eras.length; i++) {
      var e = FACETS.eras[i];
      if (e.first != null && y >= e.first && y <= e.last) return e.slug;
    }
    return '';
  }

  function placesOf(it) {
    if (it._pl) return it._pl;
    var pl = (KIND === 'documents' ? (FACETS.docplaces[it.uid] || []) : (it.pl || [])).slice();
    if (it.place && FACETS._nameSlug[it.place] && pl.indexOf(FACETS._nameSlug[it.place]) < 0) {
      pl.push(FACETS._nameSlug[it.place]);
    }
    it._pl = pl;
    return pl;
  }

  function readFilters() {
    return {
      unit: els.unit ? els.unit.value : '',
      archive: els.archive ? els.archive.value : '',
      type: els.type ? els.type.value : '',
      era: els.era ? els.era.value : '',
      theme: els.theme ? els.theme.value : '',
      lo: yearLo, hi: yearHi,
      fullYears: yearLo <= limLo && yearHi >= limHi,
      people: ms.person ? ms.person.ids() : [],
      places: ms.place ? ms.place.ids() : []
    };
  }

  function filtersActive(f) {
    return !!(f.unit || f.archive || f.type || f.era || f.theme || !f.fullYears ||
              f.people.length || f.places.length || TERM);
  }

  function passes(it, f) {
    if (f.unit && it.unit !== f.unit) return false;
    if (f.archive || f.type) {
      var u = FACETS.units[it.unit];
      if (!u) return false;
      if (f.archive && u.archive !== f.archive) return false;
      if (f.type && u.types.indexOf(f.type) < 0) return false;
    }
    if (f.era && eraOf(it) !== f.era) return false;
    if (f.theme && (it.themes || []).indexOf(f.theme) < 0) return false;
    if (!f.fullYears) {
      var y = parseInt(it.year, 10);
      if (isNaN(y) || y < f.lo || y > f.hi) return false;
    }
    if (f.people.length) {
      var pp = it.people || [];
      for (var i = 0; i < f.people.length; i++) if (pp.indexOf(f.people[i]) < 0) return false;
    }
    if (f.places.length) {
      var pl = placesOf(it);
      for (var j = 0; j < f.places.length; j++) if (pl.indexOf(f.places[j]) < 0) return false;
    }
    if (TERM && (it.gl || []).indexOf(TERM) < 0) return false;
    return true;
  }

  /* ---------------------------------------------------------------- ordering */

  function num(a, b) { return a < b ? -1 : a > b ? 1 : 0; }
  function cmpStr(a, b) { return coll ? coll.compare(a, b) : num(a, b); }

  function azKey(it) {
    if (KIND === 'documents') {
      var u = FACETS && FACETS.units[it.unit];
      return fold((u ? u.ref : it.unit) + ' ' + it.id);
    }
    var t = it.az || '';
    if (KIND !== 'literature' && LANG === 'de' && it.title_de) t = it.title_de;
    return fold(t.replace(/[\[\]]/g, ''));
  }

  function sortRows(list, order) {
    var dir = (order === 'desc' || order === 'za') ? -1 : 1;
    var byAz = order === 'az' || order === 'za';
    list.forEach(function (it) { if (it._az == null) it._az = azKey(it); });
    list.sort(function (a, b) {
      var r;
      if (byAz) {
        r = cmpStr(a._az, b._az) * dir;
      } else {
        var da = a.date || '', db = b.date || '';
        if (!da && !db) r = 0;
        else if (!da) return 1;              // undated last, in either direction
        else if (!db) return -1;
        else r = num(da, db) * dir;
      }
      if (r) return r;
      // ties: the holding, then the number or the page, in the direction asked
      r = cmpStr(a._az, b._az);
      if (!r) r = (a.n || 0) - (b.n || 0);
      return r * (byAz ? dir : 1);
    });
    return list;
  }

  /* ----------------------------------------------------------------- results */

  function titleOf(it) {
    if (KIND === 'literature') return (LANG === 'en' ? it.title_en : it.title) || it.title;
    if (LANG === 'de' && it.title_de) return it.title_de;
    return it.title_en || it.title;
  }

  function hitLabel(f) {
    return '<span class="chip chip-hit">' + esc(s_('f_hit_' + f, f)) + '</span> ';
  }

  function bodyHtml(it, hit, mt, o) {
    if (!mt) return null;
    var multi = [o.inOrig, o.inEn, o.inSum].filter(Boolean).length > 1;
    return '<p class="r-snip">' + (multi ? hitLabel(hit[0]) : '') + snippet(hit[1], mt) + '</p>';
  }

  function rowHtml(it, hit, mt, o, names) {
    var body = bodyHtml(it, hit, mt, o);
    if (KIND === 'documents') {
      return window.DocCards.card(it, {
        lang: LANG, t: T, base: window.SITE_BASE, names: names, body: body
      });
    }
    var href = WORK ? '#' + it.a : CFG.kindUrl + (KIND === 'literature' ? it.slug : it.id) + '/' + (it.a ? '#' + it.a : '');
    var lab = (LANG === 'de' && it.label_de) ? it.label_de : it.label;
    var idChip = KIND === 'literature' ? it.cite : (KIND === 'newspapers' ? it.cite : it.title);
    var head = KIND === 'maps' ? (it.title_en || it.title) : titleOf(it);
    if (KIND === 'maps' && LANG === 'de' && it.title_de) head = it.title_de;
    if (body == null) {
      var sm = (LANG === 'de' && it.summary_de) ? it.summary_de : it.summary;
      body = sm ? '<p class="r-summary">' + esc(sm) + '</p>'
                : (it.text ? '<p class="r-snip">' + esc(it.text.slice(0, 220)) + '…</p>' : '');
    }
    if (WORK) {
      return '<li class="result"><a class="r-head r-jump" href="' + esc(href) + '">' +
        '<span class="r-id">' + esc(lab || it.label || it.id) + '</span></a>' + body + '</li>';
    }
    return '<li class="result"><a class="r-head" href="' + esc(href) + '">' +
      '<span class="r-id">' + esc(idChip) + '</span>' +
      '<span class="r-date">' + esc(head) + '</span>' +
      (lab ? '<span class="r-place">' + esc(lab) + '</span>' : '') +
      '</a>' + body + '</li>';
  }

  var LAST = null;   // the current hits, for "Show more"

  function render() {
    var o = opts();
    var f = readFilters();
    var q = els.q.value.trim();
    var mt = buildMatcher(q, o);
    var active = !!mt || filtersActive(f);
    var order = els.order.value;

    if (WORK && !active) {
      // the work's own text is the list: nothing until the reader searches
      els.results.hidden = true; els.more.parentNode.hidden = true; els.empty.hidden = true;
      els.results.innerHTML = '';
      els.count.textContent = '';
      return;
    }
    if (LIST && !active) {
      // no search, no filter: the page's own cards, in the order asked
      els.results.hidden = true; els.more.parentNode.hidden = true; els.empty.hidden = true;
      cards.forEach(function (c) { c.el.hidden = false; });
      sortCards(order);
      setSourcesHidden(false);
      els.count.textContent = s_('f_showing_all', 'Showing all') + ' ' + cards.length + ' ' +
        s_('f_n_' + KIND, '');
      showTerm();
      return;
    }
    if (!LOADED) {
      ensureLoaded();
      els.count.textContent = s_('f_loading', 'Loading\u2026');
      return;
    }
    showTerm();

    // The English texts are fetched only when a search wants them.
    if (mt && o.inEn && EN_STATE === 0) {
      EN_STATE = 1;
      els.count.textContent = s_('f_loading_en', 'Loading the English texts\u2026');
      fetch(CFG.en).then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); })
        .then(function (m) { EN_MAP = m; EN_STATE = 2; render(); })
        .catch(function () { EN_MAP = {}; EN_STATE = 2; render(); });
      return;
    }
    if (mt && o.inEn && EN_STATE === 1) return;

    var hits = [];
    for (var i = 0; i < DATA.length; i++) {
      var it = DATA[i];
      if (!passes(it, f)) continue;
      if (mt) {
        var h = matchText(it, mt, o);
        if (!h) continue;
        hits.push({it: it, hit: h});
      } else hits.push({it: it, hit: null});
    }
    var rows = sortRows(hits.map(function (h) { h.it._h = h; return h.it; }), order)
      .map(function (it) { return it._h; });
    LAST = {rows: rows, mt: mt, o: o};
    shown = PAGE;
    setSourcesHidden(true);
    els.results.hidden = false;

    var noun = s_('f_n_' + KIND, '');
    els.count.textContent = (rows.length === DATA.length && !active)
      ? s_('f_showing_all', 'Showing all') + ' ' + rows.length + ' ' + noun
      : s_('f_showing', 'Showing') + ' ' + rows.length + ' / ' + DATA.length + ' ' + noun;
    els.empty.hidden = rows.length > 0;
    paint();
  }

  function paint() {
    if (!LAST) return;
    var n = Math.min(shown, LAST.rows.length);
    var html = '';
    for (var i = 0; i < n; i++) {
      var r = LAST.rows[i];
      html += rowHtml(r.it, r.hit, LAST.mt, LAST.o, PEOPLE_NAMES);
    }
    els.results.innerHTML = html;
    els.more.parentNode.hidden = LAST.rows.length <= n;
  }

  /* ------------------------------------------------------------------- cards */

  function setSourcesHidden(h) {
    var s = document.querySelector('.sources');
    if (s) s.hidden = h;
  }

  function collectCards() {
    var list = document.querySelector('.sources');
    if (!list) return;
    cards = Array.prototype.filter.call(list.children, function (el) {
      return el.classList && el.classList.contains('source');
    }).map(function (el) {
      var y = parseInt(el.getAttribute('data-date'), 10);
      return {el: el, az: fold((el.getAttribute('data-az') || '').replace(/[\[\]]/g, '')),
              date: isNaN(y) ? null : y, id: el.id};
    });
  }

  function sortCards(order) {
    var list = document.querySelector('.sources');
    if (!list) return;
    var dir = (order === 'desc' || order === 'za') ? -1 : 1;
    var byAz = order === 'az' || order === 'za';
    cards.sort(function (a, b) {
      if (byAz) return (cmpStr(a.az, b.az) || cmpStr(a.id, b.id)) * dir;
      if (a.date == null && b.date == null) return cmpStr(a.az, b.az);
      if (a.date == null) return 1;
      if (b.date == null) return -1;
      return (num(a.date, b.date) * dir) || cmpStr(a.az, b.az);
    });
    cards.forEach(function (c) { list.appendChild(c.el); });
  }

  /* --------------------------------------------------------- glossary filter */

  function showTerm() {
    var el = $('term');
    if (!el) return;
    el.hidden = !TERM;
    if (!TERM) { el.innerHTML = ''; return; }
    el.innerHTML = esc(s_('f_term', 'Containing the glossary term')) + ' <b>' +
      esc((window.GL_HEADS || {})[TERM] || TERM) + '</b> <button type="button" class="linkish" id="term-clear">' +
      esc(s_('f_term_clear', 'show all')) + '</button>';
    $('term-clear').addEventListener('click', function () { TERM = ''; render(); });
  }

  /* ------------------------------------------------------------ multi-select */

  var PEOPLE_NAMES = {};

  function MultiSelect(root, label) {
    var input = root.querySelector('.ms-input');
    var list = root.querySelector('.ms-list');
    var chipsEl = root.querySelector('.ms-chips');
    var chosen = [];      // [{id, label}]
    var options = [];     // [{id, label, key, n}]
    var active = -1, shownOpts = [];
    var self = {root: root};

    function ids() { return chosen.map(function (c) { return c.id; }); }
    function labelOf(id) {
      for (var i = 0; i < options.length; i++) if (options[i].id === id) return options[i].label;
      return id;
    }
    function drawChips() {
      chipsEl.innerHTML = chosen.map(function (c) {
        return '<span class="ms-chip"><span>' + esc(c.label) + '</span>' +
          '<button type="button" data-id="' + esc(c.id) + '" aria-label="' + esc(s_('f_remove', 'Remove')) + ' ' + esc(c.label) + '">×</button></span>';
      }).join('');
    }
    function add(id) {
      if (ids().indexOf(id) >= 0) return;
      chosen.push({id: id, label: labelOf(id)});
      drawChips(); input.value = ''; closeList(); changed();
    }
    function remove(id) {
      chosen = chosen.filter(function (c) { return c.id !== id; });
      drawChips(); changed();
    }
    function changed() { shown = PAGE; render(); }
    function closeList() { list.hidden = true; input.setAttribute('aria-expanded', 'false'); active = -1; }
    function openList() {
      var q = fold(input.value.trim());
      var have = ids();
      var m = options.filter(function (o) {
        return have.indexOf(o.id) < 0 && (!q || o.key.indexOf(q) >= 0);
      });
      m.sort(function (a, b) {
        var pa = q && a.key.indexOf(q) === 0 ? 0 : 1, pb = q && b.key.indexOf(q) === 0 ? 0 : 1;
        return pa - pb || b.n - a.n || cmpStr(a.key, b.key);
      });
      shownOpts = m.slice(0, 12);
      list.innerHTML = shownOpts.length
        ? shownOpts.map(function (o, i) {
            return '<li role="option" data-id="' + esc(o.id) + '" id="' + root.id + '-o' + i + '">' + esc(o.label) +
              ' <span class="ms-n">(' + o.n + ')</span></li>';
          }).join('')
        : '<li class="ms-none">' + esc(s_('f_no_names', 'No name matches')) + '</li>';
      active = shownOpts.length ? 0 : -1;
      mark();
      list.hidden = false; input.setAttribute('aria-expanded', 'true');
    }
    function mark() {
      Array.prototype.forEach.call(list.querySelectorAll('[role=option]'), function (li, i) {
        li.classList.toggle('is-active', i === active);
        li.setAttribute('aria-selected', i === active ? 'true' : 'false');
      });
      if (active >= 0) input.setAttribute('aria-activedescendant', root.id + '-o' + active);
      else input.removeAttribute('aria-activedescendant');
    }

    input.addEventListener('focus', function () { ensureLoaded(); if (LOADED) openList(); });
    input.addEventListener('input', function () { ensureLoaded(); if (LOADED) openList(); });
    input.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowDown') { e.preventDefault(); if (list.hidden) openList(); else { active = Math.min(shownOpts.length - 1, active + 1); mark(); } }
      else if (e.key === 'ArrowUp') { e.preventDefault(); active = Math.max(0, active - 1); mark(); }
      else if (e.key === 'Enter') {
        e.preventDefault();
        if (!list.hidden && active >= 0 && shownOpts[active]) add(shownOpts[active].id);
      } else if (e.key === 'Escape') { closeList(); }
      else if (e.key === 'Backspace' && !input.value && chosen.length) { remove(chosen[chosen.length - 1].id); }
    });
    input.addEventListener('blur', function () { setTimeout(closeList, 150); });
    list.addEventListener('mousedown', function (e) {
      var li = e.target.closest ? e.target.closest('[data-id]') : null;
      if (li) { e.preventDefault(); add(li.getAttribute('data-id')); }
    });
    chipsEl.addEventListener('click', function (e) {
      var b = e.target.closest ? e.target.closest('button[data-id]') : null;
      if (b) remove(b.getAttribute('data-id'));
    });
    root.querySelector('.ms-box').addEventListener('click', function () { input.focus(); });

    self.ids = ids;
    self.setOptions = function (o) {
      options = o;
      chosen.forEach(function (c) { c.label = labelOf(c.id); });
      drawChips();
    };
    self.count = function () { return options.length; };
    self.has = function (id) { return options.some(function (o) { return o.id === id; }); };
    self.set = function (idsIn) {
      chosen = idsIn.filter(self.has).map(function (id) { return {id: id, label: labelOf(id)}; });
      drawChips();
    };
    self.clear = function () { chosen = []; drawChips(); input.value = ''; };
    return self;
  }

  /* ------------------------------------------------------------- year range */

  function drawYears(fromUser) {
    var span = Math.max(1, limHi - limLo);
    var a = (yearLo - limLo) / span * 100, b = (yearHi - limLo) / span * 100;
    els.yfill.style.left = a + '%';
    els.yfill.style.width = Math.max(0, b - a) + '%';
    els.ylo.value = yearLo; els.yhi.value = yearHi;
    els.yfrom.value = yearLo; els.yto.value = yearHi;
  }
  function setYears(lo, hi) {
    lo = Math.round(lo); hi = Math.round(hi);
    if (isNaN(lo)) lo = yearLo;
    if (isNaN(hi)) hi = yearHi;
    lo = Math.min(Math.max(lo, limLo), limHi);
    hi = Math.min(Math.max(hi, limLo), limHi);
    if (lo > hi) { var t = lo; lo = hi; hi = t; }
    yearLo = lo; yearHi = hi;
    drawYears();
  }
  function setLimits(lo, hi) {
    limLo = lo; limHi = hi;
    [els.ylo, els.yhi, els.yfrom, els.yto].forEach(function (e) {
      e.min = lo; e.max = hi;
    });
    setYears(lo, hi);
  }

  /* ----------------------------------------------------------------- loading */

  function ensureLoaded() {
    if (LOADED || LOADING) return;
    LOADING = true;
    if (!LIST) els.results.innerHTML = '<li class="loading">' + esc(s_('f_loading', 'Loading…')) + '</li>';
    var get = function (u) {
      return fetch(u).then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); });
    };
    Promise.all([get(CFG.index), get(CFG.facets)]).then(function (res) {
      var rows = res[0];
      FACETS = res[1];
      FACETS._nameSlug = {};
      Object.keys(FACETS.places).forEach(function (s) { FACETS._nameSlug[FACETS.places[s]] = s; });
      if (WORK) rows = rows.filter(function (it) { return it.slug === WORK; });
      if (KIND === 'documents') {
        if (FIXED_UNIT) rows = rows.filter(function (it) { return it.unit === FIXED_UNIT; });
        else if (LIST) rows = rows.filter(function (it) { var u = FACETS.units[it.unit]; return u && !u.lit; });
      }
      DATA = rows;
      afterLoad();
    }).catch(function (err) {
      LOADING = false;
      els.results.hidden = false;
      els.results.innerHTML = '<li class="loading">' + esc(s_('f_load_error', 'Could not load the index')) + ' (' +
        esc(String(err.message)) + '). If you opened this file directly from disk, ' +
        'run it through a local server instead — browsers block file:// data loads.</li>';
    });
  }

  function hideField(node, hide) { if (node) node.hidden = !!hide; }

  function afterLoad() {
    // names and counts for the two multi-selects, from the rows of this page
    var pc = {}, lc = {}, eras = {}, themes = {}, years = [];
    DATA.forEach(function (it) {
      (it.people || []).forEach(function (s) { pc[s] = (pc[s] || 0) + 1; });
      placesOf(it).forEach(function (s) { lc[s] = (lc[s] || 0) + 1; });
      var e = eraOf(it); if (e) eras[e] = 1;
      (it.themes || []).forEach(function (s) { themes[s] = 1; });
      var y = parseInt(it.year, 10); if (!isNaN(y)) years.push(y);
    });
    var pOpts = Object.keys(pc).map(function (s) {
      var nm = FACETS.people[s] ? FACETS.people[s][LANG === 'de' ? 1 : 0] : s;
      PEOPLE_NAMES[s] = nm;
      return {id: s, label: nm, key: fold(nm), n: pc[s]};
    });
    var lOpts = Object.keys(lc).filter(function (s) { return FACETS.places[s]; }).map(function (s) {
      return {id: s, label: FACETS.places[s], key: fold(FACETS.places[s]), n: lc[s]};
    });
    ms.person.setOptions(pOpts);
    ms.place.setOptions(lOpts);
    // a filter that has one choice is no filter (a holding's page, a small list)
    hideField(ms.person.root, pOpts.length < 2);
    hideField(ms.place.root, lOpts.length < 2);

    narrowSelect(els.era, function (v) { return eras[v]; });
    if (KIND === 'documents') narrowSelect(els.theme, function (v) { return themes[v]; });
    if (FIXED_UNIT && years.length) {
      var lo = Math.min.apply(null, years), hi = Math.max.apply(null, years);
      var keep = (yearLo > limLo || yearHi < limHi) ? [yearLo, yearHi] : null;   // a ?year= already seeded
      setLimits(lo, hi);
      if (keep) setYears(keep[0], keep[1]);
      hideField($('yr'), lo === hi);
    }
    if (FIXED_UNIT && els.theme) {
      Array.prototype.slice.call(els.theme.options).forEach(function (o) {
        if (o.value) o.textContent = o.textContent.replace(/\s*\(\d+\)$/, '');
      });
    }

    seedFromUrl(true);
    LOADED = true; LOADING = false;
    render();
  }

  function narrowSelect(sel, present) {
    if (!sel) return;
    Array.prototype.slice.call(sel.options).forEach(function (o) {
      if (o.value && !present(o.value)) sel.removeChild(o);
    });
    if (sel.options.length < 3 && (FIXED_UNIT || KIND !== 'documents') && sel.parentNode) sel.parentNode.hidden = true;
  }

  /* ------------------------------------------------------------- the address */

  var SEEDED = false;
  function params(qs, name) {
    var out = [];
    qs.getAll(name).forEach(function (v) {
      v.split(',').forEach(function (x) { x = x.trim(); if (x) out.push(x); });
    });
    return out;
  }

  function seedFromUrl(second) {
    var qs;
    try { qs = new URLSearchParams(window.location.search); } catch (e) { return; }
    var open = false;
    if (!second) {
      // the controls the page already has
      ['unit', 'era', 'theme', 'archive', 'type'].forEach(function (k) {
        var v = qs.get(k);
        if (!v || !els[k]) return;
        var ok = Array.prototype.some.call(els[k].options, function (o) { return o.value === v; });
        if (ok) { els[k].value = v; open = true; }
      });
      var qq = qs.get('q');
      if (qq) els.q.value = qq;
      var tm = qs.get('term');
      if (tm && window.GL_HEADS && window.GL_HEADS[tm]) TERM = tm;
      var yr = qs.get('year');
      if (yr && /^\d{3,4}$/.test(yr)) { setYears(+yr, +yr); open = true; }
    } else {
      var pe = params(qs, 'person');
      if (pe.length) { ms.person.set(pe); open = true; }
      var pl = params(qs, 'place').map(function (v) {
        if (ms.place.has(v)) return v;
        var s = FACETS._nameSlug[v];
        if (s) return s;
        // "Wrocław" for the place entered as "Wrocław (Breslau)"
        var hit = Object.keys(FACETS.places).filter(function (k) {
          var n = FACETS.places[k];
          return n.indexOf(v + ' (') === 0 || n.split(' (')[0] === v;
        })[0];
        return hit || '';
      }).filter(Boolean);
      if (pl.length) { ms.place.set(pl); open = true; }
    }
    if (open) setAdvanced(true);
  }

  /* ------------------------------------------------------------ advanced bar */

  function setAdvanced(on, remember) {
    els.adv.hidden = !on;
    els.advToggle.setAttribute('aria-expanded', on ? 'true' : 'false');
    els.advToggle.classList.toggle('is-open', on);
    if (remember) { try { localStorage.setItem('browse.advanced', on ? '1' : '0'); } catch (e) { /* private window */ } }
  }

  function debounce(fn, ms_) { var t; return function () { clearTimeout(t); t = setTimeout(fn, ms_); }; }

  function reset() {
    TERM = '';
    els.q.value = '';
    ['unit', 'archive', 'type', 'era', 'theme'].forEach(function (k) { if (els[k]) els[k].value = ''; });
    ms.person.clear(); ms.place.clear();
    setYears(limLo, limHi);
    els.phrase.checked = false; els.all.checked = true; els.whole.checked = false;
    els.accents.checked = true; els.cs.checked = false;
    els.inOrig.checked = els.inEn.checked = els.inSum.checked = true;
    els.order.value = LIST ? 'az' : 'asc';
    shown = PAGE;
    render();
  }

  /* -------------------------------------------------------------------- init */

  function init() {
    ['q', 'order', 'count', 'results', 'empty', 'reset', 'more', 'unit', 'archive', 'type', 'era', 'theme',
     'adv', 'filters'].forEach(function (k) { els[k] = $(k); });
    els.advToggle = $('adv-toggle');
    els.phrase = $('o-phrase'); els.all = $('o-all'); els.any = $('o-any'); els.whole = $('o-whole');
    els.accents = $('o-accents'); els.cs = $('o-case');
    els.inOrig = $('in-orig'); els.inEn = $('in-en'); els.inSum = $('in-sum');
    els.ylo = $('y-lo'); els.yhi = $('y-hi'); els.yfrom = $('y-from'); els.yto = $('y-to'); els.yfill = $('yr-fill');
    if (!els.q || !els.results) return;
    ms.person = MultiSelect($('ms-person'), 'person');
    ms.place = MultiSelect($('ms-place'), 'place');

    limLo = +CFG.yearMin; limHi = +CFG.yearMax;
    yearLo = limLo; yearHi = limHi;
    drawYears();
    if (LIST) { collectCards(); els.filters.hidden = false; sortCards(els.order.value); }

    // Advanced: closed by default; the reader's last choice is remembered
    var adv = false;
    try { adv = localStorage.getItem('browse.advanced') === '1'; } catch (e) { adv = false; }
    setAdvanced(adv, false);
    els.advToggle.addEventListener('click', function () {
      setAdvanced(els.adv.hidden, true);
      ensureLoaded();
    });

    seedFromUrl(false);

    // On a page that lists the documents at once, load now; on a list page the
    // index waits for the first touch of the bar.
    var touch = function () { ensureLoaded(); };
    if (!LAZY) ensureLoaded();
    else {
      if (els.q.value || filtersActive(readFilters())) { ensureLoaded(); render(); }
      ['focus', 'input', 'change'].forEach(function (ev) { els.filters.addEventListener(ev, touch, true); });
    }

    var rerender = function () { shown = PAGE; render(); };
    els.q.addEventListener('input', debounce(function () { shown = PAGE; render(); }, 160));
    els.order.addEventListener('change', rerender);
    ['unit', 'archive', 'type', 'era', 'theme'].forEach(function (k) {
      if (els[k]) els[k].addEventListener('change', rerender);
    });
    [els.phrase, els.all, els.any, els.whole, els.accents, els.cs, els.inOrig, els.inEn, els.inSum]
      .forEach(function (e) { e.addEventListener('change', rerender); });

    els.ylo.addEventListener('input', function () { setYears(+els.ylo.value, Math.max(+els.ylo.value, yearHi)); rerender(); });
    els.yhi.addEventListener('input', function () { setYears(Math.min(+els.yhi.value, yearLo), +els.yhi.value); rerender(); });
    // two handles on one track: the nearer one moves when the track is pressed
    els.yfrom.addEventListener('change', function () { setYears(+els.yfrom.value, yearHi); rerender(); });
    els.yto.addEventListener('change', function () { setYears(yearLo, +els.yto.value); rerender(); });

    els.more.addEventListener('click', function () { shown += PAGE; paint(); });
    els.reset.addEventListener('click', reset);
    els.filters.addEventListener('submit', function (e) { e.preventDefault(); });

    els.count.textContent = WORK ? '' : '…';

    if (WORK) {
      // a result scrolls to its passage on this page and marks it for a moment
      els.results.addEventListener('click', function (e) {
        var a = e.target.closest ? e.target.closest('a.r-jump') : null;
        if (!a) return;
        var id = decodeURIComponent(a.getAttribute('href').slice(1));
        var t = document.getElementById(id);
        if (!t) return;
        e.preventDefault();
        t.scrollIntoView();
        try { history.replaceState(null, '', '#' + encodeURIComponent(id)); } catch (x) { /* file:// */ }
        t.classList.remove('lit-flash'); void t.offsetWidth; t.classList.add('lit-flash');
      });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else { init(); }
})();
