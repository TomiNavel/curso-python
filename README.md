# Aprende Python

> Curso interactivo de Python como aplicación web. Teoría, ejercicios ejecutables en el navegador y preparación para entrevistas técnicas.

**[▶ Abrir la demo](https://tominavel.github.io/curso-python/)** — sin instalación, corre en el navegador.

**Si te es útil, dale una estrella ⭐ — me ayuda a priorizar y a que más gente lo encuentre.**

[![GitHub stars](https://img.shields.io/github/stars/TomiNavel/curso-python?style=social)](https://github.com/TomiNavel/curso-python/stargazers)
![Node](https://img.shields.io/badge/Node-339933?logo=node.js&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?logo=typescript&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-646CFF?logo=vite&logoColor=white)
![Tailwind](https://img.shields.io/badge/Tailwind-06B6D4?logo=tailwindcss&logoColor=white)

## Características

- **Python en el navegador** con Pyodide — sin backend, sin instalación.
- **Ejercicios ejecutables** con solución emparejada por nombre de archivo.
- **Preparación para entrevistas** — preguntas, errores comunes y ejercicios de debugging.
- **Contenido en markdown** — añadir un tema no requiere tocar código TypeScript.
- **Navegación por URL** — cada subtopic tiene su propio `#/N/N.M`, compartible y recargable.

## Quick start

```bash
npm install
npm run dev
```

Abre [http://localhost:5173](http://localhost:5173). Requiere Node 20+.

## Añadir un tema

1. Crear `src/Temario/NN-slug/NN-slug.md` con la lección.
2. Registrar el tema en `src/Temario/00-temas.md` con `## N. Título` y sus subtopics.
3. Opcionalmente añadir `Ejercicios/` y `Entrevistas/`.

Guía completa: [docs/añadir-tema.md](docs/añadir-tema.md).

<details>
<summary><b>Estructura del repositorio</b></summary>

```
src/
├── App.tsx               Shell de la app: sidebar + panel, routing por hash
├── components/           Componentes de UI (Sidebar, ContentPanel, Markdown…)
├── data/
│   ├── index.ts          Parsea 00-temas.md → índice del sidebar (eager)
│   ├── content.ts        Registra cada archivo del curso como chunk lazy
│   └── topics.ts         Lista pública de temas que consume la UI
├── lib/
│   ├── content/          fetchers.ts, parsers.ts, useTopicContent.ts
│   ├── markdown.ts       marked + highlight.js
│   ├── pyodide.ts        Carga y ejecución de Python en el navegador
│   └── hashRoute.ts      Sincroniza selected ↔ window.location.hash
├── types/course.ts       Tipos de dominio (Topic, Selection, PanelData…)
└── Temario/              Contenido del curso
    ├── 00-temas.md       Índice jerárquico del curso (fuente de metadatos)
    ├── 01-Fundamentos/
    ├── 02-Strings/
    └── …
docs/                     Documentación del proyecto
```

</details>

<details>
<summary><b>Cómo funciona la app</b></summary>

1. Al arrancar se parsea `Temario/00-temas.md` y se construye el índice del sidebar (títulos + subtopics). Es lo único que se carga eagerly.
2. Cada lección, ejercicio y archivo de entrevistas es un chunk independiente de Vite. Al abrir un tema por primera vez se descarga su chunk; la segunda visita usa el cache del hook `useTopicContent`.
3. Los bloques de código Python dentro del markdown se convierten en `RunableBlock`: un editor + botón "Ejecutar" que corre el código en Pyodide (WebAssembly, sin servidor).
4. La selección actual (`{ topicId, subtopicId }`) se sincroniza con `#/N/N.M` en la URL. Recargar o compartir el link conserva el tema abierto.

</details>

<details>
<summary><b>Stack</b></summary>

- **React 19** + **TypeScript 6** + **Vite 8**
- **Tailwind CSS 4** (tema custom en `src/index.css`)
- **marked** + **marked-highlight** + **highlight.js** para renderizar markdown con syntax highlighting
- **Pyodide 0.26** (cargado desde CDN bajo demanda) para ejecutar Python en el navegador

</details>

<details>
<summary><b>Convenciones de contenido</b></summary>

- **Lección**: `# N. Título`, secciones `## N.M.`, subsecciones `### N.M.X.`
- **Ejercicios**: empiezan con un docstring `"""…"""` que la app extrae como enunciado; el resto es el código inicial del alumno.
- **Soluciones**: mismo nombre de archivo que el ejercicio, bajo `Ejercicios/Soluciones/`.
- **Entrevistas**: `Entrevistas/01-Preguntas.md` con formato `### RN. pregunta` bajo un heading `## Respuestas`.

Detalles completos en [docs/añadir-tema.md](docs/añadir-tema.md) y en el [CLAUDE.md](CLAUDE.md) del proyecto.

</details>

<details>
<summary><b>Build y deploy</b></summary>

```bash
npm run build      # dist/ autocontenido
npm run preview    # servir el build localmente
npm run lint
```

`dist/` se puede servir con cualquier static host (Netlify, Vercel, GitHub Pages, S3 + CloudFront). El bundle inicial pesa ~100 KB gzip; cada tema descarga ~10-30 KB adicionales la primera vez que se abre.

</details>

## Licencia

Doble licencia:

- **Código** (todo salvo `src/Temario/`): MIT — ver [LICENSE](LICENSE).
- **Contenido del curso** (`src/Temario/`): copyright del autor, todos los derechos reservados — ver [LICENSE-CONTENT.md](LICENSE-CONTENT.md).
