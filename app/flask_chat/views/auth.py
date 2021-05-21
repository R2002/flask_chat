from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required, current_user
import models
from database import db_insert, db_delete

app = Blueprint('auth', __name__)

@app.route('/login', methods=['GET'])
def login():
    return render_template('app/login.html')

@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    flag_remember = True if request.form.get('remember') else False

    user = models.User.query.filter_by(email=email).first()

    # ユーザーチェック
    if not user or not check_password_hash(user.password, password): 
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=flag_remember)
    return redirect(url_for('chat.chat'))

@app.route('/login_test')
def login_test():
    user = models.User.query.filter_by(id="asa").first()
    login_user(user, remember=True)
    return redirect(url_for('chat.chat'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index.index'))

@app.route('/register', methods=['GET'])
def register():
    return render_template('app/register.html')

@app.route('/register', methods=['POST'])
def register_post():

    id = request.form.get('id')
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    # 重複チェック
    if models.User.query.filter_by(id=id).first() is True:
        flash('ID address already exists')
        return redirect(url_for('auth.register'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = models.User(id=id, email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db_insert(new_user)
    
    return redirect(url_for('auth.login'))
