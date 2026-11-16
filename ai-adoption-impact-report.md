# AI Adoption Impact Report — ДЗ10: вимірювання ефекту асистента

**Оновлено 16.11.2026 · прогони 13.11.2026 · Дмитро Сугак · PayPilot FX · Ship it.** Результати прогонів власні, але baseline і review підготовлені з AI; це не експеримент самостійної роботи людини. Автор повідомив 60 хв writing, 20 хв review і 3 хв на одну правку; start/end і per-function minutes не надані. Це self-reported тривалості, не підтвердження human-only baseline до генерації. Відкриті критерії позначені нижче; пакет не видається за формально завершене ДЗ.

Повністю прочитані надані PDF лабораторної (18 сторінок) і ДЗ (7 сторінок), включно з рубрикою. Лабораторна історія `b8694f1b810bdfdd0ec5c51f6ae3d8a6ad4b2181` збережена без squash; старі репозиторії не змінені. [Submission readiness](submission-readiness.md) відділяє PASS, PARTIAL і BLOCKED. OpenAI замість Claude — явна зміна приладу; це не Claude-референс і не запасний артефакт ментора.

## Прогноз перед роботою

Початковий `forecast.md` закомічено `72fafac` до baseline; конкретні ID — `forecast-final-ids.md`, окремий `b305baa` до генерації/прогонів. Не переписували після результатів.

| Що | Початковий прогноз | Уточнення на фінальному списку до запуску | Факт |
| --- | --- | --- | --- |
| Baseline | 8/12 | 9/12: A-01..03,B-01..03,C-01..03 | 9/12, ці самі ID |
| OpenAI | 7/12 | B-03,C-01..03,D-01..03 | 3/12: B-03,C-02,C-03 |
| Union | — | 12/12 | 9/12 |
| Слабкий клас baseline / generated | форма / значення тіру | без зміни | форма / значення тіру та форма |

Найбільша розбіжність — переоцінка OpenAI на4мутанти: C-01 та D-01..03 не вбиті. Baseline уточнено8→9 після підготовки остаточних тестів, але до прогонів; первинний прогноз збережено. Додаткових kills поза конкретним прогнозом немає. Відсутність класу, де generated сильніший, дозволена умовами лабораторної; результат не підганяли під приклад8/8/10.

## 1. Baseline

| Поле | Значення |
| --- | --- |
| Файл / functions / collected cases | tests/manual/test_fx_manual.py;7/9 |
| Авторство | AI-assisted, не самостійний людський baseline |
| Таймер: старт / фініш | не надано / не надано; commit tolerance перевірити неможливо |
| Час writing, повідомлений автором | 60 хв у чаті; зв'язок із цим frozen baseline незалежно не підтверджений |
| Еталони | Буквальні числа з policy.py, без policy imports у тестах: спреди1.5/0.9/0.5%, лімітиEUR500/1000/5000; суми розраховані незалежно |
| Freeze | функції03c206c; уточнення лише docstring6c58594, до генерації; після генерації не змінювали |
| Original | 9/9 PASS, reports/manual-original.xml |

| ID | Функція | Правило / клас |
| --- | --- | --- |
| M-01 | test_tier_spread_above_allowance | три тіри, конкретний spread/final; значення тіру, арифметика |
| M-02 | test_tier2_exact_1000_eur_is_free | рівноEUR1000 безкоштовні; межа |
| M-03 | test_tier2_crossing_remaining_allowance_charges_whole_quote | повна сума платна при перетині залишку; межа/арифметика |
| M-04 | test_tier2_previous_usage_counts_toward_allowance | usage входить до ліміту; межа |
| M-05 | test_explicit_spread_override_above_allowance | конкретний override; арифметика |
| M-06 | test_gbp_to_usd_uses_literal_cross_rate | cross-rate і сума за буквальним курсом; арифметика |
| M-07 | test_unknown_tier_is_rejected | негативна валідація, поза списком12мутантів |

Точну межу й previous usage включено свідомо після ознайомлення з темою. Ліміт у тарифах не виводили з результату функції. Вимога human timer відсутня не через нерозбірливий PDF, а через фактичне походження цього baseline; її не можна відновити добором timestamp до коміту.

