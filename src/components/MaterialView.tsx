import { useState } from 'react';
import type { Cheatsheet } from '../types/course';
import MarkdownContent from './MarkdownContent';
import SubTabs from './SubTabs';

interface Props {
  cheatsheets: Cheatsheet[];
  recursosMd: string;
}

const RECURSOS_ID = '__recursos__';

export default function MaterialView({ cheatsheets, recursosMd }: Props) {
  const [active, setActive] = useState<string>(() => cheatsheets[0]?.id ?? RECURSOS_ID);

  const tabs = [
    ...cheatsheets.map(cs => ({ id: cs.id, label: cs.title })),
    ...(recursosMd ? [{ id: RECURSOS_ID, label: 'Recursos' }] : []),
  ];

  if (tabs.length === 0) {
    return <p className="text-[14px] text-muted py-8">No hay material disponible.</p>;
  }

  const currentCheatsheet = cheatsheets.find(cs => cs.id === active);
  const showRecursos = active === RECURSOS_ID;

  return (
    <div className="max-w-190 flex flex-col gap-6">
      <SubTabs tabs={tabs} active={active} onChange={setActive} />
      {currentCheatsheet && (
        currentCheatsheet.content.trim()
          ? <MarkdownContent content={currentCheatsheet.content} />
          : <InDevelopment />
      )}
      {showRecursos && <MarkdownContent content={recursosMd} />}
    </div>
  );
}

function InDevelopment() {
  return (
    <div className="flex flex-col items-center justify-center py-16 text-center">
      <p className="text-[14px] font-medium text-text">En desarrollo</p>
    </div>
  );
}
