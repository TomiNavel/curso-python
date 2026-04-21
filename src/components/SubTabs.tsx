interface SubTab {
  id: string;
  label: string;
  disabled?: boolean;
}

interface Props {
  tabs: SubTab[];
  active: string;
  onChange: (id: string) => void;
}

export default function SubTabs({ tabs, active, onChange }: Props) {
  return (
    <div className="flex gap-6 border-b border-border -mt-2">
      {tabs.map(t => {
        const isActive = t.id === active;
        return (
          <button
            key={t.id}
            disabled={t.disabled}
            onClick={() => onChange(t.id)}
            className={`relative bg-transparent border-none cursor-pointer px-0 py-2.5 text-[13px] font-medium transition-colors
              ${t.disabled
                ? 'text-muted2 cursor-not-allowed'
                : isActive
                  ? 'text-accent'
                  : 'text-muted hover:text-text'}`}
          >
            {t.label}
            {isActive && !t.disabled && (
              <span className="absolute left-0 right-0 -bottom-px h-0.5 bg-accent rounded-full" />
            )}
          </button>
        );
      })}
    </div>
  );
}
