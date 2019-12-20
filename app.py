import dbconnector

from flask import Flask, render_template, url_for, request, redirect, session, jsonify

app = Flask(__name__)
app.secret_key = "thisisasecret"

@app.route("/")
@app.route('/index')
def index():
    user_id = session.get("user_id", "")
    authenticated = False
    if user_id != "":
        authenticated = True
    return render_template('index.html', authenticated=authenticated)

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/register_user', methods=["POST"])
def register_user():
    name = request.form['name']
    surname = request.form['surname']    
    username = request.form['username']
    password = request.form['password']
    success = dbconnector.register_new_user(username, password, name, surname)
    return render_template('success.html', success=success, name=name, surname=surname)

@app.route('/login', methods=["POST"])
def login():
    username = request.form['username']
    password = request.form['password']
    user = dbconnector.verify_user(username, password)
    if user is not None:
        session["user_id"] = user[0]
        return redirect(url_for('exams'))
    else:
        return redirect(url_for('login_error'))

@app.route('/exams')
def exams():
    user_id = session.get("user_id", "")
    if user_id == "":
        return redirect(url_for('index'))
    else:
        exams = dbconnector.get_exam_results(user_id)
        return render_template('exams.html', exams = exams) 

@app.route('/login_error')
def login_error():
    return render_template('login_error.html')

@app.route('/logout')
def logout():
    del session["user_id"]
    return redirect(url_for('index'))


#API Routes
endpoint = '/api/v1'
@app.route(endpoint + '/users')
def get_all_users():
    users = dbconnector.get_all_registered_users()
    return jsonify(users)

@app.route(endpoint + '/users/<int:id>')
def get_one_user(id):
    user = dbconnector.get_one_user(id)
    return jsonify(user)


if __name__ == "__main__":
    app.run(debug=True)

