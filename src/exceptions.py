"""Custom exceptions for the Todo application."""


class TodoError(Exception):
    """Base exception for todo application errors."""
    pass


class TaskNotFoundError(TodoError):
    """Raised when a task with the given ID is not found."""

    def __init__(self, task_id: int):
        self.task_id = task_id
        super().__init__(f"Task with ID {task_id} not found")


class ValidationError(TodoError):
    """Raised when input validation fails."""

    def __init__(self, message: str):
        super().__init__(message)


class DuplicateTaskError(TodoError):
    """Raised when attempting to create a duplicate task."""

    def __init__(self, message: str = "Task already exists"):
        super().__init__(message)
