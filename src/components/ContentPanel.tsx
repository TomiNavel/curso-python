import { useEffect, useRef, useState } from 'react';
import TOPICS from '../data/topics';
import type { Selection, Tab } from '../types/course';
import { useTopicContent } from '../lib/content/useTopicContent';
import { extractSection } from '../lib/content/parsers';
import MarkdownContent from './MarkdownContent';
import ExercisesView from './ExercisesView';
import InterviewView from './InterviewView';
import MaterialView from './MaterialView';

interface Props {
  selected: Selection;
  onSelect: (s: Selection) => void;
}

const TABS: { id: Tab; label: string }[] = [
  { id: 'teoria', label: 'Teoría' },
  { id: 'ejercicios', label: 'Ejercicios' },
  { id: 'entrevistas', label: 'Entrevistas' },
  { id: 'material', label: 'Material' },
];

export default function ContentPanel({ selected, onSelect }: Props) {
  const [tab, setTab] = useState<Tab>('teoria');
  const scrollRef = useRef<HTMLDivElement>(null);

  const topic = TOPICS.find(t => t.id === selected.topicId)!;
  const subtopic = topic.subtopics.find(s => s.id === selected.subtopicId);
  const { status, data, error } = useTopicContent(topic, tab);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: 0 });
  }, [selected.topicId, selected.subtopicId, tab]);

  const renderContent = () => {
    // Material is global and does not require a topic lesson.
    if (!topic.folder && tab !== 'material') return <ComingSoon title={topic.title} />;
    if (status === 'loading') return (
      <div className="flex flex-col items-center justify-center gap-4 py-20 text-muted">
        <div className="w-9 h-9 border-3 border-border border-t-accent rounded-full animate-spin" />
        <p>Cargando…</p>
      </div>
    );
    if (status === 'error') return (
      <div className="flex items-center justify-center py-20 text-red">{error}</div>
    );
    if (!data) return null;

    if (data.type === 'teoria') return <TeoriaView selected={selected} content={data.content} onSelect={onSelect} />;
    if (data.type === 'ejercicios') return <ExercisesView exercises={data.exercises} />;
    if (data.type === 'entrevistas') return <InterviewView topicId={topic.id} questions={data.questions} errorsMd={data.errorsMd} interviewExercises={data.interviewExercises} />;
    return <MaterialView cheatsheets={data.cheatsheets} recursosMd={data.recursosMd} />;
  };

  const showTabs = !!topic.folder || tab === 'material';

  return (
    <div className="flex flex-col h-screen">
      <div className="shrink-0 border-b border-border bg-bg">
        <div className="max-w-300 mx-auto px-12 pt-6">
          <h1 className="flex items-center gap-2 text-[22px] font-bold text-text mb-4">
            <span>{topic.title}</span>
            {subtopic && <><span className="text-muted2 font-normal">›</span><span>{subtopic.title}</span></>}
          </h1>
          {showTabs && (
            <div className="flex gap-1">
              {TABS.map(t => (
                <button
                  key={t.id}
                  className={`bg-transparent border border-transparent text-muted cursor-pointer px-5 py-2.5 text-[15px] font-medium rounded-t-lg transition-all hover:text-text hover:bg-surface
                    ${tab === t.id ? 'text-text! bg-surface! border-border! border-b-transparent!' : ''}`}
                  onClick={() => setTab(t.id)}
                >
                  {t.label}
                </button>
              ))}
            </div>
          )}
        </div>
      </div>
      <div ref={scrollRef} className="flex-1 overflow-y-auto bg-surface">
        <div className="max-w-300 mx-auto px-12 pb-8">
          {renderContent()}
        </div>
      </div>
    </div>
  );
}

function TeoriaView({
  selected,
  content,
  onSelect,
}: {
  selected: Selection;
  content: string;
  onSelect: (s: Selection) => void;
}) {
  const topic = TOPICS.find(t => t.id === selected.topicId)!;
  const sectionMd = extractSection(content, selected.subtopicId);

  let nextSelection: Selection | null = null;
  let nextLabel: string | null = null;
  if (selected.subtopicId) {
    const subIdx = topic.subtopics.findIndex(s => s.id === selected.subtopicId);
    if (subIdx >= 0 && subIdx < topic.subtopics.length - 1) {
      const next = topic.subtopics[subIdx + 1];
      nextSelection = { topicId: selected.topicId, subtopicId: next.id };
      nextLabel = next.title;
    } else {
      const topicIdx = TOPICS.findIndex(t => t.id === selected.topicId);
      const nextTopic = TOPICS[topicIdx + 1];
      if (nextTopic) {
        nextSelection = { topicId: nextTopic.id, subtopicId: nextTopic.subtopics[0]?.id ?? null };
        nextLabel = nextTopic.title;
      }
    }
  }

  return (
    <>
      <MarkdownContent content={sectionMd} />
      {nextSelection && nextLabel && (
        <button
          className="mt-10 inline-flex items-center gap-3 text-left bg-surface2 border border-border rounded-lg px-4 py-2.5 cursor-pointer group hover:border-accent transition-all duration-200"
          onClick={() => onSelect(nextSelection!)}
        >
          <span className="text-[15px] font-semibold text-muted group-hover:text-accent transition-colors whitespace-nowrap">Siguiente →</span>
          <span className="w-px h-4 bg-border" />
          <span className="text-[14px] font-medium text-text group-hover:text-accent transition-colors">{nextLabel}</span>
        </button>
      )}
    </>
  );
}

function ComingSoon({ title }: { title: string }) {
  return (
    <div className="flex flex-col items-center justify-center gap-4 py-20 text-center">
      <h2 className="text-xl font-bold text-text">Contenido en preparación</h2>
      <p className="text-[14px] text-muted max-w-sm">El tema <strong>{title}</strong> todavía no tiene documentación.</p>
    </div>
  );
}
