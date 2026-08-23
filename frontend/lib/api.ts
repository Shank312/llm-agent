

const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function chat(message: string) {
  const response = await fetch(`${API_URL}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      message,
    }),
  });

  if (!response.ok) {
    throw new Error("Failed to communicate with AI agent");
  }

  return response.json();
}

export async function ragQuery(query: string) {
  const response = await fetch(`${API_URL}/rag/query`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      query,
    }),
  });

  if (!response.ok) {
    throw new Error("RAG query failed");
  }

  return response.json();
}

export async function getLogs() {
  const response = await fetch(`${API_URL}/logs`);

  if (!response.ok) {
    throw new Error("Failed to fetch logs");
  }

  return response.json();
}