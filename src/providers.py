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
    "claude-fable-5":   Model("anthropic/claude-fable-5",         "Claude Fable 5",   "flagship"),
    "claude-opus-4.8":  Model("anthropic/claude-opus-4.8",        "Claude Opus 4.8",  "flagship"),
    "gpt-5.2":          Model("openai/gpt-5.2",                   "GPT-5.2",          "flagship"),
    "gemini-3.1-pro":   Model("google/gemini-3.1-pro-preview",    "Gemini 3.1 Pro",   "flagship"),
    "qwen3.7-plus":     Model("qwen/qwen3.7-plus",                "Qwen3.7 Plus",     "efficient"),
    "claude-haiku-4.5": Model("anthropic/claude-haiku-4.5",       "Claude Haiku 4.5", "efficient"),
    "gpt-5-mini":       Model("openai/gpt-5-mini",                "GPT-5 mini",       "efficient"),
    "gemini-2.5-flash": Model("google/gemini-2.5-flash",          "Gemini 2.5 Flash", "efficient"),
    "llama-4-maverick": Model("meta-llama/llama-4-maverick",      "Llama 4 Maverick", "open"),
    "deepseek-v3.2":    Model("deepseek/deepseek-v3.2",           "DeepSeek V3.2",    "open"),
}

# A leaner default so a first real run is cheap: one model per tier pairing.
DEFAULT_LINEUP = [
    "claude-fable-5",
    "claude-opus-4.8",
    "gpt-5.2",
    "gemini-3.1-pro",
    "qwen3.7-plus",
    "llama-4-maverick",
    "deepseek-v3.2",
]

# Native Anthropic backend (Claude family only — uses ANTHROPIC_API_KEY directly,
# no OpenRouter). IDs are the bare first-party strings. Use this to run a Claude
# pilot with an Anthropic key; switch to the OpenRouter roster above for the full
# cross-provider comparison.
CLAUDE_ROSTER: dict[str, Model] = {
    "opus-4.8":   Model("claude-opus-4-8",   "Claude Opus 4.8",  "flagship"),
    "sonnet-4.6": Model("claude-sonnet-4-6", "Claude Sonnet 4.6", "efficient"),
    "haiku-4.5":  Model("claude-haiku-4-5",  "Claude Haiku 4.5",  "efficient"),
}
CLAUDE_LINEUP = ["opus-4.8", "sonnet-4.6", "haiku-4.5"]

# Native OpenAI backend (uses OPENAI_API_KEY directly). Native IDs verified on the
# OpenAI models list 2026-06-10; GPT-5.5 is the current frontier model.
OPENAI_ROSTER: dict[str, Model] = {
    "gpt-5.5":      Model("gpt-5.5",      "GPT-5.5",      "flagship"),
    "gpt-5.4-mini": Model("gpt-5.4-mini", "GPT-5.4 mini", "efficient"),
    "gpt-5.4-nano": Model("gpt-5.4-nano", "GPT-5.4 nano", "efficient"),
}
OPENAI_LINEUP = ["gpt-5.5", "gpt-5.4-mini", "gpt-5.4-nano"]


class OpenRouterClient:
    """Minimal chat-completions client with per-call latency measurement."""

    def __init__(self, api_key: str | None = None, timeout: int = 240):
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
            "max_tokens": 12000,  # ceiling so a reasoning loop can't run away on cost
        }
        start = time.perf_counter()
        try:
            resp = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=self.timeout)
            latency = time.perf_counter() - start
            resp.raise_for_status()
            data = resp.json()
            choice = data["choices"][0]
            text = choice["message"]["content"]
            meta = {"provider": data.get("provider"), "finish_reason": choice.get("finish_reason"),
                    "native_finish_reason": choice.get("native_finish_reason")}
            if not text:
                # HTTP 200 with empty content: either an infra hiccup or — for
                # finish_reason=content_filter — a model-level refusal. Either way
                # there is no answer to judge; surface the reason so the runner can
                # label refusals instead of silently scoring "wrong".
                return {"text": None, "latency_s": round(latency, 3), "ok": False,
                        "error": f"empty content (finish_reason={choice.get('finish_reason')})", **meta}
            return {"text": text, "latency_s": round(latency, 3), "ok": True, "error": None, **meta}
        except Exception as e:  # noqa: BLE001 - we want every failure captured as data
            return {
                "text": None,
                "latency_s": round(time.perf_counter() - start, 3),
                "ok": False,
                "error": str(e),
            }


class AnthropicClient:
    """Native Anthropic Messages API client (official SDK), same .complete() shape.

    Reaches Claude models only. Note: temperature/top_p are NOT sent — current
    Claude models (Opus 4.8/4.7, Fable 5) reject sampling parameters, and thinking
    is left off by default for fast, low-variance benchmark answers.
    """

    def __init__(self, api_key: str | None = None, max_tokens: int = 1024, timeout: int = 90):
        import anthropic  # imported lazily so the OpenRouter path needs no SDK

        key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not key:
            raise RuntimeError(
                "ANTHROPIC_API_KEY not set. Add it to .env (or your shell) before "
                "running with --backend anthropic."
            )
        self.client = anthropic.Anthropic(api_key=key, timeout=timeout)
        self.max_tokens = max_tokens

    def complete(self, model_id: str, prompt: str, temperature: float | None = None) -> dict:
        """Return {text, latency_s, ok, error}. ``temperature`` is accepted for a
        uniform interface with OpenRouterClient but intentionally not forwarded."""
        start = time.perf_counter()
        try:
            msg = self.client.messages.create(
                model=model_id,
                max_tokens=self.max_tokens,
                messages=[{"role": "user", "content": prompt}],
            )
            latency = time.perf_counter() - start
            text = next((b.text for b in msg.content if b.type == "text"), "")
            return {"text": text, "latency_s": round(latency, 3), "ok": True, "error": None}
        except Exception as e:  # noqa: BLE001
            return {
                "text": None,
                "latency_s": round(time.perf_counter() - start, 3),
                "ok": False,
                "error": str(e),
            }


class OpenAIClient:
    """Native OpenAI Chat Completions client (official SDK), same .complete() shape.

    Reaches OpenAI models only. Uses ``max_completion_tokens`` (GPT-5.x replaced
    ``max_tokens``) and does NOT send ``temperature`` — GPT-5.x reasoning models
    reject non-default temperature. The token budget is generous because reasoning
    tokens count against it.
    """

    def __init__(self, api_key: str | None = None, max_tokens: int = 8000, timeout: int = 180):
        from openai import OpenAI  # imported lazily so other backends need no SDK

        key = api_key or os.environ.get("OPENAI_API_KEY")
        if not key:
            raise RuntimeError(
                "OPENAI_API_KEY not set. Add it to .env (or your shell) before "
                "running with --backend openai."
            )
        self.client = OpenAI(api_key=key, timeout=timeout)
        self.max_tokens = max_tokens

    def complete(self, model_id: str, prompt: str, temperature: float | None = None) -> dict:
        start = time.perf_counter()
        try:
            resp = self.client.chat.completions.create(
                model=model_id,
                messages=[{"role": "user", "content": prompt}],
                max_completion_tokens=self.max_tokens,
            )
            latency = time.perf_counter() - start
            text = resp.choices[0].message.content or ""
            return {"text": text, "latency_s": round(latency, 3), "ok": True, "error": None}
        except Exception as e:  # noqa: BLE001
            return {
                "text": None,
                "latency_s": round(time.perf_counter() - start, 3),
                "ok": False,
                "error": str(e),
            }
