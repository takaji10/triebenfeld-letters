/* The People page's three views (_includes/people.html). The page is the era
   view; this script adds the switch. A-Z and By mentions take every person's
   primary card out of its era section into one flat list (the cards are moved,
   not copied, so their document lists keep working) and hide the second cards
   of people who belong to two eras; By era puts them back. */
(function () {
  'use strict';
  var list = document.getElementById('people-list');
  var bar = document.querySelector('.people-views');
  if (!list || !bar) return;
  var dirBar = bar.querySelector('.people-dir');
  var cards = Array.prototype.slice.call(list.querySelectorAll('.person[data-primary]'));
  var slots = cards.map(function (c) {
    var s = document.createElement('span');
    s.hidden = true; s.className = 'people-slot';
    c.parentNode.insertBefore(s, c);
    return s;
  });
  var flat = document.createElement('div');
  flat.className = 'people-flat'; flat.hidden = true;
  list.appendChild(flat);
  var collator = (window.Intl && Intl.Collator) ? new Intl.Collator('de', { sensitivity: 'base' }) : null;
  function byName(a, b) {
    var x = a.getAttribute('data-name'), y = b.getAttribute('data-name');
    return collator ? collator.compare(x, y) : (x < y ? -1 : x > y ? 1 : 0);
  }
  var view = 'era', dir = 'az';

  function toEra() {
    cards.forEach(function (c, i) { slots[i].parentNode.insertBefore(c, slots[i]); });
    flat.hidden = true;
    Array.prototype.forEach.call(list.querySelectorAll('.people-era'), function (s) { s.hidden = false; });
  }
  function toFlat() {
    var sorted = cards.slice().sort(function (a, b) {
      if (view === 'mentions') {
        var r = (+b.getAttribute('data-count')) - (+a.getAttribute('data-count'));
        return r === 0 ? byName(a, b) : r;
      }
      var n = byName(a, b);
      return dir === 'za' ? -n : n;
    });
    var frag = document.createDocumentFragment();
    sorted.forEach(function (c) { frag.appendChild(c); });
    flat.appendChild(frag);
    flat.hidden = false;
    Array.prototype.forEach.call(list.querySelectorAll('.people-era'), function (s) { s.hidden = true; });
  }
  function render() {
    list.setAttribute('data-view', view);
    if (view === 'era') toEra(); else toFlat();
    dirBar.hidden = view !== 'az';
    Array.prototype.forEach.call(bar.querySelectorAll('[data-view]'), function (b) {
      var on = b.getAttribute('data-view') === view;
      b.classList.toggle('is-on', on); b.setAttribute('aria-pressed', on);
    });
    Array.prototype.forEach.call(dirBar.querySelectorAll('[data-dir]'), function (b) {
      var on = b.getAttribute('data-dir') === dir;
      b.classList.toggle('is-on', on); b.setAttribute('aria-pressed', on);
    });
  }
  bar.hidden = false;
  bar.addEventListener('click', function (e) {
    var b = e.target.closest('button');
    if (!b) return;
    if (b.hasAttribute('data-view')) view = b.getAttribute('data-view');
    else if (b.hasAttribute('data-dir')) dir = b.getAttribute('data-dir');
    else return;
    render();
  });

  // Arriving at /people/#slug: show the card (its era's "others" may be
  // folded) and its document list opens (doc-list.js).
  function fromHash() {
    var id = decodeURIComponent((location.hash || '').slice(1));
    var el = id && document.getElementById(id);
    if (!el || !list.contains(el)) return;
    for (var n = el.parentNode; n && n !== list; n = n.parentNode) {
      if (n.tagName === 'DETAILS') n.open = true;
    }
    el.scrollIntoView();
  }
  window.addEventListener('hashchange', fromHash);
  fromHash();
})();
