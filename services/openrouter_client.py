import os
import requests
from typing import List, Dict, Any, Optional

OPENROUTER_API_URL = "https://api.openrouter.ai/v1/chat/completions"

def get_openrouter_headers() -> Dict[str, str]:
    api_key = os.environ.get("OPENROUTER_API_KEY") or ""
    # Streamlit Cloud injects secrets as env vars automatically
    # You will set OPENROUTER_API_KEY in the app's Secrets.
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        # Optional but recommended metadata:
        "HTTP-Referer": "https://share.streamlit.io/",
        "X-Title": "AI Possibility Lab",
    }
    return headers

def chat_completions(
    messages: List[Dict[str, Any]],
    model: Optional[str] = None,
    temperature: float = 0.2,
    max_tokens: Optional[int] = None,
) -> str:
    """
    Call OpenRouter chat completions. Returns the assistant message content.
    """
    model_slug = model or os.environ.get("OPENROUTER_MODEL", "").strip()
    if not model_slug:
        # Default to a Claude Sonnet if not provided; update if your account uses a different slug.
        model_slug = "openai/gpt-4o"

    payload: Dict[str, Any] = {
        "model": model_slug,
        "messages": messages,
        "temperature": temperature,
    }
    if max_tokens:
        payload["max_tokens"] = max_tokens

    r = requests.post(
        OPENROUTER_API_URL,
        headers=get_openrouter_headers(),
        json=payload,
        timeout=90,
    )
    r.raise_for_status()
    data = r.json()
    try:
        return data["choices"][0]["message"]["content"]
    except Exception:
        # Helpful error propagation
        return f"ERROR: Unexpected response: {data}"
