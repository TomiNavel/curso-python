// Course index: parses src/Temario/00-temas.md at build time to extract topic
// and subtopic metadata (titles + ids). This is the ONLY content-related file
// loaded eagerly — the actual lesson/exercise/interview bodies are lazy.
//
// Format expected in 00-temas.md:
//   ## N. Topic Title
//   - **N.M. Subtopic Title**
//     - (further nested items are ignored)

import indexMd from '/src/Temario/00-temas.md?raw';
import type { Subtopic } from '../types/course';

export interface TopicMeta {
  id: number;
  title: string;
  subtopics: Subtopic[];
}

function parseIndex(md: string): TopicMeta[] {
  const topics: TopicMeta[] = [];
  const lines = md.split('\n');
  let current: TopicMeta | null = null;

  for (const line of lines) {
    const topicMatch = line.match(/^##\s+(\d+)\.\s+(.+?)\s*$/);
    if (topicMatch) {
      current = { id: Number(topicMatch[1]), title: topicMatch[2], subtopics: [] };
      topics.push(current);
      continue;
    }
    if (!current) continue;
    const subMatch = line.match(/^-\s+\*\*(\d+\.\d+)\.\s+(.+?)\*\*\s*$/);
    if (subMatch) current.subtopics.push({ id: subMatch[1], title: subMatch[2] });
  }
  return topics;
}

export const TOPIC_META: TopicMeta[] = parseIndex(indexMd);
