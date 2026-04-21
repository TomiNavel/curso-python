// Lazy content registry. Unlike the index (which is eager), every lesson file,
// exercise, and interview resource is a separate chunk fetched only when
// needed. Vite turns each import.meta.glob entry into a dynamic import().
//
// File layout expected under src/Temario/:
//   NN-topic-slug/
//     NN-lesson.md                         (required — the lesson body)
//     Ejercicios/NN-Name.py                (optional)
//     Ejercicios/Soluciones/NN-Name.py     (optional, matches exercise name)
//     Entrevistas/01-Preguntas.md          (optional)
//     Entrevistas/02-Errores-Comunes.md    (optional)
//     Entrevistas/Ejercicios/NN-Name.py    (optional, intermediate+ topics)

type Loader = () => Promise<string>;

// eager: false — each match is a function that resolves to the file contents.
const LESSONS = import.meta.glob('/src/Temario/*/*.md', { query: '?raw', import: 'default' }) as Record<string, Loader>;
const EXERCISES = import.meta.glob('/src/Temario/*/Ejercicios/*.py', { query: '?raw', import: 'default' }) as Record<string, Loader>;
const SOLUTIONS = import.meta.glob('/src/Temario/*/Ejercicios/Soluciones/*.py', { query: '?raw', import: 'default' }) as Record<string, Loader>;
const INTERVIEW_MD = import.meta.glob('/src/Temario/*/Entrevistas/*.md', { query: '?raw', import: 'default' }) as Record<string, Loader>;
const INTERVIEW_EX = import.meta.glob('/src/Temario/*/Entrevistas/Ejercicios/*.py', { query: '?raw', import: 'default' }) as Record<string, Loader>;

export interface TopicResources {
  folderIndex: number;
  folderName: string;
  lesson: Loader | null;
  exercises: Array<{ filename: string; load: Loader; loadSolution: Loader | null }>;
  preguntas: Loader | null;
  errores: Loader | null;
  interviewExercises: Array<{ filename: string; load: Loader }>;
}

function folderInfo(path: string): { folderName: string; folderIndex: number } | null {
  const m = path.match(/^\/src\/Temario\/((\d+)-[^/]+)\//);
  if (!m) return null;
  return { folderName: m[1], folderIndex: Number(m[2]) };
}

function filename(path: string): string {
  return path.split('/').pop() ?? '';
}

function ensure(map: Map<number, TopicResources>, path: string): TopicResources | null {
  const info = folderInfo(path);
  if (!info) return null;
  let t = map.get(info.folderIndex);
  if (!t) {
    t = {
      folderIndex: info.folderIndex,
      folderName: info.folderName,
      lesson: null,
      exercises: [],
      preguntas: null,
      errores: null,
      interviewExercises: [],
    };
    map.set(info.folderIndex, t);
  }
  return t;
}

function buildRegistry(): Map<number, TopicResources> {
  const map = new Map<number, TopicResources>();

  // Lessons: pick the NN-*.md at the topic root (not inside Entrevistas/).
  // If multiple exist, prefer the one starting with "01-".
  const lessonCandidates = new Map<number, string>();
  for (const path of Object.keys(LESSONS)) {
    if (path.includes('/Entrevistas/')) continue;
    const info = folderInfo(path);
    if (!info) continue;
    const current = lessonCandidates.get(info.folderIndex);
    const name = filename(path);
    if (!current || name.startsWith('01-')) lessonCandidates.set(info.folderIndex, path);
  }
  for (const [idx, path] of lessonCandidates) {
    const t = ensure(map, path);
    if (t) t.lesson = LESSONS[path];
    void idx;
  }

  for (const [path, load] of Object.entries(EXERCISES)) {
    const t = ensure(map, path);
    if (!t) continue;
    t.exercises.push({ filename: filename(path), load, loadSolution: null });
  }

  // Pair solutions with exercises by filename.
  for (const [path, load] of Object.entries(SOLUTIONS)) {
    const t = ensure(map, path);
    if (!t) continue;
    const name = filename(path);
    const match = t.exercises.find(e => e.filename === name);
    if (match) match.loadSolution = load;
  }

  for (const [path, load] of Object.entries(INTERVIEW_MD)) {
    const t = ensure(map, path);
    if (!t) continue;
    const name = filename(path);
    if (name.startsWith('01-')) t.preguntas = load;
    else if (name.startsWith('02-')) t.errores = load;
  }

  for (const [path, load] of Object.entries(INTERVIEW_EX)) {
    const t = ensure(map, path);
    if (!t) continue;
    t.interviewExercises.push({ filename: filename(path), load });
  }

  // Stable filename order for exercises and interview exercises.
  for (const t of map.values()) {
    t.exercises.sort((a, b) => a.filename.localeCompare(b.filename));
    t.interviewExercises.sort((a, b) => a.filename.localeCompare(b.filename));
  }
  return map;
}

const REGISTRY = buildRegistry();

export function findTopicResources(id: number): TopicResources | undefined {
  return REGISTRY.get(id);
}

export function hasLesson(id: number): boolean {
  return !!REGISTRY.get(id)?.lesson;
}
