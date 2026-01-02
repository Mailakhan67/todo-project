# CLI Interface Contract

## Usage

```bash
python -m todo [command] [options]
```

## Global Options

| Option | Description |
|--------|-------------|
| `--help`, `-h` | Show help message and exit |
| `--version` | Show version (if implemented) |

## Commands

### add

Add a new task to the todo list.

```bash
python -m todo add "Task title" [--description "Optional description"]
```

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `title` | string | Yes | Task title (1+ characters) |
| `--description`, `-d` | string | No | Optional task description |

**Success Output**:
```
Task added successfully (ID: 1)
```

**Error Cases**:
- Empty title: `Error: Task title cannot be empty`

---

### list

Display all tasks, optionally filtered.

```bash
python -m todo list [--status pending|complete]
```

| Option | Description |
|--------|-------------|
| `--status`, `-s` | Filter by status: `pending`, `complete`, or omit for all |

**Success Output** (example with tasks):
```
ID  | Status    | Title
----|-----------|------------------
1   | pending   | Buy groceries
2   | complete  | Call mom
```

**Empty State**:
```
No tasks found. Add one with: todo add "Your task"
```

---

### complete

Mark a task as complete.

```bash
python -m todo complete <task_id>
```

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `task_id` | integer | Yes | Task ID to mark complete |

**Success Output**:
```
Task 1 marked as complete
```

**Error Cases**:
- Invalid ID: `Error: Task with ID 99 not found`
- Already complete: `Task 1 is already complete`

---

### update

Update a task's title and/or description.

```bash
python -m todo update <task_id> [--title "New title"] [--description "New description"]
```

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `task_id` | integer | Yes | Task ID to update |
| `--title`, `-t` | string | No | New task title |
| `--description`, `-d` | string | No | New task description |

**Success Output**:
```
Task 1 updated successfully
```

**Error Cases**:
- Invalid ID: `Error: Task with ID 99 not found`
- Empty title: `Error: Task title cannot be empty`

---

### delete

Remove a task from the list.

```bash
python -m todo delete <task_id>
```

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `task_id` | integer | Yes | Task ID to delete |

**Success Output**:
```
Task 1 deleted successfully
```

**Error Cases**:
- Invalid ID: `Error: Task with ID 99 not found`

---

### help

Show help for all commands.

```bash
python -m todo help
```

**Output**: Full usage documentation as shown in Usage section.

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error (invalid input, task not found, etc.) |

---

## Error Message Format

All errors follow this format:

```
Error: <actionable message>
```

Examples:
- `Error: Task title cannot be empty`
- `Error: Task with ID 99 not found`
- `Error: Task 1 is already complete`
