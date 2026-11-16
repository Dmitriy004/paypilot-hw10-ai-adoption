# Авторське рев'ю нової генерації — HR-G01..10

Стан: **не розпочато**. Не використовувати verdicts історичної генерації чи AI-proxy: новий output і новий baseline відрізняються.

Генерація: `c161d3cb31dc3f013e16224beb6d5759f601e191`, [незмінний raw код](generation/extracted.py),10functions/10cases, original10PASS. Порівняння новизни — з [твоїм baseline](baseline.py),8functions/15cases, і раніше прийнятими HR-G у порядку нижче. Критерії зафіксовано до генерації у [prompts/review-criteria.md](../../prompts/review-criteria.md).

## Як вести журнал

1. Після відкриття raw коду й цього файла напиши в чаті **«починаю рев'ю»** / **«начинаю ревью»** — зафіксуємо загальний старт. До цього таймер не запускається.
2. Для кожної функції окремо засікай секундоміром review, запиши фактичні **секунди** у відповідну колонку. Вони потім переводяться у хвилини діленням на60; не ділимо загальний час порівну.
3. Обери accepted/rejected, назви criterion, поясни причину своїми словами, напиши action: as-is / remove original-red / окремий rewrite. Для exceptions/properties Oracle N/A; boundary застосовується лише коли функція заявляє межу. Сам факт green не є verdict.
4. Не змінюй baseline або raw generated файл. Якщо вирішиш переписати функцію, спершу збережи її verdict і окремо засічи rewrite; новий код поклади у `experiments/human-repeat/rewritten.py`, не в raw. Якщо rewrite не робився — познач «не робив»; незаміряне не називай нулем.
5. Збережи журнал (`Ctrl+S`) і напиши **«ревью готово»**. Перерви повідомляй окремо з тривалістю. Загальний wall time й сума per-function часу — різні величини, їх не підганяємо.

| ID | Функція | Verdict | Criterion | Причина | Action | Review, секунд | Rewrite, секунд |
| --- | --- | --- | --- | --- | --- | --- | --- |
| HR-G01 | test_mid_rate_known_currencies | rejected | Oracle | Очікуваний курс обчислюється за тією самою формулою, що й production-код. Незалежний oracle відсутній. | окремий rewrite — виконано | 23 | 60 |
| HR-G02 | test_mid_rate_unknown_currency_raises | accepted | Exceptions (Oracle N/A) | Перевірено невідомі вихідну та цільову валюти, тип винятку й повідомлення. | as-is | 9 | не робив |
| HR-G03 | test_quote_unknown_tier_raises | accepted | Exceptions (Oracle N/A) | Перевірено, що невідомий тариф спричиняє ValueError з очікуваним повідомленням. | as-is | 16 | не робив |
| HR-G04 | test_quote_within_allowance_no_spread | accepted | Boundary | Перевірено точну межу безкоштовного ліміту, нульовий спред і відсутність комісії. | as-is | 17 | не робив |
| HR-G05 | test_quote_exceed_allowance_default_spread | accepted | Arithmetic | Перевірено перевищення безкоштовного ліміту, застосування стандартного спреду тарифу та правильність розрахунку комісії. | as-is | 12 | не робив |
| HR-G06 | test_quote_exceed_allowance_spread_override | accepted | Arithmetic | Перевірено застосування перевизначеного спреду 5% та правильність розрахунку spread_amount. | as-is | 10 | не робив |
| HR-G07 | test_quote_partial_allowance_applied | rejected | Oracle | Очікуваний результат повторює формулу production-коду. Відсутній незалежний числовий oracle для часткового застосування ліміту. | окремий rewrite — виконано | 25 | 81 |
| HR-G08 | test_quote_as_dict_rounds_floats | rejected | Oracle | Перевірка підтверджує лише округлення вже повернутих значень. Немає порівняння з наперед визначеними очікуваними значеннями та перевірки повноти структури. | окремий rewrite — виконано | 32 | 63 |
| HR-G09 | test_transfer_fee_known_types | accepted | Arithmetic | Перевірено компоненти комісії, підсумкову суму та структуру результату для всіх підтримуваних типів переказів. | as-is | 15 | не робив |
| HR-G10 | test_transfer_fee_unknown_type_raises | accepted | Exceptions (Oracle N/A) | Перевірено тип винятку ValueError і повідомлення для невідомого типу переказу. | as-is | 10 | не робив |

Таблиця підготовлена асистентом лише як порожня форма за AST/іменами функцій. Вердикти, причини, actions і фактичні секунди заповнює автор; цей файл поки не є завершеним review.
