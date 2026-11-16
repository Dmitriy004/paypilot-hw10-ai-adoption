# Новий авторський повтор ДЗ10

Статус17.11.2026: baseline,перша нова відповідь,авторське review й3paired mutation runs виконані. Canonical suites переключено з явного дозволу користувача в **55f6795b0dcc617058d4059947d83cc25d807e20**, без зміни змісту збережених наборів після EOL; історія й старі raw/reports лишилися. Нових paidcalls немає.

| Джерело | Факт |
| --- | --- |
| [baseline.py](baseline.py),[timing.json](timing.json) | Sourcea05b3044278886b8398c7463e94396a85f62a309;8functions/15cases;16.11,22:16:32–22:42:43Warsaw=1571с(26:11),безперервзаавтором;freezeчерез57с |
| [forecast.md](forecast.md) | Окремий16d6611e5da780c37a0501b5570be3912f72bd4cдоcall/runs:10/12,3/12,10/12;конкретніIDs,післярезультатівнезмінений |
| [generation/](generation/) | Rawc161d3cb31dc3f013e16224beb6d5759f601e191дозапуску;gpt-4.1-mini-2025-04-14,temp.7,max_output8000,storefalse/default;лишеweakprompt+fx.py;10functions/10PASS,0видалено/виправлено |
| API | req_aeefce9c3bea4ffe84edd674488cf81a;15.3283431с;795input(cached0)+1140output=1935tokens;$0.002142usage estimate,billingнезвірено;1attempt/0retries,дозвіл≤$0.05 |
| [review-log.md](review-log.md),[review-timing.json](review-timing.json) | Остаточноaccepted2/10(HR-G08/10),rejected8/10(80%).HR-G09відхиленозаfrozenOracle;кориснеcoverageзазначеноокремо.Первинні7/3збережено9b3e6a9,проміжні3/7—24d88b3 |
| Відомий human subtotal |169сreview+204сrewrites+915сtable+60самоповідомленихсamendment=1348с(22:28).915с—поясненняавторомзалишкуwall1288с,неокремийтаймер;пізнішеHR-G09нехронометрували |
| [rewritten.py](rewritten.py) |3functions/6cases:2rejectedrewritesHR-G01/07іпосиленняacceptedHR-G08;фактичні63снаG08збережено;позаcomparators |
| Нові scores |[manual](../../reports/mutants-manual-20261116-225513Z.json)10/12;[generated](../../reports/mutants-generated-20261116-225513Z.json)2/12;[all](../../reports/mutants-all-20261116-225513Z.json)10/12.GeneratedkillsB-01/C-02;marginal0/12 |
| Coverage/audit |[reports/human-repeat/](../../reports/human-repeat/):manual39/45,generated45/45;36/36outcomesmatched,усіkillsAssertionError;окремі3/3rewrittenD-witnesses |

ForecastgeneratedочікувавB-03/C-02/C-03,фактB-01/C-02.Розбірвходів/assertions,часу,рішеньіризиків—[ImpactReport](../../ai-adoption-impact-report.md).

## Відтворення й межі

~~~powershell
.venv/Scripts/python.exe -m pytest tests/manual tests/generated tests/rewritten -q -p no:cacheprovider
.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider
.venv/Scripts/python.exe tools/run_mutants.py --set all
.venv/Scripts/python.exe tools/generation_summary.py reports/generation.json
~~~

Після promotion comparator+rewritten31PASS; full45PASS (14infrastructure окремо). Новий чистий clone source124c8b7 перевірено:manual15/generated10/full45PASS,union10/12; [доказ](../../chain-ready.md). Історичні proofs не переносяться на цей код. [Готовність](../../submission-readiness.md) фіксує прогалину стандартної path-хронології й попереднє знайомство автора з historical дослідом. Без рішення ментора повну відповідність не заявляємо.

Hashes:baseline8f1999ea58e3c515d7fd82a14ec5362dea76c307cdebfc5615155b03d437c7da;raw72f79054746be5461d69ab11c82f32bc6f4e7a5fa96dac3d859ca5384bd3c0c7;responsef2bca56eead595a10c23cafca379ab984897c5d06da74c5eeaf25a5deafff17a.Canonicalhashes—[measurement-summary.json](../../reports/human-repeat/measurement-summary.json).
