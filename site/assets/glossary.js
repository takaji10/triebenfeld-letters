/* The reader's glossary on a document page.

   The build decides which words to mark (pipeline/build/glossary_build.py)
   and the page carries the list in #glossary-hits: [view, page, word, id].
   This wraps each in a span that acts as a button (a real <button> is laid
   out as an inline box: it took the paragraph's first-line indent and could
   not break across lines); a click opens a short definition, below the
   word on a wide screen, as a sheet from the bottom of the screen on a phone.
   The text in the page's HTML is not changed by the build, only here.

   The definitions come from assets/glossary.json, one file for every page,
   so the browser fetches it once. The box speaks the interface language,
   whatever the language of the text it was opened from.

   A switch beside "hide scans" turns the marks off; the choice is remembered
   in this browser (tf-glossary), like the other view preferences. */
(function () {
  'use strict';
  var KEY = 'tf-glossary';
  var me = document.currentScript;
  var holder = document.getElementById('glossary-hits');
  var toggle = document.getElementById('glossary-toggle');
  if (!holder || !me) { if (toggle) toggle.closest('label').hidden = true; return; }

  var HITS = [];
  try { HITS = JSON.parse(holder.textContent) || []; } catch (e) { HITS = []; }
  if (!HITS.length) { if (toggle) toggle.closest('label').hidden = true; return; }

  var DEFS_URL = me.getAttribute('data-defs');
  var PAGE = { en: me.getAttribute('data-page-en'), de: me.getAttribute('data-page-de') };
  var DEFS = null, pending = null;

  function lang() { return document.documentElement.getAttribute('lang') === 'de' ? 'de' : 'en'; }

  // Interface strings travel in the page's own dictionary (#i18n-data).
  var DICT = {};
  try { DICT = JSON.parse(document.getElementById('i18n-data').textContent) || {}; } catch (e) { DICT = {}; }
  var FALLBACK = { gl_more: 'In the glossary', gl_close: 'Close',
                   gl_lang_de: 'German', gl_lang_la: 'Latin', gl_lang_fr: 'French', gl_lang_pl: 'Polish',
                   gl_lang_de_la: 'German, from Latin', gl_lang_de_fr: 'German, from French' };
  function s_(k) { var d = DICT[lang()] || {}; return d[k] || FALLBACK[k] || ''; }

  // ---- find the element each view lives in --------------------------------
  function container(view, page) {
    if (view === 'sen') return document.querySelector('.letter-summary[data-summary="en"]');
    if (view === 'sde') return document.querySelector('.letter-summary[data-summary="de"]');
    var name = { dip: 'diplomatic', rd: 'reading', en: 'translation' }[view];
    var sec = document.querySelector('.ms-page[data-page="' + page + '"]');
    return sec && sec.querySelector('.text-view[data-view="' + name + '"]');
  }

  var LETTER = /[\p{L}\p{N}]/u;
  function wrap(root, word, id) {
    var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
      acceptNode: function (n) {
        return n.parentNode.closest('.gl, a, button') ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT;
      }
    });
    for (var n = walker.nextNode(); n; n = walker.nextNode()) {
      var t = n.nodeValue, from = 0, i;
      while ((i = t.indexOf(word, from)) !== -1) {
        var before = t.charAt(i - 1), after = t.charAt(i + word.length);
        if ((before && LETTER.test(before)) || (after && LETTER.test(after))) { from = i + 1; continue; }
        var rest = n.splitText(i);
        rest.splitText(word.length);
        var b = document.createElement('span');
        b.className = 'gl';
        b.setAttribute('role', 'button');
        b.tabIndex = 0;
        b.setAttribute('data-gl', id);
        b.setAttribute('aria-haspopup', 'dialog');
        b.setAttribute('aria-expanded', 'false');
        rest.parentNode.replaceChild(b, rest);
        b.appendChild(rest);
        return true;
      }
    }
    return false;
  }

  HITS.forEach(function (h) {
    var el = container(h[0], h[1]);
    if (el) wrap(el, h[2], h[3]);
  });

  // ---- the box ---------------------------------------------------------------
  var box = document.createElement('div');
  box.className = 'gl-box';
  box.setAttribute('role', 'dialog');
  box.setAttribute('aria-modal', 'false');
  box.setAttribute('aria-labelledby', 'gl-box-h');
  box.hidden = true;
  box.innerHTML = '<button type="button" class="gl-x"></button>' +
    '<p class="gl-h" id="gl-box-h"></p><p class="gl-orig"></p><p class="gl-def"></p>' +
    '<a class="gl-more"></a>';
  document.body.appendChild(box);
  var open = null;

  function defs() {
    if (DEFS) return Promise.resolve(DEFS);
    if (!pending) {
      pending = fetch(DEFS_URL).then(function (r) { return r.json(); })
        .then(function (d) { DEFS = d; return d; });
    }
    return pending;
  }

  function narrow() { return window.matchMedia('(max-width: 40rem)').matches; }

  function place(btn) {
    if (narrow()) { box.style.top = ''; box.style.left = ''; return; }
    var r = btn.getBoundingClientRect();
    var w = box.offsetWidth, h = box.offsetHeight;
    var vw = document.documentElement.clientWidth, vh = window.innerHeight;
    var left = Math.max(16, Math.min(r.left, vw - w - 16));
    var below = r.bottom + 8;
    var top = (below + h > vh - 8 && r.top - h - 8 > 8) ? r.top - h - 8 : below;
    box.style.left = (left + window.scrollX) + 'px';
    box.style.top = (top + window.scrollY) + 'px';
  }

  function close(back) {
    if (!open) return;
    open.setAttribute('aria-expanded', 'false');
    box.hidden = true;
    if (back) open.focus();
    open = null;
  }

  function show(btn) {
    var id = btn.getAttribute('data-gl');
    defs().then(function (d) {
      var e = d[id];
      if (!e) return;
      var L = lang();
      close(false);
      var head = L === 'de' ? e.head_de : e.head_en;
      box.querySelector('.gl-h').textContent = head;
      var orig = '';
      // The English page names the original; the German only when it is not German.
      if (L === 'en' || e.lang !== 'de') {
        orig = s_('gl_lang_' + e.lang);
        if (e.orig && e.orig !== head) orig += ': ' + e.orig;
      }
      box.querySelector('.gl-orig').textContent = orig;
      box.querySelector('.gl-orig').hidden = !orig;
      box.querySelector('.gl-def').textContent = L === 'de' ? e.short_de : e.short_en;
      var more = box.querySelector('.gl-more');
      more.textContent = s_('gl_more') + ' →';
      more.href = PAGE[L] + '#' + id;
      var x = box.querySelector('.gl-x');
      x.setAttribute('aria-label', s_('gl_close'));
      x.textContent = '×';
      box.hidden = false;
      place(btn);
      btn.setAttribute('aria-expanded', 'true');
      open = btn;
      if (narrow()) x.focus();
    });
  }

  document.addEventListener('click', function (ev) {
    var btn = ev.target.closest('.gl');
    if (btn && document.body.classList.contains('gl-off')) return;
    if (btn) {
      if (btn === open) { close(false); return; }
      show(btn);
      return;
    }
    if (ev.target.closest('.gl-x')) { close(true); return; }
    if (open && !ev.target.closest('.gl-box')) close(false);
  });
  document.addEventListener('keydown', function (ev) {
    if (ev.key === 'Escape' && open) { close(true); return; }
    var g = ev.target.closest && ev.target.closest('.gl');
    if (g && (ev.key === 'Enter' || ev.key === ' ')) {
      ev.preventDefault();
      if (g === open) close(false); else show(g);
    }
  });
  window.addEventListener('resize', function () { if (open) place(open); });
  // On a phone the sheet can be swiped down to close, as its handle suggests.
  var y0 = null;
  box.addEventListener('touchstart', function (ev) { y0 = ev.touches[0].clientY; }, { passive: true });
  box.addEventListener('touchmove', function (ev) {
    if (y0 !== null && narrow() && box.scrollTop === 0 && ev.touches[0].clientY - y0 > 60) {
      y0 = null; close(false);
    }
  }, { passive: true });
  // Switching view or language hides the word the box belongs to.
  document.addEventListener('click', function (ev) {
    if (ev.target.closest('.vbtn, #langswitch')) close(false);
  }, true);

  // ---- the switch -------------------------------------------------------------
  function apply(on) {
    document.body.classList.toggle('gl-off', !on);
    document.querySelectorAll('.gl').forEach(function (b) {
      if (on) { b.tabIndex = 0; b.setAttribute('role', 'button'); }
      else { b.removeAttribute('tabindex'); b.removeAttribute('role'); }
    });
    if (!on) close(false);
  }
  var saved = null;
  try { saved = localStorage.getItem(KEY); } catch (e) { saved = null; }
  var on = saved !== '0';               // on unless the reader turned it off
  if (toggle) {
    toggle.checked = on;
    toggle.addEventListener('change', function () {
      apply(toggle.checked);
      try { localStorage.setItem(KEY, toggle.checked ? '1' : '0'); } catch (e) {}
    });
  }
  apply(on);
})();
