// Runs after vite: the built index.html (relative base ./assets/) becomes
// the page of each tree, one folder down, pointing at the shared assets:
//   zelmer/index.html, trabczyn/index.html   (./assets/ -> ../assets/)
// and /genealogy/index.html itself is then replaced by the chooser page
// (chooser.html), which forwards an old #-link to zelmer/. Each tree page
// loads its own data/ folder, relative to the page, and takes its title,
// start person and media setting from that data/meta.json.
const fs = require('fs'), path = require('path')
const root = path.join(__dirname, '..')
const built = fs.readFileSync(path.join(root, 'index.html'), 'utf8')
if (!built.includes('./assets/')) throw new Error('built index.html has no ./assets/ URLs')
// neutral title; the app sets the real one from meta.json
const page = built.replace(/\.\/assets\//g, '../assets/')
  .replace(/<title>[^<]*<\/title>/, '<title>Family Explorer &middot; Trąbczyn Archive</title>')
for (const tree of ['zelmer', 'trabczyn']) {
  fs.mkdirSync(path.join(root, tree), { recursive: true })
  fs.writeFileSync(path.join(root, tree, 'index.html'), page)
}
fs.copyFileSync(path.join(root, 'chooser.html'), path.join(root, 'index.html'))
console.log('pages: zelmer/index.html, trabczyn/index.html, chooser at index.html')
