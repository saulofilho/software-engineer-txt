import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const WIKI_ROOT = path.resolve(__dirname, '..');
const REPO_ROOT = path.resolve(WIKI_ROOT, '..');
const OUT_DIR = path.join(WIKI_ROOT, 'src', 'generated');
const OUT_FILE = path.join(OUT_DIR, 'notes.json');

const SKIP_DIRS = new Set([
  '.git',
  'wiki',
  'node_modules',
  '.tools',
  'dist',
  '_assets',
]);

function slugify(text) {
  return (
    text
      .toLowerCase()
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/(^-|-$)+/g, '') || 'note'
  );
}

function walk(dir, files = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (SKIP_DIRS.has(entry.name) || entry.name.startsWith('.')) continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      walk(full, files);
    } else if (entry.isFile() && entry.name.endsWith('.md')) {
      files.push(full);
    }
  }
  return files;
}

function extractTitle(content, fallback) {
  const match = content.match(/^#\s+(.+)$/m);
  if (match) return match[1].replace(/[*_`]/g, '').trim();
  return fallback;
}

function extractWikiLinks(content) {
  const links = [];
  const regex = /\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g;
  let match;
  while ((match = regex.exec(content)) !== null) {
    links.push(match[1].trim());
  }
  return links;
}

function extractMdLinks(content, fromPath) {
  const links = [];
  const regex = /\[([^\]]+)\]\(([^)]+\.md)\)/g;
  let match;
  while ((match = regex.exec(content)) !== null) {
    const target = match[2].split('#')[0];
    const resolved = path.normalize(path.join(path.dirname(fromPath), target));
    links.push(resolved.replace(/\\/g, '/'));
  }
  return links;
}

const mdFiles = walk(REPO_ROOT);
const notes = [];

for (const full of mdFiles) {
  const rel = path.relative(REPO_ROOT, full).replace(/\\/g, '/');
  if (rel === 'README.md') continue;

  const content = fs.readFileSync(full, 'utf8');
  const parts = rel.split('/');
  const category = parts[0] || 'Geral';
  const fileBase = path.basename(rel, '.md');
  const title = extractTitle(content, fileBase.replace(/-/g, ' '));
  const id = slugify(rel.replace(/\.md$/, ''));

  notes.push({
    id,
    title,
    path: rel,
    category,
    content: content.trim() || `_(Nota vazia: \`${rel}\`)_`,
    wikiLinks: extractWikiLinks(content),
    mdLinkPaths: extractMdLinks(content, rel),
  });
}

notes.sort((a, b) => a.title.localeCompare(b.title, 'pt-BR'));

const byPath = new Map(notes.map((n) => [n.path, n.id]));
const byTitle = new Map();
for (const n of notes) {
  byTitle.set(n.title.toLowerCase(), n.id);
}

const enriched = notes.map((n) => {
  const linkIds = new Set();
  for (const title of n.wikiLinks) {
    const id = byTitle.get(title.toLowerCase());
    if (id && id !== n.id) linkIds.add(id);
  }
  for (const p of n.mdLinkPaths) {
    const id = byPath.get(p);
    if (id && id !== n.id) linkIds.add(id);
  }
  return {
    id: n.id,
    title: n.title,
    path: n.path,
    category: n.category,
    content: n.content,
    outboundIds: [...linkIds],
  };
});

fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(
  OUT_FILE,
  JSON.stringify(
    {
      generatedAt: new Date().toISOString(),
      count: enriched.length,
      notes: enriched,
    },
    null,
    2
  )
);

console.log(`Ingested ${enriched.length} notes → ${path.relative(WIKI_ROOT, OUT_FILE)}`);
