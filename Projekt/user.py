from task import Task

class User():

    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.tasks = []
        self.icon = "profile.jpg"


