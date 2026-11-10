# Examples

Real output from HabitTrack, captured from actual runs on 2026-11-10.

## Add a habit

```bash
python3 habittrack.py add --name "Reading"
```

```
Habit added: Reading
```

## Mark it done

```bash
python3 habittrack.py done --name "Reading" --date 2026-11-08
python3 habittrack.py done --name "Reading" --date 2026-11-09
python3 habittrack.py done --name "Reading" --date 2026-11-10
```

```
Marked Reading done on 2026-11-08
Marked Reading done on 2026-11-09
Marked Reading done on 2026-11-10
```

Leave out `--date` to mark today.

## List all habits

```bash
python3 habittrack.py list
```

```
Old habit: 1 days, current streak 0, last done 2026-11-05
Reading: 3 days, current streak 3, last done 2026-11-10
```

"Old habit" was only done on 2026-11-05, five days earlier, so its streak is
broken and shows 0 even though the day is still recorded.

## Streak detail with the last 7 days

```bash
python3 habittrack.py streak --name "Reading"
```

```
Reading: 3 days total
Current streak: 3
Last done: 2026-11-10
Last 7 days:
2026-11-04 [ ]
2026-11-05 [ ]
2026-11-06 [ ]
2026-11-07 [ ]
2026-11-08 [x]
2026-11-09 [x]
2026-11-10 [x]
```
