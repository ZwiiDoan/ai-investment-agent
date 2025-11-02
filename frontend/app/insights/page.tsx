import React from 'react';
import { InsightCard } from '../components/InsightCard';

// Placeholder types for future dynamic data
interface InsightItem {
  id: string;
  title: string;
  sentiment: 'positive' | 'neutral' | 'negative';
  published: string; // ISO date
}


const mockInsights: InsightItem[] = [
  {
    id: '1',
    title: 'Federal Reserve signals rate pause impacting growth sectors',
    sentiment: 'neutral',
    published: '2025-11-01'
  },
  {
    id: '2',
    title: 'Tech earnings beat expectations driving bullish sentiment',
    sentiment: 'positive',
    published: '2025-11-01'
  },
  {
    id: '3',
    title: 'Energy stocks dip as crude demand forecasts lowered',
    sentiment: 'negative',
    published: '2025-10-31'
  }
];

// Future: fetch dynamic insights from backend /query (RAG) endpoint
// async function fetchInsights() {
//   const base = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';
//   const res = await fetch(`${base}/query?prompt=market+summary`);
//   if (!res.ok) throw new Error('Failed to fetch insights');
//   return res.json();
// }

export default function InsightsPage() {
  return (
    <div className="flex flex-col gap-8">
      <header className="space-y-2">
        <h1 className="text-3xl font-semibold tracking-tight">Market Insights</h1>
        <p className="text-zinc-600 dark:text-zinc-400 max-w-prose">
          Sample investment-related headlines with simple sentiment labels. This page will later
          retrieve contextual answers from the RAG pipeline (/query).
        </p>
      </header>
      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {mockInsights.map(item => (
          <InsightCard
            key={item.id}
            title={item.title}
            sentiment={item.sentiment}
            published={item.published}
          />
        ))}
      </section>
      <footer className="flex items-center justify-between pt-4 border-t border-dashed border-zinc-300 dark:border-zinc-700">
        <span className="text-sm text-zinc-500">Pagination coming soon…</span>
        <div className="flex gap-2">
          <button disabled className="px-3 py-1 rounded border border-zinc-300 dark:border-zinc-700 text-zinc-400 text-sm bg-zinc-100 dark:bg-zinc-800">Prev</button>
          <button disabled className="px-3 py-1 rounded border border-zinc-300 dark:border-zinc-700 text-zinc-400 text-sm bg-zinc-100 dark:bg-zinc-800">Next</button>
        </div>
      </footer>
    </div>
  );
}
