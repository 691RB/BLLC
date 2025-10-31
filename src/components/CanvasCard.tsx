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
      <h3 className="card-title">{label}</h3>

      <textarea
        className="card-input"
        placeholder={`Write or paste notes for “${label}”…`}
        value={text}
        onChange={(e) => setText(e.target.value)}
      />

      <div className="row">
        <div className="row-left">
          <button
            className="btn btn-save"
            disabled={saving}
            onClick={async () => {
              if (!text.trim()) return;
              setSaving(true);
              try {
                await onSave(keyId, text.trim());
                setBadge("Saved ✓");
              } catch {
                setBadge("⚠️ Save failed");
              } finally {
                setSaving(false);
              }
            }}
          >
            {saving ? "Saving…" : "Save"}
          </button>
          <span className="badge">{badge}</span>
        </div>
        <span className="muted">{savedSummary ? "Summary saved" : "No summary yet"}</span>
      </div>

      {savedSummary && (
        <p style={{ marginTop: 8, fontSize: 13 }} className="muted">
          <em>{savedSummary}</em>
        </p>
      )}
    </div>
  );
}
