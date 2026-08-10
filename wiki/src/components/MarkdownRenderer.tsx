import { useMemo } from 'react';
import Markdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { ExternalLink, Link as LinkIcon, Copy, Check, Terminal } from 'lucide-react';
import { useState } from 'react';
import type { Note } from '../types';
import { replaceWikiLinksForRender, rewriteContentAssetUrls } from '../lib/noteUtils';

interface MarkdownRendererProps {
  content: string;
  notePath: string;
  allNotes: Note[];
  onNavigateToNote?: (noteId: string) => void;
}

function CodeBlock({ language, code }: { language: string; code: string }) {
  const [copied, setCopied] = useState(false);
  return (
    <div className="my-4 overflow-hidden rounded-xl border border-slate-800 bg-slate-900 text-slate-100">
      <div className="flex items-center justify-between border-b border-slate-800 bg-slate-950/80 px-4 py-2 text-xs text-slate-400">
        <div className="flex items-center gap-2">
          <Terminal className="h-3.5 w-3.5 text-teal-400" />
          <span className="font-semibold tracking-wider text-slate-300 uppercase">
            {language || 'code'}
          </span>
        </div>
        <button
          type="button"
          onClick={() => {
            void navigator.clipboard.writeText(code);
            setCopied(true);
            setTimeout(() => setCopied(false), 1600);
          }}
          className="inline-flex items-center gap-1 rounded bg-slate-800 px-2 py-1 text-[11px] text-slate-300 hover:bg-slate-700"
        >
          {copied ? <Check className="h-3 w-3 text-teal-400" /> : <Copy className="h-3 w-3" />}
          {copied ? 'Copiado' : 'Copiar'}
        </button>
      </div>
      <pre className="overflow-x-auto p-4 font-mono text-xs leading-relaxed text-teal-200/90">
        <code>{code}</code>
      </pre>
    </div>
  );
}

export function MarkdownRenderer({
  content,
  notePath,
  allNotes,
  onNavigateToNote,
}: MarkdownRendererProps) {
  const processed = useMemo(() => {
    const notesByTitle = new Map(allNotes.map((n) => [n.title.toLowerCase(), n]));
    const withAssets = rewriteContentAssetUrls(content, notePath);
    return replaceWikiLinksForRender(withAssets, notesByTitle);
  }, [content, notePath, allNotes]);

  return (
    <div className="prose prose-slate max-w-none text-slate-800">
      <Markdown
        remarkPlugins={[remarkGfm]}
        components={{
          h1: ({ children }) => (
            <h1 className="mt-6 mb-4 border-b border-slate-200 pb-2 text-2xl font-bold tracking-tight md:text-3xl">
              {children}
            </h1>
          ),
          h2: ({ children }) => (
            <h2 className="mt-6 mb-3 border-b border-slate-100 pb-2 text-xl font-bold md:text-2xl">
              {children}
            </h2>
          ),
          h3: ({ children }) => (
            <h3 className="mt-5 mb-2 text-lg font-semibold text-slate-800">{children}</h3>
          ),
          p: ({ children }) => (
            <p className="my-3 text-sm leading-relaxed text-slate-700 md:text-base">{children}</p>
          ),
          pre: ({ children }) => <div className="my-3">{children}</div>,
          code: ({ className, children, ...props }) => {
            const match = /language-(\w+)/.exec(className || '');
            const codeString = String(children).replace(/\n$/, '');
            const inline = !match && !codeString.includes('\n');
            if (inline) {
              return (
                <code
                  className="rounded border border-slate-200 bg-slate-100 px-1.5 py-0.5 font-mono text-[0.875em] text-teal-900"
                  {...props}
                >
                  {children}
                </code>
              );
            }
            return <CodeBlock language={match?.[1] ?? ''} code={codeString} />;
          },
          a: ({ href, children }) => {
            if (!href) return <span>{children}</span>;
            if (href.startsWith('#wiki-note-')) {
              const id = href.replace('#wiki-note-', '');
              return (
                <button
                  type="button"
                  onClick={() => onNavigateToNote?.(id)}
                  className="my-0.5 inline-flex items-center gap-1 rounded border border-teal-300/80 bg-teal-50 px-2 py-0.5 text-[0.9em] font-semibold text-teal-800 hover:bg-teal-100"
                >
                  <LinkIcon className="h-3 w-3" />
                  {children}
                </button>
              );
            }
            if (href.startsWith('#wiki-create-')) {
              return (
                <span className="my-0.5 inline-flex items-center gap-1 rounded border border-dashed border-amber-300 bg-amber-50 px-2 py-0.5 text-[0.9em] text-amber-900">
                  {children}
                </span>
              );
            }
            return (
              <a
                href={href}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1 font-semibold text-teal-700 underline decoration-teal-300 underline-offset-2"
              >
                {children}
                <ExternalLink className="h-3 w-3" />
              </a>
            );
          },
          ul: ({ children }) => (
            <ul className="my-3 ml-6 list-disc space-y-1.5 text-sm text-slate-700 md:text-base">
              {children}
            </ul>
          ),
          ol: ({ children }) => (
            <ol className="my-3 ml-6 list-decimal space-y-1.5 text-sm text-slate-700 md:text-base">
              {children}
            </ol>
          ),
          blockquote: ({ children }) => (
            <blockquote className="my-4 rounded-r-lg border-y border-r border-l-4 border-teal-500 border-y-teal-100 border-r-teal-100 bg-teal-50/60 py-2 pr-3 pl-4 text-sm text-slate-700 italic">
              {children}
            </blockquote>
          ),
          table: ({ children }) => (
            <div className="my-5 overflow-x-auto rounded-xl border border-slate-200">
              <table className="w-full border-collapse bg-white text-left text-sm">{children}</table>
            </div>
          ),
          th: ({ children }) => (
            <th className="bg-slate-100 px-4 py-3 font-semibold text-slate-800">{children}</th>
          ),
          td: ({ children }) => <td className="px-4 py-2.5 text-slate-700">{children}</td>,
        }}
      >
        {processed}
      </Markdown>
    </div>
  );
}
