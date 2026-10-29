/* The materials' lists: sort the cards A-Z (the default) or by date, and on
   the archival list filter them by archive and by type of material (2026-10-29).

   Each card (.sources > .source) carries data-az (what it sorts under),
   data-date (a year, or empty) and, on the archival list, data-archive. A-Z
   ignores brackets, accents and the Polish stroke (Ł sorts as L), as the
   literature list always has, and reads numbers as numbers (53/4 before
   53/15). A card with no date goes last by date. Ties fall to the other key,
   then to the card's id, so the order is always the same.

   The bar (.source-tools) is hidden in the page until this has run, and
   stays hidden for a list of fewer than two cards. Without the script the
   list keeps the order it was built in. */
(function () {
  'use strict';
  var tools = document.querySelector('.source-tools');
  var list = document.querySelector('.sources');
  if (!tools || !list) return;

  var cards = Array.prototype.filter.call(list.children, function (el) {
    return el.classList.contains('source');
  });
  if (cards.length < 2) return;

  var coll = new Intl.Collator('en', { numeric: true });

  function norm(s) {
    return (s || '').toLowerCase().replace(/[\[\]]/g, '').replace(/\u0142/g, 'l')
      .normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  }
  function num(a, b) { return a === b ? 0 : (a < b ? -1 : 1); }

  var items = cards.map(function (el) {
    var y = parseInt(el.getAttribute('data-date'), 10);
    return {
      el: el,
      az: norm(el.getAttribute('data-az')),
      date: isNaN(y) ? Infinity : y,
      archive: el.getAttribute('data-archive') || '',
      types: (el.getAttribute('data-types') || '').split(' '),
      id: el.id
    };
  });

  var byAz = function (a, b) {
    return coll.compare(a.az, b.az) || num(a.date, b.date) || coll.compare(a.id, b.id);
  };
  var byDate = function (a, b) {
    return num(a.date, b.date) || coll.compare(a.az, b.az) || coll.compare(a.id, b.id);
  };

  var btns = tools.querySelectorAll('[data-sort]');
  var select = tools.querySelector('select[data-filter="archive"]');
  var typeSelect = tools.querySelector('select[data-filter="type"]');
  var count = tools.querySelector('.tools-count');
  var mode = 'az';

  if (select) {
    // the archives' names in the same order as the cards: A-Z, "All" first
    var opts = Array.prototype.slice.call(select.options, 1);
    opts.sort(function (a, b) { return coll.compare(norm(a.value), norm(b.value)); });
    opts.forEach(function (o) { select.appendChild(o); });
  }

  function render() {
    items.sort(mode === 'az' ? byAz : byDate);
    var archive = select ? select.value : '';
    var type = typeSelect ? typeSelect.value : '';
    var shown = 0;
    items.forEach(function (it) {
      var show = (!archive || it.archive === archive) &&
        (!type || it.types.indexOf(type) !== -1);
      it.el.hidden = !show;
      if (show) shown++;
      list.appendChild(it.el);
    });
    btns.forEach(function (b) {
      var on = b.getAttribute('data-sort') === mode;
      b.classList.toggle('is-on', on);
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
    });
    if (count) {
      count.textContent = (count.getAttribute('data-template') || '')
        .replace('%s', shown).replace('%s', items.length);
    }
  }

  btns.forEach(function (b) {
    b.addEventListener('click', function () {
      mode = b.getAttribute('data-sort');
      render();
    });
  });
  if (select) select.addEventListener('change', render);
  if (typeSelect) typeSelect.addEventListener('change', render);

  render();
  tools.hidden = false;
})();
