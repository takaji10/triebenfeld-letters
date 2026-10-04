/* The document lists on the People and Places pages (_includes/doc-list.html).
   Each list opens to cards drawn by assets/doc-cards.js, the same card Browse
   uses, in date order or grouped by archival holding. The card data
   (assets/cards.json) is fetched once, the first time any list is opened. */
(function () {
  'use strict';
  var T = window.I18N || {};
  var LANG = window.LANG || 'en';
  var UNITS = window.UNITS || {};
  var ROWS = null, LOADING = null;
  var esc = window.DocCards.esc;

  function load() {
    if (ROWS) return Promise.resolve(ROWS);
    if (!LOADING) {
      LOADING = fetch(window.CARDS_URL)
        .then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); })
        .then(function (rows) {
          ROWS = {};
          rows.forEach(function (it) { ROWS[it.uid] = it; });
          return ROWS;
        });
    }
    return LOADING;
  }

  function entries(list) {
    return Array.prototype.map.call(list.querySelectorAll('.doclist-fallback a'), function (a) {
      return { uid: a.getAttribute('data-uid'), n: +(a.getAttribute('data-n') || 0) };
    });
  }

  function draw(list) {
    var ol = list.querySelector('.doclist-cards');
    var pressed = list.querySelector('.doclist-order [aria-pressed="true"]');
    var order = pressed ? pressed.getAttribute('data-order') : 'chrono';
    var n = {};
    var items = entries(list).map(function (e) { n[e.uid] = e.n; return ROWS[e.uid]; })
      .filter(Boolean);
    var opts = { lang: LANG, t: T, base: window.SITE_BASE, names: window.PEOPLE_NAMES,
                 exclude: list.getAttribute('data-self') };
    var html = '';
    if (order === 'unit') {
      // grouped by holding, in the order the holdings are listed on the
      // Sources page, and in archival order within each
      window.DocCards.sort(items, 'archival');
      var unitOrder = Object.keys(UNITS);
      items.sort(function (a, b) { return unitOrder.indexOf(a.unit) - unitOrder.indexOf(b.unit); });
      var last = null;
      items.forEach(function (it) {
        if (it.unit !== last) {
          var count = items.filter(function (x) { return x.unit === it.unit; }).length;
          html += '<li class="doclist-group">' + esc(UNITS[it.unit] || it.unit) +
                  ' <span>(' + count + ')</span></li>';
          last = it.unit;
        }
        opts.unit = null; opts.mentions = n[it.uid];
        html += window.DocCards.card(it, opts);
      });
    } else {
      window.DocCards.sort(items, 'chrono');
      items.forEach(function (it) {
        opts.unit = UNITS[it.unit] || it.unit; opts.mentions = n[it.uid];
        html += window.DocCards.card(it, opts);
      });
    }
    ol.innerHTML = html;
    ol.hidden = false;
    list.querySelector('.doclist-order').hidden = items.length < 2;
    list.querySelector('.doclist-fallback').hidden = true;
  }

  function open(list) {
    if (list.getAttribute('data-drawn')) return;
    list.setAttribute('data-drawn', '1');
    var ol = list.querySelector('.doclist-cards');
    ol.innerHTML = '<li class="loading">' + esc(T.f_loading || 'Loading the letters…') + '</li>';
    ol.hidden = false;
    load().then(function () { draw(list); }).catch(function () {
      // the numbered links stay: nothing is lost without the cards
      ol.hidden = true;
      list.removeAttribute('data-drawn');
    });
  }

  function init() {
    Array.prototype.forEach.call(document.querySelectorAll('details.doclist'), function (list) {
      list.addEventListener('toggle', function () { if (list.open) open(list); });
      list.querySelector('.doclist-order').addEventListener('click', function (e) {
        var b = e.target.closest('button');
        if (!b) return;
        Array.prototype.forEach.call(this.querySelectorAll('button'), function (x) {
          x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
        });
        draw(list);
      });
    });
    // Arriving from a document's "People" line (/people/#hardenberg): that
    // person's list opens.
    function fromHash() {
      var id = decodeURIComponent((location.hash || '').slice(1));
      var el = id && document.getElementById(id);
      var list = el && el.querySelector('details.doclist');
      if (list) { list.open = true; el.scrollIntoView(); }
    }
    window.addEventListener('hashchange', fromHash);
    fromHash();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