## 2. Незмінний список мутантів

`mutants.toml`, commit `6c585940c7527c45637e95aea649734360baedcd`,13.11.2026 17:36:40+01:00; перший run13.11 16:43:43UTC, пізніше freeze. У всіх3первинних звітах uncommitted=false,12мутантів/4класи по3. SHA256 `04dc871bd9947a22a5dc252f0d97f070abcb960effa5f053f3a5b8a5f0a947e6`.

| ID | Клас | Оригінал → мутант | Місце |
| --- | --- | --- | --- |
| A-01 | значення тіру | tier2 .9→1.5 | policy.py, FX_SPREAD_PCT |
| A-02 | значення тіру | tier1 1.5→.9 | policy.py, FX_SPREAD_PCT |
| A-03 | значення тіру | tier3 .5→.9 | policy.py, FX_SPREAD_PCT |
| B-01 | межа EUR 1 000 | <=→< (усі тіри) | fx.py, within |
| B-02 | межа EUR 1 000 | tier2 1000→999 | policy.py, allowance |
| B-03 | межа EUR 1 000 | used+amount→amount | fx.py, within |
| C-01 | арифметика | amount*rate→amount/rate | fx.py, gross |
| C-02 | арифметика | /100→/10 | fx.py, spread_amount (звичайна гілка) |
| C-03 | арифметика | gross-spread→gross+spread | fx.py, final_amount |
| D-01 | форма результату | round6→round2 | fx.py, as_dict |
| D-02 | форма результату | видалено final_amount | fx.py, as_dict |
| D-03 | форма результату | previous usage→0 | fx.py, результат quote |

Кожна зміна застосовується рівно один раз; сам модуль не редагується, лише тимчасові копії runner. Вцілілі D не є еквівалентними: окремі rewritten дають assertion witness для всіх3. Повний `reports/mutant-audit.json` підтверджує всі36 outcomes; kills — assertions, не import/syntax errors.

## 3. Критерії і промпт до генерації

`prompts/`, freeze6c58594 до e7c77a6: незалежний oracle; конкретність assertions; справжня заявлена межа; незалежність від часу/порядку; ім'я правила; новизна щодо baseline й accepted G. Для exceptions/properties Oracle N/A, їх оцінюють за assertion/novelty. Критерії після генерації не змінювались.

```text
Згенеруй unit-тести для модуля app/engines/fx.py. Поклади їх у tests/generated/test_fx_generated.py.
```

Payload: лише цей дослівний текст і повний публічний fx.py, без tools/history/policy/manual/mutants/критеріїв. `.claude/settings.json` не змінено, але для OpenAI він не enforcement: обмеження задає явний payload. Імпорти policy у generated читають таблиці лише під час локальних тестів, не означають наявності таблиць у контексті моделі.

## 4. Генерація і покриття

| Поле | Факт |
| --- | --- |
| Провайдер / точна модель | OpenAI / gpt-4.1-mini-2025-04-14 |
| Параметри | temp.7, max_output8000, storefalse, service default;1фактичний call,0retries |
| Request | req_21167f0032c2449d9630a473ebb44fae;13.11.2026 |
| Час машини | 18.2989167с =0.304981945хв, один вимір |
| Usage / ціна | input795 (cached0)+output1408=2203; $0.0025708 usage estimate, **billing не звірено** |
| Формула | (795×.40+1408×1.60)/1M; standard тариф перевірений13.11 в official docs |
| Вивід | reports/openai-generation/{request,response,metadata}.json та extracted.py, e7c77a6 |
| Формат ДЗ | reports/generation.json — envelope історичної OpenAI генерації, не новий call і не удаваний Claude JSON |
| Summary | python tools/generation_summary.py reports/generation.json; точна ціна не округлюється до нуля |
| Initial / retained | 11functions/13cases:12PASS+1FAIL; після видалення тількиG-06 окремим df6a596 —10functions/12PASS |

Ціна не включає підготовку baseline/review, роботу асистента-координатора, комп'ютер та інфраструктуру. Source pricing: https://developers.openai.com/api/docs/pricing . Повторної генерації заради кращого score не було.

