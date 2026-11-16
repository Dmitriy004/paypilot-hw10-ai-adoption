# Відтворення ДЗ10 на чистому локальному clone

Статус: нова перевірка ще не виконана. Історичний `reports/clean-clone.json` стосується L11, не цього пакета.

Потрібно зафіксувати exact source commit, створити окремий clone без local hardlinks, встановити requirements у нову venv, виконати manual/generated/all та повний suite. Новий mutation report лишається у перевірочному clone і не переноситься до репозиторію здачі. Human/timing критерії перевіркою запуску не підтверджуються.
