import { useMemo, useState } from 'react';
import type { QA, InterviewExercise } from '../types/course';
import MarkdownContent from './MarkdownContent';
import RunableBlock from './RunableBlock';
import SubTabs from './SubTabs';
import { parseErrors, filenameToTitle } from '../lib/content/parsers';

interface Props {
  topicId: number;
  questions: QA[];
  errorsMd: string;
  interviewExercises: InterviewExercise[];
}

type SubTab = 'preguntas' | 'errores' | 'debug';

const DEBUG_START_TOPIC = 7;

export default function InterviewView({ topicId, questions, errorsMd, interviewExercises }: Props) {
  const [sub, setSub] = useState<SubTab>('preguntas');

  const tabs: { id: SubTab; label: string }[] = [
    { id: 'preguntas', label: 'Preguntas' },
    { id: 'errores', label: 'Errores comunes' },
    { id: 'debug', label: 'Ejercicios debug' },
  ];

  return (
    <div className="max-w-190 flex flex-col gap-2">
      <SubTabs
        tabs={tabs}
        active={sub}
        onChange={id => setSub(id as SubTab)}
      />
      {sub === 'preguntas' && <Preguntas questions={questions} />}
      {sub === 'errores' && <Errores md={errorsMd} />}
      {sub === 'debug' && <Debug exercises={interviewExercises} topicId={topicId} />}
    </div>
  );
}

function Accordion({ items, emptyText }: { items: QA[]; emptyText: string }) {
  const [open, setOpen] = useState<number | null>(null);

  if (items.length === 0) return <Empty text={emptyText} />;

  return (
    <section>
      {items.map((item, i) => (
        <div key={i} className="border border-border rounded-xl overflow-hidden mb-2.5">
          <button
            className={`w-full flex items-center justify-between bg-surface2 border-none cursor-pointer px-4 py-3.5 text-[14px] font-medium text-left gap-3 transition-colors hover:bg-surface2/80
              ${open === i ? 'text-accent2' : 'text-text'}`}
            onClick={() => setOpen(open === i ? null : i)}
          >
            <span>{item.q}</span>
            <span className="text-[10px] text-muted shrink-0">{open === i ? '▲' : '▼'}</span>
          </button>
          {open === i && (
            <div className="px-4 py-3.5 text-[14px] text-[#c0c0e0] leading-[1.7] bg-bg2 border-t border-border">
              <MarkdownContent content={item.a} compact />
            </div>
          )}
        </div>
      ))}
    </section>
  );
}

function Preguntas({ questions }: { questions: QA[] }) {
  return <Accordion items={questions} emptyText="No hay preguntas para este tema." />;
}

function Errores({ md }: { md: string }) {
  const errors = useMemo(() => parseErrors(md), [md]);
  return <Accordion items={errors} emptyText="No hay errores comunes documentados para este tema." />;
}

function Debug({ exercises, topicId }: { exercises: InterviewExercise[]; topicId: number }) {
  const runnable = exercises.filter(ex => ex.content);
  const [active, setActive] = useState(0);

  if (runnable.length === 0) {
    if (topicId < DEBUG_START_TOPIC) {
      return <Empty text={`Los ejercicios debug comienzan a partir del tema ${DEBUG_START_TOPIC}.`} />;
    }
    return <Empty text="En desarrollo" />;
  }

  const currentIdx = Math.min(active, runnable.length - 1);
  const current = runnable[currentIdx];
  const currentTitle = filenameToTitle(current.filename).replace(/^Debug\s*/i, '').trim();

  return (
    <section className="flex flex-col gap-5">
      <div className="sticky top-0 z-10 bg-surface -mx-4 md:-mx-12 px-4 md:px-12 py-3 flex gap-1.5 flex-wrap border-b border-border">
        {runnable.map((_, i) => (
          <button
            key={i}
            onClick={() => setActive(i)}
            className={`w-9 h-9 rounded-lg text-[13px] font-mono border transition-colors cursor-pointer
              ${i === currentIdx
                ? 'bg-accent border-accent text-white'
                : 'bg-transparent border-border text-muted hover:text-text'}`}
          >
            {i + 1}
          </button>
        ))}
      </div>
      <div className="bg-surface2 border border-border rounded-xl p-4 md:p-6">
        <div className="flex items-center gap-3 mb-2.5">
          <span className="bg-accent text-white text-[11px] font-bold px-2.5 py-0.5 rounded-full whitespace-nowrap">
            Ejercicio {currentIdx + 1}
          </span>
          <h3 className="text-[16px] font-semibold text-text">{currentTitle}</h3>
        </div>
        <RunableBlock initialCode={current.content} lang="python" label="Tu código" storageKey={`debug:${topicId}:${current.filename}`} />
      </div>
    </section>
  );
}

function Empty({ text }: { text: string }) {
  return <p className="text-[14px] text-muted py-8">{text}</p>;
}