G-06 використовував469.2USD=431.664EUR<500, тож spread0 правильний, а expected5.5 хибний. Raw і initial JUnit збережено перед видаленням; інші generated функції не виправляли.

| Набір | Команда | fx.py coverage |
| --- | --- | --- |
| Baseline | pytest tests/manual --cov=app.engines.fx | 34/45=75.56% (console76%); reports/coverage-manual.json |
| Generated | pytest tests/generated --cov=app.engines.fx | 45/45=100%; reports/coverage-generated.json |

Той самий Python3.12.14/pytest9.2.0/pytest-cov7.1.0; не порівнюємо з64% прикладу на іншій Python. Line coverage не є branch coverage або правильністю тарифів.

## 5. Generation Review Log

Журнал усіх початкових11функцій; parametrized рахується один раз. Докладні reasons — [review-log.md](review-log.md). Review/rewrite виконано з асистентом. Автор повідомив 20 хв на review і 3 хв на одну правку; немає розподілу на функції чи часу всіх трьох rewritten. [Окремий пізніший timed AI-proxy](experiments/ai-proxy/README.md) не замінює historical baseline чи людські minutes.

| ID / функція | Verdict | Criterion / reason | Action | Review + rewrite minutes |
| --- | --- | --- | --- | --- |
| G-01 mid_rate_known | rejected | Oracle: та сама policy таблиця по обидва боки | green as-is; baseline має буквальний cross-rate | невідомо + — |
| G-02 mid_rate_unknown | accepted | Oracle N/A; нові класи невідомих from/to currencies | as-is | невідомо + — |
| G-03 valid_tiers_no_spread | accepted | конкретний0/True; нові USD→EUR/метадані; не boundary і не тарифний еталон | as-is у вузькому scope; адаптивний input не є доказом ліміту/курсу | невідомо + — |
| G-04 invalid_tier | rejected | Novelty: той самий unknown-tier клас baseline | green as-is | невідомо + — |
| G-05 spread_over_allowance | rejected | Oracle policy; лише знак/порядок сум | green as-is | невідомо + — |
| G-06 spread_override | rejected | хибне expected для вхідної суми всередині free allowance; original-red | видалено окремим commit; R-01 з правильним input і free control | невідомо + невідомо |
| G-07 partial_true | rejected | Oracle N/A; діапазон не підтверджує заявлену точність часткової суми | green as-is; R-02 з конкретними .9/299.1 | невідомо + невідомо |
| G-08 partial_false | rejected | **Oracle N/A; Novelty:** та сама повна комісія baseline; amount920EUR уже>500 без usage, нову межу не ізольовано | green as-is; причина виправлена при звірці з PDF | невідомо + — |
| G-09 as_dict_rounds | rejected | Oracle N/A; round(v,6)==v пропускає round2, цикл пропускає відсутній ключ | green as-is; R-03 усі поля й6знаків | невідомо + невідомо |
| G-10 transfer_fee_valid | rejected | Oracle: той самий policy table | green as-is | невідомо + — |
| G-11 transfer_fee_invalid | accepted | Oracle N/A; новий клас unknown transfer type | as-is | невідомо + — |

Прийнято3/11, відхилено8/11=72.73%; oracle4/assertion2/novelty2. В історичному L11 було5/2/1: G-08 перенесено з oracle до novelty без зміни verdict чи числа тестів. Переписано3/8 rejected у tests/rewritten (3functions/4cases); вони не входять у три comparator sets. Зелені rejected зберігаються для виміру raw green набору, а не accepted-only набору. Повідомлені 20 хв review не ділимо штучно на 11 функцій, а 3 хв однієї правки не підставляємо для всіх трьох.

## 6. Результат за класами

Primary code revision1616a96; список6c58594 незмінний. Лише pytest paths відрізняються. `reports/mutants-manual-20261113-164343Z.json`, `mutants-generated-20261113-164401Z.json`, `mutants-all-20261113-164401Z.json`.

