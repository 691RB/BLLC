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
    <aside className="card assistant">
      <div className="chat">
        {messages.map((m, i) => (
          <div key={i} className={`msg ${m.role}`}>
            <strong style={{ fontSize: 12, color: "var(--muted)" }}>{m.role.toUpperCase()}</strong>
            <div>{m.text}</div>
            {m.citations?.length ? (
              <div style={{ marginTop: 6, fontSize: 12 }}>
                <div className="muted">Sources:</div>
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
        <div className="composer">
          <input
            className="input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); send(); } }}
            placeholder="Ask the Possibility Partner…"
          />
          <button className="btn btn-ask" onClick={send} disabled={busy}>
            {busy ? "…" : "Ask"}
          </button>
        </div>
        <label className="muted" style={{ fontSize: 13 }}>
          <input type="checkbox" checked={ground} onChange={(e) => setGround(e.target.checked)} />
          &nbsp;Ground with Google Search (adds citations)
        </label>
      </div>
    </aside>
  );
}
