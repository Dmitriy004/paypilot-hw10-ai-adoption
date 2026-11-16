# AI Adoption Impact Report — ДЗ10: вимірювання ефекту асистента

**Дмитро Сугак · PayPilot FX · мандат Ship it.** Прогони нового повтору: 16.11.2026; підсумок: 17.11.2026. Головне: ручний baseline **10/12**, перша нова генерація **2/12**, об'єднання **10/12**. Додатково до baseline генерація не виявила жодної з цих помилок.

Це **новий повтор**, не підміна досліду 13.11. Автор написав новий baseline і провів review; автоматизація виконала ізольовану генерацію, прогони та оформлення. Автор уже бачив історичний дослід, тому це не сліпий контроль. Результати власні, не запасні. OpenAI замість Claude — явна зміна інструмента.

**Межа відповідності:** baseline спочатку перевірено на оригіналі, потім зафіксовано окремим source commit до нової генерації та порівняльних mutation runs. Raw generation зафіксовано до його першого виконання. Проте стандартні каталоги перенесено разом пізнішим commit55f6795: буквальну перевірку рубрики «commit tests/manual раніше tests/generated і manual не змінено після жодної генерації» ця історія не проходить. Не приховуємо відступ; потрібне рішення ментора про прийнятність нового повтору. Докладно — [готовність](submission-readiness.md).

## Прогноз перед роботою

Прогноз [experiments/human-repeat/forecast.md](experiments/human-repeat/forecast.md), окремий commit **16d6611e5da780c37a0501b5570be3912f72bd4c** о22:50:50 Europe/Warsaw, до нового request о22:51:14 і mutation runs. Сам прогноз після фактів не редагувався.

| Набір | Прогноз | Факт | Розбіжність |
| --- | --- | --- | --- |
| Baseline | 10/12: A-01..03, B-01..03, C-01..03, D-03 | 10/12, ті самі ID | немає |
| Generated | 3/12: B-03,C-02,C-03 | 2/12: **B-01,C-02** | B-03/C-03 не вбиті; B-01 не прогнозувався |
| Union | 10/12, як baseline | 10/12, ті самі ID | немає |

Найбільша помилка прогнозу — перенесення очікувань від історичного output на ще не отриману нову відповідь. HR-G04 реально ставить used490+amount10 рівно на ліміт500 і ловить B-01. Але при B-03 ігнорування used не змінює його безкоштовний результат: amount10 і без used нижче ліміту; інші входи теж не ізолюють перетин. C-03 переживає набір: там, де комісія ненульова, немає незалежного assertion для final_amount; у free-входах зміна знака нульової комісії непомітна. C-02 ловиться перевіркою spread_amount у HR-G05. Assertion output — [audit](reports/human-repeat/mutant-audit.json). Найслабші класи: baseline — серіалізація; generated — тарифи й форма.

## 1. Ручний baseline

| Поле | Значення |
| --- | --- |
| Каталог | tests/manual/test_fx_manual.py |
| Функції / collected cases | **8 / 15**, parametrized function рахується один раз |
| Авторство | Автор ввів код у IDE; асистент підготував порожній файл і перевірив запуск, не змінюючи реалізацію |
| Таймер | **16.11.2026,22:16:32–22:42:43 Europe/Warsaw (UTC+01)** |
| Час | **1571с =26хв11с =26.183333хв**, без перерв за підтвердженням автора |
| Межа виміру | Wall time з handoff/message latency, не active-only телеметрія |
| Джерело еталонів | Буквальні актуальні вимоги з policy.py; у тестах немає policy imports або обчислення expected через функцію під тестом |
| Freeze перед новою генерацією | **a05b3044278886b8398c7463e94396a85f62a309** о22:43:40, через57с після фінішу |
| Джерело / hash | [baseline.py](experiments/human-repeat/baseline.py), SHA256 8f1999ea58e3c515d7fd82a14ec5362dea76c307cdebfc5615155b03d437c7da |
| Promotion | 55f6795b0dcc617058d4059947d83cc25d807e20; зміст збігається зі збереженим baseline після нормалізації EOL |
| Original | **15/15 PASS**; [coverage](reports/human-repeat/coverage-manual.json) |

