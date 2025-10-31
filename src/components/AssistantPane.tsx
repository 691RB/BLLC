import { useState } from "react";
import type { Message } from "@/types";

type Props = {
  messages: Message[];
  onAsk: (text: string, ground: boolean) => Promise<void>;
};

export default function AssistantPane({ messages, onAsk }: Props) {
  const [input, setInput] = useState("");
  const [ground, setGround] = useState(true);
  const [busy, setBusy] = useState(false);

  async function send() {
    const text = input.trim();
    if (!text) return;
    setInput("");
    setBusy(true);
    try { await onAsk(text, ground); } finally { setBusy(false); }
  }

  return (
    <aside className="card" style={{ height: "100%", display: "grid", gridTemplateRows: "1fr auto", gap: 10 }}>
      <div style={{ overflow: "auto", display: "grid", gap: 10, paddingRight: 4 }}>
        {messages.map((m, i) => (
          <div key={i} className="msg" style={{
            border: "1px solid var(--border)", borderRadius: 10, padding: "10px 12px",
            background: m.role === "user" ? "#f2f4ff" : "#f8fafc"
          }}>
            <strong style={{ fontSize: 12, color: "var(--muted)" }}>{m.role.toUpperCase()}</strong>
            <div>{m.text}</div>
            {m.citations?.length ? (
              <div style={{ marginTop: 6, fontSize: 12 }}>
                <div style={{ color: "var(--muted)" }}>Sources:</div>
                <ul style={{ margin: "4px 0 0 18px" }}>
                  {m.citations.map((c, j) => (
                    <li key={j}>
                      <a href={c.uri} target="_blank" rel="noreferrer">{c.title || c.uri}</a>
                    </li>
                  ))}
                </ul>
              </div>
            ) : null}
          </div>
        ))}
      </div>

      <div style={{ display: "grid", gap: 8 }}>
        <div style={{ display: "flex", gap: 8 }}>
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); send(); } }}
            placeholder="Ask the Possibility Partner…"
            style={{ flex: 1, padding: "10px 12px", borderRadius: 10, border: "1px solid var(--border)" }}
          />
          <button onClick={send} disabled={busy} style={{ padding: "8px 12px", borderRadius: 10, background: "var(--accent)", color: "#fff", border: "1px solid var(--accent)" }}>
            {busy ? "…" : "Ask"}
          </button>
        </div>
        <label style={{ fontSize: 13, color: "var(--muted)" }}>
          <input type="checkbox" checked={ground} onChange={(e) => setGround(e.target.checked)} />
          &nbsp;Ground with Google Search (adds citations)
        </label>
      </div>
    </aside>
  );
}
