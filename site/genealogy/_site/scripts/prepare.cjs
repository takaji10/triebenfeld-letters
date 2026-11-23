// Restores the app shell before vite runs: vite consumes index.html as its
// entry and overwrites it with the transformed version, so every build (and
// dev session) starts from the committed template.
require('fs').copyFileSync(__dirname + '/../shell.html', __dirname + '/../index.html')
