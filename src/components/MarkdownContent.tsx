import { marked } from '../lib/markdown';
import RunableBlock from './RunableBlock';

interface Part {
  type: 'md' | 'code';
  text?: string;
  lang?: string;
  code?: string;
  key: number;
}

// Python fences become interactive RunableBlocks. Other languages (bash, json,
// plain text) stay in the markdown stream so `marked` can syntax-highlight them.
function splitMarkdown(content: string): Part[] {
  const parts: Part[] = [];
  const re = /```(\w*)\n([\s\S]*?)```/g;
  let last = 0, m: RegExpExecArray | null, key = 0;
  while ((m = re.exec(content)) !== null) {
    const lang = m[1];
    const isPython = !lang || lang === 'python' || lang === 'py';
    if (!isPython) continue; // leave it in the markdown stream for marked/hljs
    if (m.index > last) parts.push({ type: 'md', text: content.slice(last, m.index), key: key++ });
    parts.push({ type: 'code', lang, code: m[2].trimEnd(), key: key++ });
    last = m.index + m[0].length;
  }
  if (last < content.length) parts.push({ type: 'md', text: content.slice(last), key: key++ });
  return parts;
}

interface Props {
  content: string;
  compact?: boolean;
}

export default function MarkdownContent({ content, compact = false }: Props) {
  const parts = splitMarkdown(content);
  return (
    <div className={compact ? 'markdown-compact' : 'markdown-body max-w-190'}>
      {parts.map(p =>
        p.type === 'md'
          ? <div key={p.key} dangerouslySetInnerHTML={{ __html: marked.parse(p.text!) as string }} />
          : <RunableBlock key={p.key} initialCode={p.code!} lang={p.lang!} />
      )}
    </div>
  );
}
