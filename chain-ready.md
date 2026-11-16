# Новий повтор: чистий clone з GitHub перевірено

## Перевірка опублікованої main

17.11.2026, завершено о00:23:12 Europe/Warsaw. Окремо виконано `git clone --branch main https://github.com/Dmitriy004/paypilot-hw10-ai-adoption.git`; HEAD **21e546fb13465b894231429b5fe6c4492b2a6b2c**, initial git status порожній. Check-dir: `C:/Users/Admin/AppData/Local/Temp/paypilot-hw10-repeat-check-ou6tq61q/kit`.

Нова venv та `pip install -r requirements.txt` — exit0. `pytest tests/manual`:15passed in0.12s; `pytest tests/generated`:10passed in0.07s; full45passed in0.87s. Summary:raw10/retained10,15.328343с,$0.00214200usage estimate,billingFalse. `python tools/run_mutants.py --set all`:10/12,класи3/3,3/3,3/3,1/3,survivorsD-01/D-02,uncommitted=false,head21e546f. Усі команди exit0; tracked status після них порожній, нових APIcalls0. Версії Python3.12.14/pytest9.2.0/pytest-cov7.1.0/coverage7.17.3.

Checkreport `reports/mutants-all-20261116-232259Z.json` лишився тільки у цьому clone; SHA256 **cdf0f26ebfc7df6d760790a8aa9b49bc14ccc167e5073a0c6f2160071ecdf0e0**. Повний локальний proof: `C:/Users/Admin/AppData/Local/Temp/paypilot-hw10-repeat-check-ou6tq61q/proof.json`; його не переносимо до репозиторію. Наступні зміни лише документують публікацію/відправку, не міняють набори або runner.

## Попередня перевірка локального source

17.11.2026, завершено о00:08:37 Europe/Warsaw. Source commit **124c8b71a7795771d7a2a05e82d07d6e446aa064**; після цього змінювались лише документи. Новий clone: `C:/Users/Admin/AppData/Local/Temp/paypilot-hw10-repeat-check-pb__cuwx/kit`. Створено через git clone --no-hardlinks --branch codex/hw10-ai-adoption; HEAD збігся з source, initial git status порожній. Створено окрему venv, встановлено requirements.txt.

| Команда у новому clone | Факт | Exit |
| --- | --- | --- |
| python -m venv .venv | Нова venv |0 |
| .venv/Scripts/python.exe -m pip install -r requirements.txt | Pinned залежності встановлені |0 |
| .venv/Scripts/python.exe -m pytest tests/manual |15passed in0.11s |0 |
| .venv/Scripts/python.exe -m pytest tests/generated |10passed in0.06s |0 |
| .venv/Scripts/python.exe -m pytest -q |45passed in0.72s |0 |
| .venv/Scripts/python.exe tools/generation_summary.py reports/generation.json |15.328343с,$0.00214200estimate,raw10/retained10,billingFalse |0 |
| .venv/Scripts/python.exe tools/run_mutants.py --set all |originalgreen,10/12kills;D-01,D-02survive |0 |

Union класи:3/3,3/3,3/3,1/3; список6c58594,uncommitted=false,head124c8b7. Full suite45=manual15+generated10+rewritten6+infrastructure14. Rewritten/infrastructure/proxy не входять до union. Python3.12.14/pytest9.2.0/pytest-cov7.1.0/coverage7.17.3. Tracked git status після команд порожній. Ключі/стенд не потрібні, paid calls0.

Перевірочний `reports/mutants-all-20261116-230825Z.json` лишився **тільки у check clone**, як вимагає курс; його SHA256 **a87ed2a5b965dc05d3024c2ba3e8a450ac7ffd6dd6bf4399d7165bb2b5e4d6b3**. Повний локальний журнал команд: `C:/Users/Admin/AppData/Local/Temp/paypilot-hw10-repeat-check-pb__cuwx/proof.json`; він не скопійований і не закомічений до здачі. Це локальний proof, не public CI або доказ відповідності всім умовам протоколу; [відкрита прогалина хронології](submission-readiness.md).

## Історична перевірка попереднього source

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
