import { useMemo, useState } from 'react';
import { Network, Search, Folder, FileText, Menu, X } from 'lucide-react';
import type { Note, ViewMode } from './types';
import { loadNotesBundle } from './lib/loadNotes';
import { buildGraphData, getBacklinks } from './lib/noteUtils';
import { AtlasMark } from './components/AtlasMark';
import { Sidebar } from './components/Sidebar';
import { NoteViewer } from './components/NoteViewer';
import { GraphView } from './components/GraphView';

export default function App() {
  const { notes } = useMemo(() => loadNotesBundle(), []);
  const [selectedNoteId, setSelectedNoteId] = useState(notes[0]?.id ?? '');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [viewMode, setViewMode] = useState<ViewMode>('read');
  const [mobileOpen, setMobileOpen] = useState(false);

  const categories = useMemo(() => {
    return [...new Set(notes.map((n) => n.category))].sort((a, b) =>
      a.localeCompare(b, 'pt-BR')
    );
  }, [notes]);

  const selectedNote = useMemo(
    () => notes.find((n) => n.id === selectedNoteId) ?? notes[0] ?? null,
    [notes, selectedNoteId]
  );

  const backlinks = useMemo(() => {
    if (!selectedNote) return [] as Note[];
    return getBacklinks(notes, selectedNote.id);
  }, [notes, selectedNote]);

  const graphData = useMemo(() => buildGraphData(notes), [notes]);

  const handleSelectNote = (id: string) => {
    setSelectedNoteId(id);
    setViewMode('read');
    setMobileOpen(false);
  };

  return (
    <div className="flex h-screen w-screen flex-col overflow-hidden bg-void text-slate-100">
      <header className="scan-header flex shrink-0 items-center justify-between bg-black/70 px-4 py-3 backdrop-blur-md">
        <div className="flex items-center gap-3">
          <button
            type="button"
            className="rounded-md border border-neon/20 p-1.5 text-neon hover:bg-neon/10 lg:hidden"
            onClick={() => setMobileOpen((v) => !v)}
            aria-label="Menu"
          >
            {mobileOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
          </button>
          <div className="flex items-center gap-3">
            <div className="mark-glow flex h-10 w-10 items-center justify-center rounded-md border border-neon/40 bg-panel text-neon">
              <AtlasMark className="h-6 w-6" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="font-display text-base font-bold tracking-[0.14em] uppercase neon-text">
                  Software Engineer Atlas
                </h1>
                <span className="chip rounded px-2 py-0.5 font-mono text-[10px] font-bold tracking-[0.22em] uppercase">
                  Studies
                </span>
              </div>
              <p className="font-mono text-[11px] text-fog">
                {notes.length} notas · grafo de conceitos · fonte: Git
              </p>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-1 rounded-md border border-neon/20 bg-panel p-1 font-mono text-xs">
          <button
            type="button"
            onClick={() => setViewMode('read')}
            className={`flex items-center gap-1.5 rounded-sm px-3 py-1.5 uppercase tracking-wider transition ${
              viewMode === 'read'
                ? 'bg-neon/15 font-semibold text-neon neon-border'
                : 'text-fog hover:bg-white/5 hover:text-ice'
            }`}
          >
            <FileText className="h-3.5 w-3.5" />
            Wiki
          </button>
          <button
            type="button"
            onClick={() => setViewMode('graph')}
            className={`flex items-center gap-1.5 rounded-sm px-3 py-1.5 uppercase tracking-wider transition ${
              viewMode === 'graph'
                ? 'bg-hot/15 font-semibold text-hot'
                : 'text-fog hover:bg-white/5 hover:text-ice'
            }`}
          >
            <Network className="h-3.5 w-3.5" />
            Grafo
          </button>
        </div>
      </header>

      <div className="relative flex flex-1 gap-4 overflow-hidden p-3">
        {mobileOpen && (
          <button
            type="button"
            className="fixed inset-0 z-30 bg-void/70 lg:hidden"
            aria-label="Fechar menu"
            onClick={() => setMobileOpen(false)}
          />
        )}

        <aside
          className={`fixed inset-y-0 left-0 z-40 w-80 p-3 transition-transform duration-300 lg:static lg:translate-x-0 lg:p-0 ${
            mobileOpen ? 'translate-x-0' : '-translate-x-full'
          }`}
        >
          <Sidebar
            notes={notes}
            categories={categories}
            selectedNoteId={selectedNote?.id}
            searchQuery={searchQuery}
            onSearchChange={setSearchQuery}
            selectedCategory={selectedCategory}
            onSelectCategory={setSelectedCategory}
            onSelectNote={handleSelectNote}
          />
        </aside>

        <main className="flex min-w-0 flex-1 flex-col overflow-hidden rounded-lg border border-neon/10 bg-black/20 p-1">
          {viewMode === 'graph' ? (
            <div className="flex h-full flex-col gap-3">
              <div className="panel flex items-center justify-between rounded-lg px-3 py-2 text-xs">
                <div className="flex items-center gap-2 text-fog">
                  <Network className="h-4 w-4 text-hot" />
                  <span className="font-display font-semibold tracking-wider text-slate-100 uppercase">
                    Mapa de conexões
                  </span>
                  <span className="hidden text-neon/40 md:inline">//</span>
                  <span className="hidden font-mono md:inline">
                    {graphData.nodes.length} nós · {graphData.links.length} links
                  </span>
                </div>
                <button
                  type="button"
                  onClick={() => setViewMode('read')}
                  className="chip rounded px-2.5 py-1 font-mono font-medium uppercase tracking-wider"
                >
                  Voltar
                </button>
              </div>
              <div className="min-h-0 flex-1">
                <GraphView
                  nodes={graphData.nodes}
                  links={graphData.links}
                  selectedNoteId={selectedNote?.id}
                  onSelectNode={(id, _title, isConcept) => {
                    if (!isConcept) handleSelectNote(id);
                  }}
                />
              </div>
            </div>
          ) : selectedNote ? (
            <NoteViewer
              note={selectedNote}
              allNotes={notes}
              backlinks={backlinks}
              onNavigateToNote={handleSelectNote}
            />
          ) : (
            <div className="panel flex h-full flex-col items-center justify-center rounded-lg p-8 text-center">
              <Search className="mb-3 h-10 w-10 text-neon/40" />
              <h2 className="font-display mb-1 text-lg font-bold uppercase tracking-widest">
                Nenhuma nota
              </h2>
              <p className="font-mono text-xs text-fog">Rode npm run ingest na pasta wiki/</p>
            </div>
          )}
        </main>
      </div>

      <div className="pointer-events-none fixed bottom-3 right-3 hidden items-center gap-1 rounded border border-neon/20 bg-black/70 px-2 py-1 font-mono text-[10px] text-fog backdrop-blur-sm sm:flex">
        <Folder className="h-3 w-3 text-neon" />
        pasta = categoria · edição via Git
      </div>
    </div>
  );
}
