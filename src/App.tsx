import { useEffect, useState } from 'react';
import Sidebar from './components/Sidebar';
import ContentPanel from './components/ContentPanel';
import TOPICS from './data/topics';
import type { Selection } from './types/course';
import { parseHash, toHash } from './lib/hashRoute';

export default function App() {
  const [selected, setSelected] = useState<Selection | null>(() => parseHash(window.location.hash));
  const [collapsed, setCollapsed] = useState(false);

  useEffect(() => {
    const onHash = () => setSelected(parseHash(window.location.hash));
    window.addEventListener('hashchange', onHash);
    return () => window.removeEventListener('hashchange', onHash);
  }, []);

  const updateSelected = (s: Selection | null) => {
    const hash = toHash(s);
    if (hash !== window.location.hash) {
      if (hash) window.location.hash = hash;
      else history.replaceState(null, '', window.location.pathname + window.location.search);
    }
    setSelected(s);
  };

  return (
    <div className="flex h-screen overflow-hidden">
      <Sidebar
        selected={selected}
        onSelect={updateSelected}
        onGoHome={() => updateSelected(null)}
        collapsed={collapsed}
        onToggle={() => setCollapsed(c => !c)}
      />
      <main className="flex-1 overflow-hidden bg-surface">
        {selected
          ? <ContentPanel key={selected.topicId} selected={selected} onSelect={updateSelected} />
          : <Welcome onSelect={updateSelected} />
        }
      </main>
    </div>
  );
}

function Welcome({ onSelect }: { onSelect: (s: Selection) => void }) {
  const available = TOPICS.filter(t => !!t.folder);
  return (
    <div className="w-full h-full flex items-center justify-center overflow-y-auto">
      <div className="grid grid-cols-2 gap-12 w-full px-12 py-12 max-w-300">

        {/* Left */}
        <div className="flex flex-col">
          <span className="text-[11px] font-semibold uppercase tracking-[2px] text-muted2 font-mono mb-3.5">Curso completo</span>
          <h1 className="text-[52px] font-black text-text leading-none tracking-[-1.5px] mb-3.5">
            Aprende<br /><span className="text-accent">Python</span>
          </h1>
          <p className="text-[15px] text-muted leading-relaxed mb-6 max-w-sm">
            Teoría, ejercicios interactivos y preparación para entrevistas técnicas.
          </p>

          <div className="bg-bg2 border border-border rounded-xl overflow-hidden mb-6">
            <div className="flex items-center gap-1.5 px-3.5 py-2.5 bg-surface2 border-b border-border">
              <span className="w-2.5 h-2.5 rounded-full bg-red" />
              <span className="w-2.5 h-2.5 rounded-full bg-yellow" />
              <span className="w-2.5 h-2.5 rounded-full bg-green" />
              <span className="font-mono text-[11px] text-muted ml-1.5">python</span>
            </div>
            <div className="px-4 py-3.5 font-mono text-[13px] leading-loose">
              <div><span className="text-accent2">{'>>>'}</span> <span className="text-accent">def</span> <span className="text-blue">estudiar</span>(tema):</div>
              <div className="pl-6"><span className="text-accent">return</span> <span className="text-green">f"</span><span className="text-text">{'{tema}'}</span><span className="text-green">: aprendido"</span></div>
              <div><span className="text-accent2">{'>>>'}</span> estudiar(<span className="text-green">"Python"</span>)</div>
              <div><span className="text-text">'Python: aprendido'</span></div>
            </div>
          </div>

          <div className="grid grid-cols-4 gap-2.5">
            {[
              { value: String(available.length), label: 'Temas' },
              { value: '100+', label: 'Ejercicios' },
              { value: '300+', label: 'Preguntas' },
              { value: 'Live', label: 'Python' },
            ].map(s => (
              <div key={s.label} className="bg-surface border border-border rounded-xl py-3.5 px-2.5 flex flex-col items-center gap-1">
                <span className="text-[18px] font-extrabold text-accent font-mono">{s.value}</span>
                <small className="text-[10px] text-muted uppercase tracking-wide">{s.label}</small>
              </div>
            ))}
          </div>
        </div>

        {/* Right */}
        <div className="flex flex-col justify-center">
          <span className="text-[11px] font-semibold uppercase tracking-[1.5px] text-muted2 mb-3.5">Empieza por aquí</span>
          <div className="grid grid-cols-2 gap-2">
            {available.slice(0, 6).map(t => (
              <button
                key={t.id}
                className="bg-surface border border-border rounded-xl px-4 py-3.5 flex items-center gap-2.5 text-left cursor-pointer hover:border-accent hover:-translate-y-px transition-all"
                onClick={() => onSelect({ topicId: t.id, subtopicId: null })}
              >
                <span className="text-muted2 font-mono text-[11px] shrink-0">{t.id}.</span>
                <span className="text-[13px] font-medium text-text">{t.title}</span>
              </button>
            ))}
          </div>
        </div>

      </div>
    </div>
  );
}
