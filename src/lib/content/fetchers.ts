import type { Topic, PanelData, Tab } from '../../types/course';
import { findTopicResources, getCheatsheets, getRecursosLoader } from '../../data/content';
import { parseExercisePy, parseQA } from './parsers';

// Each loader triggers a dynamic import() for a specific file chunk. The hook
// already caches the resulting PanelData by (topicId, tab), so repeated opens
// hit the cache and skip network.

async function loadTeoria(topic: Topic): Promise<PanelData> {
  const res = findTopicResources(topic.id);
  if (!res?.lesson) throw new Error(`Topic ${topic.id} has no lesson`);
  const content = await res.lesson();
  return { type: 'teoria', content };
}

async function loadEjercicios(topic: Topic): Promise<PanelData> {
  const res = findTopicResources(topic.id);
  if (!res) throw new Error(`Topic ${topic.id} not found`);
  const exercises = await Promise.all(res.exercises.map(async ex => {
    const [content, solution] = await Promise.all([
      ex.load(),
      ex.loadSolution ? ex.loadSolution() : Promise.resolve(''),
    ]);
    return { ...parseExercisePy(ex.filename, content), solution };
  }));
  return { type: 'ejercicios', exercises };
}

async function loadEntrevistas(topic: Topic): Promise<PanelData> {
  const res = findTopicResources(topic.id);
  if (!res) throw new Error(`Topic ${topic.id} not found`);
  const [preguntasMd, errorsMd, interviewExercises] = await Promise.all([
    res.preguntas ? res.preguntas() : Promise.resolve(''),
    res.errores ? res.errores() : Promise.resolve(''),
    Promise.all(res.interviewExercises.map(async ex => ({
      filename: ex.filename,
      content: await ex.load(),
    }))),
  ]);
  return {
    type: 'entrevistas',
    questions: parseQA(preguntasMd),
    errorsMd,
    interviewExercises,
  };
}

async function loadMaterial(): Promise<PanelData> {
  const entries = getCheatsheets();
  const recursosLoader = getRecursosLoader();
  const [cheatsheets, recursosMd] = await Promise.all([
    Promise.all(entries.map(async e => ({
      id: e.id,
      title: e.title,
      content: await e.load(),
    }))),
    recursosLoader ? recursosLoader() : Promise.resolve(''),
  ]);
  return { type: 'material', cheatsheets, recursosMd };
}

export async function loadTab(topic: Topic, tab: Tab): Promise<PanelData> {
  if (tab === 'teoria') return loadTeoria(topic);
  if (tab === 'ejercicios') return loadEjercicios(topic);
  if (tab === 'entrevistas') return loadEntrevistas(topic);
  return loadMaterial();
}
