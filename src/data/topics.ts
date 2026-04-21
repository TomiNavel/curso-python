// Public topic list consumed by the UI. Metadata (title, subtopics) comes from
// the parsed index; folder presence comes from the lazy registry.

import type { Topic } from '../types/course';
import { TOPIC_META } from './index';
import { hasLesson } from './content';

const TOPICS: Topic[] = TOPIC_META.map(meta => ({
  id: meta.id,
  title: meta.title,
  subtopics: meta.subtopics,
  folder: hasLesson(meta.id) ? `topic-${meta.id}` : undefined,
}));

export default TOPICS;
