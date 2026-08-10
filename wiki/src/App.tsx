import { useMemo, useState } from 'react';
import { BookOpen, Network, Search, Folder, FileText, Menu, X } from 'lucide-react';
import type { Note, ViewMode } from './types';
import { loadNotesBundle } from './lib/loadNotes';
import { buildGraphData, getBacklinks } from './lib/noteUtils';
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
    <div className="flex h-screen w-screen flex-col overflow-hidden bg-slate-100 text-slate-900">
      <header className="flex shrink-0 items-center justify-between border-b border-slate-800 bg-slate-950 px-4 py-3 text-white">
        <div className="flex items-center gap-3">
          <button
            type="button"
            className="rounded-lg p-1.5 text-slate-300 hover:bg-slate-800 lg:hidden"
            onClick={() => setMobileOpen((v) => !v)}
            aria-label="Menu"
          >
            {mobileOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
          </button>
          <div className="flex items-center gap-2.5">
            <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-teal-700">
              <BookOpen className="h-5 w-5 text-teal-50" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-base font-bold tracking-tight">Software Engineer Atlas</h1>
                <span className="rounded border border-teal-500/40 bg-teal-950 px-2 py-0.5 text-[10px] font-bold uppercase tracking-widest text-teal-300">
                  Studies
                </span>
              </div>
              <p className="font-mono text-[11px] text-slate-400">
                {notes.length} notas · grafo de conceitos · fonte: Git
              </p>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2 rounded-lg border border-slate-700 bg-slate-900 p-1 text-xs">
          <button
            type="button"
            onClick={() => setViewMode('read')}
            className={`flex items-center gap-1.5 rounded-md px-3 py-1.5 transition ${
              viewMode === 'read'
                ? 'bg-teal-700 font-semibold text-white'
                : 'text-slate-300 hover:bg-slate-800'
            }`}
          >
            <FileText className="h-3.5 w-3.5" />
            Wiki
          </button>
          <button
            type="button"
            onClick={() => setViewMode('graph')}
            className={`flex items-center gap-1.5 rounded-md px-3 py-1.5 transition ${
              viewMode === 'graph'
                ? 'bg-teal-700 font-semibold text-white'
                : 'text-slate-300 hover:bg-slate-800'
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
            className="fixed inset-0 z-30 bg-slate-950/50 lg:hidden"
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

        <main className="flex min-w-0 flex-1 flex-col overflow-hidden rounded-xl bg-slate-200/40 p-1">
          {viewMode === 'graph' ? (
            <div className="flex h-full flex-col gap-3">
              <div className="flex items-center justify-between rounded-xl border border-slate-200 bg-white px-3 py-2 text-xs">
                <div className="flex items-center gap-2 text-slate-600">
                  <Network className="h-4 w-4 text-teal-700" />
                  <span className="font-semibold text-slate-800">Mapa de conexões</span>
                  <span className="hidden md:inline text-slate-400">|</span>
                  <span className="hidden md:inline">
                    {graphData.nodes.length} nós · {graphData.links.length} links
                  </span>
                </div>
                <button
                  type="button"
                  onClick={() => setViewMode('read')}
                  className="rounded border border-teal-200 bg-teal-50 px-2.5 py-1 font-medium text-teal-800"
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
            <div className="flex h-full flex-col items-center justify-center rounded-xl border border-slate-200 bg-white p-8 text-center">
              <Search className="mb-3 h-10 w-10 text-slate-300" />
              <h2 className="mb-1 text-lg font-bold">Nenhuma nota</h2>
              <p className="text-xs text-slate-500">Rode npm run ingest na pasta wiki/</p>
            </div>
          )}
        </main>
      </div>

      <div className="pointer-events-none fixed bottom-3 right-3 hidden items-center gap-1 rounded-lg border border-slate-200 bg-white/90 px-2 py-1 text-[10px] text-slate-500 sm:flex">
        <Folder className="h-3 w-3" />
        pasta = categoria · edição via Git
      </div>
    </div>
  );
}
