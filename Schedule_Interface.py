import ast
from tkinter import *
from tkinter import ttk
import customtkinter
from typing import Union, Any
import re

from User import User, Course, Assignment
import pickle
from datetime import timedelta, date, datetime

customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('dark-blue')


STUDY_LEVELS = ['Select an Option', 'HighSchool', 'Undergraduate', 'Graduate']
STUDY_AREAS = ['Select an Option', 'Biology', 'Chemistry', 'Cell Biology', 'Immunology', 'Genetics', 'Economics', 'Business']
COLORS = [' Select an Option', 'Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Pink', 'Orange', 'Brown', 'Beige', 'Grey']
DURATIONS = [' Length', '1', '2', '3', '4', '5']
PRIORITY_COLORS = {
    'Normal': '#A3BDF1',
    'P1': '#E58C91',
    'P2': '#EFC26F',
    'P3': '#AFEFB5'
}
CLASS_COLOR_CODES = {
    'Red': '#C64145',
    'Blue': '#809BCE',
    'Yellow': '#FDFD96',
    'Green': '#95AA63',
    'Purple': '#C784AF',
    'Pink': '#FA6969',
    'Orange': '#FEA95A',
    'Brown': '#C89D7C',
    'Beige': '#ECDDD0',
    'Grey': '#B7B5AA'
}  # red color: '#E12A36'

CLASS_DAYS_Y = {'800': '45', '830': '77', '900': '109', '930': '141',
                '1000': '173', '1030': '205', '1100': '237', '1130': '269',
                '1200': '301', '1230': '333', '1300': '365', '1330': '397',
                '1400': '429', '1430': '461', '1500': '493', '1530': '525',
                '1600': '557', '1630': '589', '1700': '621', '1730': '653',
                '1800': '685', '1830': '717', '1900': '749', '1930': '781',
                '2000': '813', '2030': '845', '2100': '877'}  # use for y position using days

CLASS_TIMES_H = {'1': 62, '2': 126, '3': 190, '4': 254, '5': 318}  # use for height

CLASS_DAYS_X = {'M': '66',
                'TU': '207',
                'W': '348',
                'TH': '489',
                'F': '630',
                'S': '771',
                'SU': '912'}  # use for x position


