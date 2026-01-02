# Tasks: In-Memory Python Console Todo App

**Feature**: 001-console-todo-app | **Input**: Design documents from `/specs/001-console-todo-app/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/cli-interface.md
**Tests**: Tests included per spec requirements (constitution mandates testing)

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure per implementation plan: `src/`, `tests/`, `tests/unit/`, `tests/integration/`
- [x] T002 Initialize pytest in project root with configuration in pyproject.toml or setup.cfg
- [x] T003 [P] Configure Python path resolution for clean imports (ensure src/ is in PYTHONPATH)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Create custom exceptions module in `src/exceptions.py` with TaskNotFoundError, ValidationError, DuplicateTaskError
- [x] T005 [P] Create Task data class in `src/todo_model.py` with id, title, description, status, created_at, updated_at fields
- [x] T006 [P] Create TaskCollection storage class in `src/todo_model.py` with all CRUD methods (create, get_by_id, get_all, get_by_status, update, delete, mark_complete)

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Add and View Todos (Priority: P1) MVP

**Goal**: Users can add new tasks with title/description and view all tasks

**Independent Test**: Add tasks and verify they appear in list with correct ID, title, description, status

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T007 [P] [US1] Unit test for Task model in `tests/unit/test_model.py`: test_task_creation, test_task_default_values
- [x] T008 [P] [US1] Unit test for TaskCollection.get_all in `tests/unit/test_model.py`: test_get_all_returns_sorted_tasks
- [x] T009 [P] [US1] Contract test for `add` command output format in `tests/integration/test_cli.py`: test_add_command_success
- [x] T010 [P] [US1] Contract test for `list` command output format in `tests/integration/test_cli.py`: test_list_command_shows_all_tasks
- [x] T011 [P] [US1] Integration test for add+list workflow in `tests/integration/test_cli.py`: test_add_then_list_shows_new_task

### Implementation for User Story 1

- [x] T012 [US1] Implement TodoService class in `src/todo_service.py` with add and list methods
- [x] T013 [US1] Implement add command handler in `src/todo_controller.py`: parse `add "title" [--description "desc"]` arguments
- [x] T014 [US1] Implement list command handler in `src/todo_controller.py`: parse `list [--status pending|complete]` arguments
- [x] T015 [US1] Create main CLI entry point in `src/main.py` with argparse for all commands, help text
- [x] T016 [US1] Wire up add command to call TodoService.create and display success message "Task added successfully (ID: X)"
- [x] T017 [US1] Wire up list command to call TodoService.get_all and display formatted table with ID, Status, Title

**Checkpoint**: User Story 1 complete - users can add and view tasks

---

## Phase 4: User Story 2 - Mark Todos Complete (Priority: P1)

**Goal**: Users can mark pending tasks as complete

**Independent Test**: Mark a pending task as complete and verify status changes while remaining visible

### Tests for User Story 2

- [x] T018 [P] [US2] Unit test for TodoService.mark_complete in `tests/unit/test_service.py`: test_mark_complete_changes_status
- [x] T019 [P] [US2] Unit test for TodoService.mark_complete idempotency in `tests/unit/test_service.py`: test_mark_complete_already_complete_no_change
- [x] T020 [P] [US2] Contract test for `complete` command success in `tests/integration/test_cli.py`: test_complete_command_success
- [x] T021 [P] [US2] Contract test for `complete` command error - invalid ID in `tests/integration/test_cli.py`: test_complete_command_invalid_id
- [x] T022 [P] [US2] Contract test for `complete` command error - already complete in `tests/integration/test_cli.py`: test_complete_command_already_complete

### Implementation for User Story 2

- [x] T023 [US2] Add mark_complete method to TodoService in `src/todo_service.py`
- [x] T024 [US2] Implement complete command handler in `src/todo_controller.py`: parse `complete <task_id>` arguments, validate ID exists
- [x] T025 [US2] Wire up complete command to call TodoService.mark_complete and display "Task X marked as complete"

**Checkpoint**: User Story 2 complete - users can mark tasks complete

---

## Phase 5: User Story 3 - Update and Delete Todos (Priority: P2)

**Goal**: Users can modify task details and remove tasks from the list

**Independent Test**: Update a task's title and delete a task, verifying changes persist

### Tests for User Story 3

- [x] T026 [P] [US3] Unit test for TodoService.update in `tests/unit/test_service.py`: test_update_changes_title_and_description
- [x] T027 [P] [US3] Unit test for TodoService.delete in `tests/unit/test_service.py`: test_delete_removes_task
- [x] T028 [P] [US3] Unit test for TodoService.update validation in `tests/unit/test_service.py`: test_update_empty_title_raises_error
- [x] T029 [P] [US3] Contract test for `update` command success in `tests/integration/test_cli.py`: test_update_command_success
- [x] T030 [P] [US3] Contract test for `delete` command success in `tests/integration/test_cli.py`: test_delete_command_success
- [x] T031 [P] [US3] Contract test for `update` command error - invalid ID in `tests/integration/test_cli.py`: test_update_command_invalid_id
- [x] T032 [P] [US3] Contract test for `delete` command error - invalid ID in `tests/integration/test_cli.py`: test_delete_command_invalid_id

### Implementation for User Story 3

- [x] T033 [US3] Add update method to TodoService in `src/todo_service.py`
- [x] T034 [US3] Add delete method to TodoService in `src/todo_service.py`
- [x] T035 [US3] Implement update command handler in `src/todo_controller.py`: parse `update <task_id> [--title "new"] [--description "new"]`
- [x] T036 [US3] Implement delete command handler in `src/todo_controller.py`: parse `delete <task_id>`
- [x] T037 [US3] Wire up update command to call TodoService.update and display "Task X updated successfully"
- [x] T038 [US3] Wire up delete command to call TodoService.delete and display "Task X deleted successfully"

**Checkpoint**: User Story 3 complete - users can update and delete tasks

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T039 [P] Add comprehensive error handling for all commands: empty title validation, invalid ID handling
- [x] T040 [P] Add help command implementation in `src/todo_controller.py` showing all commands
- [x] T041 [P] Enhance list command with `--status` filter option per CLI contract
- [x] T042 [P] Run all integration tests from `tests/integration/test_cli.py` to validate full CLI workflow
- [x] T043 Run quickstart.md validation: verify all 5 core operations (Add, View, Update, Delete, Mark Complete) work
- [x] T044 Final code cleanup: ensure consistent error message format "Error: <message>" per FR-008

---

## Dependencies & Execution Order

### Phase Dependencies

| Phase | Depends On | Blocks |
|-------|------------|--------|
| Setup (1) | None | Foundational |
| Foundational (2) | Setup | All User Stories |
| User Story 1 (3) | Foundational | - |
| User Story 2 (4) | Foundational | - |
| User Story 3 (5) | Foundational | Polish |
| Polish (6) | All User Stories | - |

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories (TaskCollection provides all needed methods)
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories

### Within Each User Story

1. Tests (T007-T011, T018-T022, T026-T032) MUST be written and FAIL before implementation
2. Model tests first, then service tests, then contract/integration tests
3. Service implementation before controller
4. Controller handlers before main entry point wiring
5. Story complete before moving to next priority

---

## Parallel Execution Examples

### Phase 1: Setup
```bash
# T001, T002, T003 can run in parallel (different files)
```

### Phase 2: Foundational
```bash
# T004, T005, T006 can run in parallel (different files)
```

### User Story 1
```bash
# All tests T007-T011 can run in parallel
# T012, T013, T014 can run in parallel (different files)
# T015 depends on T013, T014 (needs handlers defined)
# T016, T017 depend on T012, T015 (needs service and entry point)
```

### User Story 2
```bash
# All tests T018-T022 can run in parallel
# T023 depends on T006 (TaskCollection.mark_complete must exist)
# T024 depends on T023 (service method needed)
# T025 depends on T024 (needs handler defined)
```

### User Story 3
```bash
# All tests T026-T032 can run in parallel
# T033, T034 depend on T006 (TaskCollection methods must exist)
# T035 depends on T033, T034 (service methods needed)
# T036 depends on T033, T034 (service methods needed)
# T037, T038 depend on T035, T036 (handlers defined)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test add and list operations work
5. Deploy/demo if ready - MVP delivers core value

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Polish phase → Final delivery
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (add + view)
   - Developer B: User Story 2 (mark complete)
   - Developer C: User Story 3 (update + delete)
3. Stories complete and integrate independently (TaskCollection provides all data access)

---

## Task Summary

| Category | Count |
|----------|-------|
| Setup | 3 |
| Foundational | 3 |
| User Story 1 | 11 |
| User Story 2 | 8 |
| User Story 3 | 13 |
| Polish | 6 |
| **Total** | **44** |

---

## Notes

- **[P]** tasks = different files, no dependencies
- **[Story]** label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- **Verify tests fail before implementing** - this is a constitution requirement
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
