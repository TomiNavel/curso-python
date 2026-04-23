const CACHE_KEY = 'gh-stars-cache';
const TTL_MS = 60 * 60 * 1000;

interface CachedStars {
  count: number;
  ts: number;
}

function readCache(repo: string): number | null {
  try {
    const raw = localStorage.getItem(`${CACHE_KEY}:${repo}`);
    if (!raw) return null;
    const parsed = JSON.parse(raw) as CachedStars;
    if (Date.now() - parsed.ts > TTL_MS) return null;
    return parsed.count;
  } catch {
    return null;
  }
}

function writeCache(repo: string, count: number): void {
  try {
    const value: CachedStars = { count, ts: Date.now() };
    localStorage.setItem(`${CACHE_KEY}:${repo}`, JSON.stringify(value));
  } catch {
    // ignore quota errors
  }
}

export async function fetchStars(repo: string): Promise<number | null> {
  const cached = readCache(repo);
  if (cached !== null) return cached;

  try {
    const res = await fetch(`https://api.github.com/repos/${repo}`);
    if (!res.ok) return null;
    const data = await res.json();
    const count = typeof data.stargazers_count === 'number' ? data.stargazers_count : null;
    if (count !== null) writeCache(repo, count);
    return count;
  } catch {
    return null;
  }
}
