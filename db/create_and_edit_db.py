import sqlite3
import sys
import mimesis
import random
from faker import Faker
from datetime import date

class DB:
    def __init__(self):
        self.number_subjects = random.randint(2,5)
        self.subjects = ['Философия',
            'Аналитическая геометрия',
            'Администрирование баз данных',
            'Алгоритмы параллельных вычислений',
            'Введение в машинное обучение']
        self.conn = sqlite3.connect('exams.db')
        self.faker = Faker('ru_RU')
        self.person = mimesis.Person('ru')
        self.gen = mimesis.Generic('ru')
        self.cursor = self.conn.cursor()

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
    
    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS subjects_book(
    subject_id        SERIAL         PRIMARY KEY,
    subject_name      VARCHAR(1024)  NOT NULL,
    book_id           INTEGER        NOT NULL,
    full_name_teacher VARCHAR(1024)  NOT NULL,
    date_exam         TIMESTAMP      NOT NULL
) ''')

        self.cursor.execute('''
CREATE TABLE IF NOT EXISTS record_books (
    book_id           SERIAL         PRIMARY KEY,
    full_name         VARCHAR(1024)  NOT NULL,
    birth_date        TIMESTAMP      NOT NULL
)
''')
        self.conn.commit()
        print('Таблицы subjects_book и record_books созданы')
    
    def fill_table(self,number_students=20):
        for i in range(number_students):
            full_name = self.person.full_name()
            birth_date = self.calculate_age()
            book_id = i
            self.cursor.execute(f'''
                        INSERT INTO  record_books
                        (book_id,full_name,birth_date)
                        VALUES ({book_id},'{full_name}','{birth_date}');''')
        for i in range(self.number_subjects):
            full_name_teacher = self.person.full_name()
            subject_name = self.subjects[i]
            date_exam = self.faker.future_datetime()
            for _ in range(number_students):
                self.cursor.execute(f'''
                            INSERT INTO subjects_book 
                            (subject_name,book_id,full_name_teacher,date_exam)
                            VALUES ('{subject_name}',{book_id},'{full_name_teacher}','{str(date_exam)[:10]}');''')
        self.conn.commit()
        print('Таблицы subjects_book и record_books заполнены')
        self.conn.close()

db = DB()
db.create_table()
if len(sys.argv) > 1:
    db.fill_table(number_students=int(sys.argv[1]))

# db.fill_table()

