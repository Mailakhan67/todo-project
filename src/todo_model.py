"""Task data model and in-memory storage."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from src.exceptions import TaskNotFoundError, ValidationError


@dataclass
class Task:
    """Represents a single todo task."""

    id: int
    title: str
    description: str = ""
    status: str = "pending"
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def mark_complete(self) -> None:
        """Mark this task as complete."""
        self.status = "complete"
        self.updated_at = datetime.utcnow()


@dataclass
class TaskCollection:
    """Manages all Task entities in memory."""

    _tasks: dict[int, Task] = field(default_factory=dict)
    _next_id: int = 1

    def create(self, title: str, description: str = "") -> Task:
        """Create a new task with auto-generated ID."""
        if not title or not title.strip():
            raise ValidationError("Task title cannot be empty")

        task = Task(id=self._next_id, title=title.strip(), description=description.strip())
        self._tasks[self._next_id] = task
        self._next_id += 1
        return task

    def get_by_id(self, id: int) -> Optional[Task]:
        """Retrieve a task by its ID."""
        return self._tasks.get(id)

    def get_all(self) -> list[Task]:
        """Return all tasks sorted by ID (creation order)."""
        return sorted(self._tasks.values(), key=lambda t: t.id)

    def get_by_status(self, status: str) -> list[Task]:
        """Return all tasks with the given status, sorted by ID."""
        return [t for t in self._tasks.values() if t.status == status]

    def update(self, id: int, title: Optional[str] = None, description: Optional[str] = None) -> Task:
        """Update a task's title and/or description."""
        task = self._tasks.get(id)
        if task is None:
            raise TaskNotFoundError(id)

        if title is not None:
            if not title.strip():
                raise ValidationError("Task title cannot be empty")
            task.title = title.strip()

        if description is not None:
            task.description = description.strip()

        task.updated_at = datetime.utcnow()
        return task

    def delete(self, id: int) -> bool:
        """Delete a task by ID. Returns True if task existed."""
        if id in self._tasks:
            del self._tasks[id]
            return True
        return False

    def mark_complete(self, id: int) -> Task:
        """Mark a task as complete."""
        task = self._tasks.get(id)
        if task is None:
            raise TaskNotFoundError(id)

        task.mark_complete()
        return task
