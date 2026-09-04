/* Client-side sorting for the People and Places pages.
   No dependencies: the site is built to run identically offline and on GitHub
   Pages, so everything dynamic is plain JS. Entries carry data-name and
   data-count; sorting just reorders them in the DOM. */
(function () {
  'use strict';
  var wrap = document.querySelector('[data-sortable]');
  var bar = document.querySelector('.sortbar');
  if (!wrap || !bar) return;

  var items = Array.prototype.slice.call(wrap.querySelectorAll('.person'));
  var collator = (window.Intl && Intl.Collator)
    ? new Intl.Collator('de', { sensitivity: 'base' })
    : null;

  function byName(a, b) {
    var x = a.getAttribute('data-name'), y = b.getAttribute('data-name');
    return collator ? collator.compare(x, y) : (x < y ? -1 : x > y ? 1 : 0);
  }

  function apply(key, dir) {
    var sorted = items.slice().sort(function (a, b) {
      var r;
      if (key === 'count') {
        r = (+a.getAttribute('data-count')) - (+b.getAttribute('data-count'));
        if (r === 0) r = byName(a, b);     // stable tiebreak, so equal counts
      } else {                              // stay alphabetical rather than
        r = byName(a, b);                   // in whatever order they arrived
      }
      return dir === 'desc' ? -r : r;
    });
    var frag = document.createDocumentFragment();
    sorted.forEach(function (el) { frag.appendChild(el); });
    wrap.appendChild(frag);
  }

  bar.addEventListener('click', function (e) {
    var btn = e.target;
    while (btn && btn !== bar && btn.tagName !== 'BUTTON') btn = btn.parentNode;
    if (!btn || btn === bar || !btn.getAttribute('data-key')) return;
    var all = bar.querySelectorAll('button');
    for (var i = 0; i < all.length; i++) all[i].setAttribute('aria-pressed', 'false');
    btn.setAttribute('aria-pressed', 'true');
    apply(btn.getAttribute('data-key'), btn.getAttribute('data-dir'));
  });
})();
