
class User():
    def __init__(self, login, password):
        self.login = login
        self.password = password

    def getLogin(self):
        return self.login

    def getPassword(self):
        return self.password
