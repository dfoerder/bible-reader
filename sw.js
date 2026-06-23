const CACHE_NAME = 'bible-full-v1989';
const ASSETS = [
  './',
  './index.html',
  './bibles/index.json',
  './data/words.json',
  'https://cdnjs.cloudflare.com/ajax/libs/react/18.2.0/umd/react.production.min.js',
  'https://cdnjs.cloudflare.com/ajax/libs/react-dom/18.2.0/umd/react-dom.production.min.js',
  'https://cdnjs.cloudflare.com/ajax/libs/babel-standalone/7.23.9/babel.min.js'
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(ASSETS))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  const isHTML = url.pathname.endsWith('.html') || url.pathname.endsWith('/');

  if (isHTML) {
    // Network-first for HTML: always try to get the latest version
    e.respondWith(
      fetch(e.request).then(resp => {
        if (resp.ok) {
          const clone = resp.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(e.request, clone));
        }
        return resp;
      }).catch(() => caches.match(e.request))
    );
  } else {
    // Cache-first for everything else
    e.respondWith(
      caches.match(e.request).then(cached => {
        if (cached) return cached;
        return fetch(e.request).then(resp => {
          if (resp.ok && e.request.method === 'GET') {
            const clone = resp.clone();
            caches.open(CACHE_NAME).then(cache => cache.put(e.request, clone));
          }
          return resp;
        });
      })
    );
  }
});
