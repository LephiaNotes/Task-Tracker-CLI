import json
import os
import argparse
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

console = Console()

task_file = 'tasklist.json'

def load_tasks():
    if not os.path.exists(task_file):
        with open(task_file, 'w') as file:
            json.dump([], file)
        return []
    

    with open(task_file, 'r') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []

def save_tasks(tasks):
    with open(task_file, 'w') as file:
        json.dump(tasks, file, indent = 4)

def get_next_id(tasks):
    return max([task['id'] for task in tasks], default = 0) + 1


def add_task(title, status = 'not done'):
    tasks = load_tasks()
    task_id = get_next_id(tasks)
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


    task = {
        'id': task_id,
        'title': title,
        'status': status,
        'created at': current_time,
        'updated at': current_time,
    }
    tasks.append(task)
    save_tasks(tasks)
    console.print(f'Task added successfully (ID: {task_id})')

def update_tasks(task_id, title = None, status = None):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            if title:
                task['title'] = title
            if status:
                task['status'] = status
            task ['updated at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            save_tasks(tasks)
            console.print(f" Task ID {task_id} updated.")
            return
    console.print(f'Task ID {task_id} not found.')

def mark_progress(task_id):
    update_tasks(task_id, status = 'In Progress')

def mark_done(task_id):
    update_tasks(task_id, status = 'Done')

def delete_task(task_id):
    tasks = load_tasks()
    tasks = [task for task in tasks if task['id'] != task_id]
    save_tasks(tasks)
    console.print(f'Task ID {task_id} deleted.')

def list_tasks(status = None):
    # List the tasks with a specific status
    tasks = load_tasks()
    if status:
        tasks = [task for task in tasks if task['status'] == status]
    if not tasks:
        console.print("[red]No tasks found.[/red]") 
        return
    

    table = Table(show_header = True, header_style = 'bold magenta')
    table.add_column('ID', style = 'dim', width = 5)
    table.add_column('Title', style = 'dim', width = 20)
    table.add_column('Status', style = 'dim', width = 15)
    table.add_column('Created At', style = 'dim', width = 20)
    table.add_column('Updated At', style = 'dim', width = 20)
    
    table.add_row(
        str(tasks['id']),
        tasks['title'],
        tasks['status'],
        tasks['created at'],
        tasks['updated at']
    )

    console.print(table)

def main():
    parser = argparse.ArgumentParser(description = 'Task Tracker CLI')
    subparsers = parser.add_subparsers(dest = 'command', help = 'Available commands')

    add_parser = subparsers.add_parser('add', help = 'Add a new task')
    add_parser.add_argument('title', type = str, help = 'Task title')

    update_parser = subparsers.add_parser('update', help = 'Update a task')
    update_parser.add_argument('id', type = int, help = 'Task ID')
    update_parser.add_argument('--title', type = str, help = 'Task title')
    update_parser.add_argument('--status', type = str, help = 'Task status')

    progress_parser = subparsers.add_parser('progress', help = 'Mark a task as In Progress')
    progress_parser.add_argument('id', type = int, help = 'Task ID')

    done_parser = subparsers.add_parser('done', help = 'Mark a task as Done')
    done_parser.add_argument('id', type = int, help = 'Task ID')

    delete_parser = subparsers.add_parser('delete', help = 'Delete a task')
    delete_parser.add_argument('id', type = int, help = 'Task ID')

    list_parser = subparsers.add_parser('list', help = 'List tasks')
    list_parser.add_argument('--status', type = str, help = 'Filter tasks by status')

    args = parser.parse_args()

    console.print('Task Tracker CLI', style = 'bold violet')
    console.print(
        "CLI-based task tracker developed using Python and Rich library."
    )

    if args.command == 'add':
        add_task(args.title)
    elif args.command == 'update':
        update_tasks(args.id, title = args.title, status = args.status)
    elif args.command == 'progress':
        mark_progress(args.id)
    elif args.command == 'done':
        mark_done(args.id)
    elif args.command == 'delete':
        delete_task(args.id)
    elif args.command == 'list':
        list_tasks(status = args.status)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()