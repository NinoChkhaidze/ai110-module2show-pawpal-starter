from datetime import date, timedelta
from pawpal_system import Task, Pet, Owner, Scheduler


def test_mark_complete_changes_status():
    task = Task(title="Morning walk", duration_minutes=30, priority="high")
    assert task.is_complete is False
    task.mark_complete()
    assert task.is_complete is True


def test_add_task_increases_pet_task_count():
    pet = Pet(age=3)
    assert len(pet.tasks) == 0
    pet.add_task(Task(title="Feeding", duration_minutes=10, priority="high"))
    pet.add_task(Task(title="Playtime", duration_minutes=20, priority="medium"))
    assert len(pet.tasks) == 2


# ---------------------------------------------------------------------------
# Sorting Correctness
# ---------------------------------------------------------------------------

def test_sort_by_time_returns_chronological_order():
    """Tasks with start_time set should come back earliest-first."""
    pet = Pet(age=2)
    owner = Owner(name="Alex", available_start=480, available_end=1080, pet=pet)
    scheduler = Scheduler(owner)

    # Deliberately add them out of order
    t1 = Task(title="Evening walk",  duration_minutes=30, priority="medium", start_time="17:00")
    t2 = Task(title="Morning meds",  duration_minutes=5,  priority="high",   start_time="08:00")
    t3 = Task(title="Afternoon play", duration_minutes=20, priority="low",   start_time="13:30")

    scheduler.scheduled_tasks = [t1, t2, t3]
    sorted_tasks = scheduler.sort_by_time(scheduler.scheduled_tasks)

    assert [t.start_time for t in sorted_tasks] == ["08:00", "13:30", "17:00"]


def test_sort_by_time_tasks_without_time_go_last():
    """Tasks with no start_time should be placed after all timed tasks."""
    pet = Pet(age=2)
    owner = Owner(name="Alex", available_start=480, available_end=1080, pet=pet)
    scheduler = Scheduler(owner)

    timed   = Task(title="Walk",    duration_minutes=20, priority="high",   start_time="09:00")
    no_time = Task(title="Groom",   duration_minutes=15, priority="medium", start_time="")

    scheduler.scheduled_tasks = [no_time, timed]
    sorted_tasks = scheduler.sort_by_time(scheduler.scheduled_tasks)

    assert sorted_tasks[0].title == "Walk"
    assert sorted_tasks[1].title == "Groom"


# ---------------------------------------------------------------------------
# Recurrence Logic
# ---------------------------------------------------------------------------

def test_complete_daily_task_appends_next_day_occurrence():
    """Completing a daily task should add a new task due tomorrow."""
    today = date.today()
    pet = Pet(age=4)
    daily_task = Task(
        title="Morning feed",
        duration_minutes=10,
        priority="high",
        frequency="daily",
        due_date=today,
    )
    pet.add_task(daily_task)

    pet.complete_task(daily_task)

    # Original task is now complete
    assert daily_task.is_complete is True

    # A second task should have been appended
    assert len(pet.tasks) == 2
    next_task = pet.tasks[1]
    assert next_task.due_date == today + timedelta(days=1)
    assert next_task.is_complete is False
    assert next_task.frequency == "daily"


def test_complete_one_off_task_does_not_create_new_task():
    """Completing a task with no frequency should NOT append a follow-up."""
    pet = Pet(age=2)
    one_off = Task(title="Vet visit", duration_minutes=60, priority="high")
    pet.add_task(one_off)

    pet.complete_task(one_off)

    assert len(pet.tasks) == 1          # no new task added
    assert pet.tasks[0].is_complete is True


# ---------------------------------------------------------------------------
# Conflict Detection
# ---------------------------------------------------------------------------

def test_detect_conflicts_flags_overlapping_tasks():
    """Two tasks whose time windows overlap should produce a conflict warning."""
    pet = Pet(age=3)
    owner = Owner(name="Sam", available_start=480, available_end=1080, pet=pet)
    scheduler = Scheduler(owner)

    # Walk starts at 08:00 and lasts 30 min → occupies 08:00–08:30
    # Meds start at 08:15 → starts inside the walk window
    walk = Task(title="Walk", duration_minutes=30, priority="high", start_time="08:00")
    meds = Task(title="Meds", duration_minutes=10, priority="high", start_time="08:15")

    scheduler.scheduled_tasks = [walk, meds]
    warnings = scheduler.detect_conflicts()

    assert len(warnings) == 1
    assert "Walk" in warnings[0]
    assert "Meds" in warnings[0]


def test_detect_conflicts_no_warning_for_sequential_tasks():
    """Tasks that run back-to-back (no overlap) should produce no warnings."""
    pet = Pet(age=3)
    owner = Owner(name="Sam", available_start=480, available_end=1080, pet=pet)
    scheduler = Scheduler(owner)

    # Walk 08:00–08:30, feed starts exactly at 08:30
    walk = Task(title="Walk", duration_minutes=30, priority="high", start_time="08:00")
    feed = Task(title="Feed", duration_minutes=10, priority="high", start_time="08:30")

    scheduler.scheduled_tasks = [walk, feed]
    warnings = scheduler.detect_conflicts()

    assert warnings == []


def test_detect_conflicts_same_start_time_is_flagged():
    """Two tasks at the exact same start time must always be flagged."""
    pet = Pet(age=1)
    owner = Owner(name="Sam", available_start=480, available_end=1080, pet=pet)
    scheduler = Scheduler(owner)

    t1 = Task(title="Bath",  duration_minutes=20, priority="medium", start_time="10:00")
    t2 = Task(title="Brush", duration_minutes=10, priority="low",    start_time="10:00")

    scheduler.scheduled_tasks = [t1, t2]
    warnings = scheduler.detect_conflicts()

    assert len(warnings) == 1
