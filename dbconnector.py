import sqlite3

def register_new_user(username, password, name, surname):
    con = sqlite3.connect('exams.db')
    cursor = con.cursor()
    sql = "insert into Users (username, password, name, surname) values (?, ?, ?, ?)"
    cursor.execute(sql, (username, password, name, surname))
    con.commit()
    con.close()
    return 'Created new user successfully'

def get_all_registered_users():
    con = sqlite3.connect('exams.db')
    cursor = con.cursor()
    sql = "select name, surname from Users"
    cursor.execute(sql)
    users = cursor.fetchall()
    con.close()
    return users    

def get_one_user(id):
    con = sqlite3.connect('exams.db')
    cursor = con.cursor()
    sql = "select name, surname from Users where id = ?"
    sql2 = "select course from Results join Users on Results.user_id = Users.id where user_id = ?"
    cursor.execute(sql, (id, ))
    user = cursor.fetchone()
    cursor.execute(sql2, (id, ))
    courses = cursor.fetchall()
    con.close()
    return user , courses

def verify_user(username, password):
    con = sqlite3.connect('exams.db')
    cursor = con.cursor()
    sql = "select * from Users where username = ? and password = ?"
    cursor.execute(sql, (username, password))
    result = cursor.fetchone()
    con.close()
    return result
            
def get_exam_results(user_id):
    con = sqlite3.connect('exams.db')
    cursor = con.cursor()
    sql = "select course, mark from Users join Results on Results.user_id = Users.id where user_id = ?"
    cursor.execute(sql, (user_id,))
    results = cursor.fetchall()
    con.close()
    return results

if __name__ == "__main__":
    print(register_courses("New Course", 50, 7))



