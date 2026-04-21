import { useState } from 'react';
import TOPICS from '../data/topics';
import type { Selection } from '../types/course';

interface Props {
  selected: Selection | null;
  onSelect: (s: Selection) => void;
  onGoHome: () => void;
  collapsed: boolean;
  onToggle: () => void;
}

export default function Sidebar({ selected, onSelect, onGoHome, collapsed, onToggle }: Props) {
  // User-toggled overrides. Selected topic is always considered open unless
  // explicitly collapsed here, so navigation keeps context without useEffect.
  const [overrides, setOverrides] = useState<Record<number, boolean>>({});

  const isExpanded = (id: number) =>
    id in overrides ? overrides[id] : selected?.topicId === id;

  const toggle = (id: number) => setOverrides(p => ({ ...p, [id]: !isExpanded(id) }));

  return (
    <aside className={`flex flex-col bg-bg2 border-r border-border transition-all duration-250 overflow-hidden ${collapsed ? 'w-15 min-w-15' : 'w-70 min-w-70'}`}>
      <div className="flex items-center justify-between px-3 py-4 border-b border-border min-h-15 shrink-0">
        <button
          onClick={onGoHome}
          className="bg-transparent border-none cursor-pointer p-0 overflow-hidden flex items-center"
          title="Inicio"
        >
          {!collapsed && <span className="text-[15px] font-bold text-text whitespace-nowrap hover:text-accent transition-colors">Aprende Python</span>}
        </button>
        <button
          onClick={onToggle}
          className="bg-transparent border border-border text-muted rounded-md w-7 h-7 cursor-pointer text-[10px] shrink-0 hover:border-accent hover:text-accent transition-all"
        >
          {collapsed ? '▶' : '◀'}
        </button>
      </div>

      <nav className="flex-1 overflow-y-auto py-2 px-1.5 scrollbar-thin scrollbar-thumb-border2">
        {TOPICS.map(topic => {
          const open = isExpanded(topic.id);
          const isActive = selected?.topicId === topic.id && !selected?.subtopicId;

          return (
            <div key={topic.id} className="mb-0.5">
              <button
                className={`w-full flex items-center gap-2 bg-transparent border-none cursor-pointer px-2 py-1.5 rounded-lg text-[13px] text-left transition-all
                  ${isActive ? 'bg-accent/15 text-accent' : 'text-muted hover:bg-surface hover:text-text'}`}
                onClick={() => toggle(topic.id)}
                title={collapsed ? topic.title : ''}
              >
                {!collapsed && (
                  <>
                    <span className="text-muted2 text-[11px] shrink-0 font-mono">{topic.id}.</span>
                    <span className="flex-1 font-medium overflow-hidden text-ellipsis whitespace-nowrap">{topic.title}</span>
                    <span className="text-[10px] shrink-0">{open ? '▾' : '▸'}</span>
                  </>
                )}
              </button>

              {!collapsed && open && (
                <div className="pl-7 py-0.5">
                  {topic.subtopics.map(sub => (
                    <button
                      key={sub.id}
                      className={`w-full flex items-center gap-1.5 bg-transparent border-none cursor-pointer px-2 py-1 rounded-md text-[12px] text-left transition-all
                        ${selected?.subtopicId === sub.id ? 'text-accent2 bg-accent2/10' : 'text-muted hover:bg-surface hover:text-text'}`}
                      onClick={() => onSelect({ topicId: topic.id, subtopicId: sub.id })}
                    >
                      <span className="text-muted2 text-[10px] font-mono min-w-7">{sub.id}</span>
                      <span>{sub.title}</span>
                    </button>
                  ))}
                </div>
              )}
            </div>
          );
        })}
      </nav>
    </aside>
  );
}
