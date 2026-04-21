import { useEffect, useRef, useState } from 'react';
import type { Topic, PanelData, Tab } from '../../types/course';
import { loadTab } from './fetchers';

type Status = 'idle' | 'loading' | 'ready' | 'error';

interface Result {
  status: Status;
  data: PanelData | null;
  error: string | null;
}

export function useTopicContent(topic: Topic | undefined, tab: Tab): Result {
  const [status, setStatus] = useState<Status>('idle');
  const [data, setData] = useState<PanelData | null>(null);
  const [error, setError] = useState<string | null>(null);
  const cache = useRef<Map<string, PanelData>>(new Map());

  const topicId = topic?.id;
  const hasFolder = !!topic?.folder;

  useEffect(() => {
    if (!topic || !hasFolder) {
      setStatus('idle');
      setData(null);
      return;
    }

    // Material is global (not tied to a topic) — share cache across topics.
    const key = tab === 'material' ? 'global:material' : `${topicId}:${tab}`;
    const cached = cache.current.get(key);
    if (cached) {
      setData(cached);
      setStatus('ready');
      return;
    }

    let alive = true;
    setStatus('loading');
    setData(null);

    loadTab(topic, tab)
      .then(result => {
        if (!alive) return;
        cache.current.set(key, result);
        setData(result);
        setStatus('ready');
      })
      .catch((e: Error) => {
        if (!alive) return;
        setError(e.message);
        setStatus('error');
      });

    return () => { alive = false; };
  }, [topic, topicId, hasFolder, tab]);

  return { status, data, error };
}
