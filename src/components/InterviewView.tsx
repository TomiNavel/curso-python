import { useState } from 'react';
import type { QA, InterviewExercise } from '../types/course';
import MarkdownContent from './MarkdownContent';
import RunableBlock from './RunableBlock';

interface Props {
  questions: QA[];
  errorsMd: string;
  interviewExercises: InterviewExercise[];
}

export default function InterviewView({ questions, errorsMd, interviewExercises }: Props) {
  const [openQ, setOpenQ] = useState<number | null>(null);

  return (
    <div className="max-w-190 flex flex-col gap-8">
      {questions.length > 0 && (
        <section>
          <h2 className="text-[17px] font-semibold text-text mb-4 pb-2 border-b border-border">
            Preguntas de entrevista
          </h2>
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
      )}

      {errorsMd && (
        <section>
          <h2 className="text-[17px] font-semibold text-text mb-4 pb-2 border-b border-border">
            Errores comunes
          </h2>
          <MarkdownContent content={errorsMd} />
        </section>
      )}

      {interviewExercises.length > 0 && (
        <section>
          <h2 className="text-[17px] font-semibold text-text mb-4 pb-2 border-b border-border">
            Ejercicios de entrevista
          </h2>
          <div className="flex flex-col gap-4">
            {interviewExercises.map((ex, i) => (
              ex.content && <RunableBlock key={i} initialCode={ex.content} lang="python" label={ex.filename} />
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
