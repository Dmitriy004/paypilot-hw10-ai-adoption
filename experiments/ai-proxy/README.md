# Окремий timed AI-proxy експеримент

Пізніший додаток від 13.11.2026, не human baseline і не заміна історичного порівняння L11. Виконавець — окремий AI-субагент; навички або швидкість «середньої людини» цим не виміряні. Фактичні UTC-інтервали зчитано під час роботи, без навмисного очікування. Збережені тут файли — intentional inputs окремого експерименту, а не файли основних comparator sets.

| Фаза | Початок UTC | Кінець UTC | Секунди | Обсяг / перша перевірка |
| --- | --- | --- | --- | --- |
| A: написання | 2026-11-13 18:15:27 | 2026-11-13 18:16:23 | 56 | 8 функцій / 10 cases; 10 passed in 0.05s |
| B: review | 2026-11-13 18:17:31 | 2026-11-13 18:19:52 | 141 | 11 raw functions; 2 accepted / 9 rejected; raw verification 12 passed / 1 failed |
| C: одна правка | 2026-11-13 18:21:01 | 2026-11-13 18:21:32 | 31 | 1 функція / 2 cases; 2 passed in 0.04s |
| Сума timed-фаз | — | — | **228 = 3.8 хв** | Не безперервний wall time: паузи між фазами виключено |

Фази включають читання, створення файлів, перевірку й затримку інструментів. A бачила лише публічні fx.py і policy.py, не старі tests/mutants/reports/prompts. B після A бачила frozen критерії й raw generated output; novelty оцінювала щодо A, а не історичного manual. C окремо виправила original-red override та додала free-allowance control. Жодна фаза не редагувала основні набори, Git index чи HEAD. Прямих нових API-запитів немає; вартість обчислень субагента/координатора не виміряна, тому $0 загальних витрат не заявляємо.

## Межі review

[review-measurement.json](review-measurement.json) збережено без зміни початкового запису; його baseline path вказує на тодішній scratch. Той самий файл тепер збережено як [baseline.py](baseline.py), SHA256 у [measurement.json](measurement.json). Окремих minutes для кожної функції немає. Verdict G9 тут accepted лише для слабкої rounding property; historical review його відхиляє, бо вона пропускає втрату точності та ключів. Це обмеження приладу й незгода review, не доказ захисту від D-01/02. Різні novelty baselines та verdicts не змішуємо з historical 3/11 accepted чи mutation scores.

## Час, повідомлений автором

Автор повідомив у чаті 60 хв writing, 20 хв review та 3 хв на одну правку. Їх сума — 83 хв; відношення до 3.8 хв — 21.84. Це **арифметика на self-reported inputs**, не встановлений коефіцієнт прискорення: невідомі timestamps, однаковість завдань, якість і повний обсяг правок. Ці числа не виправляють походження historical baseline або порядок експерименту. Per-function minutes та commit timestamps не реконструюємо.

## Повторна offline-перевірка

З кореня репозиторію, з PYTHONPATH, рівним абсолютному шляху clone:

```powershell
$env:PYTHONPATH = (Get-Location).Path
.venv/Scripts/python.exe -m pytest experiments/ai-proxy/baseline.py -q -p no:cacheprovider
.venv/Scripts/python.exe -m pytest experiments/ai-proxy/rewrite.py -q -p no:cacheprovider
```

Файли названі не test_*.py, щоб стандартний suite і run_mutants.py не включали цей додаток. Новий запуск перевіряє код, не повторює історичні часові виміри.
