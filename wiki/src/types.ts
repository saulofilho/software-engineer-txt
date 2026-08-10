import type { SimulationLinkDatum, SimulationNodeDatum } from 'd3';

export interface Note {
  id: string;
  title: string;
  path: string;
  category: string;
  content: string;
  outboundIds: string[];
}

export interface NotesBundle {
  generatedAt: string;
  count: number;
  notes: Note[];
}

export interface GraphNode extends SimulationNodeDatum {
  id: string;
  title: string;
  type: 'note' | 'concept' | 'orphan';
  category: string;
  val: number;
}

export interface GraphLink extends SimulationLinkDatum<GraphNode> {
  source: string | GraphNode;
  target: string | GraphNode;
}

export type ViewMode = 'read' | 'graph';
