# L11 — перевірка й межі доказу

**Історичний proof13.11.2026.** Не є перевіркою нового повтору: поточні джерела й статус у [Impact Report](ai-adoption-impact-report.md) та [chain-ready](chain-ready.md).

13.11.2026. Локальна гілка `codex/l11-openai-demo`; push/merge/LMS не виконували. Вихідний кіт `d6c471a79e3bb4da33756c6e1026d3366f98faf5`.

## Чистий clone

`reports/clean-clone.json` — фактичний запуск на окремому clone `be298e3b5593f2f6e9d716514c475d21cf2f861a`. Початковий git status порожній; новий venv; установка requirements; pytest 34/34 PASS; upstream union 9/12, D-01..03 survivors. Провайдер не викликався й ключі не потрібні. Пізніші зміни — підсумкові документи/докази; comparator-код не змінювався.

## Незмінність

`git diff d6c471a..HEAD -- app .claude/settings.json requirements.txt tools/run_mutants.py` порожній. SHA256:

| Файл | Hash |
| --- | --- |
| app/engines/fx.py | b0a2262dc6b3da959bb9b87cdd9ee3a2f77447b6d4eb04ba78dd206cd88e51b2 |
| app/engines/policy.py | a1d17a111bb57181d065cd3f0f388ba62c68ed808c0fb7664090f1a2c11a8f91 |
| .claude/settings.json | 5c02b6c508e896ea25d9c96a5c395d037b931cf7a9e8e29662e22257a6b79cc4 |
| mutants.toml | 04dc871bd9947a22a5dc252f0d97f070abcb960effa5f053f3a5b8a5f0a947e6 |
| frozen baseline | 035f7fd503d2c5f9994408d5a3b6eb9090891ffdfdae6bac3e76b26275969bd9 |
| raw extracted Python | 27fc637d40c34f70bf10bd17b41eb2fe1e8802e7b3f1f98c2de5e9b53ac40b97 |
| generated після єдиного видалення G-06 | d1da67aadd317f6bd0438e87fc900c8a6da8c6edbce2fa031b77f78c3673d334 |

Прогноз до baseline `72fafac`; baseline `03c206c` (docstring уточнено `6c58594`); mutants і prompts `6c58594`; прогноз ID окремо `b305baa`; raw generation `e7c77a6`; тільки G-06 видалено `df6a596`; code used in initial mutation runs `1616a96`; числові звіти/audit `be298e3`.

## Незалежне whole-branch review

Fresh-context read-only reviewer перевірив upstream..`be298e3`, plan/spec і рішення, без API-викликів чи змін index/HEAD. Critical/Important не знайдено. Зауваження про LAB-STATUS усунене під час запланованого завершення документації.

Підтверджено: exact allowlist payload і hash request/response/code; raw transfer без змін; generated AST відрізняється лише відсутнім G-06; усі захищені файли й frozen inputs незмінні; усі 36 set/mutant outcomes узгоджені з assertion audit; rewritten/infrastructure виключені з comparator; D witnesses не еквівалентні; coverage/JUnit denominators і token-cost arithmetic сходяться; секретів у task paths не знайдено. Adapter incomplete output відхиляє, retries немає, redirects відхиляє, output directory створює ексклюзивно до відправки.

## Рішення щодо меж, які reviewer свідомо не оцінював

- Формальна human-vs-AI відповідність і продуктивність: не заявляємо. Користувач змінив протокол; інакше заощадження людини були б недоведеними.
- Billing, універсальна якість моделі та production detection: не заявляємо. Є лише один request usage і один підібраний список; ціна за тарифом не є списанням.
- Незалежна зовнішня звірка тарифу/сторінки не входила в read-only review. Тариф перевіряв основний виконавець у official docs; браузерний tail лишається недоступним. Ризик — неповна відповідність кінцевим крокам сторінки, не приховуємо.
- Слабкі oracles, policy imports, D survivors — сам результат, не баг, який слід потай виправити. G-03 accepted лише у вузькому no-spread/metadata scope; це не тарифний еталон.
- Upstream runner вважає nonzero exit kill: зберігаємо незмінний алгоритм, а фактичні результати цього прогону перевіряє assertion audit. Не поширюємо це на довільні майбутні мутанти.
- Sandbox довільного майбутнього Python не доведено: виконаний output переглянуто і він містить звичайні локальні тести. Наступні генерації потребують нового перегляду до запуску, не автоматичного виконання.

## Відхилення, які не можна «виправити» заднім числом

Baseline і review зроблено асистентом; 40/45 хв тільки припущення; модель OpenAI замість Claude обрана користувачем. Тому поточні counts придатні для технічної демонстрації, але не для висновку про перевагу над людиною або повної формальної здачі курсового експерименту. Для цього потрібен новий незалежний протокол, а не перейменування артефактів.
