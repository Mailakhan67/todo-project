"""Unit tests for Task model and TaskCollection."""

import pytest
from src.todo_model import Task, TaskCollection
from src.exceptions import ValidationError, TaskNotFoundError


class TestTask:
    """Tests for the Task dataclass."""

    def test_task_creation(self):
        """Test that a task is created with correct default values."""
        task = Task(id=1, title="Buy groceries")

        assert task.id == 1
        assert task.title == "Buy groceries"
        assert task.description == ""
        assert task.status == "pending"
        assert task.created_at is not None
        assert task.updated_at is not None

    def test_task_default_values(self):
        """Test that all default values are set correctly."""
        task = Task(id=1, title="Test task")

        assert task.status == "pending"
        assert task.description == ""
        assert isinstance(task.created_at, type(task.updated_at))

    def test_task_with_description(self):
        """Test task creation with description."""
        task = Task(id=1, title="Buy groceries", description="Milk, eggs, bread")

        assert task.description == "Milk, eggs, bread"

    def test_task_mark_complete(self):
        """Test marking a task as complete."""
        task = Task(id=1, title="Test task")
        assert task.status == "pending"

        task.mark_complete()

        assert task.status == "complete"
        assert task.updated_at >= task.created_at


class TestTaskCollection:
    """Tests for the TaskCollection class."""

    def test_create_task(self):
        """Test creating a new task."""
        collection = TaskCollection()
        task = collection.create(title="Buy groceries")

        assert task.id == 1
        assert task.title == "Buy groceries"
        assert task.status == "pending"
        assert len(collection.get_all()) == 1

    def test_create_multiple_tasks(self):
        """Test creating multiple tasks."""
        collection = TaskCollection()
        task1 = collection.create(title="Task 1")
        task2 = collection.create(title="Task 2")
        task3 = collection.create(title="Task 3")

        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3
        assert len(collection.get_all()) == 3

    def test_get_by_id(self):
        """Test retrieving a task by ID."""
        collection = TaskCollection()
        created = collection.create(title="Test task")
        retrieved = collection.get_by_id(created.id)

        assert retrieved == created
        assert collection.get_by_id(999) is None

    def test_get_all_returns_sorted_tasks(self):
        """Test that get_all returns tasks sorted by ID (creation order)."""
        collection = TaskCollection()
        task1 = collection.create(title="First")
        task2 = collection.create(title="Second")
        task3 = collection.create(title="Third")

        all_tasks = collection.get_all()

        assert len(all_tasks) == 3
        assert all_tasks[0] == task1
        assert all_tasks[1] == task2
        assert all_tasks[2] == task3

    def test_get_by_status(self):
        """Test filtering tasks by status."""
        collection = TaskCollection()
        task1 = collection.create(title="Pending 1")
        task2 = collection.create(title="Pending 2")
        task3 = collection.create(title="Complete")
        task3.mark_complete()

        pending = collection.get_by_status("pending")
        complete = collection.get_by_status("complete")

        assert len(pending) == 2
        assert len(complete) == 1
        assert task1 in pending
        assert task2 in pending
        assert task3 in complete

    def test_update_title(self):
        """Test updating a task's title."""
        collection = TaskCollection()
        task = collection.create(title="Old title")

        updated = collection.update(task.id, title="New title")

        assert updated.title == "New title"

    def test_update_description(self):
        """Test updating a task's description."""
        collection = TaskCollection()
        task = collection.create(title="Test task")

        updated = collection.update(task.id, description="New description")

        assert updated.description == "New description"

    def test_update_both_title_and_description(self):
        """Test updating both title and description."""
        collection = TaskCollection()
        task = collection.create(title="Original", description="Original desc")

        updated = collection.update(task.id, title="New", description="New desc")

        assert updated.title == "New"
        assert updated.description == "New desc"

    def test_update_empty_title_raises_error(self):
        """Test that updating with empty title raises ValidationError."""
        collection = TaskCollection()
        task = collection.create(title="Test task")

        with pytest.raises(ValidationError):
            collection.update(task.id, title="")

    def test_update_nonexistent_task_raises_error(self):
        """Test that updating a non-existent task raises TaskNotFoundError."""
        collection = TaskCollection()

        with pytest.raises(TaskNotFoundError):
            collection.update(999, title="New title")

    def test_delete(self):
        """Test deleting a task."""
        collection = TaskCollection()
        task = collection.create(title="To delete")
        assert len(collection.get_all()) == 1

        result = collection.delete(task.id)

        assert result is True
        assert len(collection.get_all()) == 0

    def test_delete_nonexistent_task(self):
        """Test that deleting a non-existent task returns False."""
        collection = TaskCollection()

        result = collection.delete(999)

        assert result is False

    def test_mark_complete(self):
        """Test marking a task as complete."""
        collection = TaskCollection()
        task = collection.create(title="Test task")
        assert task.status == "pending"

        completed = collection.mark_complete(task.id)

        assert completed.status == "complete"
        assert completed.updated_at >= completed.created_at

    def test_mark_complete_nonexistent_task_raises_error(self):
        """Test that marking complete on non-existent task raises TaskNotFoundError."""
        collection = TaskCollection()

        with pytest.raises(TaskNotFoundError):
            collection.mark_complete(999)

    def test_create_empty_title_raises_error(self):
        """Test that creating a task with empty title raises ValidationError."""
        collection = TaskCollection()

        with pytest.raises(ValidationError):
            collection.create(title="")

    def test_create_whitespace_only_title_raises_error(self):
        """Test that creating a task with whitespace-only title raises ValidationError."""
        collection = TaskCollection()

        with pytest.raises(ValidationError):
            collection.create(title="   ")
