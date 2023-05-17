from task import Task
from datetime import datetime

class User:

    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.tasks = []
        self.icon = r'images\profile.jpg'

    def json_object(self):
        return {"login": self.login,
                "password": self.password,
                "tasks": [task.__dict__ for task in self.tasks],
                "icon": self.icon}

    def load_data(self, data: dict):
        self.login = data["login"]
        self.password = data["password"]
        self.icon = data["icon"]
        for task in data["tasks"]:
            temp_task = Task("", "")
            temp_task.title = task["title"]
            temp_task.description = task["description"]
            temp_task.taskDate = datetime.strptime(task["taskDate"], "%d/%m/%Y %H:%M").strftime("%d/%m/%Y %H:%M")
            temp_task.taskFinished = task["taskFinished"]
            if task["taskFinished"]:
                temp_task.taskDateFinish = datetime.strptime(task["taskDateFinish"], "%d/%m/%Y %H:%M").strftime("%d/%m/%Y %H:%M")
            else:
                temp_task.taskDateFinish = None
            self.tasks.append(temp_task)

