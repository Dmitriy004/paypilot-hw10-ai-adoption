# Новий повтор ДЗ10 після авторського baseline

Автор обрав новий повтор, а не очікування погодження ментора, і дозволив один OpenAI request до$0.05. Його baseline зафіксовано a05b304:8functions/15PASS; timer22:16:32–22:42:43 Europe/Warsaw=1571s, перерв немає за відповіддю автора. Це новий етап після historical generation; старий baseline/генерацію/результати не перейменовувати на людський контроль. Відповідність нового повтору всій рубриці ще не заявляти.

Підхід: зберегти нові request/response/metadata/extracted у `experiments/human-repeat/generation/`; поточний adapter дістає optional `--output-dir`, default незмінний. Альтернативу перезаписати historical reports відкинуто через втрату доказів; повторне використання старої генерації не дає нового порядку baseline→generation. app/manual/generated/mutants/prompts нині не змінюються. Повторний аналіз і promotion comparator — лише після авторського review.

Payload і модель ті самі: weak prompt+public fx.py, gpt-4.1-mini-2025-04-14,temp.7,max_output8000,storefalse/default,без tools/history/policy/baseline/mutants/критеріїв. Тарифи16.11 перевірені official pricing:.40/.10/1.60USD за1M input/cached/output. Вбудований conservative cap$0.03 суворіший за дозвіл$0.05;одна спроба без retries. Ключ із наявного локального .env читається лише в пам'яті.

Спочатку optional output routing RED→GREEN offline; потім окремий forecast із конкретними mutant IDs до request або mutation runs нового набору. Raw код не правити до людського review, original-red видаляти лише окремим commit після збереження raw. Автор наступним кроком сам дає verdict/reason/action і фактичні review/rewrite minutes; асистент не заповнює ці рішення замість нього. До завершення немає нового ROI чи LMS submission.