| ID | Функція | Правило / клас |
| --- | --- | --- |
| HR-M01 | test_tier1_allowance_exact_boundary_and_one_cent_over | EUR500 і500.01, буквальна кінцева сума; межа/арифметика |
| HR-M02 | test_allowance_used_before_is_included_in_limit_check | used400+100/100.01; поле попереднього usage; межа/форма |
| HR-M03 | test_tier_specific_spread_when_free_limit_exceeded | Три тарифи, allowance500/1000/5000, spread1.5/.9/.5%, суми; значення тіру |
| HR-M04 | test_cross_currency_conversion_uses_both_eur_rates | GBP→PLN, буквальні1.17/.23; арифметика |
| HR-M05 | test_partial_allowance_charges_only_exceeding_portion | EUR200,used400: fee1.5,final198.5; арифметика |
| HR-M06 | test_partial_allowance_after_limit_exhausted_charges_full_amount | EUR200,used500: fee3,final197; арифметика |
| HR-M07 | test_spread_override_applies_only_outside_free_allowance | override2%, free100/paid600; арифметика/контроль |
| HR-M08 | test_unknown_tier_or_currency_raises_value_error | Невідомий тариф/from/to, точний ValueError; негативна валідація |

Межі, тарифні очікування та partial allowance враховано свідомо після ознайомлення з темою. Виявлення B-01 через EUR500 не є доказом окремого входу рівноEUR1000. B-02 ловиться полем allowance_total_eur==1000 у HR-M03. Перший збережений human baseline лежить не у стандартному каталозі; недолік порядку canonical paths не маскуємо датами.

## 2. Незмінний список мутантів

Файл mutants.toml, commit **6c585940c7527c45637e95aea649734360baedcd**,13.11.2026 17:36:40+01, до обох генерацій і первинних/нових прогонів. SHA256 **04dc871bd9947a22a5dc252f0d97f070abcb960effa5f053f3a5b8a5f0a947e6**. Не змінювався. У трьох нових reports uncommitted=false, HEAD55f6795,12мутантів по3в кожному класі.

| ID | Клас | Оригінал → мутант | Місце |
| --- | --- | --- | --- |
| A-01 | значення тіру | tier2 .9→1.5 | policy.py, FX_SPREAD_PCT |
| A-02 | значення тіру | tier1 1.5→.9 | policy.py, FX_SPREAD_PCT |
| A-03 | значення тіру | tier3 .5→.9 | policy.py, FX_SPREAD_PCT |
| B-01 | межа EUR 1 000 | <=→< для всіх tier | fx.py, within |
| B-02 | межа EUR 1 000 | tier2 1000→999 | policy.py, allowance |
| B-03 | межа EUR 1 000 | used+amount→amount | fx.py, within |
| C-01 | арифметика | amount*rate→amount/rate | fx.py, gross |
| C-02 | арифметика | /100→/10 у звичайній гілці | fx.py, spread_amount |
| C-03 | арифметика | gross-spread→gross+spread | fx.py, final_amount |
| D-01 | форма результату | round6→round2 | fx.py, as_dict |
| D-02 | форма результату | вилучено final_amount | fx.py, as_dict |
| D-03 | форма результату | previous usage→0 | fx.py, результат quote |

Runner змінює тільки тимчасові копії. [Аудит](reports/human-repeat/mutant-audit.json) повторив **36/36** outcome трьох наборів: усі kills — AssertionError, не import/syntax failure. Окремі rewritten witnesses вбили **3/3 D-мутанти**, отже вцілілі D-01/02 не еквівалентні. Witnesses не входять до comparators.

## 3. Критерії рев'ю і промпт до генерації

[Критерії](prompts/review-criteria.md) і [prompt](prompts/generation-prompt.md) frozen6c58594 до нового request: незалежний числовий oracle, сила assertions, справжня заявлена межа, незалежність від часу/порядку, ім'я правила, новизна щодо baseline/раніше прийнятих функцій. Для exceptions/properties Oracle N/A. Критерії не змінені заднім числом; HR-G09 зрештою відхилено саме за вихідним Oracle.

