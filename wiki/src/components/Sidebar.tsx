import { useMemo, useState } from 'react';
import { Folder, Search } from 'lucide-react';
import type { Note } from '../types';
import { AtlasMark } from './AtlasMark';

interface SidebarProps {
  notes: Note[];
  categories: string[];
  selectedNoteId?: string;
  searchQuery: string;
  onSearchChange: (q: string) => void;
  selectedCategory: string | null;
  onSelectCategory: (c: string | null) => void;
  onSelectNote: (id: string) => void;
}

export function Sidebar({
  notes,
  categories,
  selectedNoteId,
  searchQuery,
  onSearchChange,
  selectedCategory,
  onSelectCategory,
  onSelectNote,
}: SidebarProps) {
  const [sortBy, setSortBy] = useState<'title' | 'category'>('title');

  const filtered = useMemo(() => {
    return notes
      .filter((note) => {
        if (selectedCategory && note.category !== selectedCategory) return false;
        if (!searchQuery.trim()) return true;
        const q = searchQuery.toLowerCase();
        return (
          note.title.toLowerCase().includes(q) ||
          note.content.toLowerCase().includes(q) ||
          note.category.toLowerCase().includes(q) ||
          note.path.toLowerCase().includes(q)
        );
      })
      .sort((a, b) => {
        if (sortBy === 'category') {
          const cat = a.category.localeCompare(b.category, 'pt-BR');
          return cat !== 0 ? cat : a.title.localeCompare(b.title, 'pt-BR');
        }
        return a.title.localeCompare(b.title, 'pt-BR');
      });
  }, [notes, selectedCategory, searchQuery, sortBy]);

  return (
    <div className="panel flex h-full w-full flex-col overflow-hidden rounded-lg text-slate-100 lg:w-80">
      <div className="border-b border-neon/10 p-4">
        <div className="mb-3 flex items-center gap-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-md border border-neon/30 bg-black/40 text-neon">
            <AtlasMark className="h-4 w-4" />
          </div>
          <div>
            <h2 className="font-display text-sm font-bold tracking-[0.16em] uppercase">Índice</h2>
            <p className="font-mono text-[11px] text-fog">{notes.length} páginas</p>
          </div>
        </div>
        <div className="relative">
          <Search className="absolute top-2.5 left-3 h-4 w-4 text-neon/60" />
          <input
            value={searchQuery}
            onChange={(e) => onSearchChange(e.target.value)}
            placeholder="Buscar título, path ou conteúdo..."
            className="w-full rounded-md border border-neon/20 bg-black/50 py-1.5 pr-3 pl-9 font-mono text-xs text-slate-100 placeholder:text-fog/70 focus:border-neon focus:outline-none"
          />
        </div>
      </div>

      <div className="space-y-2 border-b border-neon/10 p-3 text-xs">
        <div className="flex items-center justify-between">
          <span className="font-display text-[10px] font-semibold tracking-[0.2em] text-fog uppercase">
            Categorias
          </span>
          <button
            type="button"
            onClick={() => setSortBy((s) => (s === 'title' ? 'category' : 'title'))}
            className="font-mono text-[10px] text-neon hover:text-ice"
          >
            ordenar: {sortBy}
          </button>
        </div>
        <div className="flex max-h-28 flex-wrap gap-1.5 overflow-y-auto">
          <button
            type="button"
            onClick={() => onSelectCategory(null)}
            className={`rounded-sm px-2 py-0.5 font-mono text-[11px] uppercase ${
              !selectedCategory
                ? 'chip'
                : 'border border-white/10 bg-black/40 text-fog hover:border-neon/30 hover:text-ice'
            }`}
          >
            Todas
          </button>
          {categories.map((cat) => (
            <button
              key={cat}
              type="button"
              onClick={() => onSelectCategory(selectedCategory === cat ? null : cat)}
              className={`inline-flex max-w-full items-center gap-1 truncate rounded-sm px-2 py-0.5 font-mono text-[11px] ${
                selectedCategory === cat
                  ? 'chip-hot'
                  : 'border border-white/10 bg-black/40 text-fog hover:border-hot/40 hover:text-ice'
              }`}
              title={cat}
            >
              <Folder className="h-3 w-3 shrink-0" />
              <span className="truncate">{cat}</span>
            </button>
          ))}
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-2">
        <p className="font-display mb-2 px-2 text-[10px] font-semibold tracking-[0.2em] text-fog uppercase">
          Notas ({filtered.length})
        </p>
        <ul className="space-y-0.5">
          {filtered.map((note) => (
            <li key={note.id}>
              <button
                type="button"
                onClick={() => onSelectNote(note.id)}
                className={`w-full rounded-md px-2.5 py-2 text-left transition ${
                  selectedNoteId === note.id
                    ? 'bg-neon/10 text-neon ring-1 ring-neon/40'
                    : 'hover:bg-white/5'
                }`}
              >
                <div className="truncate text-xs font-semibold tracking-wide">{note.title}</div>
                <div className="mt-0.5 truncate font-mono text-[10px] text-fog">{note.path}</div>
              </button>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
