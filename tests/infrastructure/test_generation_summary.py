"""CLI behavior, no provider calls; infrastructure tests never enter FX sets."""
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]


def run_summary(tmp_path, payload):
    path = tmp_path / "generation.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return subprocess.run([sys.executable, str(ROOT / "tools/generation_summary.py"), str(path)],
                          capture_output=True, text=True, encoding="utf-8")


def envelope():
    return {"format": "openai-responses-artifact-v1", "provider": "openai",
            "metadata": json.loads((ROOT / "reports/openai-generation/metadata.json").read_text(encoding="utf-8")),
            "raw_response": json.loads((ROOT / "reports/openai-generation/response.json").read_text(encoding="utf-8"))}


def test_openai_summary_keeps_tiny_cost_and_initial_function_count(tmp_path):
    result = run_summary(tmp_path, envelope())
    assert result.returncode == 0, result.stderr
    assert "gpt-4.1-mini-2025-04-14" in result.stdout
    assert "18.298917" in result.stdout
    assert "0.00257080" in result.stdout
    assert "Raw test functions: 11" in result.stdout
    assert "Retained test functions: 10" in result.stdout
    assert "billing reconciled: False" in result.stdout


def test_incomplete_openai_response_is_not_reported_as_success(tmp_path):
    data = envelope()
    data["raw_response"]["status"] = "incomplete"
    result = run_summary(tmp_path, data)
    assert result.returncode != 0


def test_existing_claude_summary_remains_supported(tmp_path):
    result = run_summary(tmp_path, {"modelUsage": {"example-model": {}},
                                   "duration_ms": 60000, "num_turns": 1, "total_cost_usd": 0.5})
    assert result.returncode == 0
    assert "example-model" in result.stdout
    assert "0.50" in result.stdout
