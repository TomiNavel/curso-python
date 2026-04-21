import { useState } from 'react';
import type { Exercise } from '../types/course';
import MarkdownContent from './MarkdownContent';
import RunableBlock from './RunableBlock';

interface Props {
  exercises: Exercise[];
}

export default function ExercisesView({ exercises }: Props) {
  return (
    <div className="flex flex-col gap-6 max-w-190">
      {exercises.map((ex, i) => <ExerciseCard key={i} exercise={ex} index={i} />)}
    </div>
  );
}

function ExerciseCard({ exercise, index }: { exercise: Exercise; index: number }) {
  const [showSol, setShowSol] = useState(false);

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
      <RunableBlock initialCode={exercise.starter} lang="python" label="Tu código" />
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
