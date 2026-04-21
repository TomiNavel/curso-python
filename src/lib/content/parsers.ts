import type { Exercise, QA } from '../../types/course';

export function filenameToTitle(filename: string): string {
  const base = filename.replace('.py', '').replace(/^\d+-/, '');
  return base.replace(/([A-Z])/g, ' $1').trim();
}

export function parseExercisePy(filename: string, content: string): Omit<Exercise, 'solution'> {
  const title = filenameToTitle(filename);
  const docMatch = content.match(/^"""([\s\S]*?)"""\s*/);
  const desc = docMatch ? docMatch[1].trim() : '';
  const starter = docMatch ? content.slice(docMatch[0].length).trimStart() : content;
  return { title, desc, starter };
}

export function parseQA(md: string): QA[] {
  const blocks = md
    .split(/\n(?=###\s*R\d+\.)/)
    .filter(b => /^###\s*R\d+\./.test(b.trim()));

  return blocks.map(block => {
    const titleMatch = block.match(/^###\s*R\d+\.\s*(.+)/);
    const title = titleMatch ? titleMatch[1].trim() : '';

    const body = block.replace(/^###\s*R\d+\.\s*.+\n?/, '').trim();

    return { q: title, a: body };
  }).filter(x => x.q);
}

export function parseErrors(md: string): QA[] {
  if (!md) return [];
  const body = md.replace(/^#\s.+\n?/, '');
  const blocks = body
    .split(/\n(?=##\s+Error\s+\d+)/i)
    .filter(b => /^##\s+Error\s+\d+/i.test(b.trim()));

  return blocks.map(block => {
    const titleMatch = block.match(/^##\s+Error\s+\d+\s*[:.-]?\s*(.+)/i);
    const title = titleMatch ? titleMatch[1].trim() : '';
    const content = block
      .replace(/^##\s+Error\s+\d+.*\n?/i, '')
      .replace(/\n---\s*$/, '')
      .trim();
    return { q: title, a: content };
  }).filter(x => x.q);
}

// Splits markdown into code-fence and non-code segments so section/heading
// regexes only run over prose, never over code.
interface Segment { kind: 'code' | 'prose'; text: string }

export function splitCodeFences(content: string): Segment[] {
  const re = /```\w*\n[\s\S]*?```/g;
  const segments: Segment[] = [];
  let last = 0;
  let m: RegExpExecArray | null;
  while ((m = re.exec(content)) !== null) {
    if (m.index > last) segments.push({ kind: 'prose', text: content.slice(last, m.index) });
    segments.push({ kind: 'code', text: m[0] });
    last = m.index + m[0].length;
  }
  if (last < content.length) segments.push({ kind: 'prose', text: content.slice(last) });
  return segments;
}

export function extractSection(fullMd: string, subtopicId: string | null): string {
  if (!subtopicId) return fullMd;
  const startRe = new RegExp(`^## ${subtopicId.replace('.', '\\.')}[.\\s]`);
  const segments = splitCodeFences(fullMd);
  const out: string[] = [];
  let inSection = false;
  let found = false;

  for (const seg of segments) {
    if (seg.kind === 'code') {
      if (inSection) out.push(seg.text);
      continue;
    }
    const lines = seg.text.split('\n');
    for (const line of lines) {
      if (/^## /.test(line)) {
        if (inSection) { inSection = false; break; }
        if (startRe.test(line)) { inSection = true; found = true; out.push(line); continue; }
      }
      if (inSection) out.push(line);
    }
    if (found && !inSection) break;
  }
  return out.length > 0 ? out.join('\n') : fullMd;
}
