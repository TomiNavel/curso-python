export interface Subtopic {
  id: string;
  title: string;
}

export interface Selection {
  topicId: number;
  subtopicId: string | null;
}

export interface Topic {
  id: number;
  title: string;
  subtopics: Subtopic[];
  // Present when the topic has a lesson file. Acts as the "has content" flag.
  folder?: string;
}

export interface Exercise {
  title: string;
  desc: string;
  starter: string;
  solution: string;
}

export interface QA {
  q: string;
  a: string;
}

export interface InterviewExercise {
  filename: string;
  content: string;
  solution: string;
}

export interface Cheatsheet {
  id: string;
  title: string;
  content: string;
}

export type Tab = 'teoria' | 'ejercicios' | 'entrevistas' | 'material';

export type PanelData =
  | { type: 'teoria'; content: string }
  | { type: 'ejercicios'; exercises: Exercise[] }
  | { type: 'entrevistas'; questions: QA[]; errorsMd: string; interviewExercises: InterviewExercise[] }
  | { type: 'material'; cheatsheets: Cheatsheet[]; recursosMd: string };
