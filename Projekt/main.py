import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.dialogs.dialogs import Messagebox
from ttkbootstrap.scrolled import ScrolledFrame
from tkinter import filedialog
from PIL import Image, ImageTk
from hashlib import sha256
from datetime import datetime
import re
from user import User
from task import Task

users = []
user_id = None


class RegisterPage(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        options = {"pady": 5, "anchor": 'center'}
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

        self.registerButton = ttk.Button(self, text="Sign Up", command=self.create_user)
        self.registerButton.pack(**options)

        self.loginShiftLabel = ttk.Label(self, text="Do you have an account?")
        self.loginShiftLabel.pack()
        self.loginShiftButton = ttk.Button(self, text='Sign in', command=lambda: app.show_frame("LoginPage"), bootstyle='link')
        self.loginShiftButton.pack()

    def create_user(self):
        global users
        l_pattern = "(?=.*?[a-z])(?=.*?[A-Z])"
        p_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,40}$"

        if not re.search(l_pattern, self.login.get()):
            return Messagebox.show_info(title='Validation', message='Login must contain any uppercase and lowercase character')

        if [True] == [user.login == self.login.get() for user in users]:
            return Messagebox.show_info(title='Error', message='The user with this login already exists')

        if not re.search(p_pattern, self.password.get()):
            return Messagebox.show_info(title='Validation', message='Password must contain:\n'
                                                        '-At least one special character\n'
                                                        '-At least one number\n'
                                                        '-At least one uppercase and lowercase character\n'
                                                        '-At the minimum 8 characters')

        if not self.password.get() == self.cpassword.get():
            return Messagebox.show_info(title='Validation', message='Password must be same as confirm password')

        hashed_passwd = sha256(self.password.get().encode('utf-8')).hexdigest()
        user = User(self.login.get(), hashed_passwd)
        users.append(user)
        Messagebox.show_info(parent=self, title="UserInfo", message="The user was successfully created")
        app.show_frame("LoginPage")


