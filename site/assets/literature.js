/* A work of the literature or an item of the press: which text is shown, the
   contents panel, "Go to page", the page marks.

   The page holds both texts of every passage (_layouts/literature.html). The
   buttons show the English, the original, or (from 80rem, the literature's
   works only) the two side by side, as data-lit-view on the body ("en",
   "orig", "both"); the English first (editor, 2026-10-19); side by side by
   default on a wide screen (editor, 2026-11-24). The choice is remembered
   between works. Without this script both texts stay shown, one under the
   other, and the contents panel is an open list. */
(function () {
  'use strict';
  var KEY = 'tf-lit-view2';
  var btns = document.querySelectorAll('.lit-viewbar .vbtn[data-show]');
  if (!btns.length) return;
  var hasBoth = !!document.querySelector('.lit-viewbar .vbtn[data-show="both"]');
  var wide = window.matchMedia('(min-width: 80rem)');
  var current = null;

  function effective(view) { return view === 'both' && !wide.matches ? 'en' : view; }

  function apply(view, save) {
    current = view;
    var eff = effective(view);
    btns.forEach(function (b) {
      var on = b.getAttribute('data-show') === eff;
      b.classList.toggle('is-on', on);
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
    });
    document.body.setAttribute('data-lit-view', view);
    if (save) { try { localStorage.setItem(KEY, view); } catch (e) { /* private mode */ } }
  }

  btns.forEach(function (b) {
    b.addEventListener('click', function () { apply(b.getAttribute('data-show'), true); keepPlace(); });
  });

  var saved;
  try { saved = localStorage.getItem(KEY); } catch (e) { saved = null; }
  var ok = hasBoth ? ['en', 'orig', 'both'] : ['en', 'orig'];
  apply(ok.indexOf(saved) >= 0 ? saved : (hasBoth && wide.matches ? 'both' : 'en'), false);
  var onChange = function () { apply(current, false); };
  if (wide.addEventListener) wide.addEventListener('change', onChange); else wide.addListener(onChange);

  /* The layout shifts when the view changes; stay on the passage that was linked. */
  function keepPlace() {
    var h = location.hash && document.getElementById(decodeURIComponent(location.hash.slice(1)));
    if (h) h.scrollIntoView();
  }
  window.addEventListener('load', keepPlace);
})();

/* The Related column (literature/links.yml): the button in the viewbar hides
   it page-wide and remembers the choice; without this script it shows. */
(function () {
  'use strict';
  var KEY = 'tf-lit-related';
  var tgl = document.querySelector('[data-related-toggle]');
  if (!tgl) return;

  function apply(on) {
    document.body.setAttribute('data-related', on ? 'on' : 'off');
    tgl.classList.toggle('is-on', on);
    tgl.setAttribute('aria-pressed', on ? 'true' : 'false');
    try { localStorage.setItem(KEY, on ? 'on' : 'off'); } catch (e) { /* private mode */ }
  }

  tgl.addEventListener('click', function () {
    apply(document.body.getAttribute('data-related') === 'off');
  });

  var saved;
  try { saved = localStorage.getItem(KEY); } catch (e) { saved = null; }
  apply(saved !== 'off');
})();

/* The contents panel: a drawer on a phone (closed, closing again when a link
   is followed), an open sticky column from 64rem; "Go to page" finds a
   printed page by its number (a range such as 202-203 answers to either). */
(function () {
  'use strict';
  var toc = document.querySelector('.lit-toc');
  if (!toc) return;
  var wide = window.matchMedia('(min-width: 64rem)');
  function sync() { toc.open = wide.matches; }
  sync();
  if (wide.addEventListener) wide.addEventListener('change', sync); else wide.addListener(sync);
  toc.addEventListener('click', function (e) {
    if (!wide.matches && e.target.closest && e.target.closest('li a')) toc.open = false;
  });

  var form = toc.querySelector('.lit-goto');
  if (!form) return;
  var input = form.querySelector('input');
  var msg = form.querySelector('.lit-goto-msg');
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var v = input.value.trim().toLowerCase().replace(/^(p|pp|s|str)\.?\s*/, '');
    var found = null, n = /^\d+$/.test(v) ? parseInt(v, 10) : null;
    var secs = document.querySelectorAll('.lit-passage[data-page]');
    for (var i = 0; i < secs.length && !found; i++) {
      if (secs[i].getAttribute('data-page').toLowerCase() === v) found = secs[i];
    }
    for (var j = 0; j < secs.length && !found && n !== null; j++) {
      var m = /^(\d+)[-–](\d+)$/.exec(secs[j].getAttribute('data-page'));
      if (m && n >= +m[1] && n <= +m[2]) found = secs[j];
    }
    if (!found) { msg.textContent = v ? form.getAttribute('data-none') : ''; return; }
    msg.textContent = '';
    location.hash = '#' + found.id;
    found.scrollIntoView();
    if (!wide.matches) toc.open = false;
  });
  input.addEventListener('input', function () { msg.textContent = ''; });
})();

/* A page mark of a newspaper item stands in both texts (id on the original's);
   a link to #p720 while the English is shown finds the English one. */
(function () {
  'use strict';
  function go() {
    var id = location.hash && decodeURIComponent(location.hash.slice(1));
    var t = id && document.getElementById(id);
    if (!t || t.offsetParent !== null || !t.classList.contains('pg')) return;
    var all = document.querySelectorAll('.pg[data-page="' + t.getAttribute('data-page') + '"]');
    for (var i = 0; i < all.length; i++) if (all[i].offsetParent !== null) { all[i].scrollIntoView(); return; }
  }
  window.addEventListener('hashchange', go);
  window.addEventListener('load', go);
})();