```text
Згенеруй unit-тести для модуля app/engines/fx.py. Поклади їх у tests/generated/test_fx_generated.py.
```

Модель отримала **лише дослівний prompt і public fx.py** — без policy.py, baseline, mutants, критеріїв, README, історії, tools. Імпорт policy у output читає таблиці під час локальних тестів; це не передача таблиць у request. Для OpenAI обмеження задавав payload, не .claude/settings.json.

## 4. Генерація і покриття

| Поле | Факт |
| --- | --- |
| Модель | **OpenAI gpt-4.1-mini-2025-04-14**, temp.7,max_output8000,storefalse,service default |
| Перша спроба нового повтору | Клієнтські годинникові timestamps:16.11.2026,21:51:14.225517–21:51:29.605050UTC; **1call,0retries** |
| Request | **req_aeefce9c3bea4ffe84edd674488cf81a** |
| Час машини | **15.3283431с =0.255472385хв**, один вимір |
| Usage |795input(cached0)+1140output=1935tokens |
| USD | **$0.002142 usage estimate**, не звірено з billing |
| Формула / тариф | (795×.40+1140×1.60)/1M; standard rates USD/1M input/output, cached .10; official docs перевірено16.11 |
| Budget | Дозвіл≤$0.05, внутрішній guard≤$0.03; conservative upper estimate$0.0140412 |
| Raw | [request/response/metadata/extracted](experiments/human-repeat/generation/), commit **c161d3cb31dc3f013e16224beb6d5759f601e191** до першого запуску |
| Root envelope | reports/generation.json — упакована та сама записана відповідь; новий call не виконує |
| Initial / retained | **10functions/10cases:10PASS; retained10/10**, видалено0, код не виправлявся |

