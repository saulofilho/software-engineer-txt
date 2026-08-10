import { useMemo, useState } from 'react';
import { BookOpen, Folder, Search } from 'lucide-react';
import type { Note } from '../types';

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
    <div className="flex h-full w-full flex-col overflow-hidden rounded-xl border border-slate-800 bg-slate-950 text-slate-100 shadow-xl lg:w-80">
      <div className="border-b border-slate-800 p-4">
        <div className="mb-3 flex items-center gap-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-teal-800">
            <BookOpen className="h-4 w-4 text-teal-100" />
          </div>
          <div>
            <h2 className="text-sm font-bold leading-tight">Índice</h2>
            <p className="font-mono text-[11px] text-slate-400">{notes.length} páginas</p>
          </div>
        </div>
        <div className="relative">
          <Search className="absolute top-2.5 left-3 h-4 w-4 text-slate-500" />
          <input
            value={searchQuery}
            onChange={(e) => onSearchChange(e.target.value)}
            placeholder="Buscar título, path ou conteúdo..."
            className="w-full rounded-lg border border-slate-700 bg-slate-900 py-1.5 pr-3 pl-9 text-xs text-slate-100 placeholder:text-slate-500 focus:border-teal-600 focus:outline-none"
          />
        </div>
      </div>

      <div className="space-y-2 border-b border-slate-800 p-3 text-xs">
        <div className="flex items-center justify-between">
          <span className="text-[10px] font-semibold tracking-wider text-slate-500 uppercase">
            Categorias
          </span>
          <button
            type="button"
            onClick={() => setSortBy((s) => (s === 'title' ? 'category' : 'title'))}
            className="text-[10px] text-teal-400 hover:text-teal-300"
          >
            ordenar: {sortBy}
          </button>
        </div>
        <div className="flex max-h-28 flex-wrap gap-1.5 overflow-y-auto">
          <button
            type="button"
            onClick={() => onSelectCategory(null)}
            className={`rounded-full px-2 py-0.5 text-[11px] ${
              !selectedCategory
                ? 'bg-teal-700 text-white'
                : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
            }`}
          >
            Todas
          </button>
          {categories.map((cat) => (
            <button
              key={cat}
              type="button"
              onClick={() => onSelectCategory(selectedCategory === cat ? null : cat)}
              className={`inline-flex max-w-full items-center gap-1 truncate rounded-full px-2 py-0.5 text-[11px] ${
                selectedCategory === cat
                  ? 'bg-teal-700 text-white'
                  : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
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
        <p className="mb-2 px-2 text-[10px] font-semibold tracking-wider text-slate-500 uppercase">
          Notas ({filtered.length})
        </p>
        <ul className="space-y-0.5">
          {filtered.map((note) => (
            <li key={note.id}>
              <button
                type="button"
                onClick={() => onSelectNote(note.id)}
                className={`w-full rounded-lg px-2.5 py-2 text-left transition ${
                  selectedNoteId === note.id
                    ? 'bg-teal-900/60 text-teal-50 ring-1 ring-teal-600/50'
                    : 'hover:bg-slate-900'
                }`}
              >
                <div className="truncate text-xs font-semibold">{note.title}</div>
                <div className="mt-0.5 truncate font-mono text-[10px] text-slate-500">
                  {note.path}
                </div>
              </button>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
