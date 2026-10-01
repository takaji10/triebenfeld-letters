/* A holding's page: three sections shown one at a time. The choice lives in
   the address (#about, #documents, #prepared) so a tab can be linked to. */
(function () {
  'use strict';
  var TABS = ['about', 'documents', 'prepared'];
  var nav = document.getElementById('unit-tabs');
  if (!nav) return;
  var root = nav.parentNode;
  var lang = document.querySelector('a.langswitch');
  var langHref = lang ? lang.getAttribute('href') : '';

  function current() {
    var h = window.location.hash.replace('#', '');
    return TABS.indexOf(h) === -1 ? 'about' : h;
  }

  function show(tab) {
    Array.prototype.forEach.call(root.querySelectorAll('[data-panel]'), function (p) {
      p.hidden = p.getAttribute('data-panel') !== tab;
    });
    Array.prototype.forEach.call(nav.querySelectorAll('[data-tab]'), function (a) {
      var on = a.getAttribute('data-tab') === tab;
      a.classList.toggle('is-on', on);
      if (on) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current');
    });
    // The other language opens on the same tab.
    if (lang) lang.setAttribute('href', langHref + '#' + tab);
  }

  nav.hidden = false;
  root.classList.add('tabs-on');
  nav.addEventListener('click', function (e) {
    var a = e.target.closest ? e.target.closest('[data-tab]') : null;
    if (!a) return;
    // Change the address without the browser jumping to the section.
    e.preventDefault();
    var tab = a.getAttribute('data-tab');
    try { history.replaceState(null, '', '#' + tab); } catch (err) { window.location.hash = tab; }
    show(tab);
  });
  window.addEventListener('hashchange', function () { show(current()); });
  show(current());
  if (window.location.hash) window.scrollTo(0, 0);
})();
