"""Model roster and a single OpenRouter-backed chat client.

Everything routes through OpenRouter so one API key reaches every model. Swap
``OPENROUTER_API_KEY`` for direct provider keys later if you want, but for a
cross-model benchmark the single gateway keeps the harness simple and the
latency numbers comparable (same network path for every call).
"""
from __future__ import annotations

import os
import time
from dataclasses import dataclass

import requests

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


@dataclass(frozen=True)
class Model:
    """A contestant in the benchmark."""

    id: str          # OpenRouter model id
    label: str       # short name for tables/charts
    tier: str        # flagship | efficient | open


# Verified available on OpenRouter on 2026-06-10. Edit freely — the runner
# accepts --models to override this default lineup.
ROSTER: dict[str, Model] = {
    "claude-opus-4.8":  Model("anthropic/claude-opus-4.8",        "Claude Opus 4.8",  "flagship"),
    "gpt-5.2":          Model("openai/gpt-5.2",                   "GPT-5.2",          "flagship"),
    "gemini-3.1-pro":   Model("google/gemini-3.1-pro-preview",    "Gemini 3.1 Pro",   "flagship"),
    "claude-haiku-4.5": Model("anthropic/claude-haiku-4.5",       "Claude Haiku 4.5", "efficient"),
    "gpt-5-mini":       Model("openai/gpt-5-mini",                "GPT-5 mini",       "efficient"),
    "gemini-2.5-flash": Model("google/gemini-2.5-flash",          "Gemini 2.5 Flash", "efficient"),
    "llama-4-maverick": Model("meta-llama/llama-4-maverick",      "Llama 4 Maverick", "open"),
    "deepseek-v3.2":    Model("deepseek/deepseek-v3.2",           "DeepSeek V3.2",    "open"),
}

# A leaner default so a first real run is cheap: one model per tier pairing.
DEFAULT_LINEUP = [
    "claude-opus-4.8",
    "gpt-5.2",
    "gemini-3.1-pro",
    "llama-4-maverick",
    "deepseek-v3.2",
]


class OpenRouterClient:
    """Minimal chat-completions client with per-call latency measurement."""

    def __init__(self, api_key: str | None = None, timeout: int = 90):
        self.api_key = api_key or os.environ.get("OPENROUTER_API_KEY")
        if not self.api_key:
            raise RuntimeError(
                "OPENROUTER_API_KEY not set. Copy .env.example to .env and add a key, "
                "or export it in your shell."
            )
        self.timeout = timeout

    def complete(self, model_id: str, prompt: str, temperature: float = 0.0) -> dict:
        """Return {text, latency_s, ok, error} for one prompt."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            # OpenRouter attribution headers (optional but polite).
            "HTTP-Referer": "https://periospot.com",
            "X-Title": "Periospot Dental LLM Benchmark",
        }
        payload = {
            "model": model_id,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
        }
        start = time.perf_counter()
        try:
            resp = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=self.timeout)
            latency = time.perf_counter() - start
            resp.raise_for_status()
            data = resp.json()
            text = data["choices"][0]["message"]["content"]
            return {"text": text, "latency_s": round(latency, 3), "ok": True, "error": None}
        except Exception as e:  # noqa: BLE001 - we want every failure captured as data
            return {
                "text": None,
                "latency_s": round(time.perf_counter() - start, 3),
                "ok": False,
                "error": str(e),
            }
