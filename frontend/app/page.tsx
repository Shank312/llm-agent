
"use client";

import { useState } from "react";
import { chat } from "@/lib/api";

type Message = {
  role: "user" | "assistant";
  content: string;
};

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();

    if (!input.trim() || loading) return;

    const userMessage: Message = {
      role: "user",
      content: input,
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const result = await chat(input);

      const assistantMessage: Message = {
        role: "assistant",
        content:
          typeof result === "string"
            ? result
            : result.response ?? result.message ?? JSON.stringify(result),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Something went wrong while contacting the AI agent.",
        },
      ]);

      console.error(error);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-gray-950 text-white">
      <div className="mx-auto flex min-h-screen max-w-5xl flex-col">
        {/* Header */}
        <header className="border-b border-gray-800 px-6 py-5">
          <h1 className="text-2xl font-bold">
            🧠 LLM Agent
          </h1>

          <p className="mt-1 text-sm text-gray-400">
            AI Agent with Memory, Tools and RAG
          </p>
        </header>

        {/* Messages */}
        <section className="flex-1 space-y-6 overflow-y-auto px-6 py-8">
          {messages.length === 0 && (
            <div className="flex min-h-[50vh] items-center justify-center">
              <div className="text-center">
                <div className="mb-4 text-5xl">🧠</div>

                <h2 className="text-2xl font-semibold">
                  How can I help you?
                </h2>

                <p className="mt-2 text-gray-400">
                  Ask the agent a question.
                </p>
              </div>
            </div>
          )}

          {messages.map((message, index) => (
            <div
              key={index}
              className={`flex ${
                message.role === "user"
                  ? "justify-end"
                  : "justify-start"
              }`}
            >
              <div
                className={`max-w-3xl rounded-2xl px-5 py-3 ${
                  message.role === "user"
                    ? "bg-blue-600"
                    : "bg-gray-800"
                }`}
              >
                <p className="whitespace-pre-wrap">
                  {message.content}
                </p>
              </div>
            </div>
          ))}

          {loading && (
            <div className="flex justify-start">
              <div className="rounded-2xl bg-gray-800 px-5 py-3 text-gray-400">
                Agent is thinking...
              </div>
            </div>
          )}
        </section>

        {/* Input */}
        <form
          onSubmit={handleSubmit}
          className="border-t border-gray-800 p-6"
        >
          <div className="flex gap-3">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask your AI agent..."
              disabled={loading}
              className="flex-1 rounded-xl border border-gray-700 bg-gray-900 px-4 py-3 outline-none focus:border-blue-500"
            />

            <button
              type="submit"
              disabled={loading || !input.trim()}
              className="rounded-xl bg-blue-600 px-6 py-3 font-medium hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {loading ? "..." : "Send"}
            </button>
          </div>
        </form>
      </div>
    </main>
  );
}