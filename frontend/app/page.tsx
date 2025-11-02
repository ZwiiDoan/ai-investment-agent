import { BackendStatus } from "./components/BackendStatus";

export default function Home() {
  const base = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";
  return (
    <div className="flex flex-col gap-8">
      <section>
        <h1 className="text-3xl font-semibold tracking-tight">AI Investment Agent</h1>
        <p className="mt-2 text-zinc-600 dark:text-zinc-400 max-w-prose">
          Minimal frontend connected to FastAPI backend. Live backend status below updates every 10 seconds.
          This will evolve into an interactive prompt interface for investment research workflows.
        </p>
      </section>
      <BackendStatus baseUrl={base} />
      <section className="space-y-3">
        <h2 className="text-lg font-semibold">LLM Query (Coming Soon)</h2>
        <div className="rounded border border-dashed border-zinc-300 dark:border-zinc-700 p-6 text-sm text-zinc-500">
          Prompt input + streaming response UI will be placed here (Week 2).
        </div>
      </section>
    </div>
  );
}
