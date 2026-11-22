/* The layout editor (docs/ENGLISH_EDITOR_PLAN.md, the editor's word of 2026-11-22).

   Loaded by letter.js when the address carries `?edit`. The editor changes the
   layout of the English - paragraph breaks (Enter / Backspace at a paragraph's
   start), line breaks (Shift+Enter), indentation (Tab / Shift+Tab), alignment,
   italic (Ctrl+I), and the voices set apart in boxes - but never a word: every
   keystroke that would change the text is refused, and after every operation
   the page's letters are compared with the original's, the operation undone if
   they differ. In the German view it marks where the reading text's paragraphs
   begin and which lines are a second voice.

   Nothing leaves the browser until "Export": the work is kept in local storage
   (tf-layout:<pad>, tf-german:<pad>), and Export downloads one file with every
   document's changes, which pipeline/translate/import_layout.py brings home.
   The page model is the layout of pipeline/translate/english_layout.py. */
(function () {
  'use strict';
  var L = window.tfLayout;
  var docEl = document.getElementById('tf-doc');
  if (!L || !docEl) return;
  var PAD = docEl.getAttribute('data-pad');
  var UNIT = docEl.getAttribute('data-unit');
  var LETTER = docEl.getAttribute('data-letter');
  var KEY = 'tf-layout:' + PAD, GKEY = 'tf-german:' + PAD;
  var segs = [];
  try { segs = JSON.parse(document.getElementById('translation-data').textContent) || []; } catch (e) { segs = []; }

  // ---- text identity: the same as english_layout.norm / fingerprint ----------
  var LABEL = {};
  Object.keys(L.KINDS).forEach(function (k) { LABEL[k] = true; });
  LABEL[L.CONTINUES] = true;
  var LN = /[\p{L}\p{N}]/u;
  function norm(text) {
    var keep = text.replace(/\r\n/g, '\n').split('\n\n').map(function (p) { return p.trim(); })
      .filter(function (p) { return !LABEL[p]; }).join(' ');
    keep = keep.normalize('NFC').toLowerCase();
    var out = '';
    for (var ch of keep) if (LN.test(ch)) out += ch;
    return out;
  }
  function fingerprint(text) {
    var h = 0x811c9dc5;
    for (var ch of norm(text)) { h ^= ch.codePointAt(0); h = Math.imul(h, 0x01000193) >>> 0; }
    return ('0000000' + h.toString(16)).slice(-8);
  }

  // ---- the model: a flat list of paragraphs per page ---------------------------
  // {r: [[text, ''|'i'], ...], i: 0-3, a: 'l'|'c'|'r', box: null|kind, nb: starts a new box}
  var KIND_OF = { '[Written by the receiving office:]': 'office', '[Written in the margin:]': 'margin',
                  '[Written in another hand:]': 'hand' };
  function fromEn(en) {
    var out = [], box = null, nb = false;
    en.split(/\n\s*\n/).forEach(function (para) {
      para = para.trim();
      if (!para) return;
      if (KIND_OF[para]) { box = KIND_OF[para]; nb = true; return; }
      if (para === L.CONTINUES) { box = null; return; }
      out.push({ r: [[para.replace(/\s*\n\s*/g, ' '), '']], i: 0, a: 'l', box: box, nb: nb });
      nb = false;
    });
    return out;
  }
  function fromItems(items) {
    var out = [];
    (items || []).forEach(function (it) {
      if (it.p) { out.push(paraIn(it.p, null, false)); return; }
      (it.ps || []).forEach(function (p, k) { out.push(paraIn(p, it.box, k === 0)); });
    });
    return out;
  }
  function paraIn(p, box, nb) {
    return { r: (p.r || []).map(function (x) { return [x[0], x[1] === 'i' ? 'i' : '']; }),
             i: p.i || 0, a: p.a || 'l', box: box, nb: nb };
  }
  function paraOut(p) {
    var o = { r: tidy(p.r) };
    if (p.i) o.i = p.i;
    if (p.a && p.a !== 'l') o.a = p.a;
    return o;
  }
  function toItems(flat) {
    var items = [];
    flat.forEach(function (p, k) {
      if (!p.box) { items.push({ p: paraOut(p) }); return; }
      var last = items[items.length - 1];
      var prev = flat[k - 1];
      if (last && last.box === p.box && prev && prev.box === p.box && !p.nb) last.ps.push(paraOut(p));
      else items.push({ box: p.box, ps: [paraOut(p)] });
    });
    return items;
  }
  function text(p) { return p.r.map(function (x) { return x[0]; }).join(''); }
  function modelText(flat) { return flat.map(text).join('\n\n'); }
  function tidy(runs) {
    var out = [];
    runs.forEach(function (x) {
      if (!x[0]) return;
      var last = out[out.length - 1];
      if (last && last[1] === x[1]) last[0] += x[0]; else out.push([x[0], x[1]]);
    });
    return out.length ? out : [['', '']];
  }
  function cut(runs, off) {          // runs split at a character offset
    var left = [], right = [], n = 0;
    runs.forEach(function (x) {
      var t = x[0];
      if (n + t.length <= off) left.push([t, x[1]]);
      else if (n >= off) right.push([t, x[1]]);
      else { left.push([t.slice(0, off - n), x[1]]); right.push([t.slice(off - n), x[1]]); }
      n += t.length;
    });
    return [left, right];
  }
  function trimEnd(runs) {
    runs = tidy(runs);
    var last = runs[runs.length - 1]; last[0] = last[0].replace(/[ \t]+$/, '');
    return tidy(runs);
  }
  function trimStart(runs) {
    runs = tidy(runs);
    runs[0][0] = runs[0][0].replace(/^[ \t]+/, '');
    return tidy(runs);
  }

  // ---- the operations; each returns false if it does nothing --------------------
  var OPS = {
    split: function (flat, pi, off) {
      var p = flat[pi], t = text(p);
      if (off <= 0 || off >= t.length || !t.slice(0, off).trim() || !t.slice(off).trim()) return false;
      var c = cut(p.r, off);
      var q = { r: trimStart(c[1]), i: p.i, a: p.a, box: p.box, nb: false };
      p.r = trimEnd(c[0]);
      flat.splice(pi + 1, 0, q);
      return { pi: pi + 1, off: 0 };
    },
    join: function (flat, pi) {      // paragraph pi joins the one before it
      if (pi <= 0) return false;
      var a = flat[pi - 1], b = flat[pi];
      var at = text(a).length;
      var sep = /\s$/.test(text(a)) || /^\s/.test(text(b)) ? '' : ' ';
      a.r = tidy(a.r.concat([[sep, '']], b.r));
      flat.splice(pi, 1);
      return { pi: pi - 1, off: at + sep.length };
    },
    lineBreak: function (flat, pi, off) {
      var p = flat[pi], t = text(p);
      if (off <= 0 || off >= t.length) return false;
      var c = cut(p.r, off), left = trimEnd(c[0]);
      var leftLen = left.map(function (x) { return x[0]; }).join('').length;
      p.r = tidy(left.concat([['\n', '']], trimStart(c[1])));
      return { pi: pi, off: leftLen + 1 };
    },
    unbreak: function (flat, pi, off) {   // the line break just before `off` goes
      var p = flat[pi], t = text(p);
      if (t.charAt(off - 1) !== '\n') return false;
      var c = cut(p.r, off - 1), d = cut(c[1], 1);
      p.r = tidy(c[0].concat([[' ', '']], d[1]));
      return { pi: pi, off: off };
    },
    italic: function (flat, pi, s, e) {
      if (e <= s) return false;
      var p = flat[pi], c1 = cut(p.r, s), c2 = cut(c1[1], e - s);
      var all = c2[0].every(function (x) { return x[1] === 'i' || !x[0]; });
      var mid = c2[0].map(function (x) { return [x[0], all ? '' : 'i']; });
      p.r = tidy(c1[0].concat(mid, c2[1]));
      return { pi: pi, off: s, end: e };
    },
    indent: function (flat, pis, d) {
      pis.forEach(function (k) { flat[k].i = Math.max(0, Math.min(3, (flat[k].i || 0) + d)); });
      return true;
    },
    align: function (flat, pis, a) { pis.forEach(function (k) { flat[k].a = a; }); return true; },
    voice: function (flat, pis, kind) {
      pis.forEach(function (k, n) {
        var was = flat[k].box;
        flat[k].box = kind || null;
        if (n === 0) flat[k].nb = !!kind && was !== kind;
        else flat[k].nb = false;
      });
      var after = pis[pis.length - 1] + 1;
      if (flat[after] && flat[after].box && flat[after].box === kind) flat[after].nb = true;
      return true;
    },
    newBox: function (flat, pis) {
      var p = flat[pis[0]];
      if (!p.box) return false;
      p.nb = true;
      return true;
    }
  };

  // ---- the pages ----------------------------------------------------------------
  var pages = {};          // page -> {el, orig, start, flat, undo: []}
  var saved = load(KEY) || { pad: PAD, pages: {} };
  segs.forEach(function (seg) {
    if (!seg || seg.html || !seg.en) return;
    var el = document.querySelector('.text-view[data-view="translation"][data-seg="' + seg.page + '"]');
    if (!el) return;
    var start = seg.layout ? fromItems(seg.layout) : fromEn(seg.en);
    var st = saved.pages[String(seg.page)];
    var flat = clone(start);
    var fp = fingerprint(seg.en);
    if (st && st.fp === fp && Array.isArray(st.items)) flat = fromItems(st.items);
    pages[seg.page] = { el: el, orig: seg.en, fp: fp, start: start, flat: flat, undo: [] };
  });

  function clone(x) { return JSON.parse(JSON.stringify(x)); }
  function load(k) { try { return JSON.parse(localStorage.getItem(k) || 'null'); } catch (e) { return null; } }
  function store(k, v) {
    try {
      if (v === null) localStorage.removeItem(k); else localStorage.setItem(k, JSON.stringify(v));
      return true;
    } catch (e) { say('Could not save in this browser: ' + e.message); return false; }
  }
  function save() {
    var out = { pad: PAD, unit: UNIT, letter: LETTER, saved: new Date().toISOString(), pages: {} };
    Object.keys(pages).forEach(function (k) {
      var pg = pages[k];
      if (JSON.stringify(toItems(pg.flat)) !== JSON.stringify(toItems(pg.start)))
        out.pages[k] = { fp: pg.fp, items: toItems(pg.flat) };
    });
    store(KEY, Object.keys(out.pages).length ? out : null);
    status();
  }

  // ---- rendering an editable page --------------------------------------------
  function render(pg) {
    var el = pg.el;
    while (el.firstChild) el.removeChild(el.firstChild);
    var box = null;
    pg.flat.forEach(function (p, k) {
      var node = L.para(paraOut(p));
      node.setAttribute('data-pi', String(k));
      if (!p.box) { box = null; el.appendChild(node); return; }
      var prev = pg.flat[k - 1];
      if (!box || !prev || prev.box !== p.box || p.nb) {
        box = L.box(p.box);
        box.firstChild.setAttribute('contenteditable', 'false');
        el.appendChild(box);
      }
      box.appendChild(node);
    });
    el.setAttribute('contenteditable', 'true');
    el.setAttribute('spellcheck', 'false');
    el.classList.add('tf-editing');
  }

  // ---- caret <-> (paragraph, offset) -------------------------------------------
  function offsetIn(p, node, off) {
    var n = 0, done = false;
    (function walk(x) {
      if (done) return;
      if (x === node && x.nodeType === 3) { n += off; done = true; return; }
      if (x === node) {
        for (var k = 0; k < off && k < x.childNodes.length; k++) n += lengthOf(x.childNodes[k]);
        done = true; return;
      }
      if (x.nodeType === 3) { n += x.nodeValue.length; return; }
      if (x.nodeName === 'BR') { n += 1; return; }
      for (var c = x.firstChild; c; c = c.nextSibling) { walk(c); if (done) return; }
    })(p);
    return n;
  }
  function lengthOf(x) {
    if (x.nodeType === 3) return x.nodeValue.length;
    if (x.nodeName === 'BR') return 1;
    var n = 0;
    for (var c = x.firstChild; c; c = c.nextSibling) n += lengthOf(c);
    return n;
  }
  function paraOf(node) {
    while (node && !(node.nodeType === 1 && node.hasAttribute && node.hasAttribute('data-pi'))) node = node.parentNode;
    return node;
  }
  function where() {
    var sel = window.getSelection();
    if (!sel || !sel.rangeCount) return null;
    var r = sel.getRangeAt(0);
    var p1 = paraOf(r.startContainer), p2 = paraOf(r.endContainer);
    if (!p1 || !p2) return null;
    var pane = p1.closest('.text-view');
    if (!pane || pane !== p2.closest('.text-view')) return null;
    var page = pane.getAttribute('data-seg');
    return { page: page, pi: +p1.getAttribute('data-pi'), off: offsetIn(p1, r.startContainer, r.startOffset),
             pj: +p2.getAttribute('data-pi'), end: offsetIn(p2, r.endContainer, r.endOffset),
             collapsed: r.collapsed };
  }
  function place(pg, pi, off, end) {
    var p = pg.el.querySelector('[data-pi="' + pi + '"]');
    if (!p) return;
    var sel = window.getSelection(), r = document.createRange();
    function point(o) {
      var n = 0, found = null;
      (function walk(x) {
        if (found) return;
        if (x.nodeType === 3) {
          if (o <= n + x.nodeValue.length) { found = [x, o - n]; return; }
          n += x.nodeValue.length; return;
        }
        if (x.nodeName === 'BR') {
          if (o === n) { found = [x.parentNode, Array.prototype.indexOf.call(x.parentNode.childNodes, x)]; return; }
          n += 1;
          if (o === n) { found = [x.parentNode, Array.prototype.indexOf.call(x.parentNode.childNodes, x) + 1]; }
          return;
        }
        for (var c = x.firstChild; c; c = c.nextSibling) { walk(c); if (found) return; }
      })(p);
      return found || [p, p.childNodes.length];
    }
    var a = point(off), b = point(end == null ? off : end);
    r.setStart(a[0], a[1]); r.setEnd(b[0], b[1]);
    sel.removeAllRanges(); sel.addRange(r);
  }

  // ---- doing an operation safely ----------------------------------------------
  function run(pg, fn) {
    var before = clone(pg.flat);
    var res = fn(pg.flat);
    if (!res) { pg.flat = before; return; }
    if (norm(modelText(pg.flat)) !== norm(pg.orig)) {
      pg.flat = before;
      say('That would have changed the words - undone.');
      render(pg);
      return;
    }
    pg.undo.push(before);
    if (pg.undo.length > 200) pg.undo.shift();
    render(pg);
    if (res && res.pi != null) place(pg, res.pi, res.off, res.end);
    save();
  }
  function rangeOf(w) {
    var a = Math.min(w.pi, w.pj), b = Math.max(w.pi, w.pj), out = [];
    for (var k = a; k <= b; k++) out.push(k);
    return out;
  }

  Object.keys(pages).forEach(function (k) {
    var pg = pages[k];
    render(pg);
    pg.el.addEventListener('beforeinput', function (e) {
      e.preventDefault();
      var w = where();
      if (!w || String(w.page) !== String(k)) return;
      var t = e.inputType;
      if (t === 'insertParagraph') run(pg, function (f) { return w.collapsed && OPS.split(f, w.pi, w.off); });
      else if (t === 'insertLineBreak') run(pg, function (f) { return w.collapsed && OPS.lineBreak(f, w.pi, w.off); });
      else if (t === 'deleteContentBackward') run(pg, function (f) {
        if (!w.collapsed) return false;
        return w.off === 0 ? OPS.join(f, w.pi) : OPS.unbreak(f, w.pi, w.off);
      });
      else if (t === 'deleteContentForward') run(pg, function (f) {
        if (!w.collapsed) return false;
        var len = text(f[w.pi]).length;
        return w.off >= len ? OPS.join(f, w.pi + 1) : OPS.unbreak(f, w.pi, w.off + 1);
      });
      else if (t === 'formatItalic') italic(pg, w);
    });
    // a change that got past beforeinput (an input method): put the model back
    pg.el.addEventListener('input', function () { render(pg); say('Only the layout can be changed here.'); });
    ['paste', 'drop', 'cut'].forEach(function (ev) {
      pg.el.addEventListener(ev, function (e) { e.preventDefault(); });
    });
    pg.el.addEventListener('keydown', function (e) {
      var w = where();
      if (!w) return;
      if (e.key === 'Tab') {
        e.preventDefault();
        run(pg, function (f) { return OPS.indent(f, rangeOf(w), e.shiftKey ? -1 : 1) && w; });
      } else if ((e.ctrlKey || e.metaKey) && (e.key === 'i' || e.key === 'I')) {
        e.preventDefault(); italic(pg, w);
      } else if ((e.ctrlKey || e.metaKey) && (e.key === 'z' || e.key === 'Z')) {
        e.preventDefault(); undo(pg);
      }
    });
  });
  function italic(pg, w) {
    if (w.pi !== w.pj) { say('Italic works inside one paragraph at a time.'); return; }
    run(pg, function (f) { return OPS.italic(f, w.pi, Math.min(w.off, w.end), Math.max(w.off, w.end)); });
  }
  function undo(pg) {
    if (!pg.undo.length) return;
    pg.flat = pg.undo.pop();
    render(pg); save();
  }

  // ---- the German view: paragraph starts and voices, line by line ----------------
  var german = load(GKEY) || { pad: PAD, unit: UNIT, letter: LETTER, breaks: {}, voices: [] };
  var anchor = null;
  function lineNo(li) {
    var ol = li.parentNode;
    var start = parseInt(ol.getAttribute('start') || '1', 10);
    return start + Array.prototype.indexOf.call(ol.children, li);
  }
  function germanSetup() {
    document.querySelectorAll('.ms-page').forEach(function (sec) {
      var page = sec.getAttribute('data-page');
      sec.querySelectorAll('.text-view[data-view="diplomatic"] ol.dip > li').forEach(function (li) {
        if (li.querySelector('.tf-pmark')) return;
        var n = lineNo(li);
        li.setAttribute('data-ln', String(n));
        li.setAttribute('data-page', page);
        var b = document.createElement('button');
        b.type = 'button';
        b.className = 'tf-pmark';
        b.title = 'A paragraph of the reading text begins here (click to change)';
        b.textContent = '¶';
        b.addEventListener('click', function (e) {
          e.preventDefault(); e.stopPropagation();
          var on = !isStart(li);
          var key = String(n);
          if (on === li.classList.contains('pstart')) delete german.breaks[key];
          else german.breaks[key] = { page: page, text: li.textContent.replace('¶', '').trim().slice(0, 70),
                                      decision: on ? 'break' : 'run' };
          paintGerman(); saveGerman();
        });
        li.insertBefore(b, li.firstChild);
        li.addEventListener('click', function (e) {
          if (!document.body.classList.contains('tf-german')) return;
          if (e.shiftKey && anchor && anchor.page === page) {
            var a = Math.min(anchor.n, n), z = Math.max(anchor.n, n);
            selectLines(page, a, z);
          } else { anchor = { page: page, n: n }; selectLines(page, n, n); }
        });
      });
    });
    paintGerman();
  }
  function isStart(li) {
    var d = german.breaks[li.getAttribute('data-ln')];
    return d ? d.decision === 'break' : li.classList.contains('pstart');
  }
  var chosen = null;
  function selectLines(page, a, z) {
    chosen = { page: page, from: a, to: z };
    document.querySelectorAll('li[data-ln]').forEach(function (li) {
      var n = +li.getAttribute('data-ln');
      li.classList.toggle('tf-chosen', li.getAttribute('data-page') === page && n >= a && n <= z);
    });
  }
  function paintGerman() {
    document.querySelectorAll('li[data-ln]').forEach(function (li) {
      li.classList.toggle('tf-start', isStart(li));
      li.classList.toggle('tf-changed', !!german.breaks[li.getAttribute('data-ln')]);
      var n = +li.getAttribute('data-ln'), v = null;
      german.voices.forEach(function (x) { if (n >= x.from && n <= x.to) v = x.kind; });
      ['office', 'margin', 'hand', 'none'].forEach(function (k) { li.classList.toggle('tf-v-' + k, v === k); });
    });
  }
  function saveGerman() {
    var empty = !Object.keys(german.breaks).length && !german.voices.length;
    german.saved = new Date().toISOString();
    store(GKEY, empty ? null : german);
    status();
  }
  function germanVoice(kind) {
    if (!chosen) { say('Choose the lines first: click one, shift-click the last.'); return; }
    german.voices = german.voices.filter(function (x) { return x.to < chosen.from || x.from > chosen.to; });
    german.voices.push({ page: chosen.page, from: chosen.from, to: chosen.to, kind: kind,
                         first: (document.querySelector('li[data-ln="' + chosen.from + '"]') || {}).textContent
                           .replace('¶', '').trim().slice(0, 70) });
    paintGerman(); saveGerman();
  }

  // ---- the bar ------------------------------------------------------------------
  var bar = document.createElement('div');
  bar.className = 'tf-editbar';
  bar.innerHTML =
    '<span class="tf-title">Layout editor</span>' +
    '<span class="tf-group tf-en">' +
    '<button data-a="outdent" title="Outdent (Shift+Tab)">⇤</button>' +
    '<button data-a="indent" title="Indent (Tab)">⇥</button>' +
    '<button data-a="al" title="Align left">⯇</button>' +
    '<button data-a="ac" title="Centre">≡</button>' +
    '<button data-a="ar" title="Align right">⯈</button>' +
    '<button data-a="italic" title="Italic (Ctrl+I)"><em>I</em></button>' +
    '<button data-a="br" title="Line break (Shift+Enter)">↵</button>' +
    '<select data-a="voice" title="Set apart the chosen paragraphs">' +
    '<option value="">Voice…</option><option value="none">Main text</option>' +
    '<option value="office">Receiving office</option><option value="margin">Margin</option>' +
    '<option value="hand">Another hand</option></select>' +
    '<button data-a="newbox" title="Start a new box here (a second voice of the same kind)">New box</button>' +
    '<button data-a="undo" title="Undo (Ctrl+Z)">Undo</button>' +
    '<button data-a="reset" title="Back to the published layout of this page">Reset page</button>' +
    '</span>' +
    '<button data-a="german" title="The German reading text: paragraph starts and voices, line by line">German</button>' +
    '<span class="tf-group tf-de">' +
    '<select data-a="gvoice" title="Set apart the chosen lines"><option value="">Lines…</option>' +
    '<option value="none">Main text</option><option value="office">Receiving office</option>' +
    '<option value="margin">Margin</option><option value="hand">Another hand</option></select>' +
    '<button data-a="greset" title="Forget the German changes of this document">Reset</button>' +
    '</span>' +
    '<button data-a="export" title="Download every change as one file">Export</button>' +
    '<span class="tf-status"></span>';
  document.body.appendChild(bar);
  document.body.classList.add('tf-edit');
  var last = null;
  document.addEventListener('selectionchange', function () {
    var w = where();
    if (w) last = w;
  });
  bar.addEventListener('mousedown', function (e) {
    if (e.target.closest('button')) e.preventDefault();      // keep the text selection
  });
  bar.addEventListener('click', function (e) {
    var b = e.target.closest('button');
    if (!b) return;
    var a = b.getAttribute('data-a');
    if (a === 'export') return doExport();
    if (a === 'german') return toggleGerman();
    if (a === 'greset') {
      german = { pad: PAD, unit: UNIT, letter: LETTER, breaks: {}, voices: [] };
      paintGerman(); saveGerman(); return;
    }
    var w = where() || last;
    if (!w || !pages[w.page]) { say('Put the cursor in the English first.'); return; }
    var pg = pages[w.page];
    if (a === 'undo') return undo(pg);
    if (a === 'reset') { pg.undo.push(clone(pg.flat)); pg.flat = clone(pg.start); render(pg); save(); return; }
    if (a === 'italic') return italic(pg, w);
    run(pg, function (f) {
      if (a === 'indent') return OPS.indent(f, rangeOf(w), 1) && w;
      if (a === 'outdent') return OPS.indent(f, rangeOf(w), -1) && w;
      if (a === 'al' || a === 'ac' || a === 'ar') return OPS.align(f, rangeOf(w), a.charAt(1)) && w;
      if (a === 'br') return w.collapsed && OPS.lineBreak(f, w.pi, w.off);
      if (a === 'newbox') return OPS.newBox(f, rangeOf(w)) && w;
      return false;
    });
  });
  bar.addEventListener('change', function (e) {
    var s = e.target;
    var a = s.getAttribute('data-a'), v = s.value;
    s.value = '';
    if (!v) return;
    if (a === 'gvoice') return germanVoice(v);
    var w = where() || last;
    if (!w || !pages[w.page]) { say('Put the cursor in the English first.'); return; }
    run(pages[w.page], function (f) { return OPS.voice(f, rangeOf(w), v === 'none' ? null : v) && w; });
  });
  function toggleGerman() {
    var on = !document.body.classList.contains('tf-german');
    document.body.classList.toggle('tf-german', on);
    if (window.tfShowView) window.tfShowView(on ? 'diplomatic' : 'translation');
    if (on) germanSetup();
  }
  if (window.tfShowView) window.tfShowView('translation');

  // ---- status and export ---------------------------------------------------------
  var msgTimer = null;
  function say(m) {
    var s = bar.querySelector('.tf-status');
    s.textContent = m;
    clearTimeout(msgTimer);
    msgTimer = setTimeout(status, 4000);
  }
  function allKeys() {
    var out = [];
    try {
      for (var k = 0; k < localStorage.length; k++) {
        var key = localStorage.key(k);
        if (/^tf-(layout|german):/.test(key)) out.push(key);
      }
    } catch (e) { /* storage blocked */ }
    return out;
  }
  function status() {
    var here = Object.keys((load(KEY) || {}).pages || {}).length;
    var g = load(GKEY);
    var gn = g ? Object.keys(g.breaks || {}).length + (g.voices || []).length : 0;
    var docs = {};
    allKeys().forEach(function (k) { docs[k.split(':').slice(1).join(':')] = 1; });
    bar.querySelector('.tf-status').textContent =
      'This document: ' + here + ' page(s) laid out' + (gn ? ', ' + gn + ' German change(s)' : '') +
      ' · documents with changes: ' + Object.keys(docs).length;
  }
  function doExport() {
    var out = { kind: 'triebenfeld-layout', version: 1, exported: new Date().toISOString(),
                english: [], german: [] };
    allKeys().forEach(function (k) {
      var v = load(k);
      if (!v) return;
      if (k.indexOf('tf-layout:') === 0) {
        Object.keys(v.pages || {}).forEach(function (pg) {
          out.english.push({ pad: v.pad, page: +pg, fingerprint: v.pages[pg].fp, layout: v.pages[pg].items });
        });
      } else {
        out.german.push({ pad: v.pad, unit: v.unit, letter: v.letter,
                          breaks: Object.keys(v.breaks || {}).map(function (n) {
                            var b = v.breaks[n];
                            return { doc_line: +n, page: +b.page, text: b.text, decision: b.decision };
                          }),
                          voices: v.voices || [] });
      }
    });
    if (!out.english.length && !out.german.length) { say('Nothing to export yet.'); return; }
    var blob = new Blob([JSON.stringify(out, null, 1)], { type: 'application/json' });
    var a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'english_layout_' + new Date().toISOString().slice(0, 10) + '.json';
    document.body.appendChild(a); a.click(); a.remove();
    say('Exported ' + out.english.length + ' English page(s) and ' + out.german.length +
        ' document(s) of German changes. Keep them here until they are brought home.');
  }
  status();
  // for the tests (scratch): the pure functions
  window.tfLayoutEditor = { OPS: OPS, fromEn: fromEn, fromItems: fromItems, toItems: toItems,
                            norm: norm, fingerprint: fingerprint, text: text };
})();
