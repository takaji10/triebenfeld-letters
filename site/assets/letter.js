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

  // A label in whichever language is already stored; the language switch
  // re-labels anything carrying data-i18n afterwards.
  function label(key, fallback) {
    var el = document.getElementById('i18n-data');
    if (!el) return fallback;
    try {
      var dict = JSON.parse(el.textContent) || {};
      var lang = 'en';
      try { if (localStorage.getItem('tf-lang') === 'de') lang = 'de'; } catch (e) {}
      return (dict[lang] && dict[lang][key]) || fallback;
    } catch (e) { return fallback; }
  }
  function untranslatedText() {
    return label('page_untranslated', 'This page has not been translated yet.');
  }

  // The translator returns each page in the paragraphs of the German reading
  // text, separated by a blank line. They used to be poured into one <p>, where
  // the breaks vanished and a page read as a single slab.
  var OFFICE = '[Written by the receiving office:]';
  function fillTranslation(el, en) {
    var box = el;
    en.split(/\n\s*\n/).forEach(function (para) {
      para = para.replace(/^\s+|\s+$/g, '');
      if (!para) return;
      if (para === OFFICE) {
        // What the receiving office wrote on the letter is set apart under
        // the same label as in the German views.
        box = document.createElement('div');
        box.className = 'sideways office-note';
        var note = document.createElement('div');
        note.className = 'sideways-note';
        note.setAttribute('data-i18n', 'office_note');
        note.textContent = label('office_note', 'Written by the receiving office');
        box.appendChild(note);
        el.appendChild(box);
        return;
      }
      var p = document.createElement('p');
      p.textContent = para;
      box.appendChild(p);
    });
    // A paragraph that began on the previous page starts again here; the
    // reading view marks that, and the English follows it.
    var reading = el.parentNode && el.parentNode.querySelector('.text-view[data-view="reading"] > p');
    var first = el.querySelector('p');
    if (reading && first && reading.classList.contains('runs-on')) first.classList.add('runs-on');
  }

  // ---- fill the translation panes, one per manuscript page ----------------
  var holder = document.getElementById('translation-data');
  var byPage = {};
  if (holder) {
    try {
      (JSON.parse(holder.textContent) || []).forEach(function (seg) {
        if (seg && seg.page != null && seg.en) byPage[String(seg.page)] = seg;
      });
    } catch (e) { /* malformed translation file - leave panes empty */ }
  }
  document.querySelectorAll('.text-view[data-view="translation"]').forEach(function (el) {
    var seg = byPage[el.getAttribute('data-seg')];
    // A tabulated document's English arrives as a built table, from our own
    // data file.
    if (seg && seg.html) { el.innerHTML = seg.html; return; }
    if (seg) { fillTranslation(el, seg.en); return; }
    var p = document.createElement('p');
    p.className = 'muted';
    // Marked so the language switch picks it up like any other label; the
    // initial wording follows whichever language is already stored.
    p.setAttribute('data-i18n', 'page_untranslated');
    p.textContent = untranslatedText();
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
