import json
from typing import Dict, Any, List, Tuple
import streamlit as st
from services.openrouter_client import chat_completions
from services.prompts import (
    POSSIBILITY_SYSTEM,
    IDENTITY_SYSTEM,
    UI_SYSTEM,
    BUILD_SYSTEM,
)

def _json_from_text(txt: str) -> Dict[str, Any]:
    """
    Robustly extract the largest JSON object from a string.
    - Finds first '{' and last '}' and attempts json.loads
    - Also supports fenced code blocks if present
    """
    if not isinstance(txt, str):
        raise ValueError("Model returned non-text response")

    # strip code fences if the model added them
    if "```" in txt:
        # try to take content inside the first fenced block
        parts = txt.split("```")
        # look for a json fenced block first
        for i in range(len(parts) - 1):
            if parts[i].strip().lower().endswith("json"):
                try:
                    return json.loads(parts[i + 1])
                except Exception:
                    pass
        # fallback to middle block
        if len(parts) >= 3:
            candidate = parts[1]
            try:
                return json.loads(candidate)
            except Exception:
                pass

    # generic bracket slicing
    start = txt.find("{")
    end = txt.rfind("}")
    if start != -1 and end != -1 and end > start:
        snippet = txt[start : end + 1]
        return json.loads(snippet)

    # last resort
    return json.loads(txt)

def _messages(system: str, user: str, history: List[Dict[str, str]] | None = None):
    msgs = [{"role": "system", "content": system}]
    if history:
        msgs += history
    msgs += [{"role": "user", "content": user}]
    return msgs

def chat(system: str, user: str, history: List[Dict[str, str]] | None = None) -> str:
    """
    Simple chat call (no streaming).
    """
    content = chat_completions(_messages(system, user, history))
    return content

@st.cache_data(show_spinner=False, ttl=3600, max_entries=64)
def generate_ui_cached(identity: Dict[str, Any]) -> Dict[str, str]:
    """
    Expensive call cached (Optional #6). Cache key is identity dict content.
    """
    user_prompt = (
        "Given the following assistant identity, produce UI JSON with keys "
        '"html" and "css" only.\n\nIDENTITY:\n' + json.dumps(identity, ensure_ascii=False, indent=2)
    )
    resp = chat_completions(_messages(UI_SYSTEM, user_prompt))
    try:
        data = _json_from_text(resp)
        if not isinstance(data, dict) or "html" not in data or "css" not in data:
            raise ValueError("Missing html/css keys")
        return {"html": data["html"], "css": data["css"]}
    except Exception:
        # one retry with stricter instruction
        retry_prompt = user_prompt + "\n\nReturn ONLY valid JSON: {\"html\":\"...\",\"css\":\"...\"}"
        resp2 = chat_completions(_messages(UI_SYSTEM, retry_prompt))
        data = _json_from_text(resp2)
        return {"html": data.get("html", ""), "css": data.get("css", "")}

@st.cache_data(show_spinner=False, ttl=3600, max_entries=64)
def generate_files_cached(identity: Dict[str, Any], ui: Dict[str, str] | None) -> List[Dict[str, str]]:
    """
    Expensive call cached (Optional #6). Cache key is identity+ui content.
    """
    user_payload = {
        "identity": identity,
        "ui": ui or {},
        "constraints": {
            "language": "python",
            "no_large_binaries": True,
            "target": "streamlit_minimal_scaffold",
        },
    }
    user_prompt = (
        "Generate a small app scaffold based on this payload. Return ONLY JSON with key 'files'.\n\n"
        + json.dumps(user_payload, ensure_ascii=False, indent=2)
    )
    resp = chat_completions(_messages(BUILD_SYSTEM, user_prompt))
    try:
        data = _json_from_text(resp)
        files = data.get("files", [])
        if not isinstance(files, list):
            raise ValueError("files should be a list")
        return files
    except Exception:
        # retry stricter
        retry_prompt = user_prompt + "\n\nReturn ONLY: {\"files\":[{\"name\":\"...\",\"content\":\"...\",\"mime\":\"text/plain\",\"description\":\"...\"}]}"
        resp2 = chat_completions(_messages(BUILD_SYSTEM, retry_prompt))
        data = _json_from_text(resp2)
        return data.get("files", [])

def get_system_prompt(page: str) -> str:
    if page == "possibility":
        return POSSIBILITY_SYSTEM
    if page == "identity":
        return IDENTITY_SYSTEM
    return POSSIBILITY_SYSTEM
