#!/usr/bin/env python3
"""Reliable diagnostics for OpenAI-compatible LLM proxy endpoints."""
from __future__ import annotations
import argparse, json, os, sys, time, urllib.error, urllib.request
from dataclasses import dataclass
from typing import Any, Optional
from urllib.parse import urlsplit

VERSION = "2.0.0"
USER_AGENT = f"llm-proxy-doctor/{VERSION}"

@dataclass
class Result:
    name: str
    ok: bool
    detail: str
    latency_ms: Optional[float] = None

def normalize_base_url(url: str) -> str:
    value = url.strip().rstrip("/")
    parsed = urlsplit(value)
    if parsed.scheme not in ("http", "https) or not parsed.netloc:
        raise ValueError("URL must start with http:// or https:// and include a host.")
    if parsed.username or parsed.password:
        raise ValueError("Do not put credentials in the URL. Use OPENAI_API_KEY instead.")
    return value

def validate_chat_response(data: Any) -> tuple[bool, str]:
    if not isinstance(data, dict):
        return False, "Response root must be a JSON object."
    choices = data.get("choices")
    if not isinstance(choices, list) or not choices:
        return False, "Missing non-empty choices array."
    first = choices[0]
    if not isinstance(first, dict) or not isinstance(first.get("message"), dict):
        return False, "choices[0].message must be an object."
    if "content" not in first["message"]:
        return False, "choices[0].message.content is missing."
    return True, "Valid Chat Completions response."

class Doctor:
    def __init__(self, base_url: str, api_key: Optional[str], model: str,
                 timeout: float = 15.0, verify_models: bool = True) -> None:
        self.base_url, self.api_key, self.model = normalize_base_url(base_url), api_key, model
        self.timeout, self.verify_models = timeout, verify_models
        self.results: list[Result] = []

    def _request(self, path: str, payload: Optional[dict[str, Any]] = None,
                 stream: bool = False) -> tuple[int, bytes, float]:
        headers = {"Accept": "text/event-stream" if stream else "application/json",
                   "User-Agent": USER_AGENT}
        if payload is not None:
            headers["Content-Type"] = "application/json"
        if self.api_key:
            headers["Authorization"] = "Bearer " + self.api_key
        body = json.dumps(payload).encode("utf-8") if payload is not None else None
        req = urllib.request.Request(self.base_url + "/" + path.lstrip("/"), data=body,
                                     headers=headers, method="POST" if body else "GET")
        started = time.perf_counter()
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                raw = response.read(1024 * 1024 + 1)
                elapsed = (time.perf_counter() - started) * 1000
                if len(raw) > 1024 * 1024:
                    raise ValueError("Response exceeded the 1 MiB safety limit.")
                return response.status, raw, elapsed
        except urllib.error.HTTPError as exc:
            detail = exc.read(4096).decode("utf-8", errors="replace")
            raise RuntimeError(f"HTTP {exc.code} {exc.reason}: {detail[:1000]}") from None
        except urllib.error.URLError as exc:
            raise RuntimeError(f"Connection failed: {exc.reason}") from None
        except TimeoutError:
            raise RuntimeError(f"Request timed out after {self.timeout:g}s.") from None

    def check_models(self) -> None:
        try:
            status, raw, latency = self._request("models")
            data = json.loads(raw.decode("utf-8"))
            if not isinstance(data, dict) or not isinstance(data.get("data"), list):
                raise ValueError("Expected a JSON object containing a data array.")
            ids = [x.get("id") for x in data["data"] if isinstance(x, dict)]
            note = f"HTTP {status}; {len(ids)} model(s) returned."
            if ids and self.model not in ids:
                note += " Target model not listed; aliases may still work."
            self.results.append(Result("GET /models", True, note, latency))
        except Exception as exc:
            self.results.append(Result("GET /models", False, str(exc)))

    def check_chat(self, stream: bool = False) -> None:
        payload = {"model": self.model, "messages": [{"role": "user", "content": "Reply with exactly: OK"}],
                   "max_tokens": 8, "stream": stream}
        try:
            status, raw, latency = self._request("chat/completions", payload, stream)
            if stream:
                text = raw.decode("utf-8", errors="replace")
                if "data:" not in text or "[DONE]" not in text:
                    raise ValueError("Expected SSE data events and terminal [DONE] marker.")
                self.results.append(Result("POST /chat/completions (stream)", True,
                                           f"HTTP {status}; SSE stream completed.", latency))
                return
            data = json.loads(raw.decode("utf-8"))
            valid, detail = validate_chat_response(data)
            if not valid:
                raise ValueError(detail)
            preview = str(data["choices"][0]["message"]["content"]).replace("\n", " ")[:100]
            self.results.append(Result("POST /chat/completions", True,
                                       f"HTTP {status}; {detail} Output: {preview!r}", latency))
        except Exception as exc:
            self.results.append(Result("POST /chat/completions", False, str(exc)))

    def run(self, stream: bool = False) -> bool:
        print(f"LLM Proxy Doctor v{VERSION}\nEndpoint : {self.base_url}\nModel    : {self.model}\nTimeout  : {self.timeout:g}s")
        print("-" * 60)
        if self.verify_models:
            self.check_models()
        self.check_chat(stream)
        for item in self.results:
            state = "PASS" if item.ok else "FAIL"
            timing = f" ({item.latency_ms:.1f} ms)" if item.latency_ms is not None else ""
            print(f"[{state}] {item.name}{timing}\n       {item.detail}")
        passed = sum(x.ok for x in self.results)
        failed = len(self.results) - passed
        print("-" * 60 + f"\nSummary: {passed} passed, {failed} failed")
        return failed == 0

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="llm-proxy-doctor",
        description="Diagnose an OpenAI-compatible LLM API proxy.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--url", default="http://localhost:8000/v1", help="API base URL")
    parser.add_argument("--model", default="gpt-4o-mini", help="Model identifier to test")
    parser.add_argument("--timeout", type=float, default=15.0, help="Timeout per request in seconds")
    parser.add_argument("--stream", action="store_true", help="Also verify SSE streaming")
    parser.add_argument("--skip-models", action="store_true", help="Skip GET /models discovery")
    return parser

def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.timeout <= 0:
        parser.error("--timeout must be greater than zero")
    try:
        base_url = normalize_base_url(args.url)
    except ValueError as exc:
        parser.error(str(exc))
    key = os.environ.get("OPENAI_API_KEY") or os.environ.get("API_KEY")
    if not key:
        print("Note: no API key found. Set OPENAI_API_KEY if your proxy requires authentication.")
    app = Doctor(base_url, key, args.model, args.timeout, not args.skip_models)
    return 0 if app.run(args.stream) else 1

if __name__ == "__main__":
    sys.exit(main())