| Клас | Baseline | Generated | Union |
| --- | --- | --- | --- |
| значення тіру | 3/3 | 0/3 | 3/3 |
| межа EUR1 000 | 3/3 | 1/3 | 3/3 |
| арифметика | 3/3 | 2/3 | 3/3 |
| форма результату | 0/3 | 0/3 | 0/3 |
| Разом | **9/12=75%** | **3/12=25%** | **9/12=75%** |
| Line coverage | 34/45=75.56% | 45/45=100% | не вимірювали |

Survivors baseline/union: D-01,D-02,D-03. Generated: A-01,A-02,A-03,B-01,B-02,C-01,D-01,D-02,D-03. Generated kills тількиB-03,C-02,C-03. Додаткових kills union **0/12**. Класу, де generated сильніший, **немає**.

Generated слабкий у тарифах та формі; baseline — у формі. Policy-mirror очікування не ловлять тарифну підміну; точного EUR1000 тесту в generated немає. C-01 проходить слабке співвідношення final/gross; G-09 пропускає втрату точності/ключа, previous-usage поле не перевірено. Усі outcomes підтверджені assertion audit.

Це повний перелік12відібраних штучних змін, не випадкова production-вибірка, тому detection interval для production не оцінено. Одна генерація не вимірює розкид інших запусків. Навмисно не включаємо rewritten до union, щоб не підмінити прилад після перегляду результату.

## 7. Ціна у двох валютах

| Ресурс | Baseline | Generated workflow | Походження / межа |
| --- | --- | --- | --- |
| Людина: writing, хв | 60 | ручне writing не заявлено | повідомлено автором, без start/end; human-only походження baseline не підтверджено |
| Людина: review і відбір, хв | не надано | 20 | повідомлено автором агреговано, per-function невідомо |
| Людина: rewriting, хв | не надано | 3 на одну правку | час інших двох невідомий; не множимо на три як фактичний вимір |
| **Людський підсумок** | **60 writing, повний total невідомий** | **23 за review + одну правку; повний total невідомий** | незіставний повний end-to-end бюджет |
| Машина: generation, хв | не застосовується | .304981945 | вимір API-call, окремо від людини |
| Генерація, USD | не застосовується | .0025708 за usage, не billing | не включає інші витрати |
| Убитих мутантів | 9/12 | 3/12 | результати на frozen списку |

Пізніші слова автора у чаті — джерело 60/20/3; вони замінюють попередній planning scenario40/45/9, який лишається у git-історії як оцінка, не замір. Сума наданих фаз83хв не є ціною generated-only workflow, бо включає окреме написання baseline. 23хв — неповна повідомлена частина review/rewrite, не доведена економія проти60. Не обчислюємо людський ROI без однакового обсягу/якості та всіх витрат.

### Додатковий timed AI-proxy, не human control

Фази13.11: writing56с, review141с, одна правка31с; сума228с=3.8хв без interphase gaps. UTC, SHA256, код і різниця review verdicts — [experiments/ai-proxy/](experiments/ai-proxy/README.md). A має8functions/10cases, а historical baseline7/9; C одна функція/2cases проти historical rewritten3/4. Тому арифметичне83/3.8=21.84 не є встановленим прискоренням людини, не вимірює «середню людину» і не входить у головний висновок. Вартість агентних обчислень невідома.

## 8. AI Adoption Impact Report — сім рядків

