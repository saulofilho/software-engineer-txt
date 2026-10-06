export function AtlasMark({ className = 'h-5 w-5' }: { className?: string }) {
  return (
    <svg viewBox="0 0 32 32" className={className} aria-hidden>
      <polygon
        points="16,3.4 27.8,10.2 27.8,21.8 16,28.6 4.2,21.8 4.2,10.2"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.6"
      />
      <circle cx="16" cy="16" r="2.4" fill="#ff2d95" />
      <circle cx="16" cy="7.6" r="1.2" fill="currentColor" />
      <circle cx="24.2" cy="12" r="1.2" fill="currentColor" />
      <circle cx="24.2" cy="20" r="1.2" fill="currentColor" />
      <circle cx="16" cy="24.4" r="1.2" fill="currentColor" />
      <circle cx="7.8" cy="20" r="1.2" fill="currentColor" />
      <circle cx="7.8" cy="12" r="1.2" fill="currentColor" />
      <g stroke="currentColor" strokeWidth="1" opacity="0.75">
        <line x1="16" y1="16" x2="16" y2="7.6" />
        <line x1="16" y1="16" x2="24.2" y2="12" />
        <line x1="16" y1="16" x2="24.2" y2="20" />
        <line x1="16" y1="16" x2="16" y2="24.4" />
        <line x1="16" y1="16" x2="7.8" y2="20" />
        <line x1="16" y1="16" x2="7.8" y2="12" />
      </g>
    </svg>
  );
}
