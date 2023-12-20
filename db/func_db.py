import json
from os import name
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
        self.conn = sqlite3.connect('exams.db',check_same_thread=False)
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
    
    def young_old_student(self):
        self.cursor.execute(f'''
    SELECT full_name, birth_date
    FROM record_books
    ORDER BY strftime('%Y', birth_date) DESC,
            strftime('%m', birth_date) DESC,
            strftime('%d', birth_date) DESC''')
    
        students = self.cursor.fetchall()
        self.cursor.execute('''DROP TABLE record_books;''')
        self.cursor.execute('''DROP TABLE subjects_book; ''')
        self.conn.close()
        birth1 = students[0][1]
        birth2 = students[-1][1]
        young = max(birth1,birth2)
        old = min(birth1,birth2)
        res = ''
        for student in students:
            if student[1] == old:
                res += f"   Старший студент: {student}"
            elif student[1] == young:
                res += f"   Молодой студент: {student}"
        return res
    

from flask import Flask, jsonify

app = Flask(__name__)
db = DB()

@app.route('/create_table')
def create_table():
    db.create_table()
    return json.dumps({'message':'Таблицы subjects_book и record_books созданы'})

@app.route('/fill_table/<int:number_students>')
def fill_table(number_students):
    db.fill_table(number_students)
    return json.dumps({'message':'Таблицы subjects_book и record_books заполнены'})

@app.route('/young_old_student')
def young_old_student():
    result = db.young_old_student()
    return json.dumps({'message':result})

app.run(host='127.0.0.1', port=5000,debug=True)


