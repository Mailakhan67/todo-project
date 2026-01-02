"""Integration tests for CLI commands."""

import pytest
import subprocess
import sys
from pathlib import Path


def run_todo(args: list[str]) -> subprocess.CompletedProcess:
    """Run the todo CLI with given arguments and return the result."""
    project_root = Path(__file__).parent.parent.parent
    result = subprocess.run(
        [sys.executable, "-m", "src.main"] + args,
        capture_output=True,
        text=True,
        cwd=str(project_root)
    )
    return result


def run_python_script(script: str) -> subprocess.CompletedProcess:
    """Run a Python script in the project directory."""
    project_root = Path(__file__).parent.parent.parent
    result = subprocess.run(
        [sys.executable, "-c", script],
        capture_output=True,
        text=True,
        cwd=str(project_root)
    )
    return result


class TestAddCommand:
    """Tests for the 'add' command."""

    def test_add_command_success(self):
        """Test adding a task successfully."""
        result = run_todo(["add", "Test task"])

        assert result.returncode == 0
        assert "Task added successfully" in result.stdout
        assert "ID: 1" in result.stdout

    def test_add_command_with_description(self):
        """Test adding a task with description."""
        result = run_todo(["add", "Test task", "--description", "A test description"])

        assert result.returncode == 0
        assert "Task added successfully" in result.stdout

    def test_add_command_empty_title(self):
        """Test that adding a task with empty title fails."""
        result = run_todo(["add", ""])

        assert result.returncode == 1
        assert "Error:" in result.stderr or "Error:" in result.stdout


class TestListCommand:
    """Tests for the 'list' command."""

    def test_list_command_empty(self):
        """Test listing tasks when none exist."""
        result = run_todo(["list"])

        assert result.returncode == 0
        assert "No tasks found" in result.stdout or "No tasks" in result.stdout

    def test_list_command_with_status_filter(self):
        """Test listing tasks with status filter."""
        result = run_todo(["list", "--status", "complete"])

        assert result.returncode == 0


class TestAddThenListWorkflow:
    """Integration tests for add + list workflow using same session."""

    def test_add_then_list_shows_new_task(self):
        """Test that adding a task makes it visible in list."""
        script = '''
from src.todo_controller import TodoController
controller = TodoController()
# Add task
controller.run(["add", "Buy groceries", "--description", "Milk and eggs"])
# List and verify
controller.run(["list"])
# Verify task exists in memory
tasks = controller.service.list_tasks()
assert len(tasks) == 1, f"Expected 1 task, got {len(tasks)}"
assert tasks[0].title == "Buy groceries"
'''
        result = run_python_script(script)
        assert result.returncode == 0, f"Script failed: {result.stderr}"


class TestCompleteCommand:
    """Tests for the 'complete' command."""

    def test_complete_command_success(self):
        """Test marking a task as complete."""
        script = '''
from src.todo_controller import TodoController
controller = TodoController()
controller.run(["add", "Task to complete"])
result = controller.run(["complete", "1"])
assert result == 0, "Complete should succeed"
assert controller.service.get_task(1).status == "complete"
'''
        result = run_python_script(script)
        assert result.returncode == 0, f"Script failed: {result.stderr}"

    def test_complete_command_invalid_id(self):
        """Test completing a non-existent task."""
        result = run_todo(["complete", "999"])

        assert result.returncode == 1
        assert "not found" in result.stderr.lower() or "not found" in result.stdout.lower()


class TestDeleteCommand:
    """Tests for the 'delete' command."""

    def test_delete_command_success(self):
        """Test deleting a task."""
        script = '''
from src.todo_controller import TodoController
controller = TodoController()
controller.run(["add", "Task to delete"])
result = controller.run(["delete", "1"])
assert result == 0, "Delete should succeed"
assert len(controller.service.list_tasks()) == 0
'''
        result = run_python_script(script)
        assert result.returncode == 0, f"Script failed: {result.stderr}"

    def test_delete_command_invalid_id(self):
        """Test deleting a non-existent task."""
        result = run_todo(["delete", "999"])

        assert result.returncode == 1
        assert "not found" in result.stderr.lower() or "not found" in result.stdout.lower()


class TestUpdateCommand:
    """Tests for the 'update' command."""

    def test_update_command_success(self):
        """Test updating a task's title."""
        script = '''
from src.todo_controller import TodoController
controller = TodoController()
controller.run(["add", "Original title"])
result = controller.run(["update", "1", "--title", "New title"])
assert result == 0, "Update should succeed"
assert controller.service.get_task(1).title == "New title"
'''
        result = run_python_script(script)
        assert result.returncode == 0, f"Script failed: {result.stderr}"

    def test_update_command_invalid_id(self):
        """Test updating a non-existent task."""
        result = run_todo(["update", "999", "--title", "New title"])

        assert result.returncode == 1
        assert "not found" in result.stderr.lower() or "not found" in result.stdout.lower()


class TestHelpCommand:
    """Tests for the 'help' command."""

    def test_help_command(self):
        """Test that help shows all commands."""
        result = run_todo(["--help"])

        assert result.returncode == 0
        assert "add" in result.stdout.lower()
        assert "list" in result.stdout.lower()
        assert "complete" in result.stdout.lower()
        assert "delete" in result.stdout.lower()
        assert "update" in result.stdout.lower()


class TestErrorHandling:
    """Tests for error handling."""

    def test_invalid_command_shows_error(self):
        """Test that an invalid command shows an error."""
        result = run_todo(["invalid_command"])

        # argparse returns 2 for invalid arguments, 1 for other errors
        assert result.returncode in [1, 2]
        assert "error" in result.stderr.lower() or "error" in result.stdout.lower()


class TestFullWorkflow:
    """Full integration tests for complete workflows."""

    def test_all_operations_workflow(self):
        """Test all 5 core operations in a single session."""
        script = '''
from src.todo_controller import TodoController
controller = TodoController()

# 1. Add tasks
controller.run(["add", "Buy groceries"])
controller.run(["add", "Call mom"])

# 2. List all tasks
tasks = controller.service.list_tasks()
assert len(tasks) == 2, "Should have 2 tasks"

# 3. Complete one task
controller.run(["complete", "1"])
assert controller.service.get_task(1).status == "complete"

# 4. Update a task
controller.run(["update", "2", "--title", "Call mom (birthday)"])
assert controller.service.get_task(2).title == "Call mom (birthday)"

# 5. Delete a task
controller.run(["delete", "1"])
assert controller.service.get_task(1) is None

# Final state: 1 task remaining
tasks = controller.service.list_tasks()
assert len(tasks) == 1, "Should have 1 task after delete"
assert tasks[0].status == "pending"
'''
        result = run_python_script(script)
        assert result.returncode == 0, f"Workflow failed: {result.stderr}"
