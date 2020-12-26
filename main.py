import random
import string
import re
from flask import Flask, request, url_for, redirect, render_template, session

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'kluczyk'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///links.sqlite3'
db = SQLAlchemy(app)


class Links(db.Model):
    _id = db.Column('id', db.Integer, primary_key=True)
    target = db.Column(db.String(200))
    short = db.Column(db.String(10))

    def __init__(self, target, short):
        self.target = target
        self.short = short


class Users(db.Model):
    _id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column(db.String(20))

    # hashowanie hasla
    # mail, itd later

    def __init__(self, username):
        self.username = username


@app.route('/', methods=['POST', 'GET'])
def home():
    short = None
    if request.method == 'POST':
        link = request.form['link']
        is_link = Links.query.filter_by(target=link).first()
        if not is_link:
            short = rand_gen()
            db.session.add(Links(link, short))
            db.session.commit()
        else:
            short = is_link.short

    return render_template('base.html', adress=short)


@app.route('/<short>')
def shorter(short):
    address = Links.query.filter_by(short=short).first()
    if address:
        address = address.target
        target = valid_address(address)
        return redirect(target)
    else:
        return render_template('error.html')


def valid_address(address):
    if not address.startswith('http'):
        address = 'https://' + address
    return address


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['login']
        user = Users.query.filter_by(username=username).first()
        if user:
            session['user'] = user.username
            return redirect(url_for('user_page', username=user.username))
        else:
            return '<p>zly login</p>'
    else:
        if 'user' in session:
            return '<p>jestes zalogowany</p>'
        else:
            return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['login']
        db.session.add(Users(username))
        db.session.commit()
        return redirect(url_for('login'))
    else:
        return render_template('register.html')


@app.route('/about')
def about():
    return '<p>about</p>'


@app.route('/user/<username>')
def user_page(username):
    if 'user' in session:
        if session['user'] == 'admin':
            users = Users.query.all()
            links = Links.query.all()
            data = {'users': users, 'links': links}
            return render_template('admin.html', data=data)
        return render_template('user.html', user=username)
    else:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user', None)
    return redirect(url_for('login'))

def rand_gen():
    rand = ''
    for i in range(5):
        rand += random.choice(string.ascii_lowercase)
    return rand


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
