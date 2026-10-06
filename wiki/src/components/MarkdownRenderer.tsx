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
    <div className="my-4 overflow-hidden rounded-md border border-neon/20 bg-[#06080d] text-slate-100">
      <div className="flex items-center justify-between border-b border-neon/15 bg-black/50 px-4 py-2 font-mono text-xs text-fog">
        <div className="flex items-center gap-2">
          <Terminal className="h-3.5 w-3.5 text-neon" />
          <span className="font-semibold tracking-[0.16em] text-neon uppercase">
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
          className="inline-flex items-center gap-1 rounded-sm border border-white/10 bg-white/5 px-2 py-1 text-[11px] text-fog hover:border-neon/40 hover:text-neon"
        >
          {copied ? <Check className="h-3 w-3 text-neon" /> : <Copy className="h-3 w-3" />}
          {copied ? 'Copiado' : 'Copiar'}
        </button>
      </div>
      <pre className="overflow-x-auto p-4 font-mono text-xs leading-relaxed text-neon/90">
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
    <div className="prose max-w-none prose-invert">
      <Markdown
        remarkPlugins={[remarkGfm]}
        components={{
          h1: ({ children }) => (
            <h1 className="font-display mt-6 mb-4 border-b border-neon/20 pb-2 text-2xl font-bold tracking-tight text-slate-50 neon-text md:text-3xl">
              {children}
            </h1>
          ),
          h2: ({ children }) => (
            <h2 className="font-display mt-6 mb-3 border-b border-hot/20 pb-2 text-xl font-bold text-slate-100 md:text-2xl">
              {children}
            </h2>
          ),
          h3: ({ children }) => (
            <h3 className="font-display mt-5 mb-2 text-lg font-semibold text-ice">{children}</h3>
          ),
          p: ({ children }) => (
            <p className="my-3 text-sm leading-relaxed text-slate-300 md:text-base">{children}</p>
          ),
          pre: ({ children }) => <div className="my-3">{children}</div>,
          code: ({ className, children, ...props }) => {
            const match = /language-(\w+)/.exec(className || '');
            const codeString = String(children).replace(/\n$/, '');
            const inline = !match && !codeString.includes('\n');
            if (inline) {
              return (
                <code
                  className="rounded-sm border border-neon/20 bg-neon/10 px-1.5 py-0.5 font-mono text-[0.875em] text-neon"
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
                  className="my-0.5 inline-flex items-center gap-1 rounded-sm border border-neon/30 bg-neon/10 px-2 py-0.5 text-[0.9em] font-semibold text-neon hover:bg-neon/20"
                >
                  <LinkIcon className="h-3 w-3" />
                  {children}
                </button>
              );
            }
            if (href.startsWith('#wiki-create-')) {
              return (
                <span className="chip-hot my-0.5 inline-flex items-center gap-1 rounded-sm px-2 py-0.5 text-[0.9em]">
                  {children}
                </span>
              );
            }
            return (
              <a
                href={href}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1 font-semibold text-ice underline decoration-ice/40 underline-offset-2 hover:text-neon"
              >
                {children}
                <ExternalLink className="h-3 w-3" />
              </a>
            );
          },
          ul: ({ children }) => (
            <ul className="my-3 ml-6 list-disc space-y-1.5 text-sm text-slate-300 md:text-base">
              {children}
            </ul>
          ),
          ol: ({ children }) => (
            <ol className="my-3 ml-6 list-decimal space-y-1.5 text-sm text-slate-300 md:text-base">
              {children}
            </ol>
          ),
          blockquote: ({ children }) => (
            <blockquote className="my-4 rounded-r-md border-y border-r border-l-4 border-neon/20 border-l-neon bg-neon/5 py-2 pr-3 pl-4 text-sm text-slate-300 italic">
              {children}
            </blockquote>
          ),
          table: ({ children }) => (
            <div className="my-5 overflow-x-auto rounded-md border border-neon/20">
              <table className="w-full border-collapse bg-black/30 text-left text-sm">{children}</table>
            </div>
          ),
          th: ({ children }) => (
            <th className="bg-neon/10 px-4 py-3 font-display font-semibold tracking-wide text-neon">
              {children}
            </th>
          ),
          td: ({ children }) => (
            <td className="border-t border-white/5 px-4 py-2.5 text-slate-300">{children}</td>
          ),
        }}
      >
        {processed}
      </Markdown>
    </div>
  );
}
