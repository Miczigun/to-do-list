from task import Task

class User():

    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.tasks = []
        self.icon = "profile.jpg"

    def json_object(self):
        return {"login": self.login,
                "password": self.password,
                "tasks": [task.__dict__ for task in self.tasks],
                "icon": self.icon}




