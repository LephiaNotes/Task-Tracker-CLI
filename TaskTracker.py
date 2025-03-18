import json
import os
import argparse
from datetime import datetime

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
        json.dump(tasks, file)

def add_task(title, status = 'not done'):
    tasks = load_tasks()
    task = {
        'id': len(tasks) + 1,
        'title': title,
        'status': status,
        'created at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    tasks.append(task)
    save_tasks(tasks)

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
            return
    print(f'Task ID {task_id} not found.')

def delete_task(task_id):
    tasks = load_tasks()
    tasks = [task for task in tasks if task['id'] != task_id]
    save_tasks(tasks)

def list_tasks(status = None):
    tasks = load_tasks()
    if status:
        tasks = [task for task in tasks if task['status'] == status]
    for task in tasks:
        print(f"ID: {task['id']}, Title: {task['title']}, Status: {task['status']}, Created At: {task['created at']} Updated At: {task['updated at']}")

def main():











#Add, Update, Delete
