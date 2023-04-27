import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.dialogs.dialogs import Messagebox
import hashlib
import re
from user import User

users = []
user_id = None

class RegisterPage(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        options = {"pady": 5, "anchor":'center', "expand":True}
        self.login = tk.StringVar()
        self.password = tk.StringVar()
        self.cpassword = tk.StringVar()

        self.loginLabel = ttk.Label(self, text="Username")
        self.loginLabel.pack(**options)
        self.loginEntry = ttk.Entry(self, textvariable=self.login, width=30)
        self.loginEntry.pack()
        self.loginEntry.focus()

        self.passwordLabel = ttk.Label(self, text="Password")
        self.passwordLabel.pack(**options)
        self.passwordEntry = ttk.Entry(self, textvariable=self.password, show="*", width=30)
        self.passwordEntry.pack()

        self.passwordLabel = ttk.Label(self, text="Confirm Password")
        self.passwordLabel.pack(**options)
        self.passwordEntry = ttk.Entry(self, textvariable=self.cpassword, show="*", width=30)
        self.passwordEntry.pack()

        self.loginButton = ttk.Button(self, text="Sign Up", command=self.create_user)
        self.loginButton.pack(**options)

    def create_user(self):
        l_pattern = "(?=.*?[a-z])(?=.*?[A-Z])"
        p_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
        if not re.search(l_pattern,self.login.get()):
            return Messagebox.show_info(title='Validation', message='Login must contain any uppercase and lowercase character')
        if not re.search(p_pattern, self.password.get()):
            return Messagebox.show_info(title='Validation', message='Password must contain:\n'
                                                        '-At least one special character\n'
                                                        '-At least one number\n'
                                                        '-At least one uppercase and lowercase character\n'
                                                        '-At the minimum 8 characters')
        if not self.password.get() == self.cpassword.get():
            return Messagebox.show_info(title='Validation', message='Password must be same as confirm password')

        hashed_passwd = hashlib.sha256(self.password.get().encode('utf-8')).hexdigest()
        user = User(self.login.get(), hashed_passwd)
        users.append(user)
        Messagebox.show_info(parent=self, title="UserInfo" ,message="The user was successfully created")
        app.show_frame("LoginPage")


class LoginPage(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        options = {"padx": 0, "pady": 5}
        self.login = tk.StringVar(value="")
        self.password = tk.StringVar(value="")
        self.loginLabel = ttk.Label(self, text="Username")
        self.loginLabel.pack()
        self.loginEntry = ttk.Entry(self, textvariable=self.login, width=30)
        self.loginEntry.pack(**options)
        self.loginEntry.focus()

        self.passwordLabel = ttk.Label(self, text="Password")
        self.passwordLabel.pack()
        self.passwordEntry = ttk.Entry(self, textvariable=self.password, show="*", width=30)
        self.passwordEntry.pack(**options)

        self.loginButton = ttk.Button(self, text="Sign In", command=self.checklogin)
        self.loginButton.pack(**options)

    def checklogin(self):
        login = self.login.get()
        hashed_passwd = hashlib.sha256(self.password.get().encode('utf-8')).hexdigest()
        for id, user in enumerate(users):
            if user.login == login:
                if user.password == hashed_passwd:
                    user_id = id
                    return app.show_frame("Menu")
                else:
                    return Messagebox.show_error(title="Password", message="Wrong password!")
        return Messagebox.show_warning(title="Error", message="User doesn't exist")

class Menu(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.leftframe = ttk.Frame(self, width=250)
        self.leftframe.pack(fill='x', anchor='nw')
        self.rightframe = ttk.Frame(self)
        self.rightframe.pack(fill='x')
        self.leftlabel = ttk.Label(self.leftframe, text="Miczi")
        self.leftlabel.pack(side='left')




        
        
        
class App(ttk.Window):

    def __init__(self):
        super().__init__(themename='superhero')

        self.geometry('854x500')
        self.title('Projekt')
        self.position_center()

        self.container = ttk.Frame(self)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.pack()

        self.frames = {}
        for F in (RegisterPage, LoginPage, Menu):
            page_name = F.__name__
            frame = F(parent=self.container)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("RegisterPage")

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()



if __name__ == "__main__":
    app = App()
    app.mainloop()
