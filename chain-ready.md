# Новий повтор: clean-clone перевірка ще виконується

Source55f6795:manual15/generated10/rewritten6/infrastructure14=45PASS. Нижче **історичний** proof source11422fc; він не є новим перевірочним прогоном. Новий доказ буде додано після фактичного запуску; його mutation report не переноситиметься у source repository.

---

# Відтворення ДЗ10 на чистому локальному clone

Перевірено 16.11.2026 на source commit **`11422fc87cf36d1ed87460ae0ac65769fb173051`**. Це новий доказ для ДЗ10; історичний `reports/clean-clone.json` залишається доказом попередньої L11. Подальший документальний commit із цією довідкою не є повторним запуском коду.

Окремий clone створено командою `git clone --no-hardlinks C:/Users/Admin/PycharmProjects/paypilot-hw10-ai-adoption <check-dir>`, його HEAD збігся з source. Initial `git status --porcelain` порожній. Створено нову venv; `pip install -r requirements.txt` завершився exit0. Інтерпретатор і pinned тестові залежності відповідають джерелу.

| Команда у новому clone | Факт | Exit |
| --- | --- | --- |
| .venv/Scripts/python.exe -m pytest tests/manual -q | 9 passed in 0.07s | 0 |
| .venv/Scripts/python.exe -m pytest tests/generated -q | 12 passed in 0.04s | 0 |
| .venv/Scripts/python.exe -m pytest -q | 37 passed in 0.59s | 0 |
| .venv/Scripts/python.exe tools/generation_summary.py reports/generation.json | OpenAI snapshot,18.298917с,$0.00257080,raw11/retained10,billingFalse | 0 |
| .venv/Scripts/python.exe tools/run_mutants.py --set all | original green;9/12kills=75%;D-01,D-02,D-03survive | 0 |

Класи union:3/3,3/3,3/3,0/3. Frozen список має той самий commit6c58594; app/manual/generated/prompts/mutants не змінено порівняно з b8694f1. Rewritten, infrastructure та AI-proxy не входять до union.

Локальний check-dir: `C:/Users/Admin/AppData/Local/Temp/paypilot-hw10-check-0700cb267252456fadaa053c11bbacc5`. Новий raw report `reports/mutants-all-20261116-205119Z.json` лишається **лише у перевірочному clone**, не переноситься й не комітиться до здачі. SHA256 `66e17e7eedfec124d6281b972348c9074a4a27c3dbf7132bbd66627eab77cead`; mutants_git.uncommitted=false, head11422fc. Python3.12.14/pytest9.2.0/pytest-cov7.1.0/coverage7.17.3. У source repository первинні звіти не перезаписані. Clone/logs — локальний доказ, не публічний CI.

Ця перевірка доводить runnable package, не human-only авторство, start/end таймера, per-function minutes або повний людський total. Ці критерії окремо у [submission-readiness.md](submission-readiness.md). Нових API-викликів або звірки billing не було.
