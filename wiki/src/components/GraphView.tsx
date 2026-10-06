import { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import { Maximize2, Minimize2, RefreshCw, ZoomIn, ZoomOut } from 'lucide-react';
import type { GraphLink, GraphNode } from '../types';

interface GraphViewProps {
  nodes: GraphNode[];
  links: GraphLink[];
  selectedNoteId?: string;
  onSelectNode: (nodeId: string, nodeTitle: string, isConcept: boolean) => void;
}

export function GraphView({
  nodes,
  links,
  selectedNoteId,
  onSelectNode,
}: GraphViewProps) {
  const svgRef = useRef<SVGSVGElement | null>(null);
  const containerRef = useRef<HTMLDivElement | null>(null);
  const zoomRef = useRef<d3.ZoomBehavior<SVGSVGElement, unknown> | null>(null);
  const onSelectRef = useRef(onSelectNode);
  onSelectRef.current = onSelectNode;
  const [filterType, setFilterType] = useState<'all' | 'notes' | 'concepts'>('all');
  const [hovered, setHovered] = useState<GraphNode | null>(null);
  const [fullscreen, setFullscreen] = useState(false);

  useEffect(() => {
    if (!svgRef.current || !containerRef.current) return;

    d3.select(svgRef.current).selectAll('*').remove();

    const width = containerRef.current.clientWidth || 800;
    const height = containerRef.current.clientHeight || 500;

    let filteredNodes = [...nodes];
    if (filterType === 'notes') {
      filteredNodes = filteredNodes.filter((n) => n.type === 'note' || n.type === 'orphan');
    } else if (filterType === 'concepts') {
      filteredNodes = filteredNodes.filter((n) => n.type === 'concept');
    }

    const ids = new Set(filteredNodes.map((n) => n.id));
    const filteredLinks = links
      .filter((l) => {
        const s = typeof l.source === 'object' ? l.source.id : l.source;
        const t = typeof l.target === 'object' ? l.target.id : l.target;
        return ids.has(s) && ids.has(t);
      })
      .map((l) => ({ ...l }));

    const d3Nodes: GraphNode[] = filteredNodes.map((n) => ({ ...n }));

    const svg = d3
      .select(svgRef.current)
      .attr('width', width)
      .attr('height', height)
      .attr('viewBox', [0, 0, width, height].join(' '));

    const g = svg.append('g');
    const zoom = d3
      .zoom<SVGSVGElement, unknown>()
      .scaleExtent([0.1, 4])
      .on('zoom', (event) => {
        g.attr('transform', event.transform.toString());
      });
    zoomRef.current = zoom;
    svg.call(zoom);

    const simulation = d3
      .forceSimulation<GraphNode>(d3Nodes)
      .force(
        'link',
        d3
          .forceLink<GraphNode, GraphLink>(filteredLinks)
          .id((d) => d.id)
          .distance(90)
      )
      .force('charge', d3.forceManyBody().strength(-200))
      .force('center', d3.forceCenter(width / 2, height / 2))
      .force(
        'collision',
        d3.forceCollide().radius((d) => Math.max(14, ((d as GraphNode).val ?? 1) * 4 + 10))
      );

    const linkGroup = g
      .append('g')
      .selectAll('line')
      .data(filteredLinks)
      .enter()
      .append('line')
      .attr('stroke', '#00f5d4')
      .attr('stroke-opacity', 0.28)
      .attr('stroke-width', 1.15);

    const nodeGroup = g
      .append('g')
      .selectAll('g')
      .data(d3Nodes)
      .enter()
      .append('g')
      .attr('cursor', 'pointer')
      .on('click', (_event, d) =>
        onSelectRef.current(d.id, d.title, d.type === 'concept')
      )
      .on('mouseover', (_event, d) => setHovered(d))
      .on('mouseout', () => setHovered(null));

    nodeGroup
      .append('circle')
      .attr('r', (d) => Math.min(22, Math.max(6, 5 + d.val * 1.8)))
      .attr('fill', (d) => {
        if (d.id === selectedNoteId) return '#ff2d95';
        if (d.type === 'concept') return '#7c3aed';
        if (d.type === 'orphan') return '#64748b';
        return '#00f5d4';
      })
      .attr('stroke', (d) => (d.id === selectedNoteId ? '#ffb0d6' : '#0b1220'))
      .attr('stroke-width', 1.6);

    nodeGroup
      .append('text')
      .text((d) => (d.title.length > 22 ? `${d.title.slice(0, 20)}…` : d.title))
      .attr('x', (d) => Math.min(22, Math.max(6, 5 + d.val * 1.8)) + 6)
      .attr('y', 4)
      .attr('font-size', '11px')
      .attr('fill', '#9aa8bf')
      .attr('pointer-events', 'none');

    const drag = d3
      .drag<SVGGElement, GraphNode>()
      .on('start', (event, d) => {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
      })
      .on('drag', (event, d) => {
        d.fx = event.x;
        d.fy = event.y;
      })
      .on('end', (event, d) => {
        if (!event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
      });

    nodeGroup.call(drag);

    simulation.on('tick', () => {
      linkGroup
        .attr('x1', (d) => (d.source as GraphNode).x ?? 0)
        .attr('y1', (d) => (d.source as GraphNode).y ?? 0)
        .attr('x2', (d) => (d.target as GraphNode).x ?? 0)
        .attr('y2', (d) => (d.target as GraphNode).y ?? 0);
      nodeGroup.attr('transform', (d) => `translate(${d.x ?? 0},${d.y ?? 0})`);
    });

    return () => {
      simulation.stop();
    };
  }, [nodes, links, selectedNoteId, filterType, fullscreen]);

  const applyZoom = (factor: number) => {
    if (!svgRef.current || !zoomRef.current) return;
    d3.select(svgRef.current).transition().duration(250).call(zoomRef.current.scaleBy, factor);
  };

  const resetZoom = () => {
    if (!svgRef.current || !zoomRef.current) return;
    d3.select(svgRef.current)
      .transition()
      .duration(250)
      .call(zoomRef.current.transform, d3.zoomIdentity);
  };

  return (
    <div
      ref={containerRef}
      className={`relative flex flex-col overflow-hidden rounded-lg border border-neon/20 bg-[#07090e] ${
        fullscreen ? 'panel fixed inset-4 z-50' : 'h-[min(70vh,640px)] w-full'
      }`}
    >
      <div className="absolute top-3 left-3 z-10 flex items-center gap-1 rounded-md border border-neon/20 bg-black/70 px-2 py-1 font-mono text-xs backdrop-blur">
        {(['all', 'notes', 'concepts'] as const).map((f) => (
          <button
            key={f}
            type="button"
            onClick={() => setFilterType(f)}
            className={`rounded-sm px-2 py-0.5 uppercase tracking-wider ${
              filterType === f ? 'chip' : 'text-fog hover:bg-white/5 hover:text-ice'
            }`}
          >
            {f === 'all' ? 'Todos' : f === 'notes' ? 'Notas' : 'Conceitos'}
          </button>
        ))}
      </div>

      <div className="absolute top-3 right-3 z-10 flex gap-1 rounded-md border border-neon/20 bg-black/70 p-1 backdrop-blur">
        <button type="button" className="rounded-sm p-1.5 hover:bg-neon/10" onClick={() => applyZoom(1.3)}>
          <ZoomIn className="h-4 w-4 text-neon" />
        </button>
        <button type="button" className="rounded-sm p-1.5 hover:bg-neon/10" onClick={() => applyZoom(0.7)}>
          <ZoomOut className="h-4 w-4 text-neon" />
        </button>
        <button type="button" className="rounded-sm p-1.5 hover:bg-neon/10" onClick={resetZoom}>
          <RefreshCw className="h-4 w-4 text-neon" />
        </button>
        <button
          type="button"
          className="rounded-sm p-1.5 hover:bg-hot/15"
          onClick={() => setFullscreen((v) => !v)}
        >
          {fullscreen ? (
            <Minimize2 className="h-4 w-4 text-hot" />
          ) : (
            <Maximize2 className="h-4 w-4 text-hot" />
          )}
        </button>
      </div>

      {hovered && (
        <div className="panel absolute right-3 bottom-3 z-10 max-w-xs rounded-md px-3 py-2 font-mono text-xs text-white">
          <div className="font-display font-semibold tracking-wide text-neon">{hovered.title}</div>
          <p className="text-fog">
            {hovered.type === 'concept'
              ? 'Conceito (ainda sem página)'
              : hovered.type === 'orphan'
                ? 'Nota isolada'
                : `Nota · ${hovered.category}`}
          </p>
        </div>
      )}

      <svg ref={svgRef} className="h-full w-full cursor-grab active:cursor-grabbing" />
    </div>
  );
}
