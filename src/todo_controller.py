"""CLI controller for todo application."""

import argparse
from typing import Optional

from src.todo_service import TodoService
from src.exceptions import TodoError


class TodoController:
    """Handles CLI command parsing and execution."""

    def __init__(self):
        self.service = TodoService()

    def run(self, args: Optional[list[str]] = None) -> int:
        """Parse and execute CLI commands."""
        parser = self._create_parser()
        parsed = parser.parse_args(args)

        if hasattr(parsed, 'func'):
            try:
                return parsed.func(parsed)
            except TodoError as e:
                print(f"Error: {e}")
                return 1
            except Exception as e:
                print(f"Error: {e}")
                return 1
        else:
            parser.print_help()
            return 0

    def _create_parser(self) -> argparse.ArgumentParser:
        """Create the argument parser with all commands."""
        parser = argparse.ArgumentParser(
            prog="todo",
            description="A simple console-based todo application"
        )

        subparsers = parser.add_subparsers(dest="command", help="Available commands")

        # add command
        add_parser = subparsers.add_parser("add", help="Add a new task")
        add_parser.add_argument("title", help="Task title")
        add_parser.add_argument("--description", "-d", help="Task description", default="")
        add_parser.set_defaults(func=self._cmd_add)

        # list command
        list_parser = subparsers.add_parser("list", help="List all tasks")
        list_parser.add_argument("--status", "-s", choices=["pending", "complete"],
                                 help="Filter by status")
        list_parser.set_defaults(func=self._cmd_list)

        # complete command
        complete_parser = subparsers.add_parser("complete", help="Mark a task as complete")
        complete_parser.add_argument("task_id", type=int, help="Task ID to mark complete")
        complete_parser.set_defaults(func=self._cmd_complete)

        # update command
        update_parser = subparsers.add_parser("update", help="Update a task")
        update_parser.add_argument("task_id", type=int, help="Task ID to update")
        update_parser.add_argument("--title", "-t", help="New task title")
        update_parser.add_argument("--description", "-d", help="New task description")
        update_parser.set_defaults(func=self._cmd_update)

        # delete command
        delete_parser = subparsers.add_parser("delete", help="Delete a task")
        delete_parser.add_argument("task_id", type=int, help="Task ID to delete")
        delete_parser.set_defaults(func=self._cmd_delete)

        return parser

    def _cmd_add(self, args: argparse.Namespace) -> int:
        """Handle 'add' command."""
        task = self.service.add_task(args.title, args.description)
        print(f"Task added successfully (ID: {task.id})")
        return 0

    def _cmd_list(self, args: argparse.Namespace) -> int:
        """Handle 'list' command."""
        tasks = self.service.list_tasks(args.status)

        if not tasks:
            print("No tasks found. Add one with: todo add \"Your task\"")
            return 0

        # Print header
        print(f"{'ID':<4} | {'Status':<10} | {'Title'}")
        print("-" * 50)

        # Print tasks
        for task in tasks:
            title = task.title[:40] + "..." if len(task.title) > 40 else task.title
            print(f"{task.id:<4} | {task.status:<10} | {title}")

        return 0

    def _cmd_complete(self, args: argparse.Namespace) -> int:
        """Handle 'complete' command."""
        task = self.service.complete_task(args.task_id)
        print(f"Task {task.id} marked as complete")
        return 0

    def _cmd_update(self, args: argparse.Namespace) -> int:
        """Handle 'update' command."""
        task = self.service.update_task(args.task_id, args.title, args.description)
        print(f"Task {task.id} updated successfully")
        return 0

    def _cmd_delete(self, args: argparse.Namespace) -> int:
        """Handle 'delete' command."""
        result = self.service.delete_task(args.task_id)
        if result:
            print(f"Task {args.task_id} deleted successfully")
            return 0
        else:
            print(f"Error: Task with ID {args.task_id} not found")
            return 1
