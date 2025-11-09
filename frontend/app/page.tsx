import { BackendStatus } from "./components/BackendStatus";
import { LLMQuery } from "./components/LLMQuery";

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
      <LLMQuery />
    </div>
  );
}
