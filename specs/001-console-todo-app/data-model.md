# Data Model: In-Memory Python Console Todo App

## Entities

### Task

Represents a single todo item.

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `id` | int | Yes | Auto-increment | Unique identifier, starts at 1, never reused |
| `title` | str | Yes | - | Short description of the task (1+ characters) |
| `description` | str | No | `""` | Optional detailed notes |
| `status` | str | No | `"pending"` | Either `"pending"` or `"complete"` |
| `created_at` | datetime | Yes | Auto-generated | UTC timestamp of creation |
| `updated_at` | datetime | Yes | Auto-generated | UTC timestamp of last modification |

#### Status Values

| Status | Description |
|--------|-------------|
| `pending` | Task is not yet completed (default) |
| `complete` | Task has been marked done |

#### State Transitions

```
pending --[mark_complete]--> complete
complete --[reopen]--------> pending (if implemented)
```

Note: The spec only requires marking complete, not reopening.

---

### TaskCollection

Manages all Task entities in memory.

| Field/Method | Type | Description |
|--------------|------|-------------|
| `_tasks` | dict[int, Task] | Internal storage: ID → Task mapping |
| `_next_id` | int | Next available ID for new tasks |

#### CRUD Operations

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `create(title, description)` | title: str, description: str | Task | Creates new task with auto-generated ID |
| `get_by_id(id)` | id: int | Task \| None | Retrieves task by ID |
| `get_all()` | - | list[Task] | Returns all tasks sorted by creation order |
| `get_by_status(status)` | status: str | list[Task] | Filters tasks by status |
| `update(id, title, description)` | id: int, title: str, description: str | Task | Updates task fields |
| `delete(id)` | id: int | bool | Removes task, returns True if existed |
| `mark_complete(id)` | id: int | Task | Changes status to "complete" |

---

## Validation Rules

### Task Title

- Must be non-empty (1+ characters after stripping whitespace)
- No maximum length enforced (terminal width handles display)

### Task Description

- Optional, defaults to empty string
- No maximum length enforced

### Task ID

- Must be positive integer
- Must exist in collection for operations (get, update, delete, mark_complete)

---

## Data Flow

```
User Input (CLI)
    ↓
Controller (parse args, validate)
    ↓
Service (business logic)
    ↓
Storage (TaskCollection)
    ↓
Response (CLI output)
```

---

## Python Implementation Preview

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    status: str = "pending"
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def mark_complete(self):
        self.status = "complete"
        self.updated_at = datetime.utcnow()

@dataclass
class TaskCollection:
    _tasks: dict[int, Task] = field(default_factory=dict)
    _next_id: int = 1

    def create(self, title: str, description: str = "") -> Task:
        task = Task(id=self._next_id, title=title, description=description)
        self._tasks[self._next_id] = task
        self._next_id += 1
        return task

    def get_by_id(self, id: int) -> Optional[Task]:
        return self._tasks.get(id)

    def get_all(self) -> list[Task]:
        return sorted(self._tasks.values(), key=lambda t: t.id)
```

---

## Extensibility Notes

The data model is designed to evolve:
- **Phase II**: Replace `TaskCollection` with SQLModel database-backed storage
- **Phase III**: Add `user_id` field for multi-user support
- The dataclass structure can be extended with additional fields without breaking existing code
