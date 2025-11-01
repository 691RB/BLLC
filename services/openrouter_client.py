import os
import json
import requests
from typing import List, Dict, Any, Optional, Union

# -------- Streamlit Cloud secret access (safe fallback to env) ----------
try:
    import streamlit as st  # preferred on Streamlit Cloud
    def _secret(name: str, default: str = "") -> str:
        try:
            v = st.secrets.get(name, default)
        except Exception:
            v = default
        if isinstance(v, str):
            return v.strip()
        return default
except Exception:
    def _secret(name: str, default: str = "") -> str:
        v = os.environ.get(name, default)
        return v.strip() if isinstance(v, str) else default

# -------- Constants (force THIS model only) ------------------------------
FORCED_MODEL = "openai/gpt-4.1-mini"  # use this model and this model only

# Docs show this base URL
# https://openrouter.ai/docs/api-reference/overview (Headers & endpoint)
OPENROUTER_API_URL = _secret("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1/chat/completions")


def get_openrouter_headers() -> Dict[str, str]:
    """
    Build headers per OpenRouter docs:
    - Authorization required
    - Optional 'HTTP-Referer' and 'X-Title' for attribution
    """
    api_key = _secret("OPENROUTER_API_KEY")
    if not api_key:
        # Make misconfiguration obvious in Streamlit logs
        raise RuntimeError("OPENROUTER_API_KEY is not set in Streamlit Secrets.")

    site_url = _secret("OPENROUTER_SITE_URL", "")
    app_name = _secret("OPENROUTER_APP_NAME", "AI Possibility Lab")

    headers: Dict[str, str] = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "X-Title": app_name,
    }
    # Optional but recommended for rankings / attribution
    if site_url:
        headers["HTTP-Referer"] = site_url
        headers["Referer"] = site_url  # harmless duplicate for some hosts
    return headers


def _normalize_content(msg_content: Union[str, List[Dict[str, Any]]]) -> str:
    """
    OpenRouter normalizes to OpenAI Chat; content is usually a string.
    If it's a list of parts, join text parts.
    """
    if isinstance(msg_content, str):
        return msg_content
    if isinstance(msg_content, list):
        parts: List[str] = []
        for p in msg_content:
            if isinstance(p, dict) and p.get("type") == "text" and "text" in p:
                parts.append(str(p["text"]))
        return "".join(parts).strip()
    return str(msg_content)


def chat_completions(
    messages: List[Dict[str, Any]],
    model: Optional[str] = None,          # ignored (we force FORCED_MODEL)
    temperature: float = 0.2,
    max_tokens: Optional[int] = None,
    user: Optional[str] = None,
    enforce_json: bool = False,           # if True, ask for JSON outputs
    extra: Optional[Dict[str, Any]] = None,
) -> str:
    """
    Call OpenRouter Chat Completions and return assistant text.
    Always uses FORCED_MODEL = 'openai/gpt-4.1-mini'.
    """
    payload: Dict[str, Any] = {
        "model": FORCED_MODEL,
        "messages": messages,
        "temperature": temperature,
    }
    if max_tokens is not None:
        payload["max_tokens"] = max_tokens
    if user:
        payload["user"] = user
    if enforce_json:
        # Supported by OpenAI models; ignored by others.
        payload["response_format"] = {"type": "json_object"}
    if extra:
        payload.update(extra)

    try:
        r = requests.post(
            OPENROUTER_API_URL,
            headers=get_openrouter_headers(),
            json=payload,
            timeout=90,
        )
    except requests.RequestException as e:
        return f"ERROR: Network exception: {e}"

    if r.status_code != 200:
        # Return server JSON if possible for easier debugging on Streamlit Cloud
        try:
            return "ERROR " + str(r.status_code) + ": " + json.dumps(r.json())[:1200]
        except Exception:
            return "ERROR " + str(r.status_code) + ": " + r.text[:1200]

    # Parse success response
    try:
        data = r.json()
    except ValueError:
        return "ERROR: Non-JSON response from OpenRouter."

    if isinstance(data, dict) and "error" in data:
        # OpenRouter error shape
        return "ERROR: " + json.dumps(data.get("error"))[:1200]

    try:
        choice0 = data["choices"][0]
        msg = choice0.get("message", {})
        content = msg.get("content", "")
        return _normalize_content(content) or ""
    except Exception:
        # Avoid f-strings in error paths (prevents unterminated literal issues)
        return "ERROR: Unexpected response shape: " + json.dumps(data)[:1200]