class LoginPage(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        options = {"pady": 5, "anchor": 'center'}
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

        self.loginShiftLabel = ttk.Label(self, text="Need an account?")
        self.loginShiftLabel.pack()
        self.loginShiftButton = ttk.Button(self, text='Sign up', command=lambda: app.show_frame("RegisterPage"), bootstyle='link')
        self.loginShiftButton.pack()

    def checklogin(self):
        login = self.login.get()
        hashed_passwd = sha256(self.password.get().encode('utf-8')).hexdigest()
        for id, user in enumerate(users):
            if user.login == login:
                if user.password == hashed_passwd:
                    global user_id
                    user_id = id
                    return app.show_frame("Menu")
                else:
                    return Messagebox.show_error(title="Password", message="Wrong password!")
        return Messagebox.show_warning(title="Error", message="User doesn't exist")


class Menu(ttk.Frame):
    style = {"background": '#4e5d6c'}

    def __init__(self, parent):
        super().__init__(parent)

        self.old_password = tk.StringVar(value="")
        self.new_password = tk.StringVar(value="")
        self.confirm_new_password = tk.StringVar(value="")
        self.add_task_title = tk.StringVar(value="")

        self.rightframe = ttk.Frame(self, bootstyle='secondary')

    def load_left_frame(self):
        user = users[user_id]
        options = {"pady": 5}

        self.leftframe = ttk.Frame(self, width=200, height=480)
        self.leftframe.pack_propagate(0)
        self.leftframe.pack(side='left', anchor='nw', fill='both', expand=True)

        self.img = Image.open(user.icon).resize((40, 40))
        self.img_tk = ImageTk.PhotoImage(self.img)

        profile_icon = ttk.Button(self.leftframe, image=self.img_tk, bootstyle='link', command=self.add_icon)
        profile_icon.pack(**options)

        namelabel = ttk.Label(self.leftframe, text=user.login)
        namelabel.pack()

        add_task = ttk.Button(self.leftframe, text="Add Task", bootstyle='link', command=self.add_task)
        add_task.pack(**options)

        my_task = ttk.Button(self.leftframe, text="MyTasks", bootstyle='link', command=self.my_tasks)
        my_task.pack(**options)

        completed_task = ttk.Button(self.leftframe, text="Completed", bootstyle='link', command=self.completed)
        completed_task.pack(**options)

        settings = ttk.Button(self.leftframe, text='Settings', bootstyle='link', command=self.settings)
        settings.pack(side='bottom', **options)

        logout = ttk.Button(self.leftframe, text='Logout', bootstyle='link', command=self.logout)
        logout.pack(side='bottom', **options)

    def add_icon(self):
        filetypes = (('jpg files', '*.jpg'), ('png files', '*.png'), ('jpeg files', '*.jpeg'))
        path = filedialog.askopenfilename(title='Pick a picture', initialdir='/', filetypes=filetypes)
        if path:
            user = users[user_id]
            user.icon = path
            self.leftframe.destroy()
            self.rightframe.destroy()
            self.load_left_frame()

    def my_tasks(self):
        self.rightframe.destroy()
        self.rightframe = ttk.Frame(self, bootstyle='secondary', width=654, height=480)
        self.rightframe.pack_propagate(0)
        self.rightframe.pack(side='left', fill='both', expand=True)
        user = users[user_id]
        style = {"padx": 5, "pady": 5}
        scrolled_frame = ScrolledFrame(self.rightframe, autohide=True)
        scrolled_frame.pack(fill='both', expand=True)
        id_label = ttk.Label(scrolled_frame, text='ID')
        id_label.grid(column=0, row=0, **style)
        title_label = ttk.Label(scrolled_frame, text='Title')
        title_label.grid(column=1, row=0, **style)
        date_label = ttk.Label(scrolled_frame, text='Date')
        date_label.grid(column=2, row=0, **style)

        for id, task in enumerate(user.tasks):
            if not task.taskFinished:
                id_label= ttk.Label(scrolled_frame, text=id+1)
                id_label.grid(column=0, row=id+1, **style)
                title_label = ttk.Label(scrolled_frame, text=task.title)
                title_label.grid(column=1, row=id+1, **style)
                date_label = ttk.Label(scrolled_frame, text=task.taskDate)
                date_label.grid(column=2, row=id+1, **style)
                description_button = ttk.Button(scrolled_frame, text='Description', command=lambda: print(description_button.winfo_id()))
                description_button.grid(column=3, row=id+1, **style)
                complete_button = ttk.Button(scrolled_frame, text='Complete', bootstyle='success')
                complete_button.grid(column=4, row=id+1, **style)
                delete_button = ttk.Button(scrolled_frame, text='Delete', bootstyle='danger')
                delete_button.grid(column=5, row=id+1, **style)





    def completed(self):
        pass

    def settings(self):
        self.rightframe.destroy()
        self.rightframe = ttk.Frame(self, bootstyle='secondary', width=654, height=480)
        self.rightframe.pack_propagate(0)
        self.rightframe.pack(side='left', fill='both', expand=True)

        change_label = ttk.Label(self.rightframe, text='Change password', font=('Helvetica', 20), **self.style)
        change_label.pack()

        old_password_label = ttk.Label(self.rightframe, text='Old password', **self.style)
        old_password_label.pack(pady=5)
        self.old_password_entry = ttk.Entry(self.rightframe, textvariable=self.old_password, show='*')
        self.old_password_entry.pack()

        new_password_label = ttk.Label(self.rightframe, text='New password', **self.style)
        new_password_label.pack(pady=5)
        self.new_password_entry = ttk.Entry(self.rightframe, textvariable=self.new_password, show='*')
        self.new_password_entry.pack()

        confirm_new_password_label = ttk.Label(self.rightframe, text='Confirm password', **self.style)
        confirm_new_password_label.pack(pady=5)
        self.confirm_new_password_entry = ttk.Entry(self.rightframe, textvariable=self.confirm_new_password, show='*')
        self.confirm_new_password_entry.pack()

        save_button = ttk.Button(self.rightframe, text='Save', command=self.change_password)
        save_button.pack(pady=5)

    def change_password(self):
        user = users[user_id]
        p_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,40}$"
        old_pass = sha256(self.old_password.get().encode('utf-8')).hexdigest()
        if old_pass != user.password:
            return Messagebox.show_error(title="Old password", message="Wrong password!")

        if not re.search(p_pattern, self.new_password.get()):
            return Messagebox.show_info(title='Validation', message='Password must contain:\n'
                                                        '-At least one special character\n'
                                                        '-At least one number\n'
                                                        '-At least one uppercase and lowercase character\n'
                                                        '-At the minimum 8 characters')
        if self.new_password.get() != self.confirm_new_password.get():
            return Messagebox.show_info(title='Validation', message='Password must be same as confirm password')

        new_pass = sha256(self.new_password.get().encode('utf-8')).hexdigest()
        user.password = new_pass
        self.new_password_entry.delete(0, "end")
        self.old_password_entry.delete(0, "end")
        self.confirm_new_password_entry.delete(0, "end")
        return Messagebox.show_info(parent=self, title="Password Info", message="Password was successfully changed")

    def add_task(self):
        self.rightframe.destroy()
        self.rightframe = ttk.Frame(self, bootstyle='secondary', width=654, height=480)
        self.rightframe.pack_propagate(0)
        self.rightframe.pack(side='left', fill='both', expand=True)

        title_label = ttk.Label(self.rightframe, text='Title', **self.style)
        title_label.pack(pady=5)

        title_entry = ttk.Entry(self.rightframe, textvariable=self.add_task_title)
        title_entry.pack()

        description_label = ttk.Label(self.rightframe, text='Description', **self.style)
        description_label.pack(pady=5)

        self.description_text = tk.Text(self.rightframe, height=20)
        self.description_text.pack()

        add_button = ttk.Button(self.rightframe, text='Add', command=self.add)
        add_button.pack(pady=5)

    def add(self):
        user = users[user_id]
        task = Task(self.add_task_title.get(), self.description_text.get("1.0", "end-1c"))
        user.tasks.append(task)

    def logout(self):
        self.leftframe.destroy()
        self.rightframe.destroy()
        app.show_frame("LoginPage")


class App(ttk.Window):

    def __init__(self):
        super().__init__(themename='superhero')

        self.geometry('854x480')
        self.title('Projekt')
        self.position_center()
        self.resizable(False, False)

        self.container = ttk.Frame(self)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (RegisterPage, LoginPage, Menu):
            page_name = F.__name__
            frame = F(parent=self.container)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("RegisterPage")

    def show_frame(self, name):
        frame = self.frames[name]
        if name == "Menu":
            self.container.pack(side="left", anchor="nw", fill='y')
            frame.load_left_frame()
        else:
            self.container.pack(anchor='center', expand=True)
        frame.tkraise()


if __name__ == "__main__":
    app = App()
    app.mainloop()
