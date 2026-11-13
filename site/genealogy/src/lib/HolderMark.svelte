<script>
  // The owner mark outside the chart: the small accent key beside a name
  // (search results, surname lists), or with its label as a badge on the
  // person page. Shown only for people whose index entry carries h
  // (trabczyn); the caller checks that.
  import { db } from './db.svelte.js'
  import { i18n } from './i18n.js'
  let { label = false } = $props()
  const text = $derived(db.meta?.holder_label
    ? (db.meta.holder_label[i18n.lang] || db.meta.holder_label.en) : '')
</script>

<span class="hm" class:badge={label} title={text}>
  <svg width="13" height="13" viewBox="0 0 14 14" aria-hidden="true">
    <circle cx="4" cy="4" r="3" fill="none" stroke="currentColor" stroke-width="1.4" />
    <path d="M 6.2 6.2 L 12 12 M 9.5 9.5 L 11.5 7.5 M 11 11 L 13 9"
          fill="none" stroke="currentColor" stroke-width="1.4" />
  </svg>{#if label}<span class="t">{text}</span>{/if}
</span>

<style>
  .hm { display: inline-flex; align-items: center; gap: .3rem;
    color: var(--accent); vertical-align: -2px; margin-left: .3rem; }
  .hm.badge { border: 2px solid var(--accent); border-radius: 4px;
    padding: .02rem .4rem; font-size: .74rem; font-weight: 600;
    margin-left: 0; vertical-align: baseline; }
</style>
