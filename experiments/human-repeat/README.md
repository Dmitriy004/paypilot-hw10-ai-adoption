# Новий авторський повтор ДЗ10 — поточний етап

Статус: baseline, перша нова генерація та **уточнене авторське review зафіксовані**; mutation scores та повний підсумок ще не виміряні. Це новий повтор після historical досліду, не перезапис його результатів. Root tests/manual/generated/all і старий Impact Report поки описують historical порівняння; не видаємо їх за результати цього нового baseline.

| Артефакт | Факт / immutable джерело |
| --- | --- |
| [baseline.py](baseline.py) | Авторські8functions/15cases,15PASS; commit `a05b3044278886b8398c7463e94396a85f62a309`,SHA256 `8f1999ea58e3c515d7fd82a14ec5362dea76c307cdebfc5615155b03d437c7da` |
| [timing.json](timing.json) |16.11.2026,22:16:32–22:42:43 Europe/Warsaw,1571с=26хв11с; автор підтвердив відсутність перерв. Wall time включає handoff/message latency, не active-only телеметрія. Freeze commit22:43:40 — через57с після фінішу |
| [forecast.md](forecast.md) | Окремий `16d6611e5da780c37a0501b5570be3912f72bd4c` о22:50:50 до request21:51:14UTC; прогноз конкретних IDs10/12baseline,3/12generated,10/12union, не фактичні scores |
| [generation/](generation/) | Перша відповідь нового request у `c161d3cb31dc3f013e16224beb6d5759f601e191`22:52:46, до запуску extracted.py.10functions/10cases,10passed in0.05s; код не правився |
| Модель / payload | gpt-4.1-mini-2025-04-14,temp.7,max_output8000,storefalse/default; лише weak prompt і public fx.py, без policy/baseline/mutants/критеріїв/історії. Request payload SHA `fbad640f1cbb9db373d12cc00f3993b54c8681e03a0ca90ff274f8a169eb3771` збігається з historical входом, але response новий |
| Час / usage / cost |15.3283431с;795input(cached0)+1140output=1935;(.40×795+1.60×1140)/1M=$0.002142usage estimate, billing не звірено. One attempt/0retries,дозвіл≤$0.05,conservative upper bound$0.0140412 |
| Request / raw hashes | req_aeefce9c3bea4ffe84edd674488cf81a; responseSHA `f2bca56eead595a10c23cafca379ab984897c5d06da74c5eeaf25a5deafff17a`; extractedSHA `72f79054746be5461d69ab11c82f32bc6f4e7a5fa96dac3d859ca5384bd3c0c7` |
| [review-log.md](review-log.md), [review-timing.json](review-timing.json) | Остання авторська класифікація:3/10accepted (HR-G08/09/10),7/10rejected (70%). Wall1288с включає169сreview+204сrewrite+915сзаповнення таблиці; останній компонент — пояснення залишку автором, не окремий таймер. Додаткові60с уточнення — self-report; разом1348с=22:28. Початковий snapshot9b3e6a9 збережено |
| [rewritten.py](rewritten.py) | 3функції/6cases: HR-G01/07 rejected rewrites, HR-G08 — раніше виконане посилення тепер accepted тесту; витрати63с на нього не видалені |

Тарифи й підтримку snapshot перевірено16.11 за [official pricing](https://developers.openai.com/api/docs/pricing) та [model docs](https://developers.openai.com/api/docs/models/gpt-4.1-mini). API cost не включає час людини, координатора, інфраструктуру чи інші історичні виклики. Нових платних спроб для цього повтору більше не дозволено.

## Що залишилося

Уточнення автора внесені без зміни baseline/raw/rewrites. HR-G08 прийнято лише як обмежену властивість округлення, HR-G09 — як додаткове покриття контракту, не незалежний еталон комісії. Старі20/3хв не переносяться у цей новий етап.

Потрібні три нові mutation runs на нових наборах, coverage, report і clean-clone cascade з урахуванням точних команд ДЗ. Runner вимагає стандартні каталоги з test_*.py; попередній preflight з файлами зупинився до запуску mutant execution. Заміна canonical tests/manual/generated/rewritten заблокована auto-review як зміна frozen порівняння й потребує окремого явного дозволу; жодної заміни не виконано, обхід не застосовується. До цього не заявляємо actual нові scores, ROI або завершеність ДЗ. History експерименту до16.11 відома й не приховується.

## Offline checks

```powershell
.venv/Scripts/python.exe -m pytest experiments/human-repeat/baseline.py -q -p no:cacheprovider
.venv/Scripts/python.exe -m pytest experiments/human-repeat/generation/extracted.py -q -p no:cacheprovider
.venv/Scripts/python.exe -m pytest experiments/human-repeat/rewritten.py -q -p no:cacheprovider
.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider
```

Раніше отримано15/15,10/10,6/6 та39/39 відповідно; основний suite ще не збирає файли поза `tests/`. Чистий clone proof `chain-ready.md` стосується попередньої версії11422fc, не нових files цього повтору. .idea є локальними IDE settings і не комітиться.
