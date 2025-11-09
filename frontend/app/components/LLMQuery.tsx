"use client";
import React, { useState, useRef, useEffect } from "react";
import { askQuestion, ChatMessage } from "../lib/queryApi";
import { listConversations, getConversation, upsertMessage, newConversation, clearConversation, clearAll } from "../lib/chatStore";

export const LLMQuery: React.FC = () => {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [conversationList, setConversationList] = useState<{ id: string; updatedAt: number }[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const abortRef = useRef<AbortController | null>(null);
  const scrollRef = useRef<HTMLDivElement | null>(null);

  // Initial load of stored conversations
  useEffect(() => {
    const existing = listConversations();
    setConversationList(existing.map(c => ({ id: c.id, updatedAt: c.updatedAt })));
    if (existing.length > 0) {
      setConversationId(existing[0].id);
      setMessages(existing[0].messages.map(m => ({ role: m.role, content: m.content, sources: m.sources, chunks: m.chunks })));
    }
  }, []);

  // Auto-scroll on message change
  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: 'smooth' });
  }, [messages, loading]);

  function refreshConversationList() {
    const existing = listConversations();
    setConversationList(existing.map(c => ({ id: c.id, updatedAt: c.updatedAt })));
  }

  async function sendMessage() {
    const trimmed = input.trim();
    if (!trimmed) {
      setError("Please enter a message.");
      return;
    }
    setError(null);
  setMessages(prev => [...prev, { role: 'user', content: trimmed }]);
    setInput("");
    setLoading(true);
    abortRef.current?.abort();
    const controller = new AbortController();
    abortRef.current = controller;
    try {
      // Ensure conversation exists
      let cid = conversationId;
      if (!cid) {
        cid = newConversation();
        setConversationId(cid);
        refreshConversationList();
      }
      // Persist user turn
      upsertMessage(cid, { role: 'user', content: trimmed });
      const data = await askQuestion(trimmed, { conversationId: cid, signal: controller.signal });
      // Persist AI turn
      upsertMessage(cid, { role: 'ai', content: data.answer, sources: data.sources, chunks: data.chunks });
      setConversationId(data.conversation_id);
      setMessages(prev => [...prev, { role: 'ai', content: data.answer, sources: data.sources, chunks: data.chunks }]);
      refreshConversationList();
    } catch (err: unknown) {
      if (err instanceof Error && err.name !== 'AbortError') setError(err.message || 'Unknown error');
    } finally {
      setLoading(false);
    }
  }

  function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    void sendMessage();
  }

  function handleNewChat() {
    const cid = newConversation();
    setConversationId(cid);
    setMessages([]);
    refreshConversationList();
  }

  function handleSelectConversation(id: string) {
    const convo = getConversation(id);
    if (!convo) return;
    setConversationId(id);
    setMessages(convo.messages.map(m => ({ role: m.role, content: m.content, sources: m.sources, chunks: m.chunks })));
  }

  function handleClearConversation() {
    if (!conversationId) return;
    clearConversation(conversationId);
    setMessages([]);
    setConversationId(null);
    refreshConversationList();
  }

  function handleClearAll() {
    clearAll();
    setMessages([]);
    setConversationId(null);
    refreshConversationList();
  }

  return (
    <section className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold">Chat</h2>
        <div className="flex gap-2">
          <button type="button" onClick={handleNewChat} className="px-2 py-1 text-xs rounded border border-indigo-600 text-indigo-600 hover:bg-indigo-50 dark:hover:bg-indigo-900/30">New</button>
          <button type="button" onClick={handleClearConversation} disabled={!conversationId} className="px-2 py-1 text-xs rounded border border-zinc-400 text-zinc-600 disabled:opacity-40 hover:bg-zinc-50 dark:hover:bg-zinc-800">Clear</button>
          <button type="button" onClick={handleClearAll} className="px-2 py-1 text-xs rounded border border-red-500 text-red-600 hover:bg-red-50 dark:hover:bg-red-900/30">Clear All</button>
        </div>
      </div>
      {conversationList.length > 0 && (
        <div className="flex flex-wrap gap-2 text-[10px]">
          {conversationList.map(c => (
            <button
              key={c.id}
              onClick={() => handleSelectConversation(c.id)}
              className={
                'px-2 py-1 rounded border ' +
                (c.id === conversationId ? 'border-indigo-600 bg-indigo-50 dark:bg-indigo-900/30 text-indigo-700' : 'border-zinc-300 dark:border-zinc-700')
              }
              title={c.id}
            >
              {c.id.slice(0, 8)} · {new Date(c.updatedAt).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </button>
          ))}
        </div>
      )}
      <div ref={scrollRef} className="h-80 overflow-y-auto rounded border border-zinc-300 dark:border-zinc-700 p-4 bg-white dark:bg-zinc-900 flex flex-col gap-3 text-sm">
        {messages.length === 0 && <div className="text-zinc-500">Start the conversation by asking a question about the data.</div>}
        {messages.map((m, i) => (
          <div key={i} className={
            'max-w-[80%] rounded px-3 py-2 shadow flex flex-col gap-2 ' +
            (m.role === 'user'
              ? 'self-end bg-indigo-600 text-white'
              : 'self-start bg-zinc-100 dark:bg-zinc-800 text-zinc-800 dark:text-zinc-100')
          }>
            <p className="whitespace-pre-line">{m.content}</p>
            {m.role === 'ai' && (m.sources || m.chunks) && (
              <details className="text-xs">
                <summary className="cursor-pointer select-none">Sources & Context</summary>
                {m.sources && m.sources.length > 0 && (
                  <div className="mt-1">
                    <p className="font-medium">Sources ({m.sources.length})</p>
                    <ul className="list-disc list-inside space-y-0.5">
                      {m.sources.map(s => <li key={s}>{s}</li>)}
                    </ul>
                  </div>
                )}
                {m.chunks && m.chunks.length > 0 && (
                  <div className="mt-2">
                    <p className="font-medium">Chunks ({m.chunks.length})</p>
                    <ol className="space-y-1 max-h-40 overflow-y-auto">
                      {m.chunks.map((c, idx) => (
                        <li key={idx} className="rounded bg-zinc-50 dark:bg-zinc-700/40 p-2 border border-zinc-200 dark:border-zinc-600">
                          {c}
                        </li>
                      ))}
                    </ol>
                  </div>
                )}
              </details>
            )}
          </div>
        ))}
        {loading && (
          <div className="self-start text-xs text-zinc-500 animate-pulse">Thinking...</div>
        )}
      </div>
      <form onSubmit={onSubmit} className="flex flex-col gap-2">
        <div className="flex gap-2">
          <textarea
            value={input}
            onChange={e => setInput(e.target.value)}
            placeholder="Type your message..."
            rows={2}
            className="flex-1 rounded border border-zinc-300 dark:border-zinc-700 p-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 text-sm"
            disabled={loading}
          />
          <button
            type="submit"
            disabled={loading || !input.trim()}
            className="h-fit px-4 py-2 rounded bg-indigo-600 text-white text-sm font-medium disabled:opacity-50"
          >
            {loading ? 'Sending…' : 'Send'}
          </button>
        </div>
        {error && <div className="text-xs text-red-600">{error}</div>}
        {conversationId && (
          <div className="text-[10px] text-zinc-400">Conversation ID: {conversationId}</div>
        )}
      </form>
    </section>
  );
};
