from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str  # "low", "medium", "high"
    is_complete: bool = False

    def mark_complete(self):
        pass


@dataclass
class Pet:
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        pass

    def get_pending_tasks(self) -> List[Task]:
        pass


@dataclass
class Owner:
    name: str
    available_start: str  # e.g. "08:00"
    available_end: str    # e.g. "18:00"
    pet: Pet = None

    def get_all_tasks(self) -> List[Task]:
        pass


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def generate_schedule(self) -> List[Task]:
        pass

    def explain_plan(self) -> str:
        pass
