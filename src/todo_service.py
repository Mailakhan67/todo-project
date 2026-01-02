"""Service layer for todo operations."""

from typing import Optional

from src.todo_model import Task, TaskCollection
from src.exceptions import TaskNotFoundError, ValidationError


class TodoService:
    """Business logic for todo operations."""

    def __init__(self):
        self._collection = TaskCollection()

    def add_task(self, title: str, description: str = "") -> Task:
        """Add a new task."""
        if not title or not title.strip():
            raise ValidationError("Task title cannot be empty")
        return self._collection.create(title.strip(), description.strip() if description else "")

    def list_tasks(self, status: Optional[str] = None) -> list[Task]:
        """List all tasks, optionally filtered by status."""
        if status is None:
            return self._collection.get_all()
        return self._collection.get_by_status(status)

    def complete_task(self, task_id: int) -> Task:
        """Mark a task as complete."""
        return self._collection.mark_complete(task_id)

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Task:
        """Update a task."""
        return self._collection.update(task_id, title, description)

    def delete_task(self, task_id: int) -> bool:
        """Delete a task."""
        return self._collection.delete(task_id)

    def get_task(self, task_id: int) -> Optional[Task]:
        """Get a task by ID."""
        return self._collection.get_by_id(task_id)
