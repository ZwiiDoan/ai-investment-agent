"use client";
import { useEffect, useState, useRef } from "react";

interface HealthData {
  status: string;
  version?: string;
  timestamp?: string;
  detail?: string;
}

interface BackendStatusProps {
  baseUrl: string;
  initial?: HealthData;
  intervalMs?: number;
}

export function BackendStatus({ baseUrl, initial, intervalMs = 10000 }: BackendStatusProps) {
  const [data, setData] = useState<HealthData | undefined>(initial);
  const [loading, setLoading] = useState(!initial);
  const [error, setError] = useState<string | null>(null);
  const abortRef = useRef<AbortController | null>(null);

  async function load() {
    abortRef.current?.abort();
    const controller = new AbortController();
    abortRef.current = controller;
    try {
      setLoading(true);
      const res = await fetch(`${baseUrl}/health`, { signal: controller.signal });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const json = (await res.json()) as HealthData;
      setData(json);
      setError(null);
    } catch (e: unknown) {
      if (e instanceof DOMException && e.name === "AbortError") return;
      setError(e instanceof Error ? e.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    const id = setInterval(load, intervalMs);
    // Only auto-load if no initial data
    if (!initial) load();
    return () => {
      clearInterval(id);
      abortRef.current?.abort();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [baseUrl, intervalMs]);

  const statusColor =
    data?.status === "ok"
      ? "text-green-600"
      : data?.status === "error" || data?.status === "unreachable"
      ? "text-red-600"
      : "text-zinc-600";

  return (
    <div className="rounded-lg border border-zinc-200 dark:border-zinc-700 p-5 bg-white/70 dark:bg-zinc-900/40 backdrop-blur text-sm">
      <div className="flex items-center justify-between mb-3">
        <h2 className="font-medium uppercase tracking-wide text-zinc-500">Backend Health (Live)</h2>
        {loading && (
          <span className="animate-pulse text-xs text-zinc-400" aria-label="Loading">
            updating...
          </span>
        )}
      </div>
      {error && (
        <div className="text-red-600 mb-2">Error: {error}</div>
      )}
      {data ? (
        <div className="space-y-1">
          <div>
            Status: <span className={statusColor}>{data.status}</span>
          </div>
          {data.version && <div>Version: {data.version}</div>}
          {data.timestamp && <div>Timestamp: {data.timestamp}</div>}
          {data.detail && <div className="text-zinc-500">Detail: {data.detail}</div>}
        </div>
      ) : !loading && !error ? (
        <div className="text-zinc-500">No data received.</div>
      ) : null}
    </div>
  );
}
