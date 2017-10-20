# -*- coding: utf-8 -*-

from flask import Flask, render_template, url_for, request, session, redirect

app = Flask(__name__)
app.config['SECRET_KEY']= 'e5ac358c-f0bf-11e5-9e39-d3b532c10a28'

@app.route('/')
def index():
    session['username']="Adem"
    if 'username' in session:
        return 'You are logged in as ' + session['username']
    else:
        return "Adem"


if __name__ == '__main__':
    app.run(debug=True)
