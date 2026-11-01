/* A work of the literature: which text is shown.

   The page holds both texts of every passage (_layouts/literature.html). The
   buttons show one, the English or the original, as the views of a document
   do (letter.js); the English first (editor, 2026-10-19). The choice is
   remembered between works. Without this script both texts stay shown. */
(function () {
  'use strict';
  var KEY = 'tf-lit-view';
  var VIEWS = ['en', 'orig'];

  var btns = document.querySelectorAll('.lit-viewbar .vbtn');
  if (!btns.length) return;

  function apply(view) {
    document.querySelectorAll('.lit-viewbar .viewhint').forEach(function (el) {
      el.hidden = el.getAttribute('data-hint') !== view;
    });
    btns.forEach(function (b) {
      var on = b.getAttribute('data-show') === view;
      b.classList.toggle('is-on', on);
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
    });
    document.body.setAttribute('data-lit-view', view);
    try { localStorage.setItem(KEY, view); } catch (e) { /* private mode */ }
  }

  btns.forEach(function (b) {
    b.addEventListener('click', function () { apply(b.getAttribute('data-show')); });
  });

  var saved;
  try { saved = localStorage.getItem(KEY); } catch (e) { saved = null; }
  apply(VIEWS.indexOf(saved) >= 0 ? saved : 'en');
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
