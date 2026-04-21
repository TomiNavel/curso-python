import { useState } from 'react';
import type { QA, InterviewExercise } from '../types/course';
import MarkdownContent from './MarkdownContent';
import RunableBlock from './RunableBlock';
import SubTabs from './SubTabs';

interface Props {
  questions: QA[];
  errorsMd: string;
  interviewExercises: InterviewExercise[];
}

type SubTab = 'preguntas' | 'errores' | 'debug';

export default function InterviewView({ questions, errorsMd, interviewExercises }: Props) {
  const [sub, setSub] = useState<SubTab>('preguntas');

  const tabs: { id: SubTab; label: string; disabled: boolean }[] = [
    { id: 'preguntas', label: 'Preguntas', disabled: questions.length === 0 },
    { id: 'errores', label: 'Errores comunes', disabled: !errorsMd },
    { id: 'debug', label: 'Ejercicios debug', disabled: interviewExercises.length === 0 },
  ];

  return (
    <div className="max-w-190 flex flex-col gap-6">
      <SubTabs
        tabs={tabs}
        active={sub}
        onChange={id => setSub(id as SubTab)}
      />
      {sub === 'preguntas' && <Preguntas questions={questions} />}
      {sub === 'errores' && <Errores md={errorsMd} />}
      {sub === 'debug' && <Debug exercises={interviewExercises} />}
    </div>
  );
}

function Preguntas({ questions }: { questions: QA[] }) {
  const [openQ, setOpenQ] = useState<number | null>(null);

  if (questions.length === 0) return <Empty text="No hay preguntas para este tema." />;

  return (
    <section>
      {questions.map((q, i) => (
        <div key={i} className="border border-border rounded-xl overflow-hidden mb-2.5">
          <button
            className={`w-full flex items-center justify-between bg-surface2 border-none cursor-pointer px-4 py-3.5 text-[14px] font-medium text-left gap-3 transition-colors hover:bg-surface2/80
              ${openQ === i ? 'text-accent2' : 'text-text'}`}
            onClick={() => setOpenQ(openQ === i ? null : i)}
          >
            <span>{q.q}</span>
            <span className="text-[10px] text-muted shrink-0">{openQ === i ? '▲' : '▼'}</span>
          </button>
          {openQ === i && (
            <div className="px-4 py-3.5 text-[14px] text-[#c0c0e0] leading-[1.7] bg-bg2 border-t border-border">
              <MarkdownContent content={q.a} compact />
            </div>
          )}
        </div>
      ))}
    </section>
  );
}

function Errores({ md }: { md: string }) {
  if (!md) return <Empty text="No hay errores comunes documentados para este tema." />;
  return <section><MarkdownContent content={md} /></section>;
}

function Debug({ exercises }: { exercises: InterviewExercise[] }) {
  if (exercises.length === 0) return <Empty text="No hay ejercicios de debug para este tema." />;
  return (
    <section className="flex flex-col gap-4">
      {exercises.map((ex, i) => (
        ex.content && <RunableBlock key={i} initialCode={ex.content} lang="python" label={ex.filename} />
      ))}
    </section>
  );
}

function Empty({ text }: { text: string }) {
  return <p className="text-[14px] text-muted py-8">{text}</p>;
}
