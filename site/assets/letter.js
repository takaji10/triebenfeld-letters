/* Letter page behaviour.

   Layout is two panes per manuscript page: the scan on the left, its own text
   on the right. The tabs switch which text is shown (diplomatic / reading /
   English); the scan stays put, so you can collate against any of them.

   Both the chosen tab and the hide-scans preference are remembered between
   letters. */
(function () {
  'use strict';
  var VIEW_KEY = 'tf-view';
  var SCAN_KEY = 'tf-hidescans';
  var VIEWS = ['diplomatic', 'reading', 'translation'];

  var btns = document.querySelectorAll('.vbtn');
  if (!btns.length) return;

  function untranslatedText() {
    var fallback = 'This page has not been translated yet.';
    var el = document.getElementById('i18n-data');
    if (!el) return fallback;
    try {
      var dict = JSON.parse(el.textContent) || {};
      var lang = 'en';
      try { if (localStorage.getItem('tf-lang') === 'de') lang = 'de'; } catch (e) {}
      return (dict[lang] && dict[lang].page_untranslated) || fallback;
    } catch (e) { return fallback; }
  }

  // ---- fill the translation panes, one per manuscript page ----------------
  var holder = document.getElementById('translation-data');
  var byPage = {};
  if (holder) {
    try {
      (JSON.parse(holder.textContent) || []).forEach(function (seg) {
        if (seg && seg.page != null && seg.en) byPage[String(seg.page)] = seg.en;
      });
    } catch (e) { /* malformed translation file - leave panes empty */ }
  }
  document.querySelectorAll('.text-view[data-view="translation"]').forEach(function (el) {
    var en = byPage[el.getAttribute('data-seg')];
    var p = document.createElement('p');
    if (en) {
      p.textContent = en;
    } else {
      p.className = 'muted';
      // Marked so the language switch picks it up like any other label; the
      // initial wording follows whichever language is already stored.
      p.setAttribute('data-i18n', 'page_untranslated');
      p.textContent = untranslatedText();
    }
    el.appendChild(p);
  });

  // ---- which text is showing ----------------------------------------------
  function apply(view) {
    document.querySelectorAll('.text-view').forEach(function (el) {
      el.hidden = el.getAttribute('data-view') !== view;
    });
    document.querySelectorAll('.viewhint').forEach(function (el) {
      el.hidden = el.getAttribute('data-hint') !== view;
    });
    btns.forEach(function (b) {
      var on = b.getAttribute('data-show') === view;
      b.classList.toggle('is-on', on);
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
    });
    document.body.setAttribute('data-view', view);
    try { localStorage.setItem(VIEW_KEY, view); } catch (e) { /* private mode */ }
  }

  btns.forEach(function (b) {
    b.addEventListener('click', function () { apply(b.getAttribute('data-show')); });
  });

  var saved;
  try { saved = localStorage.getItem(VIEW_KEY); } catch (e) { saved = null; }
  apply(VIEWS.indexOf(saved) >= 0 ? saved : 'diplomatic');

  // ---- hiding the scans gives the text the full width ---------------------
  var box = document.getElementById('hidescans');
  if (box) {
    function applyScans(hide) {
      document.body.classList.toggle('no-scans', hide);
      box.checked = hide;
      try { localStorage.setItem(SCAN_KEY, hide ? '1' : '0'); } catch (e) {}
    }
    var savedScans;
    try { savedScans = localStorage.getItem(SCAN_KEY); } catch (e) { savedScans = null; }
    applyScans(savedScans === '1');
    box.addEventListener('change', function () { applyScans(box.checked); });
  }
})();
