import React from 'react';
import { sentimentColor } from './sentiment';

export interface InsightCardProps {
  title: string;
  sentiment: 'positive' | 'neutral' | 'negative';
  published: string; // ISO date
}


export const InsightCard: React.FC<InsightCardProps> = ({ title, sentiment, published }) => (
  <article className="rounded border border-zinc-200 dark:border-zinc-700 p-4 flex flex-col gap-3 bg-white dark:bg-zinc-900 shadow-sm">
    <h2 className="font-medium text-zinc-900 dark:text-zinc-100 line-clamp-3">{title}</h2>
    <div className="flex items-center justify-between text-sm">
      <span className={`px-2 py-0.5 rounded border text-xs font-medium ${sentimentColor(sentiment)}`}>
        {sentiment}
      </span>
      <time className="text-zinc-500" dateTime={published}>{published}</time>
    </div>
  </article>
);
