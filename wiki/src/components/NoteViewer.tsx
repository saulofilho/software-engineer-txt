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
    <div className="panel flex h-full flex-col overflow-hidden rounded-lg">
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-neon/10 bg-black/30 px-6 py-4">
        <div className="flex flex-wrap items-center gap-2">
          <span className="chip inline-flex items-center gap-1.5 rounded-sm px-2.5 py-1 font-mono text-xs font-semibold tracking-wider uppercase">
            <Folder className="h-3.5 w-3.5" />
            {note.category}
          </span>
          <span className="font-mono text-[11px] text-fog">{note.path}</span>
        </div>
        <a
          href={`https://github.com/saulofilho/software-engineer-txt/blob/main/${note.path}`}
          target="_blank"
          rel="noopener noreferrer"
          className="rounded-md border border-hot/30 bg-hot/10 px-3 py-1.5 font-mono text-xs font-medium text-hot hover:bg-hot/20"
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

        <div className="mt-12 border-t border-neon/15 pt-8">
          <h3 className="font-display mb-4 flex items-center gap-2 text-sm font-semibold tracking-[0.18em] text-fog uppercase">
            <LinkIcon className="h-4 w-4 text-neon" />
            Backlinks ({backlinks.length})
          </h3>
          {backlinks.length === 0 ? (
            <p className="font-mono text-xs text-fog italic">
              Nenhuma outra nota aponta para esta ainda. Use{' '}
              <code className="rounded border border-neon/20 bg-black/40 px-1 text-neon">
                [[{note.title}]]
              </code>{' '}
              em outras páginas.
            </p>
          ) : (
            <div className="grid grid-cols-1 gap-3 md:grid-cols-2">
              {backlinks.map((bl) => (
                <button
                  key={bl.id}
                  type="button"
                  onClick={() => onNavigateToNote(bl.id)}
                  className="rounded-md border border-neon/15 bg-black/30 p-3 text-left transition hover:border-neon/40 hover:bg-neon/5"
                >
                  <div className="mb-1 flex items-center gap-1.5 text-xs font-semibold text-neon">
                    <LinkIcon className="h-3 w-3" />
                    {bl.title}
                  </div>
                  <p className="truncate font-mono text-[11px] text-fog">{bl.path}</p>
                </button>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
