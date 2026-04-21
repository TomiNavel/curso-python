import { useState } from 'react';
import CodeMirror from '@uiw/react-codemirror';
import { python } from '@codemirror/lang-python';
import { oneDark } from '@codemirror/theme-one-dark';
import { EditorView } from '@codemirror/view';
import { runPython } from '../lib/pyodide';

interface Props {
  initialCode: string;
  lang: string;
  label?: string;
  storageKey?: string;
}

const sessionCode = new Map<string, string>();

function resolveInitial(initialCode: string, storageKey?: string): string {
  if (storageKey && sessionCode.has(storageKey)) return sessionCode.get(storageKey)!;
  return initialCode;
}

export default function RunableBlock({ initialCode, lang, label, storageKey }: Props) {
  const [code, setCode] = useState(() => resolveInitial(initialCode, storageKey));
  const [output, setOutput] = useState<{ output: string; error: string | null } | null>(null);
  const [running, setRunning] = useState(false);
  const [prevKey, setPrevKey] = useState<{ key: string | undefined; initial: string }>({ key: storageKey, initial: initialCode });

  if (prevKey.key !== storageKey || prevKey.initial !== initialCode) {
    setPrevKey({ key: storageKey, initial: initialCode });
    setCode(resolveInitial(initialCode, storageKey));
    setOutput(null);
  }

  const isPython = !lang || lang === 'python';

  const handleChange = (value: string) => {
    setCode(value);
    if (storageKey) sessionCode.set(storageKey, value);
  };

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
      <CodeMirror
        value={code}
        onChange={handleChange}
        theme={oneDark}
        extensions={[python(), EditorView.lineWrapping]}
        basicSetup={{
          lineNumbers: true,
          foldGutter: false,
          highlightActiveLine: true,
          highlightActiveLineGutter: true,
          autocompletion: false,
        }}
        className="text-[13px]"
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
