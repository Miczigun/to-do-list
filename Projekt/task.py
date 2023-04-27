from datetime import datetime

class Task:

    def __init__(self, title, description):
        self.title = title
        self.description = description
        self.taskDate = datetime.now()
        self.taskFinished = False

