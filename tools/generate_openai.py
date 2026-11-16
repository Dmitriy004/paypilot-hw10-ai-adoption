"""One isolated Responses API call. No tools, history, retries, or FX execution.

Offline tests need no key. This command is paid: do not rerun for a nicer result.
Output directory is reserved exclusively before any request is sent.
"""
from __future__ import annotations

import argparse
import ast
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time
import urllib.error
import urllib.request

MODEL = "gpt-4.1-mini-2025-04-14"
ROOT = Path(__file__).resolve().parent.parent
PRICING_URL = "https://developers.openai.com/api/docs/pricing"


def build_payload(root: Path) -> dict:
    prompt = (root / "prompts/generation-prompt.md").read_text(encoding="utf-8").rstrip("\n")
    source = (root / "app/engines/fx.py").read_text(encoding="utf-8")
    return {"model": MODEL, "store": False, "service_tier": "default",
            "temperature": 0.7, "max_output_tokens": 8000,
            "input": prompt + "\n\n--- app/engines/fx.py ---\n" + source}


def extract_code(response: dict) -> str:
    if response.get("status") != "completed":
        raise ValueError("Response is not completed")
    text = "\n".join(c["text"] for item in response.get("output", [])
                     if item.get("type") == "message"
                     for c in item.get("content", []) if c.get("type") == "output_text")
    if "```" in text:
        blocks = re.findall(r"```(?:python|py)?\s*\n(.*?)```", text, re.DOTALL)
        if len(blocks) != 1 or text.count("```") != 2:
            raise ValueError("Ambiguous code blocks; preserve raw response for review")
        code = blocks[0]
    else:
        code = text
    try:
        tree = ast.parse(code)
    except SyntaxError as exc:
        raise ValueError("Output is not Python") from exc
    if not any(isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
               and n.name.startswith("test_") for n in ast.walk(tree)):
        raise ValueError("No test functions in output")
    return code


def estimate_cost(usage: dict) -> float:
    """Standard USD estimate, not provider billing reconciliation."""
    cached = usage.get("input_tokens_details", {}).get("cached_tokens", 0)
    return ((usage["input_tokens"] - cached) * 0.40 + cached * 0.10
            + usage["output_tokens"] * 1.60) / 1_000_000


def reserve_output(path: Path) -> None:
    path.mkdir(exist_ok=False)


def load_key(env_file: Path | None) -> str:
    key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not key and env_file:
        for line in env_file.read_text(encoding="utf-8-sig").splitlines():
            name, sep, value = line.strip().partition("=")
            if sep and name == "OPENAI_API_KEY":
                key = value.strip().strip("\"'")
                break
    if not key:
        raise ValueError("OPENAI_API_KEY is missing; do not print or commit it")
    return key


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise urllib.error.HTTPError(req.full_url, code, "Redirect refused", headers, fp)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--key-env-file", type=Path, help="Existing task config; key read only in memory")
    ap.add_argument("--output-dir", type=Path, default=ROOT / "reports/openai-generation",
                    help="New exclusive artifact directory; existing directories are refused")
    args = ap.parse_args()
    payload = build_payload(ROOT)
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    upper_usd = (len(payload["input"].encode("utf-8")) * 0.40 + 8000 * 1.60) / 1_000_000
    if upper_usd > 0.03:
        raise ValueError("Conservative input-byte/output-token budget exceeds $0.03")
    key = load_key(args.key_env_file)
    out = args.output_dir
    reserve_output(out)
    (out / "request.json").write_bytes(body)
    metadata = {"started_at": dt.datetime.now(dt.timezone.utc).isoformat(),
                "model_requested": MODEL, "attempts": 1, "automatic_retries": 0,
                "payload_sha256": sha(body), "budget_upper_estimate_usd": upper_usd,
                "source_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
                "sources": {p: sha((ROOT / p).read_bytes()) for p in (
                    "prompts/generation-prompt.md", "app/engines/fx.py")},
                "pricing_url": PRICING_URL, "rates_usd_per_million": {"input": 0.4, "cached_input": 0.1, "output": 1.6},
                "billing_reconciled": False}
    started = time.perf_counter()
    try:
        req = urllib.request.Request("https://api.openai.com/v1/responses", data=body,
                                     headers={"Authorization": "Bearer " + key,
                                              "Content-Type": "application/json"}, method="POST")
        opener = urllib.request.build_opener(NoRedirect())
        with opener.open(req, timeout=90) as result:
            raw = result.read()
            metadata.update(http_status=result.status, request_id=result.headers.get("x-request-id"))
        (out / "response.json").write_bytes(raw)
        response = json.loads(raw)
        metadata.update(response_sha256=sha(raw), response_id=response.get("id"),
                        model_returned=response.get("model"), usage=response.get("usage"),
                        response_status=response.get("status"), service_tier=response.get("service_tier"))
        if response.get("usage"):
            metadata["usage_cost_estimate_usd"] = estimate_cost(response["usage"])
        code = extract_code(response)
        (out / "extracted.py").write_bytes(code.encode("utf-8"))
        metadata.update(code_sha256=sha(code.encode("utf-8")), outcome="completed")
    except urllib.error.HTTPError as exc:
        # Error bodies may echo authentication material; do not persist them.
        metadata.update(outcome="http_error", http_status=exc.code,
                        request_id=exc.headers.get("x-request-id") if exc.headers else None)
    except Exception as exc:
        metadata.update(outcome="failed", error_type=type(exc).__name__)
    finally:
        metadata.update(elapsed_seconds=time.perf_counter() - started,
                        finished_at=dt.datetime.now(dt.timezone.utc).isoformat())
        write_json(out / "metadata.json", metadata)
    print(json.dumps({k: metadata.get(k) for k in ("outcome", "http_status", "model_returned",
                      "elapsed_seconds", "usage_cost_estimate_usd")}, ensure_ascii=False))
    return 0 if metadata.get("outcome") == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
