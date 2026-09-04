/* Language handling.

   The chrome pages exist twice, once under /de/, and their switch is an
   ordinary link between the two. The letter pages exist once and are shared:
   the transcription, the scans and the English translation are the same
   documents whichever language the interface is in, so duplicating 313 pages
   to change a dozen labels would be a poor trade. On those pages the switch
   swaps the labels in place from the dictionary the page carries, and the
   choice is remembered so the rest of the site follows it.

   Everything degrades honestly: with JavaScript off the chrome pages are still
   fully bilingual by URL, and a letter page simply stays in English. */
(function () {
  'use strict';
  var KEY = 'tf-lang';

  function stored() {
    try { return localStorage.getItem(KEY); } catch (e) { return null; }
  }
  function remember(lang) {
    try { localStorage.setItem(KEY, lang); } catch (e) { /* private mode */ }
  }

  // A switch on a chrome page is a link; it only needs to record the choice so
  // that letter pages reached afterwards open in the same language.
  var link = document.querySelector('a.langswitch[data-set-lang]');
  if (link) {
    link.addEventListener('click', function () {
      remember(link.getAttribute('data-set-lang'));
    });
  }

  var btn = document.getElementById('langswitch');
  if (!btn) return;                      // not a shared page - nothing further

  var holder = document.getElementById('i18n-data');
  var DICT = {};
  if (holder) {
    try { DICT = JSON.parse(holder.textContent) || {}; } catch (e) { DICT = {}; }
  }
  if (!DICT.en || !DICT.de) { btn.hidden = true; return; }

  function apply(lang) {
    var t = DICT[lang] || DICT.en;
    document.documentElement.setAttribute('lang', lang);

    document.querySelectorAll('[data-i18n]').forEach(function (el) {
      var v = t[el.getAttribute('data-i18n')];
      if (v != null) el.textContent = v;
    });
    // Attributes, for the few labels that are not text nodes.
    document.querySelectorAll('[data-i18n-title]').forEach(function (el) {
      var v = t[el.getAttribute('data-i18n-title')];
      if (v != null) el.setAttribute('title', v);
    });

    // The summary exists in both languages; show the one asked for, and fall
    // back to whichever is present rather than leaving an empty space.
    var wanted = document.querySelector('.letter-summary[data-summary="' + lang + '"]');
    var any = document.querySelector('.letter-summary');
    document.querySelectorAll('.letter-summary').forEach(function (el) {
      el.hidden = true;
    });
    if (wanted) wanted.hidden = false;
    else if (any) any.hidden = false;

    // The button offers the language you are not in.
    btn.textContent = (lang === 'de') ? DICT.en.name : DICT.de.name;
    btn.setAttribute('title', t.switch_title || '');
    btn.setAttribute('data-lang', lang);

    // The nav on a shared page has to point at the right half of the site.
    document.querySelectorAll('[data-href-en]').forEach(function (el) {
      var href = el.getAttribute(lang === 'de' ? 'data-href-de' : 'data-href-en');
      if (href) el.setAttribute('href', href);
    });
  }

  var current = stored() === 'de' ? 'de' : 'en';
  apply(current);

  btn.addEventListener('click', function () {
    current = (current === 'de') ? 'en' : 'de';
    remember(current);
    apply(current);
  });
})();
