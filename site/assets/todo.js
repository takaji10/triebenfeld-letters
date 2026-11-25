/* The to-do page (docs/TODO_PAGE_PLAN.md): filters, answers kept in this browser,
   export and import of the answers as a file the editor hands over. */
(function () {
  'use strict';
  var KEY = 'todo.answers.v1';
  var cards = Array.prototype.slice.call(document.querySelectorAll('.todo-card'));
  var groups = Array.prototype.slice.call(document.querySelectorAll('.todo-group'));
  var $ = function (id) { return document.getElementById(id); };
  var ans = {};
  try { ans = JSON.parse(localStorage.getItem(KEY) || '{}') || {}; } catch (e) { ans = {}; }

  function save() { try { localStorage.setItem(KEY, JSON.stringify(ans)); } catch (e) { /* private window */ } }
  function answered(id) { return !!(ans[id] && ans[id].v); }

  function paint(card) {
    var a = ans[card.dataset.id] || {};
    card.classList.toggle('done', !!a.v);
    Array.prototype.forEach.call(card.querySelectorAll('.todo-answer button'), function (b) {
      b.classList.toggle('on', b.dataset.v === a.v);
    });
    var other = card.querySelector('.todo-other');
    other.hidden = a.v !== '__other__';
    other.value = a.other || '';
    card.querySelector('.todo-note').value = a.note || '';
    card.querySelector('.todo-stale').hidden = !(a.v && a.h && a.h !== card.dataset.h);
  }

  function setAns(card, patch) {
    var id = card.dataset.id, a = ans[id] || {};
    Object.keys(patch).forEach(function (k) { a[k] = patch[k]; });
    a.h = card.dataset.h; a.title = card.dataset.title; a.t = new Date().toISOString();
    if (!a.v && !a.note) delete ans[id]; else ans[id] = a;
    save(); paint(card); filter(true);
  }

  cards.forEach(function (card) {
    paint(card);
    card.querySelector('.todo-answer').addEventListener('click', function (e) {
      var b = e.target.closest ? e.target.closest('button') : null;
      if (!b) return;
      var cur = (ans[card.dataset.id] || {}).v;
      setAns(card, {v: cur === b.dataset.v ? '' : b.dataset.v});
      if (b.dataset.v === '__other__') card.querySelector('.todo-other').focus();
    });
    card.querySelector('.todo-other').addEventListener('input', function (e) { setAns(card, {other: e.target.value}); });
    card.querySelector('.todo-note').addEventListener('input', function (e) { setAns(card, {note: e.target.value}); });
  });

  function filter(keepScroll) {
    var q = $('td-q').value.trim().toLowerCase(), kind = $('td-kind').value, g = $('td-group').value;
    var shown = 0, done = 0, total = 0;
    cards.forEach(function (c) {
      var k = c.dataset.kind;
      var okKind = kind === 'all' || kind === k || (kind === 'you' && (k === 'question' || k === 'decision' || k === 'task'));
      var okGroup = !g || c.parentNode.dataset.group === g;
      var okQ = !q || c.textContent.toLowerCase().indexOf(q) >= 0;
      var ok = okKind && okGroup && okQ;
      c.hidden = !ok;
      if (ok) { shown++; total++; if (answered(c.dataset.id)) done++; }
    });
    groups.forEach(function (s) {
      s.hidden = !Array.prototype.some.call(s.querySelectorAll('.todo-card'), function (c) { return !c.hidden; });
    });
    $('td-count').textContent = shown + ' shown, ' + done + ' answered' +
      (Object.keys(ans).length ? ' (' + Object.keys(ans).length + ' in all, not yet handed in)' : '');
    $('td-empty').hidden = shown > 0;
  }

  ['td-q', 'td-kind', 'td-group'].forEach(function (id) { $(id).addEventListener('input', function () { filter(); }); });

  $('td-export').addEventListener('click', function () {
    var out = {exported: new Date().toISOString(), answers: ans};
    var blob = new Blob([JSON.stringify(out, null, 1)], {type: 'application/json'});
    var a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'todo_answers_' + new Date().toISOString().slice(0, 10) + '.json';
    document.body.appendChild(a); a.click(); a.remove();
  });
  $('td-import').addEventListener('change', function (e) {
    var f = e.target.files[0]; if (!f) return;
    var r = new FileReader();
    r.onload = function () {
      try {
        var d = JSON.parse(r.result), n = 0;
        Object.keys(d.answers || {}).forEach(function (id) { ans[id] = d.answers[id]; n++; });
        save(); cards.forEach(paint); filter();
        $('td-count').textContent = n + ' answers read from the file.';
      } catch (x) { $('td-count').textContent = 'That file could not be read.'; }
    };
    r.readAsText(f); e.target.value = '';
  });
  $('td-clear').addEventListener('click', function () {
    if (!Object.keys(ans).length || !window.confirm('Clear every answer kept in this browser? Export first if you have not handed them in.')) return;
    ans = {}; save(); cards.forEach(paint); filter();
  });
  filter();
})();
