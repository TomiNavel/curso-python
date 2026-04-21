import type { Selection } from '../types/course';

// Hash format: #/{topicId}                — topic without subtopic
//              #/{topicId}/{subtopicId}    — specific subtopic
// Empty or unparseable hash => null (home).
export function parseHash(hash: string): Selection | null {
  const m = hash.match(/^#\/(\d+)(?:\/([\d.]+))?$/);
  if (!m) return null;
  return { topicId: Number(m[1]), subtopicId: m[2] ?? null };
}

export function toHash(sel: Selection | null): string {
  if (!sel) return '';
  return sel.subtopicId ? `#/${sel.topicId}/${sel.subtopicId}` : `#/${sel.topicId}`;
}
