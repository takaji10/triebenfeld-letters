/* The mobile-readiness crawler (pipeline/mobile_check/crawl.js, 2026-11-07).
   Measures every page at phone widths against a locally served build and
   reports horizontal overflow with the offenders that are NOT inside a
   clipping container (a clipped descendant still reports its full layout
   rect; the real extender's right edge matches documentElement.scrollWidth).

   Usage:
     node crawl.js --base http://127.0.0.1:PORT --pages pages.txt
                   --out report.json [--widths 390,360,320] [--conc 6]

   pages.txt: one URL path per line. Output JSON:
     { problems: [{page,width,overflow,offenders:[{sel,right,width,text}]}],
       unmeasured: [{page,width,error}] }

   Each page/width measurement is retried up to 3 times: the two error
   classes seen in service are races (a navigation destroying the execution
   context, documentElement briefly null during load), never page defects —
   a page that still errors after 3 tries is reported unmeasured, not
   failed. */
const fs = require("fs");
const puppeteer = require("puppeteer-core");

const args = {};
for (let i = 2; i < process.argv.length; i += 2)
  args[process.argv[i].replace(/^--/, "")] = process.argv[i + 1];
const BASE = args.base;
const widths = (args.widths || "390,360,320").split(",").map(Number);
const CONC = Number(args.conc || 6);
const pages = fs.readFileSync(args.pages, "utf-8").split("\n")
  .map(s => s.trim()).filter(Boolean);
const EDGE = ["C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
              "C:/Program Files/Microsoft/Edge/Application/msedge.exe"]
  .find(p => { try { return fs.existsSync(p); } catch { return false; } });
if (!EDGE) { console.error("no msedge.exe found"); process.exit(2); }

function pathOf(el) {
  const parts = [];
  let n = el;
  while (n && n.nodeType === 1 && parts.length < 6) {
    let s = n.tagName.toLowerCase();
    if (n.id) s += "#" + n.id;
    else if (n.className && typeof n.className === "string")
      s += "." + n.className.trim().split(/\s+/).slice(0, 2).join(".");
    parts.unshift(s);
    n = n.parentElement;
  }
  return parts.join(" > ");
}

async function once(browser, url, width) {
  const page = await browser.newPage();
  try {
    await page.setViewport({ width, height: 800, deviceScaleFactor: 1 });
    await page.goto(url, { waitUntil: "domcontentloaded", timeout: 30000 });
    await page.waitForSelector("body", { timeout: 10000 });
    await new Promise(r => setTimeout(r, 300));
    return await page.evaluate(({ pathOfSrc }) => {
      const pathOf = eval("(" + pathOfSrc + ")");
      const de = document.documentElement;
      if (!de) return null;                       // race: retried outside
      const overflow = de.scrollWidth - de.clientWidth;
      const out = { overflow, offenders: [] };
      if (overflow > 1) {
        const vw = de.clientWidth;
        // the clippers: any element whose subtree is scrolled or hidden
        // cannot extend the document through its descendants
        const clippers = [];
        for (const el of document.querySelectorAll("body *")) {
          const cs = getComputedStyle(el);
          if (/(auto|scroll|hidden|clip)/.test(cs.overflowX))
            clippers.push(el);
        }
        const clipped = el => clippers.some(c => c !== el && c.contains(el));
        const hits = [];
        for (const el of document.querySelectorAll("body *")) {
          const r = el.getBoundingClientRect();
          if (r.right > vw + 1 && r.width > 8 && !clipped(el)) {
            hits.push({ right: Math.round(r.right),
                        width: Math.round(r.width), sel: pathOf(el),
                        text: (el.textContent || "").trim().slice(0, 60) });
          }
        }
        hits.sort((a, b) => b.right - a.right);
        const seen = new Set();
        for (const h of hits) {
          if (seen.has(h.sel)) continue;
          seen.add(h.sel);
          out.offenders.push(h);
          if (out.offenders.length >= 6) break;
        }
      }
      return out;
    }, { pathOfSrc: pathOf.toString() });
  } finally {
    await page.close().catch(() => {});
  }
}

async function measure(browser, url, width) {
  for (let tryN = 0; tryN < 3; tryN++) {
    try {
      const r = await once(browser, url, width);
      if (r) return r;
    } catch (e) {
      if (tryN === 2) return { error: String(e).slice(0, 120) };
    }
    await new Promise(r => setTimeout(r, 500));
  }
}

(async () => {
  const browser = await puppeteer.launch({
    executablePath: EDGE, headless: "new",
    args: ["--disable-gpu", "--no-first-run"],
  });
  const problems = [], unmeasured = [];
  let idx = 0;
  async function worker() {
    while (idx < pages.length) {
      const p = pages[idx++];
      for (const w of widths) {
        const r = await measure(browser, BASE + p, w);
        if (r.error) unmeasured.push({ page: p, width: w, error: r.error });
        else if (r.overflow > 1) problems.push({ page: p, width: w, ...r });
      }
    }
  }
  await Promise.all(Array.from({ length: CONC }, worker));
  await browser.close();
  fs.writeFileSync(args.out,
    JSON.stringify({ problems, unmeasured }, null, 1));
  console.log(`checked ${pages.length} pages x ${widths.length} widths: ` +
    `${problems.length} overflow(s), ${unmeasured.length} unmeasured`);
})();
