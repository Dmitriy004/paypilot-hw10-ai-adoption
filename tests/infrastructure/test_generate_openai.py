"""Offline adapter contracts; never contact a provider or enter FX scores."""
import json

import pytest

from tools.generate_openai import build_payload, estimate_cost, extract_code, reserve_output


def response(text, status="completed"):
    return {"status": status, "output": [{"type": "message", "role": "assistant",
            "content": [{"type": "output_text", "text": text}]}]}


def test_payload_excludes_unapproved_files_and_tools(tmp_path):
    (tmp_path / "prompts").mkdir()
    (tmp_path / "app/engines").mkdir(parents=True)
    (tmp_path / "prompts/generation-prompt.md").write_text("WEAK\n", encoding="utf-8")
    (tmp_path / "app/engines/fx.py").write_text("FX_SOURCE\n", encoding="utf-8")
    (tmp_path / "app/engines/policy.py").write_text("SECRET_POLICY", encoding="utf-8")
    payload = build_payload(tmp_path)
    assert payload == {"model": "gpt-4.1-mini-2025-04-14", "store": False,
                       "service_tier": "default", "temperature": 0.7,
                       "max_output_tokens": 8000,
                       "input": "WEAK\n\n--- app/engines/fx.py ---\nFX_SOURCE\n"}
    assert "SECRET_POLICY" not in json.dumps(payload)


def test_extracts_single_python_block_without_editing_code():
    code = "def test_example():\n    assert 1 == 1\n"
    assert extract_code(response("Explanation\n```python\n" + code + "```")) == code


def test_accepts_plain_python():
    code = "def test_example():\n    assert 2 == 2\n"
    assert extract_code(response(code)) == code


@pytest.mark.parametrize("data", [response("```python\ndef test_a(): pass\n```", "incomplete"),
                                  response("```python\ndef test_a(): pass\n```\n```python\ndef test_b(): pass\n```"),
                                  response("Not Python"), response("x = 1")])
def test_refuses_incomplete_ambiguous_or_non_test_output(data):
    with pytest.raises(ValueError):
        extract_code(data)


def test_cost_separates_cached_input_from_standard_input():
    assert estimate_cost({"input_tokens": 1000, "output_tokens": 500,
                          "input_tokens_details": {"cached_tokens": 200}}) == pytest.approx(0.00114)


def test_existing_output_prevents_second_generation(tmp_path):
    out = tmp_path / "generation"
    reserve_output(out)
    (out / "sentinel").write_text("preserve", encoding="utf-8")
    with pytest.raises(FileExistsError):
        reserve_output(out)
    assert (out / "sentinel").read_text(encoding="utf-8") == "preserve"
