# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
## Smarter Scheduling Features

Beyond basic task management, PawPal+ now includes intelligent scheduling algorithms:

### Sorting by Time
- **`sort_by_time()`**: Organize tasks chronologically by preferred time (HH:MM format)
- Places flexible "any time" tasks at the end for visibility
- Useful for viewing your day's schedule in order

### Filtering & Querying
- **`filter_by_pet()`**: View all tasks for a specific pet
- **`filter_by_status()`**: Separate incomplete tasks from completed ones
- Enables quick lookups without traversing entire task lists

### Recurring Task Automation
- **`mark_completed()`**: When you complete a daily/weekly task, a new instance automatically generates for the next occurrence
- Uses Python's `timedelta` to calculate: Daily tasks → tomorrow, Weekly tasks → next week
- Eliminates manual re-creation of repeating tasks

### Conflict Detection
- **`detect_conflicts()`**: Warns when multiple tasks are scheduled at the same time
- Returns friendly warning messages instead of crashing
- Example: "⚠️ CONFLICT at 10:00: Dog Training (Buddy), Cat Play (Max)"
- Helps prevent double-booking across multiple pets

### Scheduling Algorithm
The scheduler uses a **greedy selection approach**:
1. Ranks all tasks by priority (high → medium → low), then by duration
2. Sequentially fits tasks into available time
3. Explains which tasks were selected and why others were skipped
- This ensures high-priority tasks (feeding, medications) are prioritized for pet health

## Testing PawPal+

A comprehensive automated test suite ensures the reliability of scheduling and filtering logic.

### Running Tests

```bash
python -m pytest tests/test_pawpal.py -v
```

For a summary without verbose output:
```bash
python -m pytest tests/test_pawpal.py
```

### Test Coverage

The test suite includes **27 automated tests** organized into 9 test classes:

| Feature | Tests | Coverage |
|---------|-------|----------|
| **Task Completion** | 1 | Basic task state tracking |
| **Task Addition** | 1 | Pet-task association |
| **Sorting by Time** | 3 | Chronological ordering, flexible times, empty lists |
| **Recurring Tasks** | 3 | Daily/weekly auto-generation, one-time tasks |
| **Conflict Detection** | 5 | Same-time conflicts, multiple conflicts, no conflicts, flexible times, empty lists |
| **Filtering by Pet** | 3 | Correct filtering, case-insensitivity, empty results |
| **Filtering by Status** | 3 | Incomplete tasks, complete tasks, empty results |
| **Priority Ranking** | 2 | Priority ordering, secondary sort by duration |
| **Daily Plan Generation** | 3 | Time limit respect, empty owners, completed task exclusion |
| **Edge Cases** | 2 | Invalid time formats, zero-duration tasks, large task lists |

### What We Test

✅ **Happy Paths** (Expected behavior)
- Tasks sort correctly by time (HH:MM format)
- Daily/weekly tasks auto-create next occurrence
- Conflicts trigger warnings without crashing
- Filters work with case-insensitivity
- Scheduler respects available time limits
- Completed tasks are excluded from plans

✅ **Edge Cases** (Boundary conditions)
- Empty task/pet lists
- Tasks with flexible "any" time
- Invalid time formats (graceful degradation)
- Zero or negative task durations (skipped)
- Large task lists (100+ tasks)
- Multiple tasks at exact same time
- One-time vs. recurring tasks

### Test Results

```
======================= 27 passed in 0.20s =======================
```

### Confidence Level: ⭐⭐⭐⭐⭐ (5 stars)

**Why high confidence:**
- All core scheduling behaviors verified by automated tests
- Edge cases handled gracefully without crashes
- Recurring task logic validated with timedelta calculations
- Conflict detection confirmed for multiple scenarios
- Performance tested with large task lists (100+ tasks)
- Filtering logic works across pets, times, and statuses
- Time constraint enforcement validated

**Limitations to note:**
- Tests assume tasks stay within a single day (no multi-day validation)
- UI integration not yet tested (only business logic)
- No tests for concurrent access or multi-user scenarios
- Real-world time zone handling not included

This test suite provides strong evidence that the PawPal+ scheduler will reliably help pet owners manage daily tasks safely and predictably.