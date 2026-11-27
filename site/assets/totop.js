/* "Back to top" (the editor, 2026-11-27: on every page that scrolls).
   The button in the default layout shows once the reader is more than a screen down
   and takes them back to the top of the page; on a page too short to scroll it never shows. */
(function () {
  'use strict';
  var btn = document.getElementById('to-top');
  if (!btn) return;
  function update() {
    var far = window.scrollY > Math.max(400, window.innerHeight);
    btn.hidden = !far;
  }
  btn.addEventListener('click', function () {
    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' });
    var main = document.getElementById('main');
    if (main) { main.setAttribute('tabindex', '-1'); main.focus({ preventScroll: true }); }
  });
  window.addEventListener('scroll', update, { passive: true });
  window.addEventListener('resize', update);
  update();
})();
