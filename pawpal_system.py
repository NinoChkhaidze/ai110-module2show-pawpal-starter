from dataclasses import dataclass, field
from datetime import date, timedelta
from itertools import combinations
from typing import List, Optional

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}
FREQUENCY_DELTA = {"daily": timedelta(days=1), "weekly": timedelta(weeks=1)}


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str              # "low", "medium", "high"
    frequency: Optional[str] = None  # "daily", "weekly", or None (one-off)
    due_date: Optional[date] = None
    start_time: str = ""       # "HH:MM", assigned by Scheduler
    is_complete: bool = False

    def mark_complete(self):
        """Mark this task as completed."""
        self.is_complete = True

    def next_occurrence(self) -> Optional["Task"]:
        """Return a fresh Task for the next due date if this is a recurring task, else None."""
        if self.frequency not in FREQUENCY_DELTA:
            return None
        next_due = (self.due_date or date.today()) + FREQUENCY_DELTA[self.frequency]
        return Task(
            title=self.title,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            frequency=self.frequency,
            due_date=next_due,
        )


@dataclass
class Pet:
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def complete_task(self, task: Task):
        """Mark a task complete and auto-schedule its next occurrence if recurring."""
        task.mark_complete()
        next_task = task.next_occurrence()
        if next_task:
            self.tasks.append(next_task)

    def get_pending_tasks(self) -> List[Task]:
        """Return all tasks that have not been completed yet."""
        return [t for t in self.tasks if not t.is_complete]

    def get_tasks_by_status(self, complete: bool) -> List[Task]:
        """Return tasks filtered by completion status."""
        return [t for t in self.tasks if t.is_complete == complete]


@dataclass
class Owner:
    name: str
    available_start: int  # minutes since midnight, e.g. 480 = 8:00 AM
    available_end: int    # minutes since midnight, e.g. 1080 = 6:00 PM
    pet: Optional[Pet] = field(default=None)

    def __post_init__(self):
        """Ensure the owner has a pet assigned at creation time."""
        if self.pet is None:
            raise ValueError("Owner must have a pet.")

    def get_all_tasks(self) -> List[Task]:
        """Return all pending tasks from the owner's pet."""
        return self.pet.get_pending_tasks()


def _time_to_minutes(t: str) -> int:
    """Convert 'HH:MM' string to minutes since midnight."""
    h, m = t.split(":")
    return int(h) * 60 + int(m)


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner
        self.scheduled_tasks: List[Task] = []
        self.skipped_tasks: List[Task] = []
        self.conflicts: List[str] = []

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by start_time in HH:MM format; tasks with no time set go last."""
        return sorted(tasks, key=lambda t: t.start_time if t.start_time else "99:99")

    def detect_conflicts(self) -> List[str]:
        """Check scheduled tasks for time overlaps; return a list of warning strings."""
        warnings = []
        timed = [t for t in self.scheduled_tasks if t.start_time]
        for a, b in combinations(timed, 2):
            a_start, b_start = _time_to_minutes(a.start_time), _time_to_minutes(b.start_time)
            if a_start < b_start + b.duration_minutes and b_start < a_start + a.duration_minutes:
                warnings.append(
                    f"CONFLICT: '{a.title}' ({a.start_time}, {a.duration_minutes} min) "
                    f"overlaps '{b.title}' ({b.start_time}, {b.duration_minutes} min)"
                )
        self.conflicts = warnings
        return warnings

    def filter_by_status(self, complete: bool) -> List[Task]:
        """Return tasks filtered by completion status."""
        return self.owner.pet.get_tasks_by_status(complete)

    def generate_schedule(self) -> List[Task]:
        """Sort pending tasks by priority then duration, assign start times, and fit into time budget."""
        self.scheduled_tasks = []
        self.skipped_tasks = []

        pending = sorted(
            self.owner.get_all_tasks(),
            key=lambda t: (PRIORITY_ORDER.get(t.priority, 99), t.duration_minutes)
        )

        current_time = self.owner.available_start
        for task in pending:
            if current_time + task.duration_minutes <= self.owner.available_end:
                if not task.start_time:  # don't overwrite manually pre-assigned times
                    task.start_time = f"{current_time // 60:02d}:{current_time % 60:02d}"
                self.scheduled_tasks.append(task)
                current_time += task.duration_minutes
            else:
                self.skipped_tasks.append(task)

        return self.scheduled_tasks

    def explain_plan(self) -> str:
        """Return a human-readable summary of scheduled and skipped tasks with start times."""
        if not self.scheduled_tasks and not self.skipped_tasks:
            return "No schedule generated yet. Call generate_schedule() first."

        lines = []
        time_budget = self.owner.available_end - self.owner.available_start
        time_used = sum(t.duration_minutes for t in self.scheduled_tasks)

        lines.append(f"Time budget: {time_budget} min | Used: {time_used} min | Remaining: {time_budget - time_used} min")
        lines.append("")

        if self.scheduled_tasks:
            lines.append("Scheduled:")
            for task in self.sort_by_time(self.scheduled_tasks):
                recur = f" [{task.frequency}]" if task.frequency else ""
                due = f" due {task.due_date}" if task.due_date else ""
                lines.append(f"  + {task.start_time}  [{task.priority.upper()}]{recur} {task.title} ({task.duration_minutes} min){due}")

        if self.skipped_tasks:
            lines.append("")
            lines.append("Skipped (not enough time):")
            for task in self.skipped_tasks:
                lines.append(f"  - [{task.priority.upper()}] {task.title} ({task.duration_minutes} min)")

        return "\n".join(lines)
