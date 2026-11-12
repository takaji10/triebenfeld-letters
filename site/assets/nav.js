/* The header's Sources menu (a <details>): close it on a click outside it
   or on Escape, and keep only one such menu open. Without script it still
   opens and closes on its own summary. */
(function () {
  'use strict';
  var drops = document.querySelectorAll('details.nav-drop');
  if (!drops.length) return;
  document.addEventListener('click', function (e) {
    drops.forEach(function (d) {
      if (d.open && !d.contains(e.target)) d.open = false;
    });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    drops.forEach(function (d) {
      if (d.open) { d.open = false; d.querySelector('summary').focus(); }
    });
  });
})();
