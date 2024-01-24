from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import login_user, login_required, logout_user, current_user
import os

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user != None:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', category='success')
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        phone_number = request.form.get('phone')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        from website.models import User
        user = User.query.filter_by(email=email).first()
        if len(password1) < 6 or len(password2) < 6:
            flash('Password must be at least 6 characters.', category='error')
        else:
            if password1 == password2:
                #check if user exists
                if user == None:
                    new_user = User(email=email, phone_number=phone_number, first_name=first_name,last_name=last_name, password=generate_password_hash(password1, method='pbkdf2:sha256'))
                    try:
                        db.session.add(new_user)
                        db.session.commit()  # Commit changes to the database

                        #login_user(new_user, remember=True)
                        flash('Account created! Please log in.', category='success')
                        return redirect(url_for('login'))  # Assuming 'login' is the name of your login route
                    except Exception as e:
                        db.session.rollback()  # Rollback changes in case of an exception
                        flash('Error creating account. Please try again.', category='error')
                        print(e)
                else:
                    flash("User already exists")
            
            else:
                flash('Passwords do not match!', category='error')
                

    return render_template("signup.html")
