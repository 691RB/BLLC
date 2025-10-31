import { GoogleAI } from "@google/genai";
import fs from "node:fs";
import path from "node:path";

const MODEL = "gemini-flash-lite-latest";

// Reads ppart_identity.txt from the repo root on each request (small file; keeps it editable)
function readIdentity(): string {
  const file = path.join(process.cwd(), "ppart_identity.txt");
  if (!fs.existsSync(file)) throw new Error("ppart_identity.txt not found at repo root.");
  return fs.readFileSync(file, "utf8");
}

function buildContext(saved?: Record<string, string>) {
  if (!saved) return "(none)";
  const lines = Object.entries(saved)
    .filter(([, v]) => typeof v === "string" && v.trim())
    .map(([k, v]) => `- ${k}: ${v.trim()}`);
  return lines.length ? lines.join("\n") : "(none)";
}

export default async function handler(req: any, res: any) {
  if (req.method === "OPTIONS") {
    res.setHeader("Access-Control-Allow-Origin", "*");
    res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
    res.setHeader("Access-Control-Allow-Headers", "Content-Type");
    return res.status(204).end();
  }

  try {
    if (req.method !== "POST") return res.status(405).json({ error: "Use POST" });

    const { action, input, elementKey, saved, ground } = req.body || {};
    if (!action) return res.status(400).json({ error: "Missing 'action'." });

    const apiKey = process.env.GOOGLE_API_KEY;
    if (!apiKey) return res.status(500).json({ error: "Missing GOOGLE_API_KEY env var." });

    const ai = new GoogleAI({ apiKey });
    const identity = readIdentity();

    if (action === "ask") {
      if (!input || typeof input !== "string") return res.status(400).json({ error: "Missing 'input' for ask." });

      const context = buildContext(saved);
      const active = elementKey || "(none)";
      const prompt =
        `Context (summaries saved so far):\n${context}\n\n` +
        `Active element: ${active}\n\n` +
        `User says:\n${input}\n\n` +
        `Respond concisely with supportive, probing guidance. Offer concrete suggestions, examples, and reframes when helpful.`;

      // Enable grounding via Google Search when requested
      const tools = ground ? [{ googleSearch: {} }] : undefined;

      const response = await ai.models.generateContent({
        model: MODEL,
        contents: prompt,
        systemInstruction: identity,
        tools
      });

      const text = (response.text || "").trim();

      // Extract grounding metadata if present (citations, queries)
      const cand = (response as any).candidates?.[0];
      const gm = cand?.groundingMetadata;
      const chunks = gm?.groundingChunks as any[] | undefined;
      const queries = gm?.webSearchQueries as string[] | undefined;

      const citations =
        chunks?.map((c) => (c.web?.uri ? { uri: c.web.uri as string, title: c.web.title as string | undefined } : null))
              ?.filter(Boolean) ?? [];

      return res.status(200).json({
        reply: text,
        grounded: Boolean(gm),
        citations,
        webSearchQueries: queries
      });
    }

    if (action === "save") {
      if (!elementKey) return res.status(400).json({ error: "Missing 'elementKey' for save." });
      if (!input || typeof input !== "string") return res.status(400).json({ error: "Missing 'input' text to summarize." });

      const prompt = `Summarize the following '${elementKey}' into 1–2 sentences. Plain text, no bullets, no headings:\n\n${input}`;
      const response = await ai.models.generateContent({
        model: MODEL,
        contents: prompt,
        systemInstruction: identity
      });
      const summary = (response.text || "").trim();
      return res.status(200).json({ summary });
    }

    return res.status(400).json({ error: "Invalid action. Use 'ask' or 'save'." });
  } catch (e: any) {
    return res.status(500).json({ error: `Server error: ${e?.message || e}` });
  }
}
