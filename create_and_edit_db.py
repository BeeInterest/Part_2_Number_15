import sqlite3
import mimesis
import random
from faker import Faker
from datetime import date

class DB:
    def __init__(self):
        self.conn = sqlite3.connect('exams.db')
        self.faker = Faker('ru_RU')
        self.person = mimesis.Person('ru')
        self.gen = mimesis.Generic('ru')

    def calculate_age(self):
        today = date.today()
        year_f = int(str(self.faker.date_of_birth(minimum_age=17, maximum_age=19)).split("-")[0])
        month_f = int(str(self.faker.date_of_birth(minimum_age=17, maximum_age=19)).split("-")[1])
        day_f = int(str(self.faker.date_of_birth(minimum_age=17, maximum_age=19)).split("-")[2])
        age_t = today.year - year_f - ((today.month, today.day) < (month_f, day_f))
        if month_f < 10:
            month_f = f"0{month_f}"
        if day_f < 10:
            day_f = f"0{day_f}"
        birth_date = f'{year_f}-{month_f}-{day_f}'
        return birth_date