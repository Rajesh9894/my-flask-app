from flask import Flask, render_template, request, flash, redirect, url_for, session,jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from business import collection
from utils import login_required

app = Flask(__name__)
app.secret_key = 'Rajesh'

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/register', methods=['GET'])
def register_get():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register_post():
    username = request.form.get("name")
    password = request.form.get("password")
    confirmPassword = request.form.get("confirmPassword")

    if password != confirmPassword:
        flash("Password Mismatch", "error")
        return render_template('register.html')
    #password hashed 
    hashed_password = generate_password_hash(password)
    user_dict = {"name": username,"password": hashed_password,"created_at": datetime.now()}
    # user_dict={"name": username,"password": password,"created_at": datetime.now()}

    if user_dict:
        collection.insert_one(user_dict)
        flash("User Registered Successfully", "success")
        return redirect(url_for("login_get"))

    flash("User Registration Failed", "error")
    return render_template('register.html')

@app.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    try:
        name = request.form.get("name")
        password = request.form.get("password")

        user = collection.find_one({"name":name})

        if not user:
            flash('User Not Found', 'error')
            return redirect(url_for('register_get'))

        # if user and user['password'] == password: 
        if user and check_password_hash(user['password'], password):
            session['username'] = name
            session['logged_in'] = True
            session['logged_at'] = datetime.now()
            flash('Login Successful', 'success')
            return redirect(url_for('home'))

        flash ('Login Failed, Try Again After Sometimes', 'error')
        return render_template('login.html')
    except Exception:
        flash('Login Failed, Try Again After Sometimes', 'error')
        return render_template('login.html')
    
@app.route('/sed')
def Session_data():
    return jsonify(session)

@app.route('/user')
@login_required
def Show_user():
    username = session.get('username')
    return f'<h1>Hello{username}</h1><br><h1>last login :{session.get('logged_at')}'

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_get'))
    
@app.route('/home')
@login_required
def home():
    return "Hello World"

if __name__ == '__main__':
    app.run(debug=True)