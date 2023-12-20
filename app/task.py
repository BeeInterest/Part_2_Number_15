import sqlite3
try:
    conn = sqlite3.connect('../db/exams.db')
    cursor = conn.cursor()
except Exception as e:
    print(str(e))
while True:
    try:
        cursor.execute(f'''
        SELECT full_name, birth_date
        FROM record_books
        ORDER BY strftime('%Y', birth_date) DESC,
                strftime('%m', birth_date) DESC,
                strftime('%d', birth_date) DESC''')
        
        students = cursor.fetchall()
        cursor.execute('''DROP TABLE record_books;''')
        cursor.execute('''DROP TABLE subjects_book; ''')
        conn.close()
    except:
        continue
    birth1 = students[0][1]
    birth2 = students[-1][1]
    young = max(birth1,birth2)
    old = min(birth1,birth2)
    for student in students:
        if student[1] == old:
            print(f"Старший студент: {student}")
        elif student[1] == young:
            print(f"Молодой студент: {student}")
    
    if students:
        break
