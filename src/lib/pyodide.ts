// Singleton Pyodide loader + runner for the course's interactive code blocks.
//
// Behavior notes:
// - Pyodide runs fully in the browser sandbox (WebAssembly). It can read a
//   virtual filesystem bundled into the WASM image but cannot touch the host.
// - By default, the interpreter is REUSED across runs: variables, imports, and
//   definitions persist. Pass freshContext: true to wipe user-defined globals
//   before running (module imports still persist to avoid re-download cost).

// eslint-disable-next-line @typescript-eslint/no-explicit-any
type Pyodide = any;

let _pyodide: Pyodide = null;
let _loading = false;
const _queue: Array<(p: Pyodide) => void> = [];

async function getPyodide(): Promise<Pyodide> {
  if (_pyodide) return _pyodide;
  if (_loading) return new Promise(r => _queue.push(r));
  _loading = true;
  try {
    await new Promise<void>((res, rej) => {
      const s = document.createElement('script');
      s.src = 'https://cdn.jsdelivr.net/pyodide/v0.26.2/full/pyodide.js';
      s.onload = () => res();
      s.onerror = () => rej(new Error('Failed to load Pyodide'));
      document.head.appendChild(s);
    });
    _pyodide = await (window as unknown as { loadPyodide(): Promise<Pyodide> }).loadPyodide();
    _loading = false;
    _queue.forEach(r => r(_pyodide));
    _queue.length = 0;
    return _pyodide;
  } catch (e) {
    _loading = false;
    _queue.length = 0;
    throw e;
  }
}

const RESET_GLOBALS = `
for _k in list(globals().keys()):
    if not _k.startswith('_') and _k not in ('sys', 'io'):
        del globals()[_k]
`;

export interface RunOptions {
  freshContext?: boolean;
}

export interface RunResult {
  output: string;
  error: string | null;
}

export async function runPython(code: string, opts: RunOptions = {}): Promise<RunResult> {
  const py = await getPyodide();
  if (opts.freshContext) {
    try { py.runPython(RESET_GLOBALS); } catch { /* best-effort */ }
  }
  py.runPython(`import sys, io\n_buf=io.StringIO()\nsys.stdout=_buf\nsys.stderr=_buf`);
  let output = '', error: string | null = null;
  try {
    // runPythonAsync handles both sync code and top-level await (needed for
    // asyncio exercises since Pyodide already has an active event loop).
    await py.runPythonAsync(code);
    output = py.runPython('_buf.getvalue()');
  } catch (e) {
    error = (e as Error).message.split('\n').slice(-3).join('\n');
    try { output = py.runPython('_buf.getvalue()'); } catch { /* ignore */ }
  } finally {
    try { py.runPython(`sys.stdout=sys.__stdout__\nsys.stderr=sys.__stderr__`); } catch { /* ignore */ }
  }
  return { output, error };
}
