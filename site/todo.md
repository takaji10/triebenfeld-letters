---
layout: default
permalink: /todo/
title: To do
lang: en
noindex: true
---
{%- assign d = site.data.todo -%}
<div class="prose">
  <h1>To do</h1>
  <p class="standfirst">The editor's working list: what is open, in the order of the holdings and projects it belongs to. Answer here as you go; answers are kept in this browser, and "Export answers" gives a file to hand over. This page is not part of the edition for readers.</p>
</div>

<form class="filters filters-list todo-bar" id="todo-bar" role="search" autocomplete="off" onsubmit="return false">
  <div class="f-main">
    <label class="f-search"><span>Search the list</span>
      <input type="search" id="td-q" placeholder="A name, a holding, a word"></label>
    <label class="f-order"><span>Show</span>
      <select id="td-kind">
        <option value="you">For you ({{ d.counts.question | plus: d.counts.decision | plus: d.counts.task }})</option>
        <option value="question">Questions ({{ d.counts.question }})</option>
        <option value="decision">Decisions ({{ d.counts.decision }})</option>
        <option value="task">Your tasks ({{ d.counts.task }})</option>
        <option value="claude">Claude's queue ({{ d.counts.claude }})</option>
        <option value="waiting">Waiting ({{ d.counts.waiting }})</option>
        <option value="all">Everything ({{ d.total }})</option>
      </select></label>
    <label class="f-type"><span>Group</span>
      <select id="td-group"><option value="">All groups</option>
        {%- for g in d.groups %}<option value="{{ forloop.index0 }}">{{ g.name | escape }} ({{ g.items.size }})</option>{% endfor -%}
      </select></label>
  </div>
  <div class="f-bar">
    <p class="f-status"><span id="td-count" aria-live="polite">…</span></p>
    <p class="f-status todo-actions">
      <button type="button" class="linkish" id="td-export">Export answers</button>
      <label class="linkish todo-import">Import answers<input type="file" id="td-import" accept="application/json,.json" hidden></label>
      <button type="button" class="linkish" id="td-clear">Clear all answers</button>
    </p>
  </div>
</form>

<div class="todo" id="todo">
{%- for g in d.groups %}
{%- assign gi = forloop.index0 %}
<section class="todo-group" data-group="{{ gi }}">
  <h2>{{ g.name | escape }}</h2>
  {%- for c in g.items %}
  <article class="todo-card" id="{{ c.id }}" data-id="{{ c.id }}" data-kind="{{ c.kind }}" data-h="{{ c.h }}" data-title="{{ c.title | escape }}">
    <h3>{{ c.title | escape }} <span class="todo-kind todo-kind-{{ c.kind }}">{% case c.kind %}{% when 'question' %}question{% when 'decision' %}decision{% when 'task' %}your task{% when 'claude' %}Claude's{% else %}waiting{% endcase %}</span></h3>
    <p>{{ c.text | escape }}</p>
    {%- if c.note != "" %}<p class="todo-aside">Audit, 25 November 2026: {{ c.note | escape }}</p>{% endif %}
    {%- if c.links.size > 0 %}
    <p class="todo-links">{% for l in c.links %}<a class="type-tag" href="{{ l.href | relative_url }}">{{ l.label | escape }}</a> {% endfor %}</p>
    {%- endif %}
    {%- if c.nc != "" %}<p class="todo-nc">Full discussion: NEEDS_CONFIRMATION, &ldquo;{{ c.nc | escape }}&rdquo;</p>{% endif %}
    <div class="todo-answer" role="group" aria-label="Your answer">
      {%- case c.kind %}
      {%- when 'question' or 'decision' %}
        {%- for o in c.options %}<button type="button" data-v="{{ o | escape }}">{{ o | escape }}</button>{% endfor %}
        <button type="button" data-v="__other__">Something else</button>
        <button type="button" data-v="__unsure__">Can&rsquo;t tell</button>
      {%- when 'task' %}
        <button type="button" data-v="__done__">Done</button>
        <button type="button" data-v="__later__">Later</button>
        <button type="button" data-v="__drop__">Not needed</button>
      {%- when 'claude' %}
        <button type="button" data-v="__go__">Go ahead</button>
        <button type="button" data-v="__later__">Later</button>
        <button type="button" data-v="__drop__">Drop it</button>
      {%- else %}
        <button type="button" data-v="__now__">Now</button>
        <button type="button" data-v="__later__">Not yet</button>
        <button type="button" data-v="__drop__">Drop it</button>
      {%- endcase %}
      <input type="text" class="todo-other" placeholder="Your answer" hidden>
      <input type="text" class="todo-note" placeholder="A note (optional)">
      <span class="todo-stale" hidden>The item changed after you answered.</span>
    </div>
  </article>
  {%- endfor %}
</section>
{%- endfor %}
</div>
<p class="empty" id="td-empty" hidden>Nothing matches.</p>
<script src="{{ '/assets/todo.js' | relative_url }}"></script>
