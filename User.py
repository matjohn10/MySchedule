import datetime


class Assignment:
    def __init__(self, name, date, course_name, priority):
        self.title = name
        self.date = date
        self.course_code = course_name
        self.priority = priority

    def make_str(self) -> str:
        return f'{self.title}  ({self.priority})  |  Course: ' \
               f'{self.course_code}  |  Due in {self.countdown_to_deadline()}'

    def countdown_to_deadline(self) -> str:
        # time_now_lst = str(datetime.datetime.now()).split(' ')[0].split('-')
        time_assign_lst = self.date.split('/')
        time_assign = datetime.datetime(int(time_assign_lst[0]), int(time_assign_lst[1]), int(time_assign_lst[2]))
        time_now = datetime.datetime.now()
        # time_assign = datetime.datetime.strptime(self.date, "%Y/%m/%d")
        diff = time_assign - time_now

        if diff.days == 0:
            return 'one day'
        elif diff.days == -1:
            return 'today'
        else:
            return f'{diff.days} days'


class Course:
    def __init__(self, course, time: str, color, duration):
        self.course = course
        self.time = time
        self.color = color
        self.duration = duration


class User:
    courses: list[Course]
    assignments: list[Assignment]

    def __init__(self, username, pwd, school, level, area):
        self.username = username
        self.password = pwd
        self.school = school
        self.level = level
        self.area = area
        self.courses = []  # Has Course objects inside
        self.assignments = []  # List of Assignments objects

    def get_courses_names(self) -> list[str]:
        """Returns a list of the course codes"""
        name_lst = []
        for course in self.courses:
            name_lst.append(course.course)
        return name_lst


def helper():
    dct = {}
    x = 66
    w = 141
    lst = ['M', 'TU', 'W', 'TH', 'F', 'S', 'SU']
    for i, item in enumerate(lst):
        dct.update({item: str(x + i*w)})
    print(dct)


def helper2():
    dct = {}
    y = 45
    t = [800, 830, 900, 930, 1000, 1030, 1100, 1130, 1200, 1230, 1300, 1330,
         1400, 1430, 1500, 1530, 1600, 1630, 1700, 1730, 1800, 1830, 1900, 1930,
         2000, 2030, 2100]
    for i, time in enumerate(t):
        dct.update({str(time): str(y + i*32)})
    print(dct)


def hel():
    lst = [1, 2, 3, 4, 5]
    dct = {}
    for duration in lst:
        dct.update({str(duration): 30 + ((duration * 2) - 1)*32})
    print(dct)


if __name__ == '__main__':
    hel()
    # date = '2022/07/02'
    # time_now = datetime.datetime.now()
    # time_assign1 = datetime.datetime.strptime(date, "%Y/%m/%d")
    # diff = time_assign1 - time_now
    # print(diff.days == -1)



