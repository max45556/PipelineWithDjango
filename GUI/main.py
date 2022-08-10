import json
import os
import subprocess
import webbrowser
from datetime import *
import requests
import tkinter as tk  # python 3
from tkinter import font as tkfont, END, messagebox, ttk, DISABLED, NORMAL  # python 3
from tkinter import filedialog  # python 3
from tkinter.messagebox import showinfo
from tkinter import filedialog as fd
from PIL import ImageTk, Image

from manager import Manager

manager = Manager()


class OutputFrame(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        # self.geometry("1200x700")
        self.geometry("700x700")
        self.minsize(width=100, height=100)

        self.resizable(True, True)
        self.title("Output")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.Output = tk.Text(container, height=5,
                              width=25,
                              bg="light cyan")

        self.Output.pack(expand=True, fill='both')

    def print_inside(self, content):
        # self.Output.delete('1.0', END)
        self.Output.insert(END, '\n' + content)


class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.geometry("750x520")  # b x h
        # self.geometry("1200x700")  # b x h
        self.minsize(width=100, height=100)

        self.resizable(True, True)
        self.title("Snippet")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (LoginPage, CodePage, OptionPage, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")
        # self.show_frame("CodePage")
        # self.show_frame("OptionPage")

    def modify(self, w, h):  # save_value
        self.geometry("{}x{}".format(w, h))

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class LoginPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label_title = tk.Label(self, text="Registrati o effettua il login", font=controller.title_font)
        label_title.pack(side="top", pady=1)

        label_login = tk.Label(self, text="Login:")
        label_login.place(x=130, y=50)

        label_username = tk.Label(self, text="Username:")
        label_username.place(x=20, y=80)
        entry_username = tk.Entry(self)
        entry_username.place(x=90, y=80)

        label_pw = tk.Label(self, text="Password:")
        label_pw.place(x=20, y=105)
        entry_pw = tk.Entry(self)
        entry_pw.place(x=90, y=105)

        button_login = tk.Button(self, text="Login", command=lambda: try_login())
        button_login.place(x=250, y=90)

        def try_login():
            sc, text = manager.login(entry_username.get(), entry_pw.get())
            if sc == 200:
                unlock()
            else:
                messagebox.showerror(sc, text)

        # -------------------------------------------REGISTER

        register_entry_list = []

        register = tk.Label(self, text="Register:")
        register.place(x=130, y=130)

        register_username = tk.Label(self, text="Username:")
        register_username.place(x=20, y=160)
        entry_register_username = tk.Entry(self)
        entry_register_username.place(x=90, y=160)
        register_entry_list.append(entry_register_username)

        register_password = tk.Label(self, text="Password:")
        register_password.place(x=20, y=185)
        entry_register_password = tk.Entry(self)
        entry_register_password.place(x=90, y=185)
        register_entry_list.append(entry_register_password)

        register_password_again = tk.Label(self, text="Again:")
        register_password_again.place(x=20, y=210)
        entry_register_password_again = tk.Entry(self)
        entry_register_password_again.place(x=90, y=210)
        register_entry_list.append(entry_register_password_again)

        register_email = tk.Label(self, text="Mail:")
        register_email.place(x=20, y=235)
        entry_register_email = tk.Entry(self)
        entry_register_email.place(x=90, y=235)
        register_entry_list.append(entry_register_email)

        register_first_name = tk.Label(self, text="First name:")
        register_first_name.place(x=20, y=260)
        entry_register_first_name = tk.Entry(self)
        entry_register_first_name.place(x=90, y=260)
        register_entry_list.append(entry_register_first_name)

        register_last_name = tk.Label(self, text="Last name:")
        register_last_name.place(x=20, y=285)
        entry_register_lastname = tk.Entry(self)
        entry_register_lastname.place(x=90, y=285)
        register_entry_list.append(entry_register_lastname)

        button_register = tk.Button(self, text="Register", command=lambda: try_register())
        button_register.place(x=250, y=220)

        def try_register():
            for field in register_entry_list:
                if field.get() == '':
                    messagebox.showerror("Missing fields", "Check data inserted")
                else:
                    if entry_register_password.get() != entry_register_password_again.get():
                        messagebox.showerror("Password error", "Password inserted are different!")
                    else:
                        sc, text = manager.register(entry_register_username.get(), entry_register_password.get(),
                                                    entry_register_password_again.get(), entry_register_email.get(),
                                                    entry_register_first_name.get(), entry_register_lastname.get())
                        if sc == 201:
                            messagebox.showinfo("Registration completed", "now you can login")
                            for j in register_entry_list:
                                j.delete(0, END)
                        else:
                            messagebox.showerror(sc, text)

        # --------------------------------------------- UPDATE PROFILE DATA

        list_locked_entry = []
        list_update_entry = []

        update = tk.Label(self, text="Update field:")
        update.place(x=495, y=50)

        update_username = tk.Label(self, text="Username:")
        update_username.place(x=400, y=80)
        entry_update_username = tk.Entry(self, state='disabled')
        entry_update_username.place(x=470, y=80)
        list_locked_entry.append(entry_update_username)
        list_update_entry.append(entry_update_username)

        update_email = tk.Label(self, text="Mail:")
        update_email.place(x=400, y=105)
        entry_update_email = tk.Entry(self, state='disabled')
        entry_update_email.place(x=470, y=105)
        list_locked_entry.append(entry_update_email)
        list_update_entry.append(entry_update_email)

        update_first_name = tk.Label(self, text="First name:")
        update_first_name.place(x=400, y=130)
        entry_update_firstname = tk.Entry(self, state='disabled')
        entry_update_firstname.place(x=470, y=130)
        list_locked_entry.append(entry_update_firstname)
        list_update_entry.append(entry_update_firstname)

        update_last_name = tk.Label(self, text="Last name:")
        update_last_name.place(x=400, y=155)
        entry_update_lastname = tk.Entry(self, state='disabled')
        entry_update_lastname.place(x=470, y=155)
        list_locked_entry.append(entry_update_lastname)
        list_update_entry.append(entry_update_lastname)

        button_update = tk.Button(self, state='disabled', text="Update", command=lambda: try_update_profile())
        button_update.place(x=630, y=115)
        list_locked_entry.append(button_update)
        list_update_entry.append(button_update)

        def unlock():
            for element in list_locked_entry:
                element.configure(state='normal')

        def try_update_profile():
            for i in list_update_entry:
                if i.get() == '':
                    messagebox.showerror("Missing fields", "Check data inserted")
                else:
                    sc, text = manager.update_profile(entry_update_username.get(), entry_update_firstname.get(),
                                                      entry_update_lastname.get(), entry_update_email.get())
                    if sc == 200:
                        messagebox.showinfo("update completed", "Now you can see your profile updated")
                        for entry in list_update_entry:
                            entry.delete("1.0", END)
                    else:
                        messagebox.showerror(sc, text)

        # --------------------------------- UPDATE PASSWORD

        list_update_pw_entry = []

        update_pw = tk.Label(self, text="Update Password:")
        update_pw.place(x=490, y=185)

        update_pw_password1 = tk.Label(self, text="New Password:")
        update_pw_password1.place(x=400, y=215)
        entry_update_pw_password1 = tk.Entry(self, state='disabled')
        entry_update_pw_password1.place(x=490, y=215)
        list_locked_entry.append(entry_update_pw_password1)
        list_update_pw_entry.append(entry_update_pw_password1)

        update_pw_password2 = tk.Label(self, text="Again:")
        update_pw_password2.place(x=400, y=240)
        entry_update_pw_password2 = tk.Entry(self, state='disabled')
        entry_update_pw_password2.place(x=490, y=240)
        list_locked_entry.append(entry_update_pw_password2)
        list_update_pw_entry.append(entry_update_pw_password2)

        update_pw_password_old = tk.Label(self, text="Old Password:")
        update_pw_password_old.place(x=400, y=265)
        entry_update_pw_password_old = tk.Entry(self, state='disabled')
        entry_update_pw_password_old.place(x=490, y=265)
        list_locked_entry.append(entry_update_pw_password_old)
        list_update_pw_entry.append(entry_update_pw_password_old)

        button_update_pw = tk.Button(self, state='disabled', text="Update", command=lambda: try_update_password())
        button_update_pw.place(x=650, y=230)
        list_locked_entry.append(button_update_pw)

        def try_update_password():
            for i in list_update_pw_entry:
                if i.get() == '':
                    messagebox.showerror("Missing fields", "Check data inserted")
                else:
                    if entry_update_pw_password1.get() != entry_update_pw_password2.get():
                        messagebox.showerror("Password error", "Password inserted are different!")
                    else:
                        sc, text = manager.update_password(entry_update_pw_password1.get(),
                                                           entry_update_pw_password2.get(),
                                                           entry_update_pw_password_old.get())
                        if sc == 200:
                            messagebox.showinfo("Password changed", "you can login now")
                            for entry in list_update_pw_entry:
                                entry.delete(0, END)
                        else:
                            messagebox.showerror(sc, text)

        # --------------------------------- DELETE

        delete = tk.Label(self, text="Delete account:")
        delete.place(x=490, y=320)

        delete_label = tk.Label(self, text="Press button to delete account:")
        delete_label.place(x=400, y=350)

        button_delete = tk.Button(self, state='disabled', text="Delete", command=lambda: try_delete())
        button_delete.place(x=580, y=350)
        list_locked_entry.append(button_delete)

        def try_delete():
            sc, text = manager.delete()
            if sc == 200:
                messagebox.showinfo("User deleted", "You should now create a new user")
            else:
                messagebox.showerror(sc, text)

        # ------------------------------- SEE DATA

        see_data = tk.Label(self, text="My information")
        see_data.place(x=100, y=320)

        see_data_label = tk.Label(self, text="Press button to see data account:")
        see_data_label.place(x=20, y=350)

        button_see_data = tk.Button(self, state='disabled', text="Get data", command=lambda: try_see_data())
        button_see_data.place(x=210, y=350)
        list_locked_entry.append(button_see_data)

        def try_see_data():
            sc, data = manager.get_user_data()
            if sc == 200:
                messagebox.showinfo("Data retrieved", data)
            else:
                messagebox.showerror(sc, data)

        label_go_to_code = tk.Label(self, text="Go to application:")
        label_go_to_code.place(x=300, y=400)

        image_asset1 = Image.open('assests/python.png')
        image_resized1 = image_asset1.resize((60, 60))
        self.image_code = ImageTk.PhotoImage(image_resized1)

        image_asset2 = Image.open('./assests/help.png')
        image_resized2 = image_asset2.resize((40, 40))
        self.image_help = ImageTk.PhotoImage(image_resized2)

        ButtonCode = tk.Button(self, image=self.image_code, state='disabled', command=lambda: go_code_page())
        ButtonCode.place(x=320, y=430)
        list_locked_entry.append(ButtonCode)

        ButtonHelp = tk.Button(self, image=self.image_help, command=lambda: help_user())
        ButtonHelp.place(x=670, y=450)
        list_locked_entry.append(ButtonCode)

        def help_user():
            webbrowser.open('http://127.0.0.1:8000/help/', new=2)

        def go_code_page():
            controller.show_frame("CodePage")
            controller.modify(1200, 700)


class CodePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Incolla o allega lo Snippet di codice:", font=controller.title_font)
        label.pack(side="top", pady=1)

        label_insert_code = tk.Label(self, text="Inserisci lo snippet:")
        label_insert_code.place(x=200, y=60)

        self.text_code = tk.Text(self, borderwidth=2, relief="groove")
        self.text_code.place(x=50, y=90, width=450, height=390)

        self.label_title = tk.Label(self, text="Inserisci il nome dello snippet:")
        self.label_title.place(x=50, y=490)

        self.entry_title = tk.Entry(self)
        self.entry_title.place(x=220, y=490)

        self.label_code_language = tk.Label(self, text="Inserisci il linguaggio snippet:")
        self.label_code_language.place(x=50, y=520)

        # -----------------------------------

        self.language_options = ['Python', 'Bash', 'Html']

        self.language_var = tk.StringVar()
        self.language_var.set(self.language_options[0])

        self.option_menu_language = tk.OptionMenu(
            self,
            self.language_var,
            *self.language_options,
        )

        self.option_menu_language.place(x=220, y=515)

        self.label_code_executable = tk.Label(self, text="il codice è eseguibile:")
        self.label_code_executable.place(x=50, y=550)

        self.executable = ['True', 'False']

        # setting variable for Integers
        self.executable_var = tk.StringVar()
        self.executable_var.set(self.executable[1])

        # creating widget
        self.option_menu_executable = tk.OptionMenu(
            self,
            self.executable_var,
            *self.executable,
        )

        # positioning widget
        self.option_menu_executable.place(x=220, y=550)

        # --------------------

        label_allega = tk.Label(self, text='Oppure allega: ')
        label_allega.place(x=50, y=650)

        button_scegli_file = tk.Button(self, text="Scegli file",
                                       command=lambda: self.select_file())
        button_scegli_file.place(x=140, y=650)

        self.text_get_snippet = tk.Text(self, state='normal', borderwidth=2, relief="groove", bg="light cyan")
        self.text_get_snippet.place(x=520, y=90)

        label_search_snippet = tk.Label(self, text='Ricerca Snippet: ')
        label_search_snippet.place(x=520, y=60)

        button_search_snippet = tk.Button(self, text="Cerca",
                                          command=lambda: self.get_user_snippet())
        button_search_snippet.place(x=620, y=60)

        image_asset_send = Image.open('assests/send.png')
        image_resized_send = image_asset_send.resize((60, 60))
        self.image_send = ImageTk.PhotoImage(image_resized_send)

        self.label_use_existing_snippet = tk.Label(self, text="Utilizza lo snippet con id:")
        self.label_use_existing_snippet.place(x=520, y=490)

        self.entry_existing_entry = tk.Entry(self)
        self.entry_existing_entry.place(x=680, y=490)

        button_select = tk.Button(self, text="Select", command=lambda: self.select())
        button_select.place(x=800, y=490)

        label_delete_snippet = tk.Label(self, text='Elimina lo snippet con id: ')
        label_delete_snippet.place(x=520, y=520)

        self.entry_delete_snippet = tk.Entry(self)
        self.entry_delete_snippet.place(x=680, y=520)

        button_delete = tk.Button(self, text="Delete", command=lambda: self.delete_snippet())
        button_delete.place(x=800, y=520)

        ButtonSend = tk.Button(self, image=self.image_send, command=lambda: self.send())
        ButtonSend.place(x=525, y=550)

        image_asset_back = Image.open('assests/back.jpg')
        image_resized_back = image_asset_back.resize((60, 60))
        self.image_back = ImageTk.PhotoImage(image_resized_back)

        BackButton = tk.Button(self, image=self.image_back, command=lambda: self.back())
        BackButton.place(x=1025, y=600)

    def back(self):
        self.controller.show_frame("LoginPage")
        self.controller.modify(750, 520)

    def delete_snippet(self):
        snippet_id = self.entry_delete_snippet.get()
        status_code = manager.delete_snippet(snippet_id)
        if status_code == 204:
            messagebox.showinfo("Snippet deleted", "Operation complete")
        else:
            messagebox.showerror("Error in delete", status_code)
        self.entry_delete_snippet.delete(0, 'end')

    def select(self):
        if len(self.entry_existing_entry.get()) != 0:
            snippet_id = self.entry_existing_entry.get()
            response_code, dict_of_value = manager.get_snippet_by_id(snippet_id)
            if response_code == 200:
                self.text_code.delete(1.0, END)
                self.text_code.insert('1.0', dict_of_value['code'])  # json parsed
                self.entry_title.delete(0, END)
                self.entry_title.insert(0, dict_of_value['title'])  # json parsed
                self.executable_var.set(self.executable[0]) if dict_of_value['executable'] == 'True' \
                    else self.executable_var.set(self.executable[1])
                self.language_var.set(self.language_options[0]) if dict_of_value['language'] == 'Python' \
                    else self.language_var.set(self.language_options[2])
            else:
                messagebox.showerror(response_code, dict_of_value['response'])
        else:
            messagebox.showerror("Select an id", "Seems that entry is empty")

    def get_user_snippet(self):
        response_code, result = manager.get_user_snippets()
        self.text_get_snippet.delete(1.0, END)
        if response_code == 200:
            self.text_get_snippet.insert('1.0', "Data found: \n" + result)  # json parsed
        else:
            messagebox.showerror(response_code, result)

    def send(self, **kwargs):
        snippet_id = self.entry_existing_entry.get()
        code = self.text_code.get(1.0, END)
        title = self.entry_title.get()
        language = self.language_var.get()
        executable = self.executable_var.get()
        if len(self.entry_existing_entry.get()) != 0:
            sc, t = manager.update_snippet_by_id(snippet_id, code, title, language, executable)
            if sc != 200:
                messagebox.showerror("Error in update" + sc, t)
            else:
                self.go_option_page()
        else:
            if not self.text_code.compare("end-1c", "==", "1.0"):
                sc, t = manager.create_snippet(code, title, language, executable)
                if sc != 201:
                    messagebox.showerror("Error in create" + sc, t)
                else:
                    self.go_option_page()
            else:
                messagebox.showerror("Code is required", "Create or use a snippet")

    def select_file(self):
        filetypes = (
            ('Python', '*.py'),
            ('Shell', '*.sh')
        )
        file = fd.askopenfile(mode='r', filetypes=filetypes)
        if file:
            content = file.read()
            file.close()
            self.entry_code.insert('1.0', content)

    def go_option_page(self):
        self.controller.show_frame("OptionPage")
        self.controller.modify(1400, 700)


# --------------------------------------  OPTION

class OptionPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Scegli le opzioni", font=controller.title_font)
        label.place(x=300, y=20)

        label_tipo = tk.Label(self, text="Seleziona la procedura:")
        label_tipo.place(x=10, y=75)

        def display_selected(choice):
            self.text_code.delete('1.0', END)
            choice = self.valore_tipo.get()
            if choice == 'Pipeline':
                for c in self.checkboxes:
                    c.config(state="disabled")
            else:
                for c in self.checkboxes:
                    c.config(state="active")
            if len(self.text_code.get("1.0", "end-1c")) == 0:
                self.text_code.insert(1.0, manager.get_snippet_code())

        tipo = ['Pipeline', 'Single operation']
        self.valore_tipo = tk.StringVar(self)
        self.valore_tipo.set('')
        question_menu = tk.OptionMenu(self, self.valore_tipo, *tipo, command=display_selected)
        question_menu.place(x=130, y=70)

        label_spunta = tk.Label(self, text="Spunta per selezionare le opzioni:")
        label_spunta.place(x=10, y=110)

        self.option = {
            'language recognition': tk.IntVar(),
            'reindent code': tk.IntVar(),
            'order imports': tk.IntVar(),
            'pylint checker': tk.IntVar(),
            'pyflakes checker': tk.IntVar(),
            'flake8 checker': tk.IntVar(),
            'mypy checker': tk.IntVar(),
            'check execution': tk.IntVar()
        }

        self.checkboxes_value = []
        self.checkboxes = []
        xvalue, yvalue = 50, 140
        for machine in self.option:
            l = tk.Checkbutton(self, text=machine, variable=self.option[machine], onvalue=1, offvalue=0)
            l.place(x=xvalue, y=yvalue)
            self.checkboxes_value.append(self.option[machine])
            self.checkboxes.append(l)
            yvalue += 20

        def cb_check():
            self.cb_multiple_output.config(
                state=DISABLED) if self.single_output.get() else self.cb_multiple_output.config(state=NORMAL)
            self.multiple_output.get() if self.cb_single_output.config(
                state=DISABLED) else self.cb_single_output.config(state=NORMAL)
            self.cb_save_output.config(state=DISABLED) if self.multiple_output.get() else self.cb_save_output.config(
                state=NORMAL)

        self.single_output = tk.IntVar()
        self.cb_single_output = tk.Checkbutton(self, text="singolo Output", variable=self.single_output, onvalue=1,
                                               offvalue=0, command=cb_check)
        self.cb_single_output.place(x=10, y=450)

        self.multiple_output = tk.IntVar()
        self.cb_multiple_output = tk.Checkbutton(self, text="output Multipli", variable=self.multiple_output, onvalue=1,
                                                 offvalue=0, command=cb_check)
        self.cb_multiple_output.place(x=10, y=470)

        self.file_creation = tk.IntVar()
        cb_file_creation = tk.Checkbutton(self, text="Creazione file", variable=self.file_creation,
                                          onvalue=1, offvalue=0)
        cb_file_creation.place(x=10, y=510)

        self.save_on_server = tk.IntVar()
        self.cb_save_output = tk.Checkbutton(self, text="Salva modifiche", variable=self.save_on_server,
                                             onvalue=1, offvalue=0, state=DISABLED)
        self.cb_save_output.place(x=10, y=550)

        button = tk.Button(self, text="Invia", command=lambda: check_option())
        button.place(x=50, y=650)

        button = tk.Button(self, text="Back", command=lambda: go_code_page())
        button.place(x=150, y=650)

        self.text_code = tk.Text(self, borderwidth=2, relief="groove")
        self.text_code.place(x=250, y=60, width=1100, height=600)

        def go_code_page():
            self.controller.show_frame("CodePage")
            self.controller.modify(1200, 700)

        def check_option():
            option_chose = []
            if self.valore_tipo.get() == 'Pipeline':
                option_chose = self.option.keys()
            elif self.valore_tipo.get() == 'Single operation':
                for i in range(len(self.checkboxes_value)):
                    if self.checkboxes_value[i].get():
                        option_chose.append(list(self.option.items())[i][0])  # 0 valore e i = iteratore
            if len(option_chose) == 0:
                messagebox.showerror("Select at least one Option", "Check value")
            else:
                if self.multiple_output.get():
                    op = manager.multiple_operation(option_chose,
                                                    True if self.file_creation.get() else False)  # write
                    self.text_code.delete('1.0', END)
                    self.text_code.insert('1.0', op)
                if self.single_output.get():
                    op = manager.single_operation(option_chose,
                                                  True if self.file_creation.get() else False,
                                                  True if self.save_on_server.get() else False)
                    self.text_code.delete('1.0', END)
                    self.text_code.insert('1.0', op)


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
