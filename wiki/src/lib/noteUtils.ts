import type { GraphLink, GraphNode, Note } from '../types';

export const WIKI_LINK_REGEX = /\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g;

export function replaceWikiLinksForRender(
  content: string,
  notesByTitle: Map<string, Note>
): string {
  return content.replace(WIKI_LINK_REGEX, (_match, title: string, alias?: string) => {
    const cleanTitle = title.trim();
    const displayText = alias ? alias.trim() : cleanTitle;
    const note = notesByTitle.get(cleanTitle.toLowerCase());
    if (note) {
      return `[${displayText}](#wiki-note-${note.id})`;
    }
    return `[${displayText} ?](#wiki-create-${encodeURIComponent(cleanTitle)})`;
  });
}

export function getBacklinks(notes: Note[], noteId: string): Note[] {
  return notes.filter((n) => n.id !== noteId && n.outboundIds.includes(noteId));
}

export function buildGraphData(notes: Note[]): { nodes: GraphNode[]; links: GraphLink[] } {
  const nodesMap = new Map<string, GraphNode>();
  const links: GraphLink[] = [];
  const notesByTitle = new Map(notes.map((n) => [n.title.toLowerCase(), n]));
  const linkKey = new Set<string>();

  const addLink = (source: string, target: string) => {
    const key = source < target ? `${source}→${target}` : `${target}→${source}`;
    if (linkKey.has(key) || source === target) return;
    linkKey.add(key);
    links.push({ source, target });
  };

  for (const note of notes) {
    nodesMap.set(note.id, {
      id: note.id,
      title: note.title,
      type: 'note',
      category: note.category,
      val: 1 + note.outboundIds.length * 0.5,
    });
  }

  // Category hubs so the graph is useful before [[wiki links]] exist
  const categories = [...new Set(notes.map((n) => n.category))];
  for (const category of categories) {
    const hubId = `category-${category.toLowerCase().replace(/\s+/g, '-')}`;
    const members = notes.filter((n) => n.category === category);
    nodesMap.set(hubId, {
      id: hubId,
      title: category,
      type: 'concept',
      category,
      val: Math.max(2, members.length * 0.35),
    });
    for (const member of members) {
      addLink(member.id, hubId);
    }
  }

  for (const note of notes) {
    for (const targetId of note.outboundIds) {
      if (!nodesMap.has(targetId)) continue;
      addLink(note.id, targetId);
      const target = nodesMap.get(targetId);
      if (target) target.val += 1;
    }

    const wikiMatches = note.content.matchAll(WIKI_LINK_REGEX);
    for (const match of wikiMatches) {
      const title = match[1].trim();
      if (notesByTitle.has(title.toLowerCase())) continue;
      const conceptId = `concept-${title.toLowerCase().replace(/\s+/g, '-')}`;
      if (!nodesMap.has(conceptId)) {
        nodesMap.set(conceptId, {
          id: conceptId,
          title,
          type: 'concept',
          category: 'conceito',
          val: 1,
        });
      } else {
        const concept = nodesMap.get(conceptId);
        if (concept) concept.val += 1;
      }
      addLink(note.id, conceptId);
    }
  }

  for (const node of nodesMap.values()) {
    if (node.type !== 'note') continue;
    const connected = links.some((l) => {
      const s = typeof l.source === 'string' ? l.source : l.source.id;
      const t = typeof l.target === 'string' ? l.target : l.target.id;
      return s === node.id || t === node.id;
    });
    if (!connected) node.type = 'orphan';
  }

  return { nodes: [...nodesMap.values()], links };
}

export function rewriteContentAssetUrls(content: string, notePath: string): string {
  const dir = notePath.includes('/') ? notePath.slice(0, notePath.lastIndexOf('/')) : '';
  return content.replace(
    /!\[([^\]]*)\]\((?!https?:|data:|#)([^)]+)\)/g,
    (_m, alt: string, src: string) => {
      const cleaned = src.replace(/^\.\//, '');
      const assetPath = dir ? `${dir}/${cleaned}` : cleaned;
      const url = `https://raw.githubusercontent.com/saulofilho/software-engineer-txt/main/${assetPath}`;
      return `![${alt}](${url})`;
    }
  );
}
