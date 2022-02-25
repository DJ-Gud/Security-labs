from flask import Flask, render_template, request, flash
from tools import *
import sys

app = Flask(__name__)
app.secret_key = '123124'
data = load_data()


@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/login",  methods=['POST'])
def login_post():
    login = request.form.get('login')
    password = request.form.get('password')

    if not login in data.keys():
        flash("Error: Can't find user.")
        return render_template('login.html')
    elif data[login][1] != hash_password(password, data[login][2])[0]:
        flash("Error: Wrong passwod.")
        return render_template('login.html')

    #print(data[login], file=sys.stderr)
    if data[login][3] == 1:
        honey_pot_activation(login, request.remote_addr)

    return render_template('login_success.html', name=data[login][0])

@app.route("/register")
def register():
    return render_template('register.html')

@app.route("/register",  methods=['POST'])
def register_post():

    name = request.form.get('name')
    login = request.form.get('login')
    password = request.form.get('password')


    if login in data.keys():
        flash('Error: Login already exists!')
        return render_template('register.html')

    elif weak_password(password):
        flash('Error: Password is too weak.')
        flash('Your password must be at least 8 characters long')
        flash('and also contain a digit or symbol.')
        return render_template('register.html')
    
    else:
        password, salt = hash_password(password)
        save_user(name, login, password, salt)
        data[login] = (name, password, salt, 0)

    return render_template('register_success.html', name=name, login=login)