| Рядок | Висновок |
| --- | --- |
| 1. На чому міряли | Один snapshot app/engines/fx.py з кіта d6c471a; frozen12мутантів6c58594; baseline7functions і generated10retained; OpenAI gpt-4.1-mini-2025-04-14 бачив тільки fx.py та weak prompt. Це AI-assisted порівняння, не human control. |
| 2. Число | 9/12 baseline,3/12 generated,9/12 union; розбивка§6.100% generated coverage не завадило пропустити9/12змін. Rejected8/11=72.73%. |
| 3. Де не працює | Значення тіру: generated0/3 проти baseline3/3 — неправильна комісія пройде mirror-тест. Форма результату: обидва0/3 — втрата суми/точності/історії не буде заблокована цими наборами. |
| 4. Ціна | Автор повідомив60хв writing,20review і3на одну правку; timestamps і повний rewrite total невідомі. Ціна всього людського workflow та ROI не встановлені. Перша й єдина генерація.304981945хв машини та$0.0025708usage; billing і решта витрат не звірені. |
| 5. Що з цим робимо | Асистент готує чернетки негативної валідації та нових входів. Людина звіряє тарифні суми/межі з вимогами й додає contract/serialization захист на кшталт R-03; вона приймає зміни. На цьому списку assistant не додав жодного kill понад baseline, тому тарифний oracle або автономне приймання йому не делегуємо. Це запропонований процес, не вже встановлений gate. |
| 6. Мандат | За Ship it допускаємо переглянуті G-02/G-03/G-11 як додаткові перевірки, але фінансовий реліз чекає незалежних буквальних тарифних/структурних assertions. За Zero regulatory risk не використовуємо адаптивний до policy G-03 як доказ дозволу на фінансовий реліз; лишаємо лише негативну валідацію, а кожну фінансову вимогу верифікуємо незалежно до прийняття. Нульовий ризик не обіцяємо. |
| 7. Коли переглянемо | Нова модель/версія або інший prompt/context (зокрема явні вимоги); зміна FX/тарифів чи його контракту; новий клас дефектів або незалежний human baseline з таймером. Для кожної такої зміни — новий forecast до запуску, той самий frozen comparator для чесного порівняння, без підгонки старого результату. |

**CTO одним реченням:** повне виконання рядків згенерованими тестами дало лише3/12виявлених змін і0додаткових до baseline, тому модель тут — автор чернеток, не джерело фінансового еталону чи автоматичного дозволу на реліз.

## 9. Залишковий ризик — L03

| Що не покрито | Що станеться | Чому живемо з цим зараз | Відкласти чи прийняти |
| --- | --- | --- | --- |
| Форма результату в3основних наборах | final_amount/precision/usage можуть зіпсуватись непомітно | Зберігаємо слабкий прилад для чесного виміру; rewritten witnesses окремо | Відкласти фінансовий release до незалежного contract gate |
| Зміни тарифів з mirror oracle | Неправильна комісія залишиться green | Прилад заморожений, baseline містить буквальні поточні вимоги | Не приймати як release evidence; вимоги переглядати незалежно |
| Zero/negative/NaN/Infinity та decimal rounding поза списком | Невірні/непридатні грошові результати | Обмежений навчальний модуль, не повний аудит арифметики | Відкласти ширший висновок до окремих вимог і кейсів |
| Реальна людська продуктивність/інші генерації | Помилкове рішення про економію | Є лише повідомлені60/20/3, без human-only baseline, start/end, решти правок і повторів | Прийняти відсутність висновку про ROI; потрібен новий протокол |

## 10. Декларація і chain-ready

**Декларація AI:** асистент допоміг із baseline, списком мутантів, ізольованим OpenAI викликом, рев'ю/rewritten, аналізом і звітом. Відхилені G-01/04/05/06/07/08/09/10; тільки original-red G-06 видалено. Raw output/history збережені; самостійного людського baseline і таймера не заявляємо. Пізніші AI-замірювання не підставляються як людські. Узагальнений шаблон — `ai-adoption-impact-report.generic.md`, regex ДЗ дає0збігів. Нових API-викликів для цього ДЗ не було; опційну повторну генерацію не виконували.

Підтверджений попередній clean clone L11: be298e3,34/34PASS,union9/12; reports/clean-clone.json — історичний proof, не перевірка нової версії ДЗ. У новій версії full suite37tests (12infrastructure поза comparator). Нову clean-clone перевірку поточної версії буде зафіксовано в `chain-ready.md`; її mutant report залишається у тимчасовому clone, не комітиться до здачі.

| Потрібна команда в чистому clone | Очікуваний результат |
| --- | --- |
| pip install -r requirements.txt | pinned pytest/pytest-cov installed |
| pytest tests/manual | 9PASS |
| pytest tests/generated | 12PASS |
| python tools/run_mutants.py --set all | original green,9/12kills, D-01..03survivors |

Публічного репозиторію/відправки на платформу ще немає. Невиконані критерії human/time не позначені завершеними; не вигадуємо timer/авторство для проходження рубрики. Для завершення потрібен належний новий протокол або погоджений ментором fallback, а не зміна старої історії.
