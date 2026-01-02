#!/usr/bin/env python3
"""
Interactive Todo Application with Menu Options
This script provides an interactive menu-based todo application
where you can select options by number.
"""

from src.todo_service import TodoService
from src.exceptions import ValidationError, TaskNotFoundError


def display_menu():
    print("\n" + "="*40)
    print("TODO APPLICATION")
    print("="*40)
    print("1. Add Task")
    print("2. View Tasks")
    print("3. View Pending Tasks")
    print("4. View Completed Tasks")
    print("5. Mark Task as Complete")
    print("6. Update Task")
    print("7. Delete Task")
    print("8. Help")
    print("9. Exit")
    print("="*40)


def get_user_choice():
    try:
        choice = int(input("Enter your choice (1-9): "))
        return choice
    except ValueError:
        print("Invalid input! Please enter a number between 1-9.")
        return None


def add_task(service):
    print("\n--- Add New Task ---")
    title = input("Enter task title: ").strip()
    
    if not title:
        print("Error: Task title cannot be empty!")
        return
    
    description = input("Enter task description (optional): ").strip()
    
    try:
        task = service.add_task(title, description)
        print(f"Task added successfully! (ID: {task.id})")
    except ValidationError as e:
        print(f"Error: {e}")


def view_tasks(service, status=None):
    print("\n--- View Tasks ---")
    print("1. View all tasks")
    print("2. View specific task by ID")

    try:
        choice = int(input("Enter your choice (1-2): "))

        if choice == 1:
            # Show all tasks
            tasks = service.list_tasks(status)

            if not tasks:
                if status:
                    print(f"No {status} tasks found.")
                else:
                    print("No tasks found. Add some tasks first!")
                return

            # Print header
            print(f"{'ID':<4} | {'Status':<10} | {'Title':<30} | {'Description'}")
            print("-" * 70)

            # Print tasks
            for task in tasks:
                title = task.title[:25] + "..." if len(task.title) > 25 else task.title
                desc = task.description[:20] + "..." if len(task.description) > 20 else task.description
                print(f"{task.id:<4} | {task.status:<10} | {title:<30} | {desc}")

        elif choice == 2:
            # View specific task by ID
            task_id = int(input("Enter task ID to view: "))
            task = service.get_task(task_id)

            if task:
                print(f"\nTask Details (ID: {task.id}):")
                print(f"Status: {task.status}")
                print(f"Title: {task.title}")
                print(f"Description: {task.description}")
                print(f"Created: {task.created_at}")
                print(f"Updated: {task.updated_at}")
            else:
                print(f"Error: Task with ID {task_id} not found!")
        else:
            print("Invalid choice! Please enter 1 or 2.")

    except ValueError:
        print("Invalid input! Please enter a number.")
    except Exception as e:
        print(f"Error: {e}")


def mark_complete(service):
    print("\n--- Mark Task as Complete ---")
    try:
        task_id = int(input("Enter task ID to mark as complete: "))
        task = service.complete_task(task_id)
        print(f"Task {task.id} marked as complete!")
    except ValueError:
        print("Error: Please enter a valid task ID (number)!")
    except TaskNotFoundError as e:
        print(f"Error: {e}")


def update_task(service):
    print("\n--- Update Task ---")
    try:
        task_id = int(input("Enter task ID to update: "))
        
        # Get current task to show current values
        current_task = service.get_task(task_id)
        if not current_task:
            print(f"Error: Task with ID {task_id} not found!")
            return
        
        print(f"Current title: {current_task.title}")
        new_title = input("Enter new title (or press Enter to keep current): ").strip()
        
        print(f"Current description: {current_task.description}")
        new_description = input("Enter new description (or press Enter to keep current): ").strip()
        
        # Use current values if user didn't provide new ones
        title = new_title if new_title else current_task.title
        description = new_description if new_description else current_task.description
        
        updated_task = service.update_task(task_id, title, description)
        print(f"Task {updated_task.id} updated successfully!")
        
    except ValueError:
        print("Error: Please enter a valid task ID (number)!")
    except ValidationError as e:
        print(f"Error: {e}")
    except TaskNotFoundError as e:
        print(f"Error: {e}")


def delete_task(service):
    print("\n--- Delete Task ---")
    try:
        task_id = int(input("Enter task ID to delete: "))
        result = service.delete_task(task_id)
        if result:
            print(f"Task {task_id} deleted successfully!")
        else:
            print(f"Error: Task with ID {task_id} not found!")
    except ValueError:
        print("Error: Please enter a valid task ID (number)!")


def show_help():
    print("\n--- Help ---")
    print("This is a simple todo application that helps you manage your tasks.")
    print("\nFeatures:")
    print("- Add new tasks with titles and descriptions")
    print("- View all tasks, or filter by status (pending/complete)")
    print("- Mark tasks as complete when finished")
    print("- Update task details")
    print("- Delete tasks you no longer need")
    print("\nTips:")
    print("- Each task has a unique ID that's assigned automatically")
    print("- You can only update or delete tasks that exist")
    print("- Completed tasks can't be 'uncompleted' in this version")


def main():
    print("Welcome to the Interactive Todo Application!")
    
    # Create a single instance of TodoService to maintain state across commands
    service = TodoService()
    
    while True:
        display_menu()
        choice = get_user_choice()
        
        if choice == 1:
            add_task(service)
        elif choice == 2:
            view_tasks(service)
        elif choice == 3:
            view_tasks(service, "pending")
        elif choice == 4:
            view_tasks(service, "complete")
        elif choice == 5:
            mark_complete(service)
        elif choice == 6:
            update_task(service)
        elif choice == 7:
            delete_task(service)
        elif choice == 8:
            show_help()
        elif choice == 9:
            print("Thank you for using the Todo Application. Goodbye!")
            break
        else:
            if choice is not None:  # Only show error if input was a number but not in range
                print("Invalid choice! Please enter a number between 1-9.")
        
        # Pause before showing menu again
        if choice != 9:
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()