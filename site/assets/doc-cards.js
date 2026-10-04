/* The document card, one design for every list of documents on the site.
   Browse draws its results with it, and the People and Places pages draw each
   person's or place's documents with it, so a card looks and reads the same
   wherever it appears. No dependencies.

   DocCards.card(item, opts) -> '<li class="result">...</li>'
     item   a row of assets/search-index.json or assets/cards.json
     opts   lang      'en' | 'de'
            t         interface strings (window.I18N)
            base      the site's base URL (window.SITE_BASE)
            names     {person slug: name}, for the line of people named
            body      HTML for the card's body instead of the summary
                      (Browse passes the matching passage when searching)
            unit      the holding's reference, shown in the card's head
            mentions  how many times the document names the person or place
            exclude   a person slug left out of the line of people named
                      (on that person's own list)
   DocCards.sort(list, 'chrono' | 'archival')  sorts in place, as Browse does */
(function () {
  'use strict';

  function esc(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  function archivalKey(id) {
    var m = /^(\d+)([a-z]*)$/.exec(id) || [0, '0', id];
    return [parseInt(m[1], 10), m[2] || ''];
  }

  function sort(list, order) {
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

  function card(it, opts) {
    opts = opts || {};
    var T = opts.t || {};
    var de = opts.lang === 'de';
    function s_(k, dflt) { return T[k] != null ? T[k] : dflt; }

    var flags = [];
    if (opts.mentions) {
      flags.push('<span class="chip chip-n">' + esc(opts.mentions === 1
        ? s_('card_mention_one', 'named once')
        : s_('card_mentions', 'named %d times').replace('%d', opts.mentions)) + '</span>');
    }
    if (it.type === 'register') flags.push('<span class="chip">' + esc(s_('chip_register', 'register')) + '</span>');
    if (!it.date) flags.push('<span class="chip">' + esc(s_('chip_undated', 'undated')) + '</span>');
    else if (it.source !== 'signature') flags.push('<span class="chip">' + esc(s_('chip_supplied', 'date supplied')) + '</span>');
    if (it.dup) flags.push('<span class="chip">' + esc(s_('chip_duplicate', 'duplicate of')) + ' ' + esc(it.dup) + '</span>');
    if (it.parent) flags.push('<span class="chip">' + esc(s_('chip_part', 'part of')) + ' ' + esc(it.parent) + '</span>');
    if (it.damage) flags.push('<span class="chip warn">' + esc(s_('chip_damaged', 'damaged')) + '</span>');
    if (it.unc) flags.push('<span class="chip">' + it.unc + ' ' + esc(s_('chip_uncertain', 'uncertain')) + '</span>');

    var names = (it.people || []).filter(function (s) { return s !== opts.exclude; })
      .slice(0, 6).map(function (s) {
      return esc((opts.names && opts.names[s]) || s);
    }).join(' · ');

    var corr = '';
    if (it.from || it.to) {
      corr = '<p class="r-corr">' + esc((de && it.from_de) || it.from || '?') +
             ' <span class="c-arrow">&rarr;</span> ' + esc((de && it.to_de) || it.to || '?') + '</p>';
    }

    var body = opts.body;
    if (body == null) {
      var sum = (de && it.summary_de) ? it.summary_de : it.summary;
      body = sum ? '<p class="r-summary">' + esc(sum) + '</p>' : '';
    }

    return '<li class="result">' +
      '<a class="r-head" href="' + esc((opts.base || '') + it.url) + '">' +
        '<span class="r-id">' + esc(it.id) + '</span>' +
        '<span class="r-date">' + esc((de && it.label_de) ? it.label_de : it.label) + '</span>' +
        (it.place ? '<span class="r-place">' + esc(it.place) + '</span>' : '') +
        (opts.unit ? '<span class="r-unit">' + esc(opts.unit) + '</span>' : '') +
      '</a>' +
      corr +
      (flags.length ? '<p class="r-flags">' + flags.join('') + '</p>' : '') +
      body +
      (names ? '<p class="r-people">' + names + '</p>' : '') +
    '</li>';
  }

  window.DocCards = { card: card, sort: sort, esc: esc };
})();
