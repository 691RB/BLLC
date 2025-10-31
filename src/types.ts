export type ElementKey = "what" | "who" | "why" | "how" | "contribution" | "name";

export type SavedMap = Partial<Record<ElementKey, string>>;

export type Message = {
  role: "user" | "assistant";
  text: string;
  grounded?: boolean;
  citations?: { title?: string; uri?: string }[];
  queries?: string[];
};

export type AskPayload = {
  action: "ask" | "save";
  input: string;
  elementKey?: ElementKey;
  saved?: SavedMap;
  ground?: boolean;
};

export type AskReply =
  | { reply: string; grounded?: boolean; citations?: { title?: string; uri?: string }[]; webSearchQueries?: string[] }
  | { summary: string }
  | { error: string };
