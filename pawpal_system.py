from dataclasses import dataclass, field
from typing import List, Optional

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str  # "low", "medium", "high"
    is_complete: bool = False

    def mark_complete(self):
        """Mark this task as completed."""
        self.is_complete = True


@dataclass
class Pet:
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def get_pending_tasks(self) -> List[Task]:
        """Return all tasks that have not been completed yet."""
        return [t for t in self.tasks if not t.is_complete]


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


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner
        self.scheduled_tasks: List[Task] = []
        self.skipped_tasks: List[Task] = []

    def generate_schedule(self) -> List[Task]:
        """Sort pending tasks by priority and fit as many as possible into the available time budget."""
        self.scheduled_tasks = []
        self.skipped_tasks = []

        time_budget = self.owner.available_end - self.owner.available_start
        pending = sorted(
            self.owner.get_all_tasks(),
            key=lambda t: PRIORITY_ORDER.get(t.priority, 99)
        )

        time_used = 0
        for task in pending:
            if time_used + task.duration_minutes <= time_budget:
                self.scheduled_tasks.append(task)
                time_used += task.duration_minutes
            else:
                self.skipped_tasks.append(task)

        return self.scheduled_tasks

    def explain_plan(self) -> str:
        if not self.scheduled_tasks and not self.skipped_tasks:
            return "No schedule generated yet. Call generate_schedule() first."

        lines = []
        time_budget = self.owner.available_end - self.owner.available_start
        time_used = sum(t.duration_minutes for t in self.scheduled_tasks)

        lines.append(f"Time budget: {time_budget} min | Used: {time_used} min | Remaining: {time_budget - time_used} min")
        lines.append("")

        if self.scheduled_tasks:
            lines.append("Scheduled:")
            for task in self.scheduled_tasks:
                lines.append(f"  + [{task.priority.upper()}] {task.title} ({task.duration_minutes} min)")

        if self.skipped_tasks:
            lines.append("")
            lines.append("Skipped (not enough time):")
            for task in self.skipped_tasks:
                lines.append(f"  - [{task.priority.upper()}] {task.title} ({task.duration_minutes} min)")

        return "\n".join(lines)
