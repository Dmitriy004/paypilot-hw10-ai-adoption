# Прогноз нового повтору — ДО генерації та mutation runs

Зафіксований авторський baseline: `a05b3044278886b8398c7463e94396a85f62a309`,8functions/15cases, SHA256 `8f1999ea58e3c515d7fd82a14ec5362dea76c307cdebfc5615155b03d437c7da`. Підготовлено асистентом за читанням коду, не результатами нового mutation run. Список12мутантів frozen6c58594, SHA256 `04dc871bd9947a22a5dc252f0d97f070abcb960effa5f053f3a5b8a5f0a947e6`. Список і baseline не змінюємо після прогнозу для кращого результату.

| Набір | Прогноз kills | Конкретні IDs | Очікувані survivors |
| --- | --- | --- | --- |
| Новий author baseline | 10/12 | A-01,A-02,A-03,B-01,B-02,B-03,C-01,C-02,C-03,D-03 | D-01,D-02 |
| Нова перша OpenAI генерація | 3/12 | B-03,C-02,C-03 | A-01,A-02,A-03,B-01,B-02,C-01,D-01,D-02,D-03 |
| Union нового повтору | 10/12 | A-01,A-02,A-03,B-01,B-02,B-03,C-01,C-02,C-03,D-03 | D-01,D-02 |

Baseline: tier-specific буквальні спреди/ліміти повинні вбити A іB-02; exact500 case — B-01; used400+amount100.01 — B-03; буквальний cross-rate — C-01, конкретні spread/final — C-02/03. Поле allowance_used_before_eur==400 має вбитиD-03. Жоден тест не викликає as_dict, томуD-01/02 очікуються живими. B-01 мутує<= для всіх tier: виявлення через500 не є доказом окремого кейса рівноEUR1000.

Generated forecast — обережне припущення з historical first call, не прочитаний новий output і не обіцянка збігу: модель може згенерувати інші тести. Очікую повторення production tables та слабкі серіалізаційні properties; найслабші класи generated — значення тіру/форма. Найслабший baseline — as_dict. Після запуску розбіжності пояснюємо, прогноз не редагуємо.

Параметри: gpt-4.1-mini-2025-04-14,temp.7,max_output8000,storefalse/default; weak prompt+fx.py без policy/baseline/мутантів/критеріїв/історії. Один новий request,0авторетраїв, дозвіл користувача≤$0.05, внутрішній upper guard≤$0.03. Official model і standard pricing перевірено16.11.2026: https://developers.openai.com/api/docs/models/gpt-4.1-mini та https://developers.openai.com/api/docs/pricing . Перед першим request цей прогноз комітиться окремо.

Historical experiment13.11 лишається historical; новий baseline не підставляється під старі reports чи старі передбачення. Новий human review ще попереду, його час/рішення не припускаємо.
