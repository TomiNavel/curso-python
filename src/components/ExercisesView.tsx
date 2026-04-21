import { useState } from 'react';
import type { Exercise } from '../types/course';
import MarkdownContent from './MarkdownContent';
import RunableBlock from './RunableBlock';

interface Props {
  topicId: number;
  exercises: Exercise[];
}

export default function ExercisesView({ topicId, exercises }: Props) {
  const [active, setActive] = useState(0);

  if (exercises.length === 0) {
    return <p className="text-[14px] text-muted py-8">No hay ejercicios para este tema.</p>;
  }

  const currentIdx = Math.min(active, exercises.length - 1);
  const current = exercises[currentIdx];

  return (
    <div className="flex flex-col gap-5 max-w-190">
      <div className="sticky top-0 z-10 bg-surface -mx-12 px-12 py-3 flex gap-1.5 flex-wrap border-b border-border">
        {exercises.map((_, i) => (
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
      <ExerciseCard topicId={topicId} exercise={current} index={currentIdx} />
    </div>
  );
}

function ExerciseCard({ topicId, exercise, index }: { topicId: number; exercise: Exercise; index: number }) {
  const [showSol, setShowSol] = useState(false);
  const storageKey = `ex:${topicId}:${exercise.title}`;

  return (
    <div className="bg-surface2 border border-border rounded-xl p-6">
      <div className="flex items-center gap-3 mb-2.5">
        <span className="bg-accent text-white text-[11px] font-bold px-2.5 py-0.5 rounded-full whitespace-nowrap">
          Ejercicio {index + 1}
        </span>
        <h3 className="text-[16px] font-semibold text-text">{exercise.title}</h3>
      </div>
      {exercise.desc && (
        <div className="text-[13px] text-[#b8b8d8] mb-4">
          <MarkdownContent content={exercise.desc} compact />
        </div>
      )}
      <RunableBlock initialCode={exercise.starter} lang="python" label="Tu código" storageKey={storageKey} />
      {exercise.solution && (
        <>
          <div className="mt-3">
            <button
              className="bg-transparent border border-border text-muted px-4 py-1.5 rounded-lg text-[13px] cursor-pointer hover:border-green hover:text-green transition-all"
              onClick={() => setShowSol(!showSol)}
            >
              {showSol ? 'Ocultar solución' : 'Ver solución'}
            </button>
          </div>
          {showSol && (
            <div className="border-t border-border pt-4 mt-4">
              <div className="text-[11px] font-semibold text-green uppercase tracking-wide mb-2">Solución</div>
              <RunableBlock initialCode={exercise.solution} lang="python" />
            </div>
          )}
        </>
      )}
    </div>
  );
}
