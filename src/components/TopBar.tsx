interface Props {
  onMobileMenu: () => void;
}

const REPO_URL = 'https://github.com/TomiNavel/curso-python';
const ISSUES_URL = 'https://github.com/TomiNavel/curso-python/issues/new';
const TWITTER_URL = 'https://x.com/TomiNavel';
const WEB_URL = 'https://www.tominavel.com';
const EMAIL = 'hola@tominavel.com';

export default function TopBar({ onMobileMenu }: Props) {
  return (
    <header className="h-11 shrink-0 flex items-center justify-between px-3 md:px-5 bg-bg2 border-b border-border">
      <div className="flex items-center gap-2">
        <button
          onClick={onMobileMenu}
          className="md:hidden bg-transparent border border-border text-text rounded-md w-8 h-8 flex items-center justify-center cursor-pointer text-[16px] hover:border-accent hover:text-accent transition-all"
          title="Menú"
        >
          ☰
        </button>
        <a
          href={WEB_URL}
          target="_blank"
          rel="noopener noreferrer"
          className="text-[13px] font-semibold text-text hover:text-accent transition-colors"
        >
          tominavel.com
        </a>
      </div>

      <div className="flex items-center gap-1 md:gap-3">
        <a
          href={`mailto:${EMAIL}`}
          className="hidden md:inline text-[12px] text-muted hover:text-accent transition-colors"
        >
          {EMAIL}
        </a>
        <a
          href={ISSUES_URL}
          target="_blank"
          rel="noopener noreferrer"
          className="text-[12px] text-muted hover:text-accent transition-colors px-2 py-1 rounded-md hover:bg-surface"
          title="Reportar un error en GitHub"
        >
          Reportar error
        </a>
        <a
          href={REPO_URL}
          target="_blank"
          rel="noopener noreferrer"
          className="text-muted hover:text-accent transition-colors w-8 h-8 flex items-center justify-center rounded-md hover:bg-surface"
          title="Repositorio en GitHub"
          aria-label="GitHub"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
            <path d="M12 0C5.37 0 0 5.37 0 12c0 5.3 3.44 9.8 8.2 11.39.6.11.82-.26.82-.58 0-.29-.01-1.04-.02-2.05-3.34.73-4.04-1.61-4.04-1.61-.55-1.39-1.34-1.76-1.34-1.76-1.09-.75.08-.73.08-.73 1.21.09 1.84 1.24 1.84 1.24 1.07 1.84 2.81 1.3 3.5.99.11-.78.42-1.3.76-1.6-2.67-.3-5.47-1.33-5.47-5.93 0-1.31.47-2.38 1.24-3.22-.12-.3-.54-1.52.12-3.18 0 0 1.01-.32 3.3 1.23a11.5 11.5 0 0 1 6 0c2.29-1.55 3.3-1.23 3.3-1.23.66 1.66.24 2.88.12 3.18.77.84 1.24 1.91 1.24 3.22 0 4.61-2.8 5.63-5.48 5.92.43.37.81 1.1.81 2.22 0 1.6-.01 2.89-.01 3.29 0 .32.22.69.82.58A12 12 0 0 0 24 12c0-6.63-5.37-12-12-12z" />
          </svg>
        </a>
        <a
          href={TWITTER_URL}
          target="_blank"
          rel="noopener noreferrer"
          className="text-muted hover:text-accent transition-colors w-8 h-8 flex items-center justify-center rounded-md hover:bg-surface"
          title="Twitter / X"
          aria-label="Twitter"
        >
          <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
            <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z" />
          </svg>
        </a>
      </div>
    </header>
  );
}
