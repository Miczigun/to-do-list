from datetime import datetime


class Task:

    def __init__(self, title, description):
        self.title = title
        self.description = description
        self.taskDate = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.taskFinished = False
        self.taskDateFinish = None
