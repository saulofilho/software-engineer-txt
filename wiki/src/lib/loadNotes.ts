import type { NotesBundle } from '../types';
import bundle from '../generated/notes.json';

export function loadNotesBundle(): NotesBundle {
  return bundle as NotesBundle;
}
