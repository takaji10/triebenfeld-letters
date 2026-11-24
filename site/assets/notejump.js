/* Footnote jumps: a click on a footnote reference or its back-link scrolls
   the target to the middle of the window and flashes it, so the eye finds
   it. The hash is kept (history.replaceState) so back/forward still work. */
(function () {
  var calm = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href^="#fn"]');
    if (!a || e.defaultPrevented || e.button || e.metaKey || e.ctrlKey || e.shiftKey) return;
    var id;
    try { id = decodeURIComponent(a.getAttribute('href').slice(1)); } catch (x) { return; }
    if (!/^fn(ref)?:/.test(id)) return;
    var t = document.getElementById(id);
    if (!t) return;
    e.preventDefault();
    t.scrollIntoView({ block: 'center', behavior: calm ? 'auto' : 'smooth' });
    try { history.replaceState(null, '', '#' + id); } catch (x) {}
    t.classList.remove('nj-flash');
    void t.offsetWidth;
    t.classList.add('nj-flash');
    setTimeout(function () { t.classList.remove('nj-flash'); }, 1700);
  });
})();
