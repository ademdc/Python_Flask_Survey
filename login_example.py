from flask import Flask, render_template, url_for, request, session, redirect, flash
from flask_pymongo import PyMongo
import bcrypt

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'mongodatabase'
app.config['SECRET_KEY']= 'e5ac358c-f0bf-11e5-9e39-d3b532c10a28'

mongo = PyMongo(app)

@app.route('/')
def index():
    if 'username' in session:
        return '<head><link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous"></head>'+\
        '<div class="container"><br><p>You are logged in as ' + session['username'] + "</p>" + \
        "<br>  <a class='btn btn-warning' href='/logout'>Logout</a><br><a class='btn btn-info' href='/survey'>Survey</a></div>"

    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['username']})

    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
            session['username'] = request.form['username']
            return redirect(url_for('index'))

    return 'Invalid username/password combination'

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name' : request.form['username'], 'password' : hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('index'))

        return 'That username already exists!'

    return render_template('register.html')

@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   return redirect(url_for('index'))

@app.route('/survey', methods=['POST', 'GET'])
def survey():
    error = None
    if request.method == 'POST':
        answers = mongo.db.answers
        if answers.insert({'year' : request.form['year'], 'comfortable' : request.form['comfortable'], 'java':request.form['java'],'python':request.form['python'], \
        'c++':request.form['c++'],'javascript':request.form['javascript'],'C#':request.form['c#'],"learnNext":request.form['learnNext']}):
            flash("Succesfully added info")
        else:
            error = "Error occured"
        return redirect(url_for('survey'))

    return render_template("survey.html",error=error)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
