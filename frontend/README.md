# Frontend (Next.js)

This directory contains the experimental Next.js frontend for the AI Investment Agent.

## Pages

- `/` Home page (backend status + intro)
- `/insights` Sample market insights (static mock data) — will later integrate with backend `/query` RAG endpoint.

## Development

```bash
npm install
npm run dev
```

If port 3000 is occupied (Grafana etc.), start on another port:
```bash
set PORT=3002 && npm run dev   # Windows cmd
PORT=3002 npm run dev          # macOS/Linux
```

## Environment Variables

Set the backend base URL (FastAPI) for future dynamic fetches:
```
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```
Place in `.env.local` at the frontend root.

## Planned Integrations

- Replace mock insights with real RAG responses via `/query`
- Streaming LLM responses
- Auth & API keys (Month 2+)

## Components

- `BackendStatus` displays backend health every 10s.
- `InsightCard` reusable sentiment-labeled headline card.

## Notes

Tailwind utility classes used for rapid iteration; design system will evolve later.
