export type Sentiment = 'positive' | 'neutral' | 'negative';

export function sentimentColor(sentiment: Sentiment) {
  switch (sentiment) {
    case 'positive':
      return 'bg-green-100 text-green-700 border-green-300';
    case 'negative':
      return 'bg-red-100 text-red-700 border-red-300';
    default:
      return 'bg-gray-100 text-gray-700 border-gray-300';
  }
}
