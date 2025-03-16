import json
import os
import argparse
from datetime import datetime


def load_tasks():
    with open('tasklist.json', 'w') as file:
        json.dump([], file)
    return []

    with open('tasklist.json', 'r') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []














#Add, Update, Delete
