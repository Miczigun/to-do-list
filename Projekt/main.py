import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.dialogs.dialogs import Messagebox
from ttkbootstrap.scrolled import ScrolledFrame
from tkinter import filedialog
from PIL import Image, ImageTk
from hashlib import sha256
from datetime import datetime
import re
import json
import os
import shutil
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

        self.password_confirm_Label = ttk.Label(self, text="Confirm Password")
        self.password_confirm_Label.pack(**options)
        self.password_confirm_Entry = ttk.Entry(self, textvariable=self.cpassword, show="*", width=30)
        self.password_confirm_Entry.pack()

        self.registerButton = ttk.Button(self, text="Sign Up", command=self.create_user)
        self.registerButton.pack(**options)

        self.loginShiftLabel = ttk.Label(self, text="Do you have an account?")
        self.loginShiftLabel.pack()
        self.loginShiftButton = ttk.Button(self, text='Sign in',
                                           command=lambda: app.show_frame("LoginPage"), bootstyle='link')
        self.loginShiftButton.pack()

    def create_user(self):
        global users
        l_pattern = "(?=.*?[a-z])(?=.*?[A-Z])"
        p_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,40}$"

        if not re.search(l_pattern, self.login.get()):
            return Messagebox.show_info(title='Validation',
                                        message='Login must contain any uppercase and lowercase character')

        if any(self.login.get() == user.login for user in users):
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
        self.loginEntry.delete(0, 'end')
        self.passwordEntry.delete(0, 'end')
        self.password_confirm_Entry.delete(0, 'end')
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
        self.loginShiftButton = ttk.Button(self, text='Sign up', command=lambda: app.show_frame("RegisterPage"),
                                           bootstyle='link')
        self.loginShiftButton.pack()

    def checklogin(self):
        login = self.login.get()
        hashed_passwd = sha256(self.password.get().encode('utf-8')).hexdigest()
        for id, user in enumerate(users):
            if user.login == login:
                if user.password == hashed_passwd:
                    self.loginEntry.delete(0,'end')
                    self.passwordEntry.delete(0,'end')
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
        self.add_task_info = ""

        self.rightframe = ttk.Frame(self, bootstyle='secondary')

    def load_left_frame(self):
        user = users[user_id]
        options = {"pady": 5}

        self.leftframe = ttk.Frame(self, width=200, height=480)
        self.leftframe.pack_propagate(False)
        self.leftframe.pack(side='left', anchor='nw', fill='both', expand=True)

        if os.path.isfile(user.icon):
            self.img = Image.open(user.icon).resize((40, 40))
            self.img_tk = ImageTk.PhotoImage(self.img)
            profile_icon = ttk.Button(self.leftframe, image=self.img_tk, bootstyle='link', command=self.add_icon)
            profile_icon.pack(**options)
        else:
            profile_icon = ttk.Button(self.leftframe, bootstyle='link', command=self.add_icon, text="Add photo")
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
            destination_directory = os.getcwd() + "\images"
            filename = os.path.basename(path)
            if not os.path.isfile(os.path.join(destination_directory, filename)):
                shutil.copy(path, destination_directory)
            user.icon = fr'images\{filename}'
            self.leftframe.destroy()
            self.rightframe.destroy()
            self.load_left_frame()
            self.my_tasks()

    def my_tasks(self):
        self.rightframe.destroy()
        self.rightframe = ttk.Frame(self, bootstyle='secondary', width=654, height=480)
        self.rightframe.pack_propagate(0)
        self.rightframe.pack(side='left', fill='both', expand=True)
        user = users[user_id]
        style = {"padx": 5, "pady": 5}
        scrolled_frame = ScrolledFrame(self.rightframe, autohide=True, bootstyle='secondary', scrollheight=1500)
        scrolled_frame.pack(fill='both', expand=True)
        title_label = ttk.Label(scrolled_frame, text='Title', **self.style, font=('Helvetica', 15, 'bold'))
        title_label.grid(column=0, row=0, **style)
        date_label = ttk.Label(scrolled_frame, text='Date', **self.style, font=('Helvetica', 15, 'bold'))
        date_label.grid(column=1, row=0, **style)

        for id, task in enumerate(user.tasks):
            if not task.taskFinished:
                title_label = ttk.Label(scrolled_frame, text=task.title, **self.style)
                title_label.grid(column=0, row=id+1, **style)
                date_label = ttk.Label(scrolled_frame, text=task.taskDate, **self.style)
                date_label.grid(column=1, row=id+1, **style)
                description_button = ttk.Button(scrolled_frame, text='Description',
                                                command=lambda var=task.description:
                                                Messagebox.ok(title='Description', message=var))
                description_button.grid(column=2, row=id+1, **style)
                complete_button = ttk.Button(scrolled_frame, text='Complete', bootstyle='success',
                                             command=lambda var=id: self.complete_task(var))
                complete_button.grid(column=3, row=id+1, **style)
                delete_button = ttk.Button(scrolled_frame, text='Delete', bootstyle='danger',
                                           command=lambda var=id: self.delete_task(var))
                delete_button.grid(column=4, row=id+1, **style)

    def complete_task(self, id):
        user = users[user_id]
        user.tasks[id].taskFinished = True
        user.tasks[id].taskDateFinish = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.my_tasks()

    def completed(self):
        self.rightframe.destroy()
        self.rightframe = ttk.Frame(self, bootstyle='secondary', width=654, height=480)
        self.rightframe.pack_propagate(0)
        self.rightframe.pack(side='left', fill='both', expand=True)
        user = users[user_id]
        style = {"padx": 5, "pady": 5}
        scrolled_frame = ScrolledFrame(self.rightframe, autohide=True, bootstyle='secondary', scrollheight=1500)
        scrolled_frame.pack(fill='both', expand=True)
        title_label = ttk.Label(scrolled_frame, text='Title', **self.style, font=('Helvetica', 15, 'bold'))
        title_label.grid(column=0, row=0, **style)
        date_label = ttk.Label(scrolled_frame, text='Start Date', **self.style, font=('Helvetica', 15, 'bold'))
        date_label.grid(column=1, row=0, **style)
        finish_date_label = ttk.Label(scrolled_frame, text='Finish Date', **self.style, font=('Helvetica', 15, 'bold'))
        finish_date_label.grid(column=2, row=0, **style)

        for id, task in enumerate(user.tasks):
            if task.taskFinished:
                title_label = ttk.Label(scrolled_frame, text=task.title, **self.style)
                title_label.grid(column=0, row=id+1, **style)
                date_label = ttk.Label(scrolled_frame, text=task.taskDate, **self.style)
                date_label.grid(column=1, row=id+1, **style)
                finish_date_label = ttk.Label(scrolled_frame, text=task.taskDateFinish, **self.style)
                finish_date_label.grid(column=2, row=id+1, **style)
                description_button = ttk.Button(scrolled_frame, text='Description',
                                                command=lambda var=task.description:
                                                Messagebox.ok(title='Description', message=var))
                description_button.grid(column=3, row=id+1, **style)
                delete_button = ttk.Button(scrolled_frame, text='Delete', bootstyle='danger',
                                           command=lambda var=id: self.delete_task(var))
                delete_button.grid(column=4, row=id+1, **style)

    def delete_task(self, id):
        user = users[user_id]
        confirmation = Messagebox.yesno(title='Delete', message='Are you sure to delete this task?')
        if confirmation == 'Yes':
            del user.tasks[id]
            self.my_tasks()

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

        self.title_entry = ttk.Entry(self.rightframe, textvariable=self.add_task_title, width=40)
        self.title_entry.pack()

        description_label = ttk.Label(self.rightframe, text='Description', **self.style)
        description_label.pack(pady=5)

        self.description_text = tk.Text(self.rightframe, height=20)
        self.description_text.pack()

        add_button = ttk.Button(self.rightframe, text='Add', command=self.add)
        add_button.pack(pady=5)

        info_label = ttk.Label(self.rightframe, text=self.add_task_info, **self.style)
        info_label.pack(pady=5)

    def add(self):
        user = users[user_id]
        if self.add_task_title.get() == "" or self.description_text.get("1.0", "end-1c") == "":
            return Messagebox.show_info(title='Empty', message='Task must have title and description!')
        if len(self.add_task_title.get()) > 40:
            return Messagebox.show_info(title='Length', message='Title can not be longer than 40 characters')
        task = Task(self.add_task_title.get(), self.description_text.get("1.0", "end-1c"))
        user.tasks.append(task)
        self.add_task_info = f"Task {self.add_task_title.get()} was added"
        self.title_entry.delete(0, "end")
        self.description_text.delete("1.0", "end-1c")
        self.add_task()

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
        self.show_frame("LoginPage")

    def show_frame(self, name):
        frame = self.frames[name]
        if name == "Menu":
            self.container.pack(side="left", anchor="nw", fill='y')
            frame.load_left_frame()
            frame.my_tasks()
        else:
            self.container.pack(anchor='center', expand=True)
        frame.tkraise()


if __name__ == "__main__":
    try:
        with open('data.json', 'r') as f:
            json_load_data = json.loads(f.read())
            for data in json_load_data:
                temp_user = User("", "")
                temp_user.load_data(data)
                users.append(temp_user)
    except IOError:
        print("Error: could not read file data.json")

    app = App()
    app.mainloop()
    with open('data.json', 'w') as file:
        json_data = json.dumps([user.json_object() for user in users], indent=4)
        file.write(json_data)