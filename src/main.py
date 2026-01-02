"""Main entry point for the todo CLI application."""

import sys

from src.todo_controller import TodoController


def main() -> int:
    """Entry point for the todo application."""
    controller = TodoController()
    return controller.run(sys.argv[1:])


if __name__ == "__main__":
    sys.exit(main())