[Офіційний тариф](https://developers.openai.com/api/docs/pricing), [snapshot](https://developers.openai.com/api/docs/models/gpt-4.1-mini). Ціна тільки цього нового request; попередній дослід мав окремий call і не прихований. Billing/інфраструктура/робота асистента-координатора не виміряні та не оголошені нульовими.

**Межа часової звірки:** metadata містить клієнтський інтервал вище, а raw response created_at=1794865901 і completed_at=1794865914 відповідають21:51:41–21:51:54UTC. Годинники клієнта й провайдера не звірені; поправку не вигадуємо. Час15.3283431с виміряно монотонним клієнтським таймером, не відніманням timestamps різних систем. Прогноз передує обом записаним інтервалам; raw freeze22:52:46Warsaw пізніше обох.

| Набір | Команда | Покриття fx.py |
| --- | --- | --- |
| Baseline | pytest tests/manual --cov=app.engines.fx | **39/45=86.67%**, console87%; reports/human-repeat/coverage-manual.json |
| Generated | pytest tests/generated --cov=app.engines.fx | **45/45=100%**; reports/human-repeat/coverage-generated.json |

Python3.12.14/pytest9.2.0/pytest-cov7.1.0/coverage7.17.3 однакові. Це line coverage, не branch coverage і не доказ правильних сум; приклад64% з курсу на іншій Python не наш вимір.

## 5. Generation Review Log

Усі **10функцій**, порядок AST raw; verdicts надав автор. Остаточний журнал — [review-log.md](review-log.md); джерело уточнень — [human journal](experiments/human-repeat/review-log.md). Хвилини нижче дорівнюють секундам/60; таблицю не заповнювали рівними частками загального часу.

| ID / функція | Verdict | Критерій / причина | Action | Review хв | Rewrite хв |
| --- | --- | --- | --- | --- | --- |
| HR-G01 test_mid_rate_known_currencies | rejected | Oracle: та сама таблиця/формула | green as-is; окремий literal rewrite |23/60 |60/60 |
| HR-G02 test_mid_rate_unknown_currency_raises | rejected | Novelty: baseline уже має невідомі from/to; окремий mid_rate не новий input-клас | green as-is |9/60 |не робив |
| HR-G03 test_quote_unknown_tier_raises | rejected | Novelty: unknown tier уже є | green as-is |16/60 |не робив |
| HR-G04 test_quote_within_allowance_no_spread | rejected | Novelty: exact boundary вже є | green as-is |17/60 |не робив |
| HR-G05 test_quote_exceed_allowance_default_spread | rejected | Novelty / Oracle: paid/три спреди вже є; policy-derived expected | green as-is |12/60 |не робив |
| HR-G06 test_quote_exceed_allowance_spread_override | rejected | Novelty: override уже перевірений | green as-is |10/60 |не робив |
| HR-G07 test_quote_partial_allowance_applied | rejected | Novelty / Assertion strength; property Oracle N/A, повтор алгоритму слабший за literal baseline | green as-is; окремий rewrite |25/60 |81/60 |
| HR-G08 test_quote_as_dict_rounds_floats | accepted | Property Oracle N/A: нова обмежена rounding-властивість, не точні значення/повний словник | as-is; окреме попереднє посилення збережено |32/60 |63/60 |
| HR-G09 test_transfer_fee_known_types | rejected | Oracle: expected із policy; нове покриття4типів/5полів корисне, але не незалежний еталон | green as-is |15/60 |не робив |
| HR-G10 test_transfer_fee_unknown_type_raises | accepted | Exceptions Oracle N/A: новий unknown transfer type | as-is |10/60 |не робив |

**Accepted2/10; rejected8/10=80%.** Усі rejected green залишені в raw comparator; original-red немає. Переписано3функції/6cases, але це **2rejected (G01/G07) + посилення1accepted (G08)**. Rewritten поза manual/generated/all. HR-G08 round(v,6)==v пропускає round2/відсутній ключ: accepted лише як обмежена властивість, не повний контракт.

Початкові7accepted/3rejected збережено9b3e6a9; проміжні3/7 —24d88b3. Після авторської перевірки новизни/Oracle остаточно2/8; це корекція застосування незмінних критеріїв, не редагування output. Пізніше рішення HR-G09 окремо не хронометрували.

Review169с=2.816667хв; rewrites204с=3.4хв. Wall timer23:14:35–23:36:03Europe/Warsaw=1288с(21:28). Автор пояснив залишок915с(15:15) заповненням таблиці: це витрати процесу, не пауза; пояснення вирахуваного залишку, не незалежний секундомір. Додаткові60с уточнення повідомлені автором без timestamps. Відомий subtotal **169+204+915+60=1348с=22:28**; первинні секунди не додані повторно. [Timing JSON](experiments/human-repeat/review-timing.json).

## 6. Результат за класами мутантів

Незмінний runner, frozen12, code revision **55f6795b0dcc617058d4059947d83cc25d807e20**. Між трьома наборами змінювались лише pytest paths; rewritten/infrastructure/proxy не входять.

| Набір / команда | Звіт (UTC у назві) |
| --- | --- |
| python tools/run_mutants.py --set manual | [manual](reports/mutants-manual-20261116-225513Z.json) |
| python tools/run_mutants.py --set generated | [generated](reports/mutants-generated-20261116-225513Z.json) |
| python tools/run_mutants.py --set all | [union](reports/mutants-all-20261116-225513Z.json) |

| Клас | Baseline | Generated | Union |
| --- | --- | --- | --- |
| значення тіру |3/3 |0/3 |3/3 |
| межа EUR 1 000 |3/3 |1/3 |3/3 |
| арифметика |3/3 |1/3 |3/3 |
| форма результату |1/3 |0/3 |1/3 |
| **Разом / score** |**10/12=83.33%** |**2/12=16.67%** |**10/12=83.33%** |
| Line coverage |39/45=86.67% |45/45=100% |не вимірювали |

Baseline/union survivors: **D-01,D-02**. Generated survivors: **A-01,A-02,A-03,B-02,B-03,C-01,C-03,D-01,D-02,D-03**; kills **B-01,C-02**. Додатково union до baseline **0/12**; класу, де generated сильніший, **немає**.

Generated не захищає значення тарифів, форму або кінцеву суму в paid-кейсах. Baseline ловить usage-поле D-03, але не викликає as_dict і пропускає D-01/02. Повне виконання45/45рядків не завадило пропустити10/12штучних дефектів.

Список відібраний, не випадкова production-вибірка. Інтервал для production detection rate не оцінюємо; розкид інших генерацій/людей не виміряно. [Машинна сводка](reports/human-repeat/measurement-summary.json) фіксує scope, hashes, знаменники й витрати.

## 7. Ціна у двох валютах

| Ресурс | Baseline | Generated workflow | Походження |
| --- | --- | --- | --- |
| Людина: написання, хв |**1571/60=26.183333** |0 окремого ручного написання raw |baseline wall timer; не включає попереднє навчання |
| Людина: review й відбір, хв |окремої фази не було |**169/60=2.816667** |per-function авторські записи |
| Людина: переписування rejected, хв |окремої фази не було |**141/60=2.35** |G01=60с,G07=81с |
| Людина: посилення accepted, хв |окремої фази не було |**63/60=1.05** |G08; не приховане як «не робив» |
| Заповнення таблиці, хв |у baseline wall окремо не розділялось |**915/60=15.25** |пояснення залишку автором |
| Уточнення журналу, хв |— |**60/60=1** |self-report; пізніше HR-G09 окремо не заміряне |
| **Відомі хвилини людини** |**26.183333 (26:11)** |**22.466667 (22:28)** |не повний час усієї підготовки/координації |
| Машина: generation, хв |— |**0.255472385** |metadata одного request |
| Generation USD |— |**$0.002142 estimate** |usage, billing не звірено |
| Убитих /12 |**10/12** |**2/12** |rewritten не додані до generated |

Різниця відомих людських фаз — **223с=3:43**, але generated-only ловить2/12 проти10/12: це **не економія за однакової якості й не ROI**. Додавання generated до вже написаного baseline коштує ще щонайменше22:28відомих людських витрат плюс generation і дає0нових kills на цьому списку. Сума writing+known review=2919с=48:39 — витрати виконання двох гілок експерименту, не час generated-only. Старі planning40/45, self-report60/20/3 та AI-proxy228с не використовуються як нові людські виміри.

## 8. AI Adoption Impact Report — сім рядків

| Рядок | Висновок |
| --- | --- |
| 1. На чому міряли | Один snapshot app/engines/fx.py кітаd6c471a, frozen12мутацій6c58594; baseline8функцій/15cases проти першої нової OpenAI відповіді10/10, модельgpt-4.1-mini-2025-04-14 бачила лише weak prompt+fx.py. Первинний code55f6795; чистий clone і межі хронології —§10. |
| 2. Число | Baseline10/12,generated2/12,union10/12; класи§6. Відхилено8/10(80%).100%line coverage не підтверджує фінансовий контракт. |
| 3. Де не працює | Тарифи: generated0/3 протиbaseline3/3 — хибна комісія може лишитися green. Форма: baseline/union1/3,generated0/3 — точність і наявність підсумкової суми не захищені comparators. |
| 4. Ціна | Відомі людські26:11writing проти22:28review/rewrite/table/amendment, плюс15.3283431смашини й$0.002142usage. Пізніша координація/інфраструктура/обчислення координатора не виміряні; через10/12проти2/12рівноякісного прискорення немає. |
| 5. Що з цим робимо | Модель може пропонувати чернетки негативних перевірок і властивостей; людина відбирає лише нові класи, задає незалежні суми/межі та повний вихідний контракт. На цьому списку немає класу, де виграла модель, тому не передаємо їй фінансовий oracle або автоматичне приймання. |
| 6. Мандат | Ship it: беремо HR-G10 як додаткову негативну перевірку, HR-G08 лише як допоміжну властивість; фінансовий release чекає незалежного contract-захисту. Zero regulatory risk: не зараховуємо HR-G08 до release evidence й блокуємо фінансовий випуск до незалежних literal/повних контрактних перевірок та розширеного списку дефектів. Нульового ризику не обіцяємо. |
| 7. Коли переглянемо | Нова модель/snapshot; новий prompt/context із явними вимогами; зміна FX/тарифів/схеми; новий клас дефектів або контрольований людський повтор. Перед кожним порівнянням — окремий прогноз на frozen списку й усі витрати review, не підгонка цього результату. |

**CTO одним реченням:** згенеровані тести виконали весь модуль, але виявили2/12помилок і не додали нічого понадbaseline, тому тут модель — автор чернеток, не джерело фінансового еталону чи дозволу на випуск.

## 9. Залишковий ризик — L03

| Що не покрито | Що станеться | Чому живемо з цим зараз | Відкласти чи прийняти |
| --- | --- | --- | --- |
| as_dict precision і обов'язковий final_amount у comparators | Клієнт отримає втрату точності/відсутню суму при green | Frozen прилад зберігаємо для виміру; rewritten демонструють дефекти окремо | Відкласти фінансовий release до повного незалежного contract gate |
| Тарифна підміна в policy-mirror generated | Неправильна комісія стане «правильною» для тесту | Порівнюємо першу відповідь без прихованого покращення | Не використовувати generated-only як release evidence; literal вимоги задає людина |
| Zero/negative/NaN/Infinity/decimal rounding поза списком | Непридатні грошові результати не зловлені цим виміром | Вузький навчальний модуль, не повний фінансовий аудит | Відкласти загальний висновок до явних вимог/окремих кейсів |
| Інші генерації, люди та попереднє знайомство автора | Помилковий прогноз окупності в команді | Один повтор після історичного досліду; timing має описані межі | Прийняти відсутність загального ROI, запланувати контрольований повтор |
| Невиміряна пізніша координація й фактичний billing | Повна ціна вища за наведений subtotal | Не підставляємо нулі або оцінки як факти | Прийняти лише нижню межу відомих витрат; звіряти окремо за потреби |

## 10. Декларація і chain-ready

**Декларація AI:** новий baseline і первинний review/rewrites надав автор; асистент підготував порожню форму, ізольований OpenAI request, технічні прогони, перевірку застосування критеріїв і оформлення. Відхилені HR-G01..07/09; HR-G08/10 прийняті у вузькому scope. Історичний baseline/review13.11були AI-assisted і не перейменовані на людські. Нова генерація не є спробою приховано покращити стару; це окремий повтор після нового baseline, у ньому1call/0retries. Strong-prompt опційний експеримент не виконувався.

Стандартні тести перенесено тільки після авторського review й явного дозволу користувача. Raw commitc161d3c передує запуску; rootgenerated побітово за текстом/EOL збігається з raw. Старий root report/envelope доступні у **24d88b38ba767bf93e29749024faf1078ef4aebd**; reports/openai-generation/, первинні звіти13.11, LAB-STATUS.md і verification.md залишаються історичними, не доказом цього повтору.

Поточний offline full suite після promotion: **45/45PASS =manual15+generated10+rewritten6+infrastructure14**. Infrastructure/rewritten не входять у три comparators. [Узагальнений шаблон](ai-adoption-impact-report.generic.md) не містить термінів/команд кіта за regex ДЗ.

**Новий clean clone перевірено17.11.2026 на source124c8b71a7795771d7a2a05e82d07d6e446aa064.** Нова venv й установка requirements exit0; manual15PASS,generated10PASS,full45PASS; generation_summary raw10/retained10,$0.002142estimate; union10/12,D-01/D-02survive,uncommitted=false. Усі команди exit0; [chain-ready.md](chain-ready.md) містить точний check-dir, версії й hash. Перевірочний mutant report лишився лише у clone, не закомічений до source. Публічний пакет: [Dmitriy004/paypilot-hw10-ai-adoption](https://github.com/Dmitriy004/paypilot-hw10-ai-adoption), main; користувач доручив відправку з розкритим відступом. Це не погодження ментора або твердження про прийняття ДЗ. Точна хронологія стандартних paths і незалежність від попереднього досліду залишаються обмеженням протоколу.
