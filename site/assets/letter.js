/* Letter page behaviour.

   Layout is two panes per manuscript page: the scan on the left, its own text
   on the right. The tabs switch which text is shown (diplomatic / reading /
   English); the scan stays put, so you can collate against any of them.

   Both the chosen tab and the hide-scans preference are remembered between
   letters. */
(function () {
  // where this script was loaded from: the editor loads beside it (?edit)
  var SELF = (document.currentScript && document.currentScript.src) || '';
  'use strict';
  var VIEW_KEY = 'tf-view';
  // The summary: clamped to a few lines, with a button for the rest. The button
  // stays hidden when the visible summary fits, and the check runs again when the
  // language changes (the two summaries differ in length).
  (function () {
    var btn = document.querySelector('.summary-more');
    var sums = document.querySelectorAll('.letter-summary');
    if (!btn || !sums.length) return;
    var open = false;
    function fit() {
      var cur = document.querySelector('.letter-summary:not([hidden])');
      sums.forEach(function (s) { s.classList.toggle('is-clamped', !open); });
      btn.hidden = true;
      if (!cur) return;
      if (open) { btn.hidden = false; return; }
      btn.hidden = cur.scrollHeight <= cur.clientHeight + 2;
    }
    function label() {
      btn.querySelector('.sm-more').hidden = open;
      btn.querySelector('.sm-less').hidden = !open;
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    }
    btn.addEventListener('click', function () { open = !open; label(); fit(); });
    document.addEventListener('click', function (ev) {
      if (ev.target.closest('#langswitch')) setTimeout(function () { label(); fit(); }, 50);
    });
    window.addEventListener('load', fit);
    fit();
  })();

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
  // The edition's own label lines in the English, one paragraph each. A label
  // opens a box of its kind, which holds what follows until the next label or
  // the end marker; the end marker itself is not shown (2026-11-22: a set-apart
  // block in mid-page, such as the notes in the margin of Nr. 421's petition,
  // used to swallow the rest of the page).
  var KINDS = {
    '[Written by the receiving office:]': ['office_note', 'office-note', 'Written by the receiving office'],
    '[Written in the margin:]': ['margin_note', 'margin-note', 'Written in the margin'],
    '[Written in another hand:]': ['hand_note', 'hand-note', 'Written in another hand']
  };
  var CONTINUES = '[The document continues:]';
  function fillTranslation(el, en) {
    var box = el;
    en.split(/\n\s*\n/).forEach(function (para) {
      para = para.replace(/^\s+|\s+$/g, '');
      if (!para) return;
      if (para === CONTINUES) { box = el; return; }
      var kind = KINDS[para];
      if (kind) {
        // What the receiving office wrote on the letter, a note in the margin,
        // or a second voice in another hand, set apart under the same label as
        // in the other views.
        box = document.createElement('div');
        box.className = 'sideways ' + kind[1];
        var note = document.createElement('div');
        note.className = 'sideways-note';
        note.setAttribute('data-i18n', kind[0]);
        note.textContent = label(kind[0], kind[2]);
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
  // The editor's layout of a page (docs/ENGLISH_EDITOR_PLAN.md): paragraphs with
  // their indentation, alignment, italic runs and line breaks, and the voices in
  // their boxes. Built from DOM nodes, never as HTML. Exposed for the editor.
  function layoutPara(p) {
    var el = document.createElement('p');
    if (p.i) el.className = 'indent-' + p.i;
    if (p.a === 'c' || p.a === 'r') el.className = (el.className ? el.className + ' ' : '') +
                                                     (p.a === 'c' ? 'align-c' : 'align-r');
    // A paragraph broken into lines (Shift+Enter) is a block - a dateline, an
    // address, a signature - not prose: no first-line indent (the editor,
    // 2026-11-23: "Vienna, the 25th of October // 1814.").
    if ((p.r || []).some(function (run) { return String(run[0]).indexOf('\n') >= 0; }))
      el.className = (el.className ? el.className + ' ' : '') + 'lines';
    (p.r || []).forEach(function (run) {
      var parts = String(run[0]).split('\n');
      parts.forEach(function (t, k) {
        if (k) el.appendChild(document.createElement('br'));
        if (!t) return;
        var node = document.createTextNode(t);
        if (run[1] === 'i') { var em = document.createElement('em'); em.appendChild(node); node = em; }
        el.appendChild(node);
      });
    });
    return el;
  }
  function boxFor(kind) {
    var k = { office: KINDS['[Written by the receiving office:]'],
              margin: KINDS['[Written in the margin:]'],
              hand: KINDS['[Written in another hand:]'] }[kind];
    var box = document.createElement('div');
    box.className = 'sideways ' + k[1];
    var note = document.createElement('div');
    note.className = 'sideways-note';
    note.setAttribute('data-i18n', k[0]);
    note.textContent = label(k[0], k[2]);
    box.appendChild(note);
    return box;
  }
  function fillLayout(el, layout) {
    (layout || []).forEach(function (item) {
      if (item.p) { el.appendChild(layoutPara(item.p)); return; }
      var box = boxFor(item.box);
      (item.ps || []).forEach(function (p) { box.appendChild(layoutPara(p)); });
      el.appendChild(box);
    });
  }
  window.tfLayout = { para: layoutPara, box: boxFor, fill: fillLayout, KINDS: KINDS, CONTINUES: CONTINUES };

  document.querySelectorAll('.text-view[data-view="translation"]').forEach(function (el) {
    var seg = byPage[el.getAttribute('data-seg')];
    // A tabulated document's English arrives as a built table, from our own
    // data file.
    if (seg && seg.html) { el.innerHTML = seg.html; return; }
    if (seg && seg.layout) { fillLayout(el, seg.layout); return; }
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
  if (box && !document.querySelector('.pane-scan')) box.closest('label').hidden = true;
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
  // ---- the layout editor (docs/ENGLISH_EDITOR_PLAN.md): `?edit` in the address ----
  window.tfShowView = apply;
  if (/[?&]edit(?:[=&]|$)/.test(location.search) && SELF) {
    var ed = document.createElement('script');
    ed.src = SELF.replace(/letter\.js(\?.*)?$/, 'layout-editor.js');
    document.body.appendChild(ed);
  }
})();
