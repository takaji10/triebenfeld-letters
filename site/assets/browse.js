/* Browse + search. No dependencies, no network beyond the index itself. */
(function () {
  'use strict';
  // Interface strings come from the page (window.I18N, set by the browse
  // include from _data/i18n.yml), so the German list is not a second copy of
  // this file. Falls back to English wording if the page did not set them.
  var T = window.I18N || {};
  var LANG = window.LANG || 'en';
  function s_(k, dflt) { return (T && T[k] != null) ? T[k] : dflt; }

  var DATA = [];
  var els = {};
  var PEOPLE_NAMES = {};

  function $(id) { return document.getElementById(id); }

  function fold(s) {
    // Diacritic-insensitive matching, so "Trabczyn" finds "Trąbczyn".
    return s.toLowerCase()
      .replace(/[ąäàáâ]/g, 'a')
      .replace(/[ęéèê]/g, 'e')
      .replace(/[öóô]/g, 'o')
      .replace(/[üûù]/g, 'u')
      .replace(/[śźż]/g, 's')
      .replace(/[ł]/g, 'l')
      .replace(/[ń]/g, 'n')
      .replace(/ß/g, 'ss')
      .replace(/ſ/g, 's');   // long s
  }

  function esc(s) {
    return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  function snippet(item, needle) {
    var hay = item._fold;
    var i = needle ? hay.indexOf(needle) : -1;
    if (i < 0) return esc(item.text.slice(0, 180)) + '…';
    var start = Math.max(0, i - 70);
    var end = Math.min(item.text.length, i + needle.length + 110);
    var before = item.text.slice(start, i);
    var hit = item.text.slice(i, i + needle.length);
    var after = item.text.slice(i + needle.length, end);
    return (start > 0 ? '…' : '') + esc(before) +
           '<mark>' + esc(hit) + '</mark>' + esc(after) +
           (end < item.text.length ? '…' : '');
  }

  function matches(item, f) {
    if (f.unit && item.unit !== f.unit) return false;
    if (f.year && item.year !== f.year) return false;
    if (f.person && item.people.indexOf(f.person) === -1) return false;
    if (f.place && item.place !== f.place) return false;
    switch (f.flag) {
      case 'dated':    if (item.source !== 'signature') return false; break;
      case 'supplied': if (item.source !== 'supplied' && item.source !== 'inferred' && item.source !== 'twin') return false; break;
      case 'undated':  if (item.date) return false; break;
      case 'damage':   if (!item.damage) return false; break;
      case 'unc':      if (!item.unc) return false; break;
      case 'dup':      if (!item.dup) return false; break;
    }
    if (f.q && item._fold.indexOf(f.q) === -1) return false;
    return true;
  }

  function archivalKey(id) {
    var m = /^(\d+)([a-z]*)$/.exec(id);
    return [parseInt(m[1], 10), m[2] || ''];
  }

  function sortItems(list, order) {
    return list.sort(function (a, b) {
      if (order === 'archival') {
        // an archival number orders documents only within its own holding
        if (a.unit !== b.unit) return a.unit < b.unit ? -1 : 1;
        var ka = archivalKey(a.id), kb = archivalKey(b.id);
        return ka[0] - kb[0] || (ka[1] < kb[1] ? -1 : ka[1] > kb[1] ? 1 : 0);
      }
      if (!a.date && !b.date) return archivalKey(a.id)[0] - archivalKey(b.id)[0];
      if (!a.date) return 1;
      if (!b.date) return -1;
      return a.date < b.date ? -1 : a.date > b.date ? 1 : 0;
    });
  }

  function render() {
    var f = {
      q: fold(els.q.value.trim()),
      unit: els.unit ? els.unit.value : '',
      year: els.year.value,
      person: els.person.value,
      place: els.place.value,
      flag: els.flag.value
    };
    var hits = DATA.filter(function (it) { return matches(it, f); });
    sortItems(hits, els.order.value);

    els.count.textContent = hits.length === DATA.length
      ? s_('f_showing_all', 'Showing all') + ' ' + hits.length + ' ' +
        s_('fig_documents', 'documents')
      : s_('f_showing', 'Showing') + ' ' + hits.length + ' / ' + DATA.length;
    els.empty.hidden = hits.length > 0;

    var html = hits.map(function (it) {
      var flags = [];
      if (it.type === 'register') flags.push('<span class="chip">' + esc(s_('chip_register','register')) + '</span>');
      if (!it.date) flags.push('<span class="chip">' + esc(s_('chip_undated','undated')) + '</span>');
      else if (it.source !== 'signature') flags.push('<span class="chip">' + esc(s_('chip_supplied','date supplied')) + '</span>');
      if (it.dup) flags.push('<span class="chip">' + esc(s_('chip_duplicate','duplicate of')) + ' ' + esc(it.dup) + '</span>');
      if (it.parent) flags.push('<span class="chip">' + esc(s_('chip_part','part of')) + ' ' + esc(it.parent) + '</span>');
      if (it.damage) flags.push('<span class="chip warn">' + esc(s_('chip_damaged','damaged')) + '</span>');
      if (it.unc) flags.push('<span class="chip">' + it.unc + ' ' + esc(s_('chip_uncertain','uncertain')) + '</span>');

      var names = it.people.slice(0, 6).map(function (s) {
        return esc(PEOPLE_NAMES[s] || s);
      }).join(' · ');

      var corr = '';
      if (it.from || it.to) {
        corr = '<p class="r-corr">' + esc(it.from || '?') +
               ' <span class="c-arrow">&rarr;</span> ' + esc(it.to || '?') + '</p>';
      }

      // With a query, show the matching passage - that is what the reader is
      // looking for. Without one, the summary is far more use than the opening
      // words of the letter, which are almost always the same salutation.
      var sum = (LANG === 'de' && it.summary_de) ? it.summary_de : it.summary;
      var body = (!f.q && sum)
        ? '<p class="r-summary">' + esc(sum) + '</p>'
        : '<p class="r-snip">' + snippet(it, f.q) + '</p>';

      return '<li class="result">' +
        '<a class="r-head" href="' + window.LETTER_BASE + encodeURIComponent(it.unit) + '/' + encodeURIComponent(it.id) + '/">' +
          '<span class="r-id">' + esc(it.id) + '</span>' +
          '<span class="r-date">' + esc(it.label) + '</span>' +
          (it.place ? '<span class="r-place">' + esc(it.place) + '</span>' : '') +
        '</a>' +
        corr +
        (flags.length ? '<p class="r-flags">' + flags.join('') + '</p>' : '') +
        body +
        (names ? '<p class="r-people">' + names + '</p>' : '') +
      '</li>';
    }).join('');

    els.results.innerHTML = html;
  }

  function debounce(fn, ms) {
    var t; return function () { clearTimeout(t); t = setTimeout(fn, ms); };
  }

  function init() {
    ['q', 'unit', 'year', 'person', 'place', 'flag', 'order', 'count', 'results', 'empty', 'reset']
      .forEach(function (k) { els[k] = $(k); });

    // The timeline links here with ?year=, and a holding's page with ?unit=.
    // Seed the controls from the query string so those links actually arrive
    // somewhere; a value the select does not offer is ignored rather than
    // silently filtering everything away.
    try {
      var qs = new URLSearchParams(window.location.search);
      ['unit', 'year'].forEach(function (k) {
        var v = qs.get(k);
        if (!v || !els[k]) return;
        var ok = Array.prototype.some.call(els[k].options, function (o) { return o.value === v; });
        if (ok) els[k].value = v;
      });
    } catch (e) { /* older browser: filters just start empty */ }

    Array.prototype.forEach.call(document.querySelectorAll('#person option'), function (o) {
      if (o.value) PEOPLE_NAMES[o.value] = o.textContent.replace(/\s*\(\d+\)$/, '');
    });

    els.results.innerHTML = '<li class="loading">' + esc(s_('f_loading','Loading the letters…')) + '</li>';

    fetch(window.SEARCH_INDEX_URL)
      .then(function (r) {
        if (!r.ok) throw new Error('HTTP ' + r.status);
        return r.json();
      })
      .then(function (rows) {
        DATA = rows;
        DATA.forEach(function (it) { it._fold = fold(it.text); });
        render();
      })
      .catch(function (err) {
        els.results.innerHTML = '<li class="loading">' + esc(s_('f_load_error','Could not load the index')) + ' (' +
          esc(String(err.message)) + '). If you opened this file directly from disk, ' +
          'run it through a local server instead — browsers block file:// data loads.</li>';
      });

    els.q.addEventListener('input', debounce(render, 120));
    ['unit', 'year', 'person', 'place', 'flag', 'order'].forEach(function (k) {
      if (els[k]) els[k].addEventListener('change', render);
    });
    els.reset.addEventListener('click', function () {
      els.q.value = ''; els.year.value = ''; els.person.value = '';
      els.place.value = ''; els.flag.value = ''; els.order.value = 'chrono';
      if (els.unit) els.unit.value = '';
      render();
    });
    $('filters').addEventListener('submit', function (e) { e.preventDefault(); });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else { init(); }
})();
