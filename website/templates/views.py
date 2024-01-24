from flask import render_template, redirect, url_for, request, flash, make_response, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
import uuid
import json
from flask_login import login_user, login_required, current_user
from . import app, db  
from .models import User
from .auth import login_manager 

login_manager = LoginManager(app)


# Home route
@app.route('/')
def home():
    return render_template('home.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Existing login logicfrom website import auth
    return render_template('login.html')

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # Existing signup logic
    return render_template('signup.html')

# Account route
@app.route('/account')
@login_required
def account():
    # Existing account logic
    return render_template('account.html')

# Serve uploaded file route
@app.route('/uploads/<filename>')
def serve_uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Upload file route
@app.route('/upload', methods=['POST', 'GET'])
@login_required
def upload_file():
    # Existing upload file logic
    return render_template('sell.html')

# Display properties route
@app.route('/properties')
def display_properties():
    # Existing display properties logic
    return render_template('2.html', properties=property_list)

# Link to buy HTML route
@app.route('/link_to_buy_html')
def link_to_2_html():
    return render_template('2.html', properties=property_list)

# Error handler for file size limit
@app.errorhandler(413)
def too_large(e):
    return make_response(jsonify(message="File is too large"), 413)

# Reset uploads route
@app.route('/reset_uploads', methods=['POST'])
def reset_uploads():
    # Existing reset uploads logic
    return redirect(url_for('home'))
