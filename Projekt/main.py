import tkinter as tk
import ttkbootstrap as ttk
from tkinter import ttk

class RegisterPage(ttk.Frame):

    def __init__(self, parent):
        super().__init__()
        options = {"padx": 0, "pady": 5}
        self.login = tk.StringVar()
        self.password = tk.StringVar()
        self.cpassword = tk.StringVar()

        self.loginLabel = ttk.Label(self, text="Username")
        self.loginLabel.pack()
        self.loginEntry = ttk.Entry(self, textvariable=self.login, width="30")
        self.loginEntry.pack(**options)
        self.loginEntry.focus()

        self.passwordLabel = ttk.Label(self, text="Password")
        self.passwordLabel.pack()
        self.passwordEntry = ttk.Entry(self, textvariable=self.password, show="*", width="30")
        self.passwordEntry.pack(**options)

        self.passwordLabel = ttk.Label(self, text="Confirm Password")
        self.passwordLabel.pack()
        self.passwordEntry = ttk.Entry(self, textvariable=self.cpassword, show="*", width="30")
        self.passwordEntry.pack(**options)

        self.loginButton = ttk.Button(self, text="Sign Up",)
        self.loginButton.pack(**options)

class LoginPage(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        options = {"padx": 0, "pady": 5}
        self.login = tk.StringVar()
        self.password = tk.StringVar()
        print(self.password)
        self.loginLabel = ttk.Label(self, text="Username")
        self.loginLabel.pack()
        self.loginEntry = ttk.Entry(self, textvariable=self.login, width="30")
        self.loginEntry.pack(**options)
        self.loginEntry.focus()

        self.passwordLabel = ttk.Label(self, text="Password")
        self.passwordLabel.pack()
        self.passwordEntry = ttk.Entry(self, textvariable=self.password, show="*", width="30")
        self.passwordEntry.pack(**options)

        self.loginButton = ttk.Button(self, text="Sign In", command=self.checklogin)
        self.loginButton.pack(**options)

    def checklogin(self):
        print(self.login.get())
        print(b'self.password.get()')
        
        
        
class App(tk.Tk):

    def __init__(self):
        super().__init__()

        self.geometry('854x480')
        self.title('Projekt')
        self.resizable(False,False)

        RegisterPage(self).place(relx=0.5 , rely=0.4, anchor="center")


if __name__ == "__main__":
    app = App()
    app.mainloop()