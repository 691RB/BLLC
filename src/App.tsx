import { useMemo, useState } from "react";
import CanvasCard from "@/components/CanvasCard";
import AssistantPane from "@/components/AssistantPane";
import { postJSON } from "@/lib/api";
import type { AskPayload, AskReply, ElementKey, Message, SavedMap } from "@/types";

const KEYS: { key: ElementKey; label: string }[] = [
  { key: "what", label: "What is the Problem or Need?" },
  { key: "who", label: "Who are you helping?" },
  { key: "why", label: "Why does solving this matter?" },
  { key: "how", label: "How will the assistant address it?" },
  { key: "contribution", label: "What contribution will your assistant make?" },
  { key: "name", label: "Assistant Name" },
];

export default function App() {
  const [active, setActive] = useState<ElementKey>("what");
  const [saved, setSaved] = useState<SavedMap>({});
  const [messages, setMessages] = useState<Message[]>([]);

  async function saveElement(elementKey: ElementKey, text: string) {
    const payload: AskPayload = { action: "save", input: text, elementKey };
    const res = await postJSON<AskReply>("/api/ask", payload) as any;
    setSaved((s) => ({ ...s, [elementKey]: res.summary }));
  }

  async function ask(text: string, ground: boolean) {
    setMessages((m) => [...m, { role: "user", text }]);
    const payload: AskPayload = { action: "ask", input: text, elementKey: active, saved, ground };
    const res = await postJSON<AskReply>("/api/ask", payload) as any;
    setMessages((m) => [
      ...m,
      {
        role: "assistant",
        text: res.reply || "(no reply)",
        grounded: Boolean(res.grounded),
        citations: res.citations,
        queries: res.webSearchQueries,
      },
    ]);
  }

  // -------- Export --------
  function exportJSON() {
    const blob = new Blob(
      [JSON.stringify({ saved, messages, exportedAt: new Date().toISOString() }, null, 2)],
      { type: "application/json" }
    );
    const url = URL.createObjectURL(blob);
    download(url, "possibility_lab_export.json");
  }

  const markdown = useMemo(() => {
    const lines: string[] = [];
    lines.push("# Possibility Finding — Export");
    lines.push("");
    for (const { key, label } of KEYS) {
      lines.push(`## ${label}`);
      lines.push(saved[key] ? saved[key]! : "_(empty)_");
      lines.push("");
    }
    lines.push("## Conversation");
    messages.forEach((m) => {
      lines.push(`**${m.role.toUpperCase()}**: ${m.text}`);
      if (m.citations?.length) {
        const list = m.citations.map((c, i) => `[${i + 1}] ${c.title || c.uri} — ${c.uri}`).join("\n");
        lines.push(list);
      }
    });
    return lines.join("\n");
  }, [saved, messages]);

  function exportMarkdown() {
    const blob = new Blob([markdown], { type: "text/markdown" });
    const url = URL.createObjectURL(blob);
    download(url, "possibility_lab_export.md");
  }

  function download(url: string, filename: string) {
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  }

  // -------- Render --------
  return (
    <>
      <section className="grid" style={{ alignContent: "start" }}>
        {KEYS.map(({ key, label }) => (
          <CanvasCard
            key={key}
            keyId={key}
            label={label}
            active={active === key}
            onClick={() => setActive(key)}
            savedSummary={saved[key]}
            onSave={saveElement}
          />
        ))}
        <div className="card" style={{ gridColumn: "1 / -1", display: "flex", gap: 8 }}>
          <button onClick={exportJSON} style={{ padding: "8px 12px", borderRadius: 10, border: "1px solid var(--border)", cursor: "pointer" }}>
            Export JSON
          </button>
          <button onClick={exportMarkdown} style={{ padding: "8px 12px", borderRadius: 10, border: "1px solid var(--border)", cursor: "pointer" }}>
            Export Markdown
          </button>
        </div>
      </section>

      <AssistantPane messages={messages} onAsk={ask} />
    </>
  );
}
