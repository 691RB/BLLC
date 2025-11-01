import os
import json
import requests
from typing import List, Dict, Any, Optional, Union

# Use the documented base URL; allow override via env if needed.
OPENROUTER_API_URL = os.environ.get(
    "OPENROUTER_BASE_URL",
    "https://openrouter.ai/api/v1/chat/completions"
)

def _env(name: str, default: str = "") -> str:
    v = os.environ.get(name)
    return v.strip() if isinstance(v, str) else default

def get_openrouter_headers() -> Dict[str, str]:
    """
    Builds headers per OpenRouter docs.
    - Authorization is required.
    - HTTP-Referer and X-Title are optional but recommended.
    """
    api_key = _env("OPENROUTER_API_KEY")
    if not api_key:
        # Keep explicit to make misconfigurations obvious in Streamlit logs.
        raise RuntimeError(
            "OPENROUTER_API_KEY is not set. Add it in Streamlit → Settings → Secrets."
        )

    site_url = _env("OPENROUTER_SITE_URL")  # e.g., your Streamlit share URL
    app_name = _env("OPENROUTER_APP_NAME", "AI Possibility Lab")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        # OpenRouter attribution headers (optional but helpful):
        # If you don't know your final URL yet, you can omit this;
        # once deployed, set OPENROUTER_SITE_URL to your public app URL.
        **({"HTTP-Referer": site_url} if site_url else {}),
        "X-Title": app_name,
    }
    # Some hosts add/expect 'Referer'; harmless to include both.
    if site_url:
        headers["Referer"] = site_url
    return headers

def _normalize_content(msg_content: Union[str, List[Dict[str, Any]]]) -> str:
    """
    OpenRouter normalizes to OpenAI's Chat API; content is usually a string.
    In rare cases (or via other endpoints), it may be a list of parts—join any text parts.
    """
    if isinstance(msg_content, str):
        return msg_content
    if isinstance(msg_content, list):
        parts: List[str] = []
        for p in msg_content:
            # Typical shape: {"type": "text", "text": "..."}
            if isinstance(p, dict) and p.get("type") == "text" and "text" in p:
                parts.append(str(p["text"]))
        return "".join(parts).strip()
    return str(msg_content)

def chat_completions(
    messages: List[Dict[str, Any]],
    model: Optional[str] = None,
    temperature: float = 0.2,
    max_tokens: Optional[int] = None,
    user: Optional[str] = None,
    enforce_json: bool = False,
    extra: Optional[Dict[str, Any]] = None,
) -> str:
    """
    Call OpenRouter Chat Completions and return assistant text.
    - model: if omitted, uses OPENROUTER_MODEL or defaults to openai/gpt-4.1-mini
    - enforce_json: if True, sets response_format={"type":"json_object"} (OpenAI+supported models)
    - user: stable end-user id (recommended for abuse detection)
    - extra: advanced params passthrough (e.g., tools, top_p, etc.)
    """
    model_slug = (model or _env("OPENROUTER_MODEL") or "openai/gpt-4.1-mini").strip()

    payload: Dict[str, Any] = {
        "model": model_slug,
        "messages": messages,
        "temperature": temperature,
    }
    if max_tokens is not None:
        payload["max_tokens"] = max_tokens
    if user:
        payload["user"] = user
    if enforce_json:
        # Only supported by OpenAI + some models; harmlessly ignored by others.
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
        return f"ERROR: Network/requests exception: {e}"

    # Surface non-200s (OpenRouter returns useful JSON in many error cases).
    if r.status_code != 200:
        try:
            err = r.json()
            return f"ERROR {r.status_code}: {json.dumps(err)}"
        except Exception:
            return f"ERROR {r.status_code}: {r.text}"

    data = r.json()

    # Handle top-level API error field if present
    if isinstance(data, dict) and "error" in data:
        return f"ERROR: {data[']()
