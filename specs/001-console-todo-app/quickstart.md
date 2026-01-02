# Quickstart: In-Memory Python Console Todo App

## Prerequisites

- Python 3.10 or higher
- No external dependencies (uses stdlib only)

## Installation

Clone the repository and navigate to the project:

```bash
git clone <repo-url>
cd hackathon-2-evolution-of-todo
```

## Running the Application

### Option 1: Direct execution

```bash
python -m src.main
```

### Option 2: Using the launcher script

```bash
python scripts/run.py
```

## Usage Guide

### Add a task

```bash
python -m src.main add "Buy groceries" --description "Milk, eggs, bread"
```

### View all tasks

```bash
python -m src.main list
```

### View only pending tasks

```bash
python -m src.main list --status pending
```

### Mark a task as complete

```bash
python -m src.main complete 1
```

### Update a task

```bash
python -m src.main update 1 --title "Buy organic groceries"
```

### Delete a task

```bash
python -m src.main delete 1
```

### Get help

```bash
python -m src.main --help
python -m src.main add --help
```

## Testing

Run the full test suite:

```bash
pytest tests/ -v
```

Run specific test categories:

```bash
pytest tests/unit/        # Unit tests only
pytest tests/integration/ # Integration tests only
```

## Project Structure

```
src/
├── main.py              # CLI entry point
├── todo_controller.py   # Command handling
├── todo_service.py      # Business logic
├── todo_model.py        # Data models
└── exceptions.py        # Custom exceptions

tests/
├── unit/
│   ├── test_model.py
│   ├── test_service.py
│   └── test_controller.py
└── integration/
    └── test_cli.py
```

## Next Steps

After completing Phase I:
- Phase II: Add web API with FastAPI and persistent storage
- Phase III: Add AI-powered todo management
- See [plan.md](./plan.md) for full architecture
