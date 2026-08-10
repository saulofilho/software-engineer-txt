import { Folder, Link as LinkIcon } from 'lucide-react';
import type { Note } from '../types';
import { MarkdownRenderer } from './MarkdownRenderer';

interface NoteViewerProps {
  note: Note;
  allNotes: Note[];
  backlinks: Note[];
  onNavigateToNote: (id: string) => void;
}

export function NoteViewer({
  note,
  allNotes,
  backlinks,
  onNavigateToNote,
}: NoteViewerProps) {
  return (
    <div className="flex h-full flex-col overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm">
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-200 bg-slate-50/80 px-6 py-4">
        <div className="flex flex-wrap items-center gap-2">
          <span className="inline-flex items-center gap-1.5 rounded-md bg-slate-200/80 px-2.5 py-1 text-xs font-semibold tracking-wider text-slate-600 uppercase">
            <Folder className="h-3.5 w-3.5" />
            {note.category}
          </span>
          <span className="font-mono text-[11px] text-slate-400">{note.path}</span>
        </div>
        <a
          href={`https://github.com/saulofilho/software-engineer-txt/blob/main/${note.path}`}
          target="_blank"
          rel="noopener noreferrer"
          className="rounded-lg border border-slate-300 bg-white px-3 py-1.5 text-xs font-medium text-slate-700 hover:bg-slate-100"
        >
          Editar no GitHub
        </a>
      </div>

      <div className="flex-1 overflow-y-auto p-6 md:p-8">
        <MarkdownRenderer
          content={note.content}
          notePath={note.path}
          allNotes={allNotes}
          onNavigateToNote={onNavigateToNote}
        />

        <div className="mt-12 border-t border-slate-200 pt-8">
          <h3 className="mb-4 flex items-center gap-2 text-sm font-semibold tracking-wider text-slate-500 uppercase">
            <LinkIcon className="h-4 w-4 text-teal-700" />
            Backlinks ({backlinks.length})
          </h3>
          {backlinks.length === 0 ? (
            <p className="text-xs text-slate-400 italic">
              Nenhuma outra nota aponta para esta ainda. Use{' '}
              <code className="rounded bg-slate-100 px-1">[[{note.title}]]</code> em outras
              páginas.
            </p>
          ) : (
            <div className="grid grid-cols-1 gap-3 md:grid-cols-2">
              {backlinks.map((bl) => (
                <button
                  key={bl.id}
                  type="button"
                  onClick={() => onNavigateToNote(bl.id)}
                  className="rounded-lg border border-slate-200 bg-slate-50 p-3 text-left transition hover:bg-slate-100"
                >
                  <div className="mb-1 flex items-center gap-1.5 text-xs font-semibold text-teal-700">
                    <LinkIcon className="h-3 w-3" />
                    {bl.title}
                  </div>
                  <p className="truncate font-mono text-[11px] text-slate-500">{bl.path}</p>
                </button>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
