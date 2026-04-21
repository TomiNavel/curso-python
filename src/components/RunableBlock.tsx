import { useEffect, useState } from 'react';
import { runPython } from '../lib/pyodide';

interface Props {
  initialCode: string;
  lang: string;
  label?: string;
}

export default function RunableBlock({ initialCode, lang, label }: Props) {
  const [code, setCode] = useState(initialCode);
  const [output, setOutput] = useState<{ output: string; error: string | null } | null>(null);
  const [running, setRunning] = useState(false);

  useEffect(() => {
    setCode(initialCode);
    setOutput(null);
  }, [initialCode]);
  const isPython = !lang || lang === 'python';
  const rows = Math.max(3, code.split('\n').length + 1);

  const handleRun = async () => {
    setRunning(true);
    setOutput(null);
    const result = await runPython(code).catch(e => ({ output: '', error: (e as Error).message }));
    setRunning(false);
    setOutput(result);
  };

  return (
    <div className="bg-bg2 border border-border rounded-xl overflow-hidden my-4">
      {label && (
        <div className="px-3.5 py-1.5 text-[11px] font-semibold text-muted bg-bg border-b border-border uppercase tracking-wide">
          {label}
        </div>
      )}
      <div className="flex items-center justify-between px-3.5 py-2 bg-bg border-b border-border">
        <span className="font-mono text-[11px] text-muted uppercase">{lang || 'python'}</span>
        {isPython && (
          <button
            className="bg-transparent text-accent2 border border-accent2/40 cursor-pointer px-3 py-1 rounded-md text-[11px] font-semibold uppercase tracking-wide disabled:opacity-60 disabled:cursor-not-allowed hover:enabled:bg-accent2/12 transition-all"
            onClick={handleRun}
            disabled={running}
          >
            {running ? 'Ejecutando…' : 'Ejecutar'}
          </button>
        )}
      </div>
      <textarea
        className="w-full px-4 py-3.5 bg-bg2 text-[#c8e6ff] font-mono text-[13px] leading-relaxed border-none outline-none resize-y tab-size-4 focus:bg-bg2/90"
        value={code}
        onChange={e => setCode(e.target.value)}
        spellCheck={false}
        rows={rows}
      />
      {output && (
        <div className={`px-4 py-3 border-t border-border font-mono text-[12px] ${output.error ? 'bg-red/8' : 'bg-green/8'}`}>
          <span className={`block text-[10px] font-semibold uppercase tracking-wide mb-1.5 ${output.error ? 'text-red' : 'text-green'}`}>
            {output.error ? 'Error' : 'Salida'}
          </span>
          <pre className="whitespace-pre-wrap wrap-break-word text-text leading-snug">
            {output.error || output.output || '(sin salida)'}
          </pre>
        </div>
      )}
    </div>
  );
}
