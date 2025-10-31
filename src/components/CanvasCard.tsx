import { useState } from "react";
import type { ElementKey } from "@/types";

type Props = {
  keyId: ElementKey;
  label: string;
  savedSummary?: string;
  active: boolean;
  onClick: () => void;
  onSave: (keyId: ElementKey, text: string) => Promise<void>;
};

export default function CanvasCard({ keyId, label, savedSummary, active, onClick, onSave }: Props) {
  const [text, setText] = useState("");
  const [saving, setSaving] = useState(false);
  const [badge, setBadge] = useState(savedSummary ? "Saved ✓" : "");

  return (
    <div className={`card ${active ? "active" : ""}`} onClick={(e) => {
      if ((e.target as HTMLElement).tagName === "BUTTON") return;
      onClick();
    }}>
      <h3 style={{ margin: 0, fontSize: 14, color: "var(--muted)", textTransform: "uppercase", letterSpacing: ".3px" }}>
        {label}
      </h3>

      <textarea
        placeholder={`Write or paste notes for “${label}”…`}
        style={{ width: "100%", minHeight: 120, resize: "vertical", border: "1px solid var(--border)", borderRadius: 10, padding: 10, background: "#fafafa" }}
        value={text}
        onChange={(e) => setText(e.target.value)}
      />

      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", gap: 8 }}>
        <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
          <button
            disabled={saving}
            onClick={async () => {
              if (!text.trim()) return;
              setSaving(true);
              try {
                await onSave(keyId, text.trim());
                setBadge("Saved ✓");
              } catch (e) {
                setBadge("⚠️ Save failed");
              } finally {
                setSaving(false);
              }
            }}
            style={{ padding: "8px 12px", borderRadius: 10, border: "1px solid var(--border)", background: "#eefbf4", cursor: "pointer" }}
          >
            {saving ? "Saving…" : "Save"}
          </button>
          <span style={{ fontSize: 12, color: "var(--ok)" }}>{badge}</span>
        </div>
        <span style={{ fontSize: 12, color: "var(--muted)" }}>{savedSummary ? "Summary saved" : "No summary yet"}</span>
      </div>

      {savedSummary && (
        <p style={{ marginTop: 8, fontSize: 13, color: "var(--muted)" }}>
          <em>{savedSummary}</em>
        </p>
      )}
    </div>
  );
}
