// UI strings only: the genealogical data itself is shown as recorded
// (German, Polish, Latin sources are not translated - the edition's rule).

const STRINGS = {
  en: {
    app: 'Zelmer Family Explorer',
    nav_home: 'Home', nav_search: 'Search', nav_surnames: 'Surnames',
    nav_places: 'Places', nav_map: 'Map',
    born: 'Born', died: 'Died', living: 'Living', male: 'man', female: 'woman',
    unknown_sex: '?',
    parents: 'Parents', partnerships: 'Partnerships', children: 'Children',
    married: 'Married', divorced: 'Divorced', annulled: 'Annulled',
    timeline: 'Life events', notes: 'Notes', media: 'Media', sources: 'Sources',
    citations: 'citations', citation: 'Citation', repository: 'Repository',
    page: 'Page', show_region: 'focus', hide_region: 'full image',
    no_media_note: 'image not published',
    search_placeholder: 'Search people, places, years …',
    search_results: 'results', no_results: 'Nothing found.',
    people_count: 'people', families_count: 'families', media_count: 'media',
    places_count: 'places', geocoded_count: 'with coordinates',
    data_as_of: 'Data as of', events_at: 'Events here',
    surname_count: 'people', back: 'Back',
    privacy_note: 'Living person: details are not published.',
    in_tree: 'In the tree',
    boot_loading: 'Loading the family database …',
    boot_slow: 'Still loading — a slow connection, or a content blocker (tracking protection, ad blocker), can hold the database back.',
    siblings: 'Siblings',
    sort_az: 'A–Z', sort_za: 'Z–A',
    sort_count: 'by count',
    tree_hint: 'Click a person to bring their tree into view · scroll to zoom · drag to pan',
  },
  de: {
    app: 'Zelmer-Familien-Explorer',
    nav_home: 'Start', nav_search: 'Suche', nav_surnames: 'Namen',
    nav_places: 'Orte', nav_map: 'Karte',
    born: 'Geboren', died: 'Gestorben', living: 'Lebend', male: 'Mann', female: 'Frau',
    unknown_sex: '?',
    parents: 'Eltern', partnerships: 'Partnerschaften', children: 'Kinder',
    married: 'Heirat', divorced: 'Geschieden', annulled: 'Annulliert',
    timeline: 'Lebensereignisse', notes: 'Notizen', media: 'Medien', sources: 'Quellen',
    citations: 'Belege', citation: 'Beleg', repository: 'Aufbewahrungsort',
    page: 'Stelle', show_region: 'Fokus', hide_region: 'ganzes Bild',
    no_media_note: 'Bild nicht veröffentlicht',
    search_placeholder: 'Personen, Orte, Jahre suchen …',
    search_results: 'Treffer', no_results: 'Nichts gefunden.',
    people_count: 'Personen', families_count: 'Familien', media_count: 'Medien',
    places_count: 'Orte', geocoded_count: 'mit Koordinaten',
    data_as_of: 'Datenstand', events_at: 'Ereignisse hier',
    surname_count: 'Personen', back: 'Zurück',
    privacy_note: 'Lebende Person: Details werden nicht veröffentlicht.',
    in_tree: 'Im Baum',
    boot_loading: 'Die Familiendatenbank wird geladen …',
    boot_slow: 'Es wird noch geladen – eine langsame Verbindung oder ein Inhaltsblocker (Tracking-Schutz, Adblocker) kann die Datenbank aufhalten.',
    siblings: 'Geschwister',
    sort_az: 'A–Z', sort_za: 'Z–A',
    sort_count: 'nach Anzahl',
    tree_hint: 'Klicken Sie auf eine Person, um ihren Baum zu zentrieren · scrollen zum Vergrößern · ziehen zum Verschieben',
  },
  pl: {
    app: 'Eksplorator rodziny Zelmer',
    nav_home: 'Start', nav_search: 'Szukaj', nav_surnames: 'Nazwiska',
    nav_places: 'Miejsca', nav_map: 'Mapa',
    born: 'Urodzony', died: 'Zmarł', living: 'Żyjący', male: 'mężczyzna', female: 'kobieta',
    unknown_sex: '?',
    parents: 'Rodzice', partnerships: 'Związki', children: 'Dzieci',
    married: 'Ślub', divorced: 'Rozwód', annulled: 'Unieważniony',
    timeline: 'Wydarzenia życiowe', notes: 'Notatki', media: 'Materiały', sources: 'Źródła',
    citations: 'przypisy', citation: 'Przypis', repository: 'Archiwum',
    page: 'Strona', show_region: 'fokus', hide_region: 'cały obraz',
    no_media_note: 'obraz nieopublikowany',
    search_placeholder: 'Szukaj osób, miejsc, lat …',
    search_results: 'wyników', no_results: 'Nic nie znaleziono.',
    people_count: 'osób', families_count: 'rodzin', media_count: 'materiałów',
    places_count: 'miejsc', geocoded_count: 'ze współrzędnymi',
    data_as_of: 'Stan danych', events_at: 'Wydarzenia w tym miejscu',
    surname_count: 'osób', back: 'Wstecz',
    privacy_note: 'Osoba żyjąca: szczegóły nie są publikowane.',
    in_tree: 'W drzewie',
    boot_loading: 'Wczytywanie bazy rodzinnej …',
    boot_slow: 'Nadal wczytywanie – wolne połączenie lub bloker treści (ochrona przed śledzeniem, bloker reklam) może opóźniać bazę.',
    siblings: 'Rodzeństwo',
    sort_az: 'A–Z', sort_za: 'Z–A',
    sort_count: 'według liczby',
    tree_hint: 'Kliknij osobę, aby wyśrodkować jej drzewo · kółko = powiększanie · przeciąganie = przesuwanie',
  },
}

let lang = localStorage.getItem('gen-lang') || 'en'
if (!STRINGS[lang]) lang = 'en'

const listeners = new Set()

export const i18n = {
  get lang() { return lang },
  set lang(v) {
    if (STRINGS[v] && v !== lang) {
      lang = v
      localStorage.setItem('gen-lang', v)
      listeners.forEach(fn => fn())
    }
  },
  langs: Object.keys(STRINGS),
  t(key) { return (STRINGS[lang] && STRINGS[lang][key]) || STRINGS.en[key] || key },
  subscribe(fn) { listeners.add(fn); return () => listeners.delete(fn) },
}

// Event tags -> label keys. Tags not listed render as their raw tag.
export const EVENT_LABELS = {
  BIRT: 'born', BAPM: 'baptised', CHR: 'baptised', BAPL: 'baptised',
  ADOP: 'adopted', CONF: 'confirmed', EDUC: 'education', GRAD: 'graduated',
  RESI: 'residence', OCCU: 'occupation', PROP: 'property',
  IMMI: 'immigrated', EMIG: 'emigrated', NATU: 'naturalised',
  CENS: 'census', MILIT: 'military', _MILT: 'military', RETI: 'retired',
  MARR: 'married', DIV: 'divorced', ANUL: 'annulled',
  EVEN: 'event', FACT: 'fact', DEAT: 'died', BURI: 'buried', CREM: 'cremated',
}