class MyScheduleApp(object):

    def __init__(self):
        self.root = Tk()
        self.root.geometry('300x400+590+250')
        self.root.configure(background='#3E6C7B')
        self.root.title('MySchedule')
        self.style = ttk.Style(self.root)
        self.style.theme_use('clam')
        self.style.configure('TButton', background='#FFFDFD',
                             bordercolor='#E5A8A9', foreground='#3E6C7B',
                             font=('Times', 16, 'bold'))
        self.style2 = ttk.Style(self.root)
        self.style2.theme_use('clam')
        self.style2.configure('W.TButton', background='#FFFDFD',
                              bordercolor='#E5A8A9', foreground='#3E6C7B',
                              font=('Times', 16, 'bold'))

        # connected user
        self.current_user = None
        self.current_pwd = None

        # Variables to use later for entries and stuff
        self.username = StringVar(value='Username...')
        self.password = StringVar(value='*****')
        self.create_username = StringVar(value='Create Username')
        self.create_pwd = StringVar(value='Password')
        self.confirm_pwd = StringVar(value='Confirm Password')
        self.school = StringVar()
        self.level_study = StringVar()
        self.area_study = StringVar()
        self.username_forgot = StringVar()

        self.label_title = Label(self.root, text='MySchedule',
                                 background='#3E6C7B', foreground='#E5A8A9',
                                 font=('Times', 28, 'bold'))
        self.label_title.grid(column=1, row=1)
        # self.filler1 = Label(self.root, text='   ', background='#3E6C7B')
        # self.filler1.grid(column=1, row=2)

        self.button_login = ttk.Button(self.root, text='Login',
                                       style='my.TButton',
                                       command=self.open_login_page,
                                       cursor='hand')
        self.button_login.grid(column=1, row=3)
        self.filler2 = Label(self.root, text='   ', background='#3E6C7B')
        self.filler2.grid(column=1, row=4)

        self.button_signup = ttk.Button(self.root, text='Signup!',
                                        command=self.open_signup_page,
                                        cursor='hand')
        self.button_signup.grid(column=1, row=5)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_rowconfigure(6, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(2, weight=1)

        self.root.mainloop()

    def open_login_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.style.configure('my.TButton', background='#3E6C7B',
                             foreground='#E5A8A9', borderwidth='#3E6C7B',
                             font=('Times', 30, 'bold'))
        # label_signup = Label(self.root, text='Login', background='#3E6C7B',
        # foreground='#E5A8A9', font=('Times', 28, 'bold'))
        # label_signup.grid(column=1, row=1)

        button1 = ttk.Button(self.root, style='my.TButton', text='Login',
                             command=self.login, cursor='hand')
        button1.grid(column=1, row=1)

        username = Entry(self.root, textvariable=self.username, width=14,
                         foreground='#E5A8A9', background='#3E6C7B',
                         font=('Times', 18))
        username.grid(column=1, row=3)
        password = Entry(self.root, textvariable=self.password, width=14,
                         foreground='#E5A8A9', background='#3E6C7B',
                         font=('Times', 18), show='*')
        password.grid(column=1, row=5)
        Label(self.root, text='   ', background='#3E6C7B').grid(column=1, row=4)

        label = Label(self.root, text='Forgot password?', background='#3E6C7B', font=('Times', 18, 'underline'), cursor='hand', foreground='#E5A8A9')
        label.bind("<Button-1>", lambda e: self.get_pwd(label))
        label.grid(column=1, row=6)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_rowconfigure(7, weight=1)
        self.root.grid_rowconfigure(10, weight=0)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(2, weight=1)

    def login(self):
        user = self.username.get()
        pwd = self.password.get()
        self.username.set('Username...')
        self.password.set('*****')

        file = open('login_info.txt')
        info = file.read()
        login_dct = ast.literal_eval(info)
        file.close()

        if user in login_dct and pwd == login_dct[user][0]:
            self.current_user = user
            self.current_pwd = pwd
            self.create_user_account()

        else:
            bad = Toplevel(self.root)
            if len(user) > 14:
                bad.geometry('400x150')
            elif len(user) > 20:
                bad.geometry('500x150')
            else:
                bad.geometry('350x150')
            bad.configure(background='#3E6C7B')
            Label(bad, text=f'The username "{user}" or your password\nare not a valid.\nPlease create an account.', foreground='#E5A8A9', background='#3E6C7B', font=('Times', 16)).grid(column=1, row=1)

            bad.grid_rowconfigure(0, weight=1)
            bad.grid_rowconfigure(2, weight=1)
            bad.grid_columnconfigure(0, weight=1)
            bad.grid_columnconfigure(2, weight=1)

    def open_signup_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.style.configure('my.TButton', background='#3E6C7B',
                             foreground='#E5A8A9', borderwidth='#3E6C7B',
                             font=('Times', 30, 'bold'))
        button1 = ttk.Button(self.root, style='my.TButton', text='Signup',
                             command=lambda: self.signup(signup_filler, signup_login_btn, pwd_id), cursor='hand')
        button1.grid(column=1, row=1)
        username = Entry(self.root, textvariable=self.create_username, width=15,
                         foreground='#3E6C7B', background='#FBF8F8',
                         font=('Times', 18))
        username.grid(column=1, row=3)
        filler1 = Label(self.root, text='  ', background='#3E6C7B',
                        foreground='#E5A8A9', font=('Times', 14, 'bold'))
        filler1.grid(column=1, row=4)

        pwd = Entry(self.root, textvariable=self.create_pwd, width=15,
                    foreground='#3E6C7B', background='#FBF8F8',
                    font=('Times', 18))
        pwd.grid(column=1, row=5)
        filler2 = Label(self.root, text='  ', background='#3E6C7B',
                        foreground='#E5A8A9', font=('Times', 14, 'bold'))
        filler2.grid(column=1, row=6)

        confirm_pwd = Entry(self.root, textvariable=self.confirm_pwd, width=15,
                            foreground='#3E6C7B', background='#FBF8F8',
                            font=('Times', 18))
        confirm_pwd.grid(column=1, row=7)

        signup_filler = Label(self.root, text='   ', background='#3E6C7B')
        signup_login_btn = ttk.Button(self.root, text='Go Login', style='W.TButton', command=self.open_login_page, cursor='hand')

        pwd_id = self.confirm_pwd.trace('w', lambda name, index, mode, text=self.confirm_pwd: self.verify_same_pwd(filler2))
        self.create_username.trace('w', lambda name, index, mode, text=self.username: self.verify_different_username(filler1))

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_rowconfigure(6, weight=0)
        self.root.grid_rowconfigure(10, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(2, weight=1)

    def signup(self, filler, btn, pwd_id):
        self.confirm_pwd.trace_vdelete('w', pwd_id)
        user = self.create_username.get()
        pwd = self.create_pwd.get()
        self.create_username.set('Create Username')
        self.create_pwd.set('Password')
        self.confirm_pwd.set('Confirm Password')

        file = open('login_info.txt')
        info = file.read()
        login_dct = ast.literal_eval(info)
        file.close()

        if user not in login_dct:
            login_dct.update({user: (pwd, 0)})
            filler.grid(column=1, row=8)
            btn.grid(column=1, row=9)
        else:
            print('Username already used! Start Over.')

        file = open('login_info.txt', 'w')
        file.write(str(login_dct))
        file.close()

    def get_pwd(self, label):
        forgot = Toplevel(self.root)
        forgot.title('Get Password')
        self.style.configure('my.TButton', font=('Times', 20))
        forgot.geometry('300x150')
        forgot.configure(background='#E5A8A9')
        user_label = Label(forgot, background='#E5A8A9', foreground='#3E6C7B', text='Enter exact user name:', font=('Times', 17, 'bold'))
        user_label.place(x='60', y='20')
        user_entry = Entry(forgot, width=15, textvariable=self.username_forgot)
        user_entry.place(x='73', y='50')
        user_btn = ttk.Button(forgot, style='my.TButton', text='Search', width=7, command=lambda: self.give_pwd(forgot))
        user_btn.place(x='105', y='100')

    def give_pwd(self, master):
        user = self.username_forgot.get()
        self.username_forgot.set('')
        for widget in master.winfo_children():
            widget.destroy()
        master.title('Your Password')
        file = open('login_info.txt')
        info = file.read()
        login_dct = ast.literal_eval(info)
        file.close()
        pwd = login_dct[user][0]
        lab = Label(master, text=pwd, background='#E5A8A9', foreground='#3E6C7B', font=('Times', 20, 'bold'))
        if len(pwd) > 18:
            master.geometry('400x150')
        lab.place(relx=0.5, rely=0.5, anchor='center')
        btn = ttk.Button(master, style='my.TButton', text='Login', width=7, command=lambda: self.open_log(master))
        btn.place(x='110', y='105')

    def open_log(self, master):
        self.open_login_page()
        master.destroy()

    def verify_same_pwd(self, label):
        if self.create_pwd.get() != self.confirm_pwd.get():
            label.configure(text='Passwords do not match')
        else:
            label.configure(text='    ')

    def verify_same_pwd2(self):
        if self.create_pwd.get() != self.confirm_pwd.get():
            return False
        else:
            return True

    def verify_different_username(self, label):
        file = open('login_info.txt')
        info = file.read()
        login_dct = ast.literal_eval(info)
        file.close()

        if self.create_username.get() in login_dct:
            label.configure(text='Username is already used')
            return False
        else:
            label.configure(text='  ')
            return True

    def verify_different_username2(self):
        file = open('login_info.txt')
        info = file.read()
        login_dct = ast.literal_eval(info)
        file.close()

        if self.create_username.get() in login_dct:
            return False
        else:
            return True

    def create_user_account(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(2, weight=0)
        self.root.grid_rowconfigure(7, weight=0)
        self.root.grid_columnconfigure(0, weight=0)
        self.root.grid_columnconfigure(2, weight=0)

        if self.get_connection() == 0:
            self.survey()
            self.add_connection()
        else:
            self.add_connection()
            SchedulePage(self.root, self.current_pwd)

    def get_connection(self):
        user_file = open('login_info.txt')
        info = user_file.read()
        dct = ast.literal_eval(info)
        connections = dct[self.current_user][1]
        return connections

    def add_connection(self):
        user_file = open('login_info.txt')
        info = user_file.read()
        dct = ast.literal_eval(info)
        user_file.close()
        dct[self.current_user] = (dct[self.current_user][0], dct[self.current_user][1] + 1)

        user_file = open('login_info.txt', 'w')
        user_file.write(str(dct))
        user_file.close()

    def survey(self):
        self.root.geometry('400x300')
        self.style.configure('my.TButton', font=('Times', 24, 'bold'), background='white', foreground='#3E6C7B')
        Label(self.root, text='School Name: ', background='#3E6C7B', font=('Times', 20, 'bold'), foreground='#E5A8A9').grid(column=1, row=1)
        Label(self.root, text='    ', background='#3E6C7B', font=('Times', 20)).grid(column=1, row=2)
        Label(self.root, text='Level of study: ', background='#3E6C7B', font=('Times', 20, 'bold'), foreground='#E5A8A9').grid(column=1, row=3)
        Label(self.root, text='    ', background='#3E6C7B', font=('Times', 20)).grid(column=1, row=4)
        Label(self.root, text='Area of study: ', background='#3E6C7B', font=('Times', 20, 'bold'), foreground='#E5A8A9').grid(column=1, row=5)
        Entry(self.root, textvariable=self.school, width=20).grid(column=2, row=1)
        combo_level = ttk.Combobox(self.root, width=20, textvariable=self.level_study, cursor='hand')
        combo_level['values'] = STUDY_LEVELS
        combo_level.current(0)
        combo_level.grid(column=2, row=3)
        combo_area = ttk.Combobox(self.root, width=20, textvariable=self.area_study, cursor='hand')
        combo_area['values'] = STUDY_AREAS
        combo_area.current(0)
        combo_area.grid(column=2, row=5)
        Label(self.root, text='    ', background='#3E6C7B', font=('Times', 20)).grid(column=1, row=6)
        ttk.Button(self.root, text='Continue', style='my.TButton', cursor='hand', command=self.move_to_schedule).grid(column=2, row=7)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(8, weight=1)
        self.root. grid_columnconfigure(0, weight=1)
        self.root. grid_columnconfigure(3, weight=1)

    def move_to_schedule(self):
        school = self.school.get()
        level = self.level_study.get()
        area = self.area_study.get()
        self.school.set('')

        # Stores the Users data and info
        user_info = User(self.current_user, self.current_pwd, school, level, area)
        dct = None
        for users_dct in pickle_loader('Users_file.txt'):
            dct = users_dct
        if dct is None:
            pickle_input('Users_file.txt', {self.current_pwd: user_info})
        else:
            dct.update({self.current_pwd: user_info})
            pickle_delete('Users_file.txt')
            pickle_input('Users_file.txt', dct)

        SchedulePage(self.root, self.current_pwd)


class SchedulePage(object):
    def __init__(self, x, pwd):
        x.destroy()
        self.pwd = pwd
        # x += 2
        self.root = Tk()
        self.root.title('MySchedule')
        self.root.geometry('1500x910+7+5')
        self.root.configure(background='white')
        self.root.resizable(False, False)
        self.style = ttk.Style(self.root)
        self.style.theme_use('clam')
        self.style.configure('TButton', background='#DCE6F3',
                             foreground='#3E6C7B', font=('Times', 20, 'bold'),
                             bordercolor='#DCE6F3', borderwidth=1)

        # Important User information
        self.user = self.get_user()
        self.take_courses = self.user.courses  # Length max of 6
        if len(self.take_courses) == 0:
            self.course_index = len(self.take_courses)
        else:
            self.course_index = len(self.take_courses) - 1
        self.num_of_courses = len(self.take_courses)

        # True if display btn clicked, false if not
        self.clicked = False

        # Variables to use
        self.course = StringVar()
        self.time_class = StringVar()
        self.time_class.set('M: TU: W: TH: F: S: SU:')
        self.color = StringVar()
        self.duration = StringVar()

        self.banner = Label(self.root, text='         \n    \n  ', background='#3E6C7B')
        self.banner2 = Label(self.root, text='      ', background='#3E6C7B')
        self.banner3 = Label(self.root, text='    ', background='#DCE6F3')
        self.banner4 = Label(self.root, text='    ', background='#3E6C7B')
        self.banner5 = Label(self.root, text='    ', background='#3E6C7B')
        self.build_banners()

        self.monday_label = Label(self.root, text='MON', background='#3E6C7B', font=('Times', 25, 'bold'), foreground='#DCE6F3')
        self.mo_day = Label(self.root, background='#3E6C7B', font=('Times', 23), foreground='#DCE6F3')
        self.tues_label = Label(self.root, text='TUE', background='#3E6C7B', font=('Times', 25, 'bold'), foreground='#DCE6F3')
        self.tu_day = Label(self.root, background='#3E6C7B', font=('Times', 23), foreground='#DCE6F3')
        self.wed_label = Label(self.root, text='WED', background='#3E6C7B', font=('Times', 25, 'bold'), foreground='#DCE6F3')
        self.wed_day = Label(self.root, background='#3E6C7B', font=('Times', 23), foreground='#DCE6F3')
        self.thur_label = Label(self.root, text='THU', background='#3E6C7B', font=('Times', 25, 'bold'), foreground='#DCE6F3')
        self.thu_day = Label(self.root, background='#3E6C7B', font=('Times', 23), foreground='#DCE6F3')
        self.frid_label = Label(self.root, text='FRI', background='#3E6C7B', font=('Times', 25, 'bold'), foreground='#DCE6F3')
        self.fri_day = Label(self.root, background='#3E6C7B', font=('Times', 23), foreground='#DCE6F3')
        self.sat_label = Label(self.root, text='SAT', background='#3E6C7B', font=('Times', 25, 'bold'), foreground='#DCE6F3')
        self.sat_day = Label(self.root, background='#3E6C7B', font=('Times', 23), foreground='#DCE6F3')
        self.sun_label = Label(self.root, text='SUN', background='#3E6C7B', font=('Times', 25, 'bold'), foreground='#DCE6F3')
        self.sun_day = Label(self.root, background='#3E6C7B', font=('Times', 23), foreground='#DCE6F3')
        self.weekdays_lst = [self.mo_day, self.tu_day, self.wed_day, self.thu_day, self.fri_day, self.sat_day, self.sun_day]
        self.config_weekdays()
        self.build_weekdays()

        self.time8 = Label(self.root, text=' 8:00 ', background='#DCE6F3', font=('Times', 22), borderwidth=1, relief='ridge')
        self.time83 = Label(self.root, text=' 8:30 ', background='#DCE6F3', font=('Times', 22), borderwidth=1, relief='ridge')
        self.time9 = Label(self.root, text=' 9:00 ', background='#DCE6F3', font=('Times', 22), borderwidth=1, relief='ridge')
        self.time93 = Label(self.root, text=' 9:30 ', background='#DCE6F3', font=('Times', 22), borderwidth=1, relief='ridge')
        self.time10 = Label(self.root, text='10:00', background='#DCE6F3', font=('Times', 22), borderwidth=1, relief='ridge')
        self.time103 = Label(self.root, text='10:30', background='#DCE6F3', font=('Times', 22), borderwidth=1, relief='ridge')
        self.time11 = Label(self.root, text='11:00', background='#DCE6F3', font=('Times', 22), borderwidth=1, relief='ridge')
        self.time113 = Label(self.root, text='11:30', background='#DCE6F3', font=('Times', 22), borderwidth=1, relief='ridge')
        self.time12 = Label(self.root, text='12:00', background='#DCE6F3', font=('Times', 22), borderwidth=1, relief='ridge')
        self.time123 = Label(self.root, text='12:30', background='#DCE6F3', font=('Times', 22), borderwidth=1, relief='ridge')
        self.time13 = Label(self.root, text='13:00', background='#DCE6F3', font=('Times', 22), borderwidth=1, relief='ridge')
        self.time133 = Label(self.root, text='13:30', background='#DCE6F3', font=('Times', 22), borderwidth=1, relief='ridge')
        self.time14 = Label(self.root, text='14:00', background='#DCE6F3', font=('Times', 22), borderwidth=1, relief='ridge')
        self.time143 = Label(self.root, text='14:30', background='#DCE6F3', font=('Times', 22), borderwidth=1, relief='ridge')
        self.time15 = Label(self.root, text='15:00', background='#DCE6F3', font=('Times', 22), borderwidth=1, relief='ridge')
        self.time153 = Label(self.root, text='15:30', background='#DCE6F3', font=('Times', 22), borderwidth=1, relief='ridge')
        self.time16 = Label(self.root, text='16:00', background='#DCE6F3', font=('Times', 22), borderwidth=1, relief='ridge')
        self.time163 = Label(self.root, text='16:30', background='#DCE6F3', font=('Times', 22), borderwidth=1, relief='ridge')
        self.time17 = Label(self.root, text='17:00', background='#DCE6F3', font=('Times', 22), borderwidth=1, relief='ridge')
        self.time173 = Label(self.root, text='17:30', background='#DCE6F3', font=('Times', 22), borderwidth=1, relief='ridge')
        self.time18 = Label(self.root, text='18:00', background='#DCE6F3', font=('Times', 22), borderwidth=1, relief='ridge')
        self.time183 = Label(self.root, text='18:30', background='#DCE6F3', font=('Times', 22), borderwidth=1, relief='ridge')
        self.time19 = Label(self.root, text='19:00', background='#DCE6F3', font=('Times', 22), borderwidth=1, relief='ridge')
        self.time193 = Label(self.root, text='19:30', background='#DCE6F3', font=('Times', 22), borderwidth=1, relief='ridge')
        self.time20 = Label(self.root, text='20:00', background='#DCE6F3', font=('Times', 22), borderwidth=1, relief='ridge')
        self.time203 = Label(self.root, text='20:30', background='#DCE6F3', font=('Times', 22), borderwidth=1, relief='ridge')
        self.time21 = Label(self.root, text='21:00', background='#DCE6F3', font=('Times', 22), borderwidth=1, relief='ridge')
        self.build_times()

        self.school_label = Label(self.root, text='School: ', font=('Times', 23, 'bold'), background='#3E6C7B', foreground='#DCE6F3')
        self.area_label = Label(self.root, text='Area of study: ', font=('Times', 23, 'bold'), background='#3E6C7B', foreground='#DCE6F3')
        self.level_label = Label(self.root, text='Level of study: ', font=('Times', 23, 'bold'), background='#3E6C7B', foreground='#DCE6F3')
        self.course_list_label = Label(self.root, text='Course List', font=('Times', 23, 'bold', 'underline'), background='#3E6C7B', foreground='#DCE6F3')
        self.school_name = Label(self.root, text=self.user.school, font=('Times', 23), background='#3E6C7B', foreground='#DCE6F3')
        self.study_area = Label(self.root, text=self.user.area, font=('Times', 23), background='#3E6C7B', foreground='#DCE6F3')
        self.study_level = Label(self.root, text=self.user.level, font=('Times', 23), background='#3E6C7B', foreground='#DCE6F3')
        self.build_info_section()

        self.line_label1 = Label(self.root, text='    ', background='#DCE6F3')
        self.line_label1.place(x='1100', y='45', height=2, width=340)
        self.line_label2 = Label(self.root, text='    ', background='#DCE6F3')
        self.line_label2.place(x='1100', y='87', height=2, width=340)

        self.course_label = Label(self.root, text='Enter Course Title: ', font=('Times', 21, 'bold'), background='#3E6C7B', foreground='#DCE6F3')
        self.time_label = Label(self.root, text='Time of classes:\n(M:930, TU:1400)', font=('Times', 21, 'bold'), background='#3E6C7B', foreground='#DCE6F3')
        self.color_label = Label(self.root, text='Choose a Color: ', font=('Times', 21, 'bold'), background='#3E6C7B', foreground='#DCE6F3')
        self.entry_course = Entry(self.root, width=20, borderwidth=1, textvariable=self.course, background='#DCE6F3')
        self.entry_time = Entry(self.root, width=20, borderwidth=1, textvariable=self.time_class, background='#DCE6F3')
        self.combo_color = ttk.Combobox(self.root, width=20, textvariable=self.color, background='#DCE6F3', style='my.TButton')
        self.combo_color['values'] = COLORS
        self.combo_color.current(0)
        self.duration_combo = ttk.Combobox(self.root, width=5, textvariable=self.duration, background='#DCE6F3', style='my.TButton')
        self.duration_combo['values'] = DURATIONS
        self.duration_combo.current(0)
        self.add_btn = ttk.Button(self.root, text='Add Course', style='my.TButton', cursor='hand', command=self.add_course)
        self.assignments_btn = ttk.Button(self.root, text='Assignment Page', style='my.TButton', cursor='hand', command=self.open_assignments)
        self.calendar_btn = ttk.Button(self.root, text='Open Calendar', style='my.TButton', cursor='hand', command=self.open_calendar)
        self.display_btn = ttk.Button(self.root, text='Display', style='my.TButton', cursor='hand', command=self.show_timetable, width=8)
        self.display_btn.bind('<Button-1>', self.check_clicked)
        self.build_adding_section()

        self.course1 = Label(self.root, font=('Times', 21), background='#3E6C7B', foreground='#DCE6F3')
        self.course2 = Label(self.root, font=('Times', 21), background='#3E6C7B', foreground='#DCE6F3')
        self.course3 = Label(self.root, font=('Times', 21), background='#3E6C7B', foreground='#DCE6F3')
        self.course4 = Label(self.root, font=('Times', 21), background='#3E6C7B', foreground='#DCE6F3')
        self.course5 = Label(self.root, font=('Times', 21), background='#3E6C7B', foreground='#DCE6F3')
        self.course6 = Label(self.root, font=('Times', 21), background='#3E6C7B', foreground='#DCE6F3')
        self.courses = [self.course1, self.course2, self.course3, self.course4, self.course5, self.course6]
        self.class_time1 = Label(self.root, font=('Times', 18), background='#3E6C7B', foreground='#DCE6F3')
        self.class_time2 = Label(self.root, font=('Times', 18), background='#3E6C7B', foreground='#DCE6F3')
        self.class_time3 = Label(self.root, font=('Times', 18), background='#3E6C7B', foreground='#DCE6F3')
        self.class_time4 = Label(self.root, font=('Times', 18), background='#3E6C7B', foreground='#DCE6F3')
        self.class_time5 = Label(self.root, font=('Times', 18), background='#3E6C7B', foreground='#DCE6F3')
        self.class_time6 = Label(self.root, font=('Times', 18), background='#3E6C7B', foreground='#DCE6F3')
        self.times = [self.class_time1, self.class_time2, self.class_time3, self.class_time4, self.class_time5, self.class_time6]
        self.class_btn1 = ttk.Button(self.root, text='Drop', style='my.TButton', command=lambda: self.drop_course(0), width=5)
        self.class_btn2 = ttk.Button(self.root, text='Drop', style='my.TButton', command=lambda: self.drop_course(1), width=5)
        self.class_btn3 = ttk.Button(self.root, text='Drop', style='my.TButton', command=lambda: self.drop_course(2), width=5)
        self.class_btn4 = ttk.Button(self.root, text='Drop', style='my.TButton', command=lambda: self.drop_course(3), width=5)
        self.class_btn5 = ttk.Button(self.root, text='Drop', style='my.TButton', command=lambda: self.drop_course(4), width=5)
        self.class_btn6 = ttk.Button(self.root, text='Drop', style='my.TButton', command=lambda: self.drop_course(5), width=5)
        self.drop_btn = [self.class_btn1, self.class_btn2, self.class_btn3, self.class_btn4, self.class_btn5, self.class_btn6]

        if 0 < len(self.take_courses) <= 6:
            self.build_known_courses()

        self.sep1 = ttk.Separator(self.root, orient='vertical')
        self.sep1.place(height='906', x='1053', y='2')
        self.sep2 = ttk.Separator(self.root, orient='horizontal')
        self.sep2.place(width='500', x='1053', y='550')
        self.sep3 = ttk.Separator(self.root, orient='vertical')
        self.sep3.place(height='870', x='65', y='44')
        self.sep4 = ttk.Separator(self.root, orient='horizontal')
        self.sep4.place(width='988', x='65', y='44')

        # Separators for the timetable display (Horizontal)
        self.sep5 = ttk.Separator(self.root, orient='horizontal')
        self.sep5.place(x='0', y='108', width=1054)
        self.sep6 = ttk.Separator(self.root, orient='horizontal')
        self.sep6.place(x='0', y='172', width=1054)
        self.sep7 = ttk.Separator(self.root, orient='horizontal')
        self.sep7.place(x='0', y='236', width=1054)
        self.sep8 = ttk.Separator(self.root, orient='horizontal')
        self.sep8.place(x='0', y='300', width=1054)
        self.sep9 = ttk.Separator(self.root, orient='horizontal')
        self.sep9.place(x='0', y='364', width=1054)
        self.sep10 = ttk.Separator(self.root, orient='horizontal')
        self.sep10.place(x='0', y='428', width=1054)
        self.sep11 = ttk.Separator(self.root, orient='horizontal')
        self.sep11.place(x='0', y='492', width=1054)
        self.sep12 = ttk.Separator(self.root, orient='horizontal')
        self.sep12.place(x='0', y='556', width=1054)
        self.sep13 = ttk.Separator(self.root, orient='horizontal')
        self.sep13.place(x='0', y='620', width=1054)
        self.sep14 = ttk.Separator(self.root, orient='horizontal')
        self.sep14.place(x='0', y='684', width=1054)
        self.sep15 = ttk.Separator(self.root, orient='horizontal')
        self.sep15.place(x='0', y='748', width=1054)
        self.sep16 = ttk.Separator(self.root, orient='horizontal')
        self.sep16.place(x='0', y='812', width=1054)
        self.sep17 = ttk.Separator(self.root, orient='horizontal')
        self.sep17.place(x='0', y='876', width=1054)

        # Separators for the timetable display (Vertical)
        self.sep25 = ttk.Separator(self.root, orient='vertical')
        self.sep25.place(x='207', y='44', height=870)
        self.sep26 = ttk.Separator(self.root, orient='vertical')
        self.sep26.place(x='348', y='44', height=870)
        self.sep27 = ttk.Separator(self.root, orient='vertical')
        self.sep27.place(x='489', y='44', height=870)
        self.sep28 = ttk.Separator(self.root, orient='vertical')
        self.sep28.place(x='630', y='44', height=870)
        self.sep29 = ttk.Separator(self.root, orient='vertical')
        self.sep29.place(x='771', y='44', height=870)
        self.sep20 = ttk.Separator(self.root, orient='vertical')
        self.sep20.place(x='912', y='44', height=870)

        # The labels for displaying courses
        self.display_class1 = Label(self.root, font=('Times', 18))
        self.display_class2 = Label(self.root, font=('Times', 18))
        self.display_class3 = Label(self.root, font=('Times', 18))
        self.display_class4 = Label(self.root, font=('Times', 18))
        self.display_class5 = Label(self.root, font=('Times', 18))
        self.display_class6 = Label(self.root, font=('Times', 18))
        self.display_class7 = Label(self.root, font=('Times', 18))
        self.display_class8 = Label(self.root, font=('Times', 18))
        self.display_class11 = Label(self.root, font=('Times', 18))
        self.display_class12 = Label(self.root, font=('Times', 18))
        self.display_class13 = Label(self.root, font=('Times', 18))
        self.display_class14 = Label(self.root, font=('Times', 18))
        self.display_class15 = Label(self.root, font=('Times', 18))
        self.display_class16 = Label(self.root, font=('Times', 18))
        self.display_class17 = Label(self.root, font=('Times', 18))
        self.display_class18 = Label(self.root, font=('Times', 18))
        self.display_class21 = Label(self.root, font=('Times', 18))
        self.display_class22 = Label(self.root, font=('Times', 18))
        self.display_class23 = Label(self.root, font=('Times', 18))
        self.display_class24 = Label(self.root, font=('Times', 18))
        self.display_class25 = Label(self.root, font=('Times', 18))
        self.display_class26 = Label(self.root, font=('Times', 18))
        self.display_class27 = Label(self.root, font=('Times', 18))
        self.display_class28 = Label(self.root, font=('Times', 18))

        self.display_labels = [[self.display_class1, self.display_class2, self.display_class3, self.display_class4],
                               [self.display_class5, self.display_class6, self.display_class7, self.display_class8],
                               [self.display_class11, self.display_class12, self.display_class13, self.display_class14],
                               [self.display_class15, self.display_class16, self.display_class17, self.display_class18],
                               [self.display_class21, self.display_class22, self.display_class23, self.display_class24],
                               [self.display_class25, self.display_class26, self.display_class27, self.display_class28]]
        self.display_index = 0

        self.btn_test = ttk.Button(self.root, style='my.TButton', text='test', command=self.test_it, width=6)
        # self.btn_test.place(x='1400', y='830')

        self.line_label3 = Label(self.root, text='   ', background='#DCE6F3')
        self.line_label3.place(x='1100', y='772', height=2, width=340)

        self.root.mainloop()

    def test_it(self):
        pass

    def build_banners(self):
        # self.banner = Label(self.root, text='         ', background='#B8CDD4')
        self.banner.place(width='1053', height=65, x='0', y='0')
        self.banner5.place(width='1053', height=5, x='0', y='40')
        # self.banner2 = Label(self.root, text='      ', background='#B8CDD4')
        self.banner2.place(width='65', height='910', x='0', y='0')
        # self.banner3 = Label(self.root, text='    ', background='#EAECEF')
        self.banner3.place(width='988', height='869', x='65', y='41')
        # self.banner4 = Label(self.root, text='    ', background='#EAECEF')
        self.banner4.place(width='447', height='910', x='1053', y='0')

    def config_weekdays(self):
        dates = get_real_times()
        for i in range(len(self.weekdays_lst)):
            self.weekdays_lst[i].configure(text=dates[i])

    def build_weekdays(self):
        self.monday_label.place(x='75', y='5')
        self.mo_day.place(x='142', y='9')
        self.tues_label.place(x='221', y='5')
        self.tu_day.place(x='276', y='9')
        self.wed_label.place(x='356', y='5')
        self.wed_day.place(x='420', y='9')
        self.thur_label.place(x='501', y='5')
        self.thu_day.place(x='560', y='9')
        self.frid_label.place(x='645', y='5')
        self.fri_day.place(x='695', y='9')
        self.sat_label.place(x='785', y='5')
        self.sat_day.place(x='835', y='9')
        self.sun_label.place(x='926', y='5')
        self.sun_day.place(x='981', y='9')

    def build_times(self):
        self.time8.place(x='5', y='45')
        self.time83.place(x='5', y='77')
        self.time9.place(x='5', y='109')
        self.time93.place(x='5', y='141')
        self.time10.place(x='5', y='173')
        self.time103.place(x='5', y='205')
        self.time11.place(x='5', y='237')
        self.time113.place(x='5', y='269')
        self.time12.place(x='5', y='301')
        self.time123.place(x='5', y='333')
        self.time13.place(x='5', y='365')
        self.time133.place(x='5', y='397')
        self.time14.place(x='5', y='429')
        self.time143.place(x='5', y='461')
        self.time15.place(x='5', y='493')
        self.time153.place(x='5', y='525')
        self.time16.place(x='5', y='557')
        self.time163.place(x='5', y='589')
        self.time17.place(x='5', y='621')
        self.time173.place(x='5', y='653')
        self.time18.place(x='5', y='685')
        self.time183.place(x='5', y='717')
        self.time19.place(x='5', y='749')
        self.time193.place(x='5', y='781')
        self.time20.place(x='5', y='813')
        self.time203.place(x='5', y='845')
        self.time21.place(x='5', y='877')

    def build_info_section(self):
        self.school_label.place(x='1100', y='10')
        self.area_label.place(x='1100', y='50')
        self.level_label.place(x='1100', y='90')
        self.course_list_label.place(x='1218', y='150')
        self.school_name.place(x='1200', y='10')
        self.study_area.place(x='1300', y='50')
        self.study_level.place(x='1300', y='90')

    def build_adding_section(self):
        self.course_label.place(x='1065', y='580')
        self.time_label.place(x='1060', y='635')
        self.color_label.place(x='1065', y='715')

        self.entry_course.place(x='1275', y='584')
        self.entry_time.place(x='1275', y='641')
        self.duration_combo.place(x='1435', y='638')  # x='1398', y='668'
        self.combo_color.place(x='1275', y='720')

        self.add_btn.place(x='1310', y='795')
        self.assignments_btn.place(x='1094', y='850')
        # self.calendar_btn.place(x='1080', y='840')
        self.display_btn.place(x='1127', y='795')

    def build_known_courses(self):
        indx = self.course_index
        if indx == 0:
            self.course1.configure(text=self.user.courses[0].course)
            self.class_time1.configure(text=self.user.courses[0].time)
            self.build_course1()
        elif indx == 1:
            self.course1.configure(text=self.user.courses[0].course)
            self.class_time1.configure(text=self.user.courses[0].time)
            self.course2.configure(text=self.user.courses[1].course)
            self.class_time2.configure(text=self.user.courses[1].time)
            self.build_course1()
            self.build_course2()
        elif indx == 2:
            self.course1.configure(text=self.user.courses[0].course)
            self.class_time1.configure(text=self.user.courses[0].time)
            self.course2.configure(text=self.user.courses[1].course)
            self.class_time2.configure(text=self.user.courses[1].time)
            self.course3.configure(text=self.user.courses[2].course)
            self.class_time3.configure(text=self.user.courses[2].time)
            self.build_course1()
            self.build_course2()
            self.build_course3()
        elif indx == 3:
            self.course1.configure(text=self.user.courses[0].course)
            self.class_time1.configure(text=self.user.courses[0].time)
            self.course2.configure(text=self.user.courses[1].course)
            self.class_time2.configure(text=self.user.courses[1].time)
            self.course3.configure(text=self.user.courses[2].course)
            self.class_time3.configure(text=self.user.courses[2].time)
            self.course4.configure(text=self.user.courses[3].course)
            self.class_time4.configure(text=self.user.courses[3].time)
            self.build_course1()
            self.build_course2()
            self.build_course3()
            self.build_course4()
        elif indx == 4:
            self.course1.configure(text=self.user.courses[0].course)
            self.class_time1.configure(text=self.user.courses[0].time)
            self.course2.configure(text=self.user.courses[1].course)
            self.class_time2.configure(text=self.user.courses[1].time)
            self.course3.configure(text=self.user.courses[2].course)
            self.class_time3.configure(text=self.user.courses[2].time)
            self.course4.configure(text=self.user.courses[3].course)
            self.class_time4.configure(text=self.user.courses[3].time)
            self.course5.configure(text=self.user.courses[4].course)
            self.class_time5.configure(text=self.user.courses[4].time)
            self.build_course1()
            self.build_course2()
            self.build_course3()
            self.build_course4()
            self.build_course5()
        elif indx == 5:
            self.course1.configure(text=self.user.courses[0].course)
            self.class_time1.configure(text=self.user.courses[0].time)
            self.course2.configure(text=self.user.courses[1].course)
            self.class_time2.configure(text=self.user.courses[1].time)
            self.course3.configure(text=self.user.courses[2].course)
            self.class_time3.configure(text=self.user.courses[2].time)
            self.course4.configure(text=self.user.courses[3].course)
            self.class_time4.configure(text=self.user.courses[3].time)
            self.course5.configure(text=self.user.courses[4].course)
            self.class_time5.configure(text=self.user.courses[4].time)
            self.course6.configure(text=self.user.courses[5].course)
            self.class_time6.configure(text=self.user.courses[5].time)
            self.build_course1()
            self.build_course2()
            self.build_course3()
            self.build_course4()
            self.build_course5()
            self.build_course6()

    def build_course1(self):
        self.course1.place(x='1100', y='200')
        self.class_time1.place(x='1218', y='200')
        self.class_btn1.place(x='1400', y='200')

    def build_course2(self):
        self.course2.place(x='1100', y='260')
        self.class_time2.place(x='1218', y='260')
        self.class_btn2.place(x='1400', y='260')

    def build_course3(self):
        self.course3.place(x='1100', y='320')
        self.class_time3.place(x='1218', y='320')
        self.class_btn3.place(x='1400', y='320')

    def build_course4(self):
        self.course4.place(x='1100', y='380')
        self.class_time4.place(x='1218', y='380')
        self.class_btn4.place(x='1400', y='380')

    def build_course5(self):
        self.course5.place(x='1100', y='440')
        self.class_time5.place(x='1218', y='440')
        self.class_btn5.place(x='1400', y='440')

    def build_course6(self):
        self.course6.place(x='1100', y='500')
        self.class_time6.place(x='1218', y='500')
        self.class_btn6.place(x='1400', y='500')

    def check_clicked(self, event):
        self.clicked = True

    def get_user(self):
        """Using password, get User"""
        users_dct = None
        for dct in pickle_loader('Users_file.txt'):
            users_dct = dct
        if isinstance(users_dct, User):
            return users_dct
        else:
            if users_dct is not None:
                return users_dct[self.pwd]
            else:
                print('The user file is empty!')

    def add_course(self):
        course_code = self.course.get()
        self.course.set('')
        time = self.time_class.get()
        time_lst = time.split(', ')
        self.time_class.set('M: TU: W: TH: F: S: SU:')
        color = self.color.get()
        duration = self.duration.get()

        time_display = make_time_str(time_lst)
        course = Course(course_code, time_display, color, duration)
        if len(self.take_courses) == 6:
            max_course = Toplevel(self.root)
            max_course.geometry('400x200')
            max_course.configure(background='#C0294E')
            msg_error = Label(max_course, text='You cannot add more than 6 courses!')
            msg_error.configure(foreground='white', font=('Times', 18, 'bold'), background='#C0294E')
            msg_error.place(relx=0.5, rely=0.5, anchor='center')
            print('Reached max courses')
        elif len(self.take_courses) < 6:
            self.user.courses.append(course)
            update_pickle_data('Users_file.txt', self.user, self.pwd)
            self.user = self.get_user()
            if self.num_of_courses == 0:
                self.courses[0].configure(text=course.course)
                self.times[0].configure(text=time_display)
                self.build_course1()
                self.num_of_courses += 1
            elif self.num_of_courses == 1:
                self.courses[1].configure(text=course.course)
                self.times[1].configure(text=time_display)
                self.build_course2()
                self.num_of_courses += 1
                self.course_index += 1
            elif self.num_of_courses == 2:
                self.courses[2].configure(text=course.course)
                self.times[2].configure(text=time_display)
                self.build_course3()
                self.num_of_courses += 1
                self.course_index += 1
            elif self.num_of_courses == 3:
                self.courses[3].configure(text=course.course)
                self.times[3].configure(text=time_display)
                self.build_course4()
                self.num_of_courses += 1
                self.course_index += 1
            elif self.num_of_courses == 4:
                self.courses[4].configure(text=course.course)
                self.times[4].configure(text=time_display)
                self.build_course5()
                self.num_of_courses += 1
                self.course_index += 1
            elif self.num_of_courses == 5:
                self.courses[5].configure(text=course.course)
                self.times[5].configure(text=time_display)
                self.build_course6()
                self.num_of_courses += 1
                self.course_index += 1

        if len(self.take_courses) < 6 and self.clicked:
            self.update_timetable(course.course, course.duration, course.time, course.color)

    def open_assignments(self):
        AssignmentPage(self.root, self.user)

    def open_calendar(self):
        pass

    def drop_course(self, indx):
        self.user.courses.pop(indx)

        self.remove_info_widget()
        if self.course_index != 0:
            self.course_index -= 1
            self.num_of_courses -= 1
            self.build_known_courses()
        else:
            self.num_of_courses -= 1
        if self.clicked:
            self.remove_from_timetable(indx)

        update_pickle_data('Users_file.txt', self.user, self.user.password)
        self.user = self.get_user()

    def remove_info_widget(self):
        self.course1.place_forget()
        self.class_btn1.place_forget()
        self.class_time1.place_forget()
        self.course2.place_forget()
        self.class_btn2.place_forget()
        self.class_time2.place_forget()
        self.course3.place_forget()
        self.class_btn3.place_forget()
        self.class_time3.place_forget()
        self.course4.place_forget()
        self.class_btn4.place_forget()
        self.class_time4.place_forget()
        self.course5.place_forget()
        self.class_btn5.place_forget()
        self.class_time5.place_forget()
        self.course6.place_forget()
        self.class_btn6.place_forget()
        self.class_time6.place_forget()

    def show_timetable_test(self):
        class_title1 = make_display_str(self.user.courses[0].course, self.user.courses[0].time, self.user.courses[0].duration)
        class_color1 = CLASS_COLOR_CODES[self.user.courses[0].color]
        class_title2 = self.user.courses[1].course
        class_color2 = CLASS_COLOR_CODES[self.user.courses[1].color]
        class_title3 = self.user.courses[2].course
        class_color3 = CLASS_COLOR_CODES[self.user.courses[2].color]
        class_title4 = self.user.courses[3].course
        class_color4 = CLASS_COLOR_CODES[self.user.courses[3].color]
        y = '237'
        h = 126
        print(self.user.courses[1].time)

        self.display_class1.configure(text=class_title1, background=class_color1)
        self.display_class1.place(x='66', y=y, width=141, height=h)
        self.display_class2.configure(text=class_title2, background=class_color2)
        self.display_class2.place(x='207', y='45', width=141, height=94)
        self.display_class3.configure(text=class_title3, background=class_color3)
        self.display_class3.place(x='348', y='45', width=141, height=62)
        self.display_class4.configure(text=class_title4, background=class_color4)
        self.display_class4.place(x='489', y='45', width=141, height=30)
        self.display_class5.configure(text=class_title1, background=class_color1)
        self.display_class5.place(x='630', y='45', width=141, height=126)
        self.display_class6.configure(text=class_title2, background=class_color2)
        self.display_class6.place(x='771', y='45', width=141)

    def show_timetable(self):
        for i in range(len(self.user.courses)):
            class_name = self.user.courses[i].course
            class_length = self.user.courses[i].duration
            class_time = self.user.courses[i].time
            class_color = CLASS_COLOR_CODES[self.user.courses[i].color]
            time_tuples = make_time_useful(class_time)

            class_display = make_display_str(class_name, class_time, class_length)
            if isinstance(class_display, str):
                self.add_class_from_str(class_display, class_length, time_tuples, class_color)
            else:
                self.add_class_from_lst(class_display, class_length, time_tuples, class_color)

    def add_class_from_str(self, text: str, length, time: list[tuple[str, str]], color):
        weekday, start_time = time[0]
        x_position = str(int(CLASS_DAYS_X[weekday]) + 1)
        y_position = CLASS_DAYS_Y[start_time]
        height = CLASS_TIMES_H[length] + 1
        course_label = self.display_labels[self.display_index][0]
        course_label.configure(text=text, background=color)
        course_label.place(x=x_position, y=y_position, width=141, height=height)
        self.display_index += 1

    def add_class_from_lst(self, text: list, length, time: list[tuple[str, str]], color):
        height = CLASS_TIMES_H[length] + 1
        for i, tup in enumerate(time):
            weekday, start_time = tup
            text_to_show = text[i]
            x_position = CLASS_DAYS_X[weekday]
            y_position = CLASS_DAYS_Y[start_time]
            course_label = self.display_labels[self.display_index][i]
            course_label.configure(text=text_to_show, background=color)
            course_label.place(x=x_position, y=y_position, width=141, height=height)
        self.display_index += 1

    def remove_from_timetable(self, indx):
        for label in self.display_labels[indx]:
            label.configure(text='')
            label.place_forget()
        x = self.display_labels.pop(indx)
        self.display_labels.append(x)
        self.display_index -= 1

    def update_timetable(self, name, length, time, color):
        time_tuples = make_time_useful(time)
        color_code = CLASS_COLOR_CODES[color]
        class_display = make_display_str(name, time, length)
        if isinstance(class_display, str):
            self.add_class_from_str(class_display, length, time_tuples, color_code)
        else:
            self.add_class_from_lst(class_display, length, time_tuples, color_code)


class AssignmentPage:
    def __init__(self, old_root, user):
        old_root.destroy()
        # self.old = old_root
        self.user = user
        self.root = Tk()
        self.root.geometry('1000x650')
        self.root.configure(background='#B8CDD4')
        self.root.title('MyAssignments')
        self.style = ttk.Style(self.root)
        self.style.theme_use('clam')
        self.style.configure('TButton', background='#8596AD',
                             foreground='#F9FBFD', font=('Times', 21, 'bold'),
                             bordercolor='#B8CDD4')
        self.style2 = ttk.Style(self.root)
        self.style2.theme_use('clam')
        self.style2.configure('W.TButton', background='#8596AD',
                              foreground='#F9FBFD', font=('Times', 17, 'bold'),
                              bordercolor='#B8CDD4')

        # Index to keep track of assignment list
        self.num_assignments = len(self.user.assignments)

        # User's courses title as list
        self.user_courses = self.user.get_courses_names()

        # Important variables to use later
        self.assign_name = StringVar(self.root)
        self.assign_date = StringVar(self.root)
        self.assign_course = StringVar(self.root)
        self.priority1 = StringVar(self.root)

        self.assignment_label = Label(self.root, text='Your Assignments', font=('Times', 20, 'bold', 'underline'), background='#B8CDD4')
        self.assignment_info = Listbox(self.root, height=26, width=75, background='#DEE8ED', font=('Times', 18), selectmode=SINGLE)
        self.assignment_info.bind('<Double-Button-1>', self.more_info)
        self.assignment_info.bind('<<ListboxSelect>>', self.change_color)

        self.assign_name_label = Label(self.root, text='Ttile of Assignment:', font=('Times', 20), background='#B8CDD4')
        self.assignment_entry = Entry(self.root, width=23, textvariable=self.assign_name)

        self.assign_date_label = Label(self.root, text='Due Date\n(YYYY/MM/DD):', font=('Times', 20), background='#B8CDD4')
        self.assign_date_entry = Entry(self.root, width=23, textvariable=self.assign_date)

        self.assign_course_label = Label(self.root, text='Course:', font=('Times', 20), background='#B8CDD4')
        self.assign_course_combo = ttk.Combobox(self.root, width=23, textvariable=self.assign_course)
        if self.user_courses:
            self.assign_course_combo['values'] = self.user_courses
        else:
            self.assign_course_combo['values'] = ['Add a course to your list...']

        self.priority_label = Label(self.root, text='Priority:', font=('Times', 20, 'underline'), background='#B8CDD4')
        self.priority_combo = ttk.Combobox(self.root, width=17, textvariable=self.priority1)
        self.priority_combo['values'] = ['Select one...', 'Normal', 'P1', 'P2', 'P3']
        self.priority_combo.current(0)
        # self.p1_check = Checkbutton(self.root, text='P1', font=('Times', 14, 'bold'), textvariable=self.priority1, background='#B8CDD4')
        # self.p1_check.configure(state=DISABLED)
        # self.p2_check = Checkbutton(self.root, text='P2', font=('Times', 14, 'bold'), textvariable=self.priority2, background='#B8CDD4')
        # self.p2_check.configure(state=DISABLED)
        # self.p3_check = Checkbutton(self.root, text='P3', font=('Times', 14, 'bold'), textvariable=self.priority3, background='#B8CDD4')
        # self.p3_check.configure(state=DISABLED)
        self.add_assign_btn = ttk.Button(self.root, style='my.TButton', text='Add Assignment', command=self.add_assignment)

        self.timetable_btn = ttk.Button(self.root, style='W.TButton', text='Timetable', command=self.back_timetable)

        self.build_main_ui()

        self.assignment_display_at_opening()

        self.root.mainloop()

    def build_main_ui(self):
        self.assignment_label.place(x='270', y='10')
        self.assignment_info.place(x='10', y='45')
        self.assign_name_label.place(x='760', y='45')
        self.assignment_entry.place(x='738', y='73')

        self.assign_date_label.place(x='767', y='120')
        self.assign_date_entry.place(x='738', y='170')
        self.assign_course_label.place(x='810', y='217')
        self.assign_course_combo.place(x='738', y='245')

        self.priority_label.place(x='810', y='295')
        self.priority_combo.place(x='762', y='325')
        # self.p1_check.place(x='755', y='340')
        # self.p2_check.place(x='825', y='340')
        # self.p3_check.place(x='895', y='340')

        self.add_assign_btn.place(x='766', y='385')
        self.timetable_btn.place(x='792', y='450')

    def add_assignment(self):
        title = self.assign_name.get()
        self.assign_name.set('')
        date = self.assign_date.get()
        self.assign_date.set('')
        course_name = self.assign_course.get()
        self.assign_course.set('')
        priority = self.priority1.get()
        # priority = 'Normal'
        # if self.priority1:
        #     priority = 'P1'
        # elif self.priority2:
        #     priority = 'P2'
        # elif self.priority3:
        #     priority = 'P3'

        assignment = Assignment(title, date, course_name, priority)
        self.user.assignments.append(assignment)
        update_pickle_data('Users_file.txt', self.user, self.user.password)

        self.update_assign_display(assignment)

    def update_assign_display(self, new_assign):
        new_insert = new_assign.make_str()
        self.assignment_info.insert(self.num_assignments, new_insert)
        self.num_assignments += 1

    def assignment_display_at_opening(self):

        if self.num_assignments == 0:
            pass
        else:
            assign_lst = self.user.assignments
            for i in range(self.num_assignments):
                assign_str = assign_lst[i].make_str()
                self.assignment_info.insert(i, assign_str)

    def back_timetable(self):
        SchedulePage(self.root, self.user.password)

    def more_info(self, event):
        indx = int(self.assignment_info.curselection()[0])
        # value = self.assignment_info.get(indx)
        delete_it = Toplevel(self.root)
        delete_it.geometry('200x100')
        delete_it.configure(background='#B8CDD4')
        delete_it.title('Delete')
        del_btn = ttk.Button(delete_it, text='Delete', style='W.TButton', command=lambda: self.destroy_assign(indx))
        del_btn.place(x='40', y='30')

    def change_color(self, event):
        indx = int(self.assignment_info.curselection()[0])
        value = self.assignment_info.get(indx)
        lst = value.split(' ')
        final = ''
        for word in lst:
            if '(' in word:
                final += word.strip("()")
        color = PRIORITY_COLORS[final]
        self.assignment_info.configure(selectbackground=color)

    def destroy_assign(self, x: int):
        self.assignment_info.delete(x)
        self.user.assignments.pop(x)
        self.num_assignments -= 1
        update_pickle_data('Users_file.txt', self.user, self.user.password)
        # print(self.user.assignments[x].make_str())


def go_back(root):
    root.destroy()
    MyScheduleApp()


def make_time_useful(text: str) -> list[tuple[str, str]]:
    text = re.sub(r'\n', ' ', text)
    lst = text.split(', ')
    final_lst = []
    for item in lst:
        stuff = None
        if '-' in item:
            stuff = item.split('-')
        elif ':' in item:
            stuff = item.split(':')
        x = stuff[0], stuff[1]
        final_lst.append(x)
    return final_lst


def make_time_str(time_lst) -> str:
    final = ''
    if len(time_lst) < 3:
        for time in time_lst:
            time.replace(':', '-')
            final = final + time + ', '
    else:
        count = 0
        for time in time_lst:
            time.replace(':', '-')
            if count == 1:
                final = final + time + ',\n'
                count = 0
            else:
                final = final + time + ", "
                count += 1
    final = final.replace(':', '-')
    return final.strip(', ')


def make_display_str(name: str, time: str, duration: str) -> Union[str, list]:
    # time format (DAY-0000)
    time = time.replace('\n', ' ')
    time_lst = time.split(', ')
    if not time_lst[0] and len(time_lst) == 1:
        return name
    elif len(time_lst) == 1:
        if '-' in time:
            time = time.split('-')[1]
        elif ':' in time:
            time = time.split(':')[1]
        if '3' in time and len(time.split('3')[1]) != 2:
            end = str(int(time)//100 + int(duration)) + ':30'
        else:
            end = str(int(time)//100 + int(duration)) + ':00'
        time = time[0:2] + ':' + time[2:]
        return f'{name}\n{time} to {end}'
    else:
        lst = []
        for time in time_lst:
            if '-' in time:
                time = time.split('-')[1]
                if int(time)//100 < 10:
                    time = '0' + time
            elif ':' in time:
                time = time.split(':')[1]
                if int(time)//100 < 10:
                    time = '0' + time
            if '3' in time and len(time.split('3')[1]) != 2:
                end = str(int(time)//100 + int(duration)) + ':30'
                if int(time)//100 + int(duration) < 10:
                    end = '0' + end
            else:
                end = str(int(time)//100 + int(duration)) + ':00'
                if int(time)//100 + int(duration) < 10:
                    end = '0' + end
            strg = time[0:2] + ':' + time[2:] + ' to ' + end
            final_str = f'{name}\n{strg}'
            lst.append(final_str)
        return lst


def get_real_times() -> list[str]:
    actual_date = datetime.now()
    # actual_month = actual_date_lst[0]
    # actual_today = int(actual_date_lst[1])  # lose the 0 in 05
    actual_day = datetime.today().weekday()
    temp_lst = []
    for i in range(0, actual_day):
        day = actual_date - timedelta(days=i+1)
        temp_lst.insert(0, day)
    for i in range(actual_day, 6):
        day = actual_date + timedelta(days=i)
        temp_lst.append(day)
    temp_lst.insert(actual_day, actual_date)
    final_lst = []
    for item in temp_lst:
        lst = str(item).split()[0].split('-')[1:]
        t_month = lst[0]
        t_day = lst[1]
        t = t_month + '/' + t_day
        final_lst.append(t)
    return final_lst


def pickle_loader(filename):
    """ Deserialize a file of pickled objects. """
    with open(filename, "rb") as f:
        while True:
            try:
                yield pickle.load(f)
            except EOFError:
                break


def pickle_input(filename, lst_objects):
    with open(filename, 'wb') as outp:  # Overwrites any existing file.
        pickle.dump(lst_objects, outp, pickle.HIGHEST_PROTOCOL)


# Use this function when putting new objects into pickle file
# Steps:
# 1- Get stuff out (pickle_loader())
# 2- Delete (pickle_delete())
# 3- Put stuff in (pickle_input())
def pickle_delete(filename):
    with open(filename, 'wb') as file:
        file.close()


def update_pickle_data(filename, data_to_add, pwd):
    users_dct = None
    for dct in pickle_loader(filename):
        users_dct = dct
    if users_dct is not None:
        # print(type(users_dct))
        # if isinstance(users_dct, User):
        #     users_dct.courses = data_to_add.courses
        # else:
        users_dct.update({pwd: data_to_add})
        pickle_delete(filename)
        pickle_input(filename, users_dct)


def update_pickle_data2(filename, data_to_add, pwd):
    users_dct = None
    for dct in pickle_loader(filename):
        users_dct = dct
    if users_dct is not None:
        # print(type(users_dct))
        if isinstance(users_dct, User):
            users_dct.courses = data_to_add.courses
        else:
            users_dct.update({pwd: data_to_add})
        pickle_delete(filename)
        pickle_input(filename, users_dct)


def aaa():
    print(datetime.now())


class Hello:
    def __init__(self, name):
        self.name = name


def make():
    x = []
    for i in range(10):
        a = Hello('hello')
        x.append(a)
    return x


if __name__ == '__main__':
    MyScheduleApp()
    # SchedulePage(3, '12')

    # get_real_times()

    # lst = make()
    # print(lst)
